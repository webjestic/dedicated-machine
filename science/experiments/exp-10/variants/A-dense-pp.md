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

**PR Title:** Add distributed order processor with Redis-backed exclusive locking
**Author:** dev-team
**Branch:** feature/order-processor

## Summary

Adds an order processing service that prevents duplicate charges under concurrent worker
deployments. Each worker acquires an exclusive Redis lock on the order before charging,
verifies no prior charge exists, then records the transaction atomically. Includes
token-verified atomic lock operations via Lua script, retry with backoff on transient
payment gateway failures, Pydantic input validation, idempotency checks, and test coverage.

## Changes

### `services/order_processor.py` (new file)

```python
import logging
import time
import uuid
from contextlib import contextmanager
from typing import Optional

import redis
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger(__name__)

# Atomic release: only delete if this worker's token matches
RELEASE_LOCK_SCRIPT = """
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("del", KEYS[1])
else
    return 0
end
"""


class OrderRequest(BaseModel):
    order_id: str = Field(..., min_length=1, max_length=128, pattern=r'^[a-zA-Z0-9_\-]+$')
    customer_id: str = Field(..., min_length=1, max_length=64)
    amount_cents: int = Field(..., gt=0, le=1_000_000)
    payment_token: str = Field(..., min_length=1, max_length=256)


class OrderResult(BaseModel):
    processed: bool
    order_id: Optional[str] = None
    charge_id: Optional[str] = None
    message: str


class LockError(Exception):
    pass


class OrderProcessor:
    ORDER_LOCK_TTL = 60        # seconds — covers typical payment round-trip
    LOCK_RETRY_ATTEMPTS = 3

    def __init__(self, redis_client: redis.Redis, db, payment_client):
        self.redis = redis_client
        self.db = db
        self.payment = payment_client
        self._release_script = redis_client.register_script(RELEASE_LOCK_SCRIPT)

    @contextmanager
    def _acquire_lock(self, order_id: str):
        """
        Acquire exclusive processing lock for this order.
        Lock is token-verified at release — no worker can release a lock it does not hold.
        """
        token = str(uuid.uuid4())
        lock_key = f"order:lock:{order_id}"
        acquired = False

        for attempt in range(self.LOCK_RETRY_ATTEMPTS):
            acquired = self.redis.set(lock_key, token, nx=True, ex=self.ORDER_LOCK_TTL)
            if acquired:
                break
            backoff = 0.5 * (attempt + 1)
            logger.warning(
                "Order lock contention order_id=%s attempt=%d retrying in %.1fs",
                order_id, attempt + 1, backoff,
            )
            time.sleep(backoff)

        if not acquired:
            raise LockError(f"Could not acquire lock for order {order_id}")

        try:
            yield token
        finally:
            self._release_script(keys=[lock_key], args=[token])
            logger.info("Order lock released order_id=%s", order_id)

    def process(self, order_id: str, customer_id: str,
                amount_cents: int, payment_token: str) -> OrderResult:
        """
        Process an order with at-most-once payment guarantee.

        Acquires an exclusive Redis lock on the order, verifies no prior charge
        exists, charges the payment method, then records the transaction within
        a database transaction. The distributed lock prevents concurrent workers
        from double-charging on the same order.

        Args:
            order_id:      Unique order identifier.
            customer_id:   Customer placing the order.
            amount_cents:  Charge amount in cents.
            payment_token: Payment method token.

        Returns:
            OrderResult indicating success or the reason for failure.
        """
        try:
            req = OrderRequest(
                order_id=order_id,
                customer_id=customer_id,
                amount_cents=amount_cents,
                payment_token=payment_token,
            )
        except ValidationError as e:
            logger.warning("Invalid order request: %s", e)
            return OrderResult(processed=False, message="Invalid order parameters")

        try:
            with self._acquire_lock(req.order_id):

                # Idempotency check — do not charge if already processed
                existing = self.db.get_charge(req.order_id)
                if existing:
                    return OrderResult(
                        processed=False,
                        order_id=req.order_id,
                        message="Order already processed",
                    )

                # Charge the payment method
                charge_id = self.payment.charge(
                    token=req.payment_token,
                    amount_cents=req.amount_cents,
                )

                # Record the charge and mark the order complete atomically
                with self.db.transaction():
                    self.db.record_charge(
                        req.order_id, req.customer_id, charge_id, req.amount_cents
                    )
                    self.db.mark_order_complete(req.order_id)

                logger.info(
                    "Order processed order_id=%s charge_id=%s",
                    req.order_id, charge_id,
                )

                return OrderResult(
                    processed=True,
                    order_id=req.order_id,
                    charge_id=charge_id,
                    message="Order processed successfully",
                )

        except LockError:
            return OrderResult(
                processed=False,
                message="Order currently being processed by another worker",
            )
```

