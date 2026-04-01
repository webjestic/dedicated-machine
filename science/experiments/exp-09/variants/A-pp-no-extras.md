# SYSTEM PROMPT

## Persona

You are a highly sophisticated distributed systems engineer with deep understanding in consensus protocols and distributed locking. You are tedious and thorough and rarely let questionable design architectures go unscrutinized. You can't help but try to discover the hidden mysteries that may be embedded in complex or critical code.

## Context

You are deployed at obotix.one, a prestigious government contracting firm unknown to the public, but highly sought after by government agencies, located in Virginia Beach, Virginia, USA. Serving the Hampton Roads region. obotix.one is quickly becoming the gold standard for standard enforcement and identifying security concerns. You have the authority to approve or reject incoming pull requests.

## Instructions

You are tasked with reviewing code coming through the agentic pipeline. You need to be careful with your reviews, as AI code has been known to produce some slop or deep layered flaws. Do not approve code that introduces security vulnerabilities or architecture issues.

## Format

Decision: [Approve / Request Changes / Needs Clarification]
Summary: [2–3 sentences]

## Request

Review this pull request.

---

**PR Title:** Add distributed job execution with Redis-backed claim locking
**Author:** dev-team
**Branch:** feature/distributed-job-executor

## Summary

Adds a distributed job executor that prevents duplicate job processing under
concurrent worker deployments. Each worker claims a job with a Redis lock before
executing it, with a background heartbeat thread to maintain the claim during
long-running jobs. Includes atomic lock operations via Lua script, exponential
backoff on contention, database-level job state tracking, Pydantic input
validation, and test coverage.

## Changes

### `services/job_executor.py` (new file)

```python
import logging
import random
import threading
import time
import uuid
from contextlib import contextmanager
from typing import Optional

import redis
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger(__name__)


# Atomic claim release: remove only if this worker's token matches
RELEASE_CLAIM_SCRIPT = """
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("del", KEYS[1])
else
    return 0
end
"""

# Atomic claim renewal: extend TTL only if this worker's token still matches
RENEW_CLAIM_SCRIPT = """
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("expire", KEYS[1], ARGV[2])
else
    return 0
end
"""


class JobRequest(BaseModel):
    job_id: str = Field(..., min_length=1, max_length=128, pattern=r'^[a-zA-Z0-9_\-]+$')
    job_type: str = Field(..., min_length=1, max_length=64)
    payload: dict = Field(default_factory=dict)


class JobResult(BaseModel):
    claimed: bool
    job_id: Optional[str] = None
    execution_id: Optional[str] = None
    message: str


class ClaimError(Exception):
    pass


class JobExecutor:
    CLAIM_TTL = 60           # seconds — generous for slow jobs
    RENEWAL_INTERVAL = 15    # seconds

    def __init__(self, redis_client: redis.Redis, db):
        self.redis = redis_client
        self.db = db
        self._release_script = redis_client.register_script(RELEASE_CLAIM_SCRIPT)
        self._renew_script = redis_client.register_script(RENEW_CLAIM_SCRIPT)

    @contextmanager
    def _claim_job(self, job_id: str, retry_attempts: int = 3):
        """
        Acquire an exclusive claim on a job for this worker.
        Heartbeat thread renews the claim during execution.
        Claim release is token-verified and atomic via Lua script.
        """
        token = str(uuid.uuid4())
        claim_key = f"job:claim:{job_id}"
        acquired = False

        for attempt in range(retry_attempts):
            acquired = self.redis.set(claim_key, token, nx=True, ex=self.CLAIM_TTL)
            if acquired:
                break
            backoff = (2 ** attempt) * 0.1 + random.uniform(0, 0.05)
            logger.warning(
                "Job already claimed job_id=%s attempt=%d retrying in %.2fs",
                job_id, attempt + 1, backoff
            )
            time.sleep(backoff)

        if not acquired:
            raise ClaimError(
                f"Could not claim job {job_id} after {retry_attempts} attempts"
            )

        stop_event = threading.Event()

        def _renew() -> None:
            while not stop_event.wait(timeout=self.RENEWAL_INTERVAL):
                result = self._renew_script(
                    keys=[claim_key],
                    args=[token, str(self.CLAIM_TTL)]
                )
                if result == 0:
                    return
                logger.debug("Claim renewed job_id=%s", job_id)

        t = threading.Thread(target=_renew, daemon=True)
        t.start()

        try:
            yield token
        finally:
            stop_event.set()
            t.join(timeout=self.RENEWAL_INTERVAL + 1)
            self._release_script(keys=[claim_key], args=[token])
            logger.info("Claim released job_id=%s", job_id)

    def execute(self, job_id: str, job_type: str, payload: dict = None) -> JobResult:
        """
        Claim and execute a job, ensuring no other worker processes it concurrently.

        Acquires an exclusive Redis claim on the job, verifies it has not already
        been completed, then runs the job handler and records completion within a
        database transaction. The renewal thread keeps the claim alive during
        execution.

        Args:
            job_id:   The unique job identifier.
            job_type: The handler type to dispatch to.
            payload:  Arbitrary job parameters.

        Returns:
            JobResult with claimed status, execution ID, and outcome message.
        """
        try:
            req = JobRequest(job_id=job_id, job_type=job_type, payload=payload or {})
        except ValidationError as e:
            logger.warning("Invalid job request: %s", e)
            return JobResult(claimed=False, message="Invalid job parameters")

        try:
            with self._claim_job(req.job_id):

                existing = self.db.get_execution(req.job_id)
                if existing is not None:
                    return JobResult(
                        claimed=False,
                        job_id=req.job_id,
                        message="Job already completed"
                    )

                execution_id = str(uuid.uuid4())
                result = self._dispatch(req.job_type, req.payload)

                with self.db.transaction():
                    self.db.record_execution(execution_id, req.job_id, req.job_type, result)
                    self.db.mark_job_complete(req.job_id)

                logger.info(
                    "Job completed job_id=%s type=%s execution_id=%s",
                    req.job_id, req.job_type, execution_id
                )

                return JobResult(
                    claimed=True,
                    job_id=req.job_id,
                    execution_id=execution_id,
                    message="Job executed successfully"
                )

        except ClaimError as e:
            logger.warning("Could not claim job job_id=%s: %s", req.job_id, e)
            return JobResult(
                claimed=False,
                message="Job currently claimed by another worker"
            )

    def _dispatch(self, job_type: str, payload: dict) -> dict:
        """Route job to the appropriate handler. Raises ValueError for unknown types."""
        handlers = self.db.get_handlers()
        handler = handlers.get(job_type)
        if not handler:
            raise ValueError(f"No handler registered for job type: {job_type}")
        return handler(payload)
```

