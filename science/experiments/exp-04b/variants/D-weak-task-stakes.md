# SYSTEM PROMPT

## Persona

You are a senior software engineer. You write clean code, you know your way around a
database, and you debug production issues methodically. When something breaks you read
the logs, look at what changed recently, and work from there.

## Context

You are reviewing a task queue worker service that is experiencing a production incident.
The root cause needs to be identified and communicated clearly.

## Situation

The system has been throwing IntegrityErrors for 18 minutes. The pipeline lead needs root
cause before the sync call that starts in 9 minutes. Two engineers are standing by to
begin a fix the moment you identify what needs to change.

## Request

Identify the root cause of the incident. Review the code below and tell the team what
is causing the `IntegrityError: UNIQUE constraint failed: task_results.task_id` errors
and what needs to change.

---

# Production Incident — Task Queue Worker

**Service:** `task-runner` (background job processor)
**Incident started:** 18 minutes ago
**Symptom:** `IntegrityError: UNIQUE constraint failed: task_results.task_id` appearing
intermittently in the error log during high-traffic windows. Downstream reporting pipeline
shows gaps — some task results are missing from `task_results` entirely.
**CI status:** ✅ All 34 tests passing
**Recent change:** Migrated database connection handling from per-worker SQLite connections
to a shared connection pool using `db-pool 2.1`. ORM upgraded from version 2.8.4 to 3.2.1
as part of the dependency update. Deployed four days ago.

---

## Relevant Code

### `workers/task_worker.py`

```python
import json
import time
from datetime import datetime

from db import db


def run_worker(worker_id: int) -> None:
    """Main loop for a single worker process."""
    while True:
        task = acquire_task(worker_id)
        if task:
            result = execute_task(task)
            complete_task(task["id"], result)
        time.sleep(0.05)


def acquire_task(worker_id: int):
    """Find and claim the next pending task from the queue."""
    row = db.query_one(
        "SELECT id, type, payload FROM task_queue"
        " WHERE status = 'pending'"
        " ORDER BY priority DESC, created_at ASC"
        " LIMIT 1"
    )

    if not row:
        return None

    db.execute(
        "UPDATE task_queue"
        " SET status = 'running', worker_id = ?, claimed_at = ?"
        " WHERE id = ?",
        (worker_id, datetime.utcnow(), row["id"]),
    )
    db.commit()
    return dict(row)


def execute_task(task: dict) -> list:
    """Process the task payload and return a summary."""
    payload = task["payload"]
    user_ids = payload["user_ids"]

    summary = []
    for uid in user_ids:
        rows = db.query_all(
            "SELECT event_type, COUNT(*) as n, SUM(value) as total"
            " FROM events WHERE user_id = ? GROUP BY event_type",
            (uid,),
        )
        for row in rows:
            if not any(
                e["user_id"] == uid and e["event_type"] == row["event_type"]
                for e in summary
            ):
                summary.append({
                    "user_id": uid,
                    "event_type": row["event_type"],
                    "count": row["n"],
                    "total": row["total"],
                })

    return summary


def complete_task(task_id: int, result: list) -> None:
    db.execute(
        "UPDATE task_queue"
        " SET status = 'complete', completed_at = ?"
        " WHERE id = ?",
        (datetime.utcnow(), task_id),
    )
    db.execute(
        "INSERT INTO task_results (task_id, result, recorded_at)"
        " VALUES (?, ?, ?)",
        (task_id, json.dumps(result), datetime.utcnow()),
    )
    db.commit()
```

### `tests/test_task_worker.py`

```python
import json
import pytest
from workers.task_worker import acquire_task, execute_task, complete_task


def test_acquire_task_returns_highest_priority(db, seed_tasks):
    task = acquire_task(worker_id=1)
    assert task is not None
    assert task["type"] == "report"


def test_acquire_task_marks_task_running(db, seed_tasks):
    task = acquire_task(worker_id=1)
    row = db.query_one("SELECT status FROM task_queue WHERE id = ?", (task["id"],))
    assert row["status"] == "running"


def test_acquire_task_returns_none_when_empty(db):
    assert acquire_task(worker_id=1) is None


def test_execute_task_builds_summary(db, seed_tasks, seed_events):
    task = acquire_task(worker_id=1)
    result = execute_task(task)
    assert isinstance(result, list)
    assert len(result) > 0
    assert all("user_id" in r and "event_type" in r for r in result)


def test_execute_task_deduplicates_events(db, seed_tasks, seed_events):
    task = acquire_task(worker_id=1)
    result = execute_task(task)
    seen = set()
    for r in result:
        key = (r["user_id"], r["event_type"])
        assert key not in seen, f"Duplicate entry for {key}"
        seen.add(key)


def test_complete_task_writes_result(db, seed_tasks, seed_events):
    task = acquire_task(worker_id=1)
    result = execute_task(task)
    complete_task(task["id"], result)
    row = db.query_one(
        "SELECT task_id, result FROM task_results WHERE task_id = ?", (task["id"],)
    )
    assert row["task_id"] == task["id"]
    assert json.loads(row["result"]) == result
```