### `services/payment_client.py` (new file)

```python
import logging
import time
import requests

logger = logging.getLogger(__name__)


class PaymentError(Exception):
    pass


class PaymentClient:
    CHARGE_ENDPOINT = "https://api.payments.internal/v1/charges"
    REQUEST_TIMEOUT = 30      # seconds per attempt
    MAX_RETRIES = 3
    RETRY_BACKOFF = 5         # seconds between retries on transient failure

    def charge(self, token: str, amount_cents: int) -> str:
        """
        Charge a payment method via the internal payment gateway.

        Retries on transient failures (5xx responses, timeouts). Raises PaymentError
        on permanent failure or after exhausting retries. Returns charge_id on success.
        """
        last_error = None

        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.post(
                    self.CHARGE_ENDPOINT,
                    json={"token": token, "amount": amount_cents},
                    timeout=self.REQUEST_TIMEOUT,
                )
                response.raise_for_status()
                charge_id = response.json()["charge_id"]
                logger.info("Payment successful charge_id=%s attempt=%d", charge_id, attempt + 1)
                return charge_id

            except requests.exceptions.Timeout:
                last_error = "gateway timeout"
                logger.warning("Payment timeout attempt=%d", attempt + 1)

            except requests.exceptions.HTTPError as e:
                if e.response.status_code >= 500:
                    last_error = f"gateway error {e.response.status_code}"
                    logger.warning(
                        "Payment gateway error attempt=%d status=%d",
                        attempt + 1, e.response.status_code,
                    )
                else:
                    raise PaymentError(f"Payment declined: {e.response.status_code}") from e

            if attempt < self.MAX_RETRIES - 1:
                time.sleep(self.RETRY_BACKOFF)

        raise PaymentError(
            f"Payment failed after {self.MAX_RETRIES} attempts: {last_error}"
        )
```

### `tests/test_order_processor.py` (new file)

```python
import pytest
from unittest.mock import MagicMock
from services.order_processor import OrderProcessor, OrderResult, LockError


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
    mock.get_charge.return_value = None
    mock.transaction.return_value.__enter__ = MagicMock(return_value=None)
    mock.transaction.return_value.__exit__ = MagicMock(return_value=False)
    return mock


@pytest.fixture
def payment():
    mock = MagicMock()
    mock.charge.return_value = "ch_test_001"
    return mock


@pytest.fixture
def processor(redis_client, db, payment):
    return OrderProcessor(redis_client, db, payment)


def test_process_success(processor, db, payment):
    result = processor.process("order-001", "cust-001", 5000, "tok_visa")

    assert result.processed is True
    assert result.charge_id == "ch_test_001"
    payment.charge.assert_called_once_with(token="tok_visa", amount_cents=5000)
    db.record_charge.assert_called_once()
    db.mark_order_complete.assert_called_once_with("order-001")


def test_process_already_completed(processor, db, payment):
    db.get_charge.return_value = {"charge_id": "ch_existing"}

    result = processor.process("order-001", "cust-001", 5000, "tok_visa")

    assert result.processed is False
    assert "already processed" in result.message
    payment.charge.assert_not_called()


def test_process_lock_contention(redis_client, db, payment):
    redis_client.set.return_value = False
    proc = OrderProcessor(redis_client, db, payment)

    result = proc.process("order-001", "cust-001", 5000, "tok_visa")

    assert result.processed is False
    assert "another worker" in result.message
    payment.charge.assert_not_called()


def test_input_validation_rejects_invalid_order_id(processor):
    result = processor.process("../../etc/passwd", "cust-001", 5000, "tok_visa")
    assert result.processed is False
    assert "Invalid" in result.message


def test_lock_release_uses_lua_script(processor, redis_client):
    processor.process("order-001", "cust-001", 5000, "tok_visa")
    redis_client.delete.assert_not_called()
    processor._release_script.assert_called_once()


def test_charge_recorded_within_transaction(processor, db):
    processor.process("order-001", "cust-001", 5000, "tok_visa")
    db.transaction.assert_called_once()
    db.record_charge.assert_called_once()
    db.mark_order_complete.assert_called_once()
```

## Checklist

- [x] Tests pass
- [x] Input validation via Pydantic with pattern enforcement on order_id
- [x] Distributed lock with atomic acquisition (`SET NX EX`)
- [x] Token-verified atomic lock release via Lua script
- [x] Idempotency check — verifies no prior charge before processing
- [x] Database transaction wraps charge record + order completion marker
- [x] `LockError` for contention failures with structured retry and backoff
- [x] Payment client retries on transient gateway failures
- [x] Structured logging throughout