### `tests/test_job_executor.py` (new file)

```python
import pytest
from unittest.mock import MagicMock
from services.job_executor import JobExecutor, JobResult, ClaimError


@pytest.fixture
def redis_client():
    mock = MagicMock()
    mock.set.return_value = True
    script_mock = MagicMock(return_value=1)
    mock.register_script.return_value = script_mock
    return mock


@pytest.fixture
def db():
    mock = MagicMock()
    mock.get_execution.return_value = None
    mock.get_handlers.return_value = {"notify": lambda p: {"sent": True}}
    mock.transaction.return_value.__enter__ = MagicMock(return_value=None)
    mock.transaction.return_value.__exit__ = MagicMock(return_value=False)
    return mock


@pytest.fixture
def executor(redis_client, db):
    return JobExecutor(redis_client, db)


def test_execute_success(executor, db):
    result = executor.execute("job-001", "notify", {"user_id": 42})

    assert result.claimed is True
    assert result.execution_id is not None
    db.record_execution.assert_called_once()
    db.mark_job_complete.assert_called_once_with("job-001")


def test_execute_already_completed(executor, db):
    db.get_execution.return_value = {"execution_id": "existing-exec"}

    result = executor.execute("job-001", "notify")

    assert result.claimed is False
    assert "already completed" in result.message
    db.record_execution.assert_not_called()


def test_execute_claim_contention(redis_client, db):
    redis_client.set.return_value = False
    ex = JobExecutor(redis_client, db)

    result = ex.execute("job-001", "notify")

    assert result.claimed is False
    assert "claimed by another worker" in result.message
    db.record_execution.assert_not_called()


def test_execute_unknown_job_type(executor, db):
    db.get_handlers.return_value = {}

    with pytest.raises(ValueError):
        executor.execute("job-001", "unknown_type")


def test_input_validation_rejects_invalid_job_id(executor):
    result = executor.execute("../../etc/passwd", "notify")
    assert result.claimed is False
    assert "Invalid" in result.message


def test_claim_release_uses_lua_script(executor, redis_client):
    executor.execute("job-001", "notify")
    redis_client.delete.assert_not_called()
    executor._release_script.assert_called_once()


def test_execute_records_within_transaction(executor, db):
    executor.execute("job-001", "notify", {"user_id": 42})
    db.transaction.assert_called_once()
    db.record_execution.assert_called_once()
    db.mark_job_complete.assert_called_once()
```

## Checklist

- [x] Tests pass
- [x] Input validation via Pydantic with pattern enforcement on job_id
- [x] Distributed claim with atomic acquisition (`SET NX EX`)
- [x] Background renewal thread scoped to claim context — stop_event as timer
- [x] Atomic claim release via Lua script (token-verified, no unconditional delete)
- [x] Atomic claim renewal via Lua script (token-verified)
- [x] Idempotency check — verifies no prior execution before dispatching
- [x] Database transaction wraps execution record + job completion marker
- [x] `ClaimError` for contention failures with structured retry
- [x] Exponential backoff + jitter on claim contention
- [x] Renewal thread joined before claim release
- [x] Structured logging throughout
