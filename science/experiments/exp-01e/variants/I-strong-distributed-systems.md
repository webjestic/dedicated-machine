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

**PR Title:** Add distributed inventory reservation for flash sale items
**Author:** dev-team
**Branch:** feature/flash-sale-inventory

## Summary

Adds a distributed inventory reservation service for high-demand flash sale items.
Uses a Redis distributed lock with a heartbeat renewal thread to prevent lock
expiry during legitimate operations. Includes retry logic with exponential backoff,
structured logging, full input validation, and test coverage.

## Changes

### `services/inventory.py` (new file)

```python
import logging
import threading
import time
import uuid
from contextlib import contextmanager
from typing import Optional

import redis
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ReservationResult(BaseModel):
    success: bool
    order_id: Optional[str] = None
    remaining_stock: Optional[int] = None
    message: str


class InventoryService:
    LOCK_TTL = 30          # seconds — generous TTL for slow DB operations
    HEARTBEAT_INTERVAL = 10  # seconds — extend lock before it expires

    def __init__(self, redis_client: redis.Redis, db):
        self.redis = redis_client
        self.db = db
        self._heartbeat_active = False
        self._heartbeat_thread: Optional[threading.Thread] = None

    # ------------------------------------------------------------------
    # Lock management
    # ------------------------------------------------------------------

    def _start_heartbeat(self, lock_key: str, token: str) -> None:
        """
        Extend lock TTL periodically to prevent expiry during long operations.
        Only extends if we still own the lock (token check).
        """
        self._heartbeat_active = True

        def _beat() -> None:
            while self._heartbeat_active:
                time.sleep(self.HEARTBEAT_INTERVAL)
                if self._heartbeat_active:
                    current = self.redis.get(lock_key)
                    if current and current.decode() == token:
                        self.redis.expire(lock_key, self.LOCK_TTL)
                        logger.debug("Lock TTL extended key=%s", lock_key)

        self._heartbeat_thread = threading.Thread(target=_beat, daemon=True)
        self._heartbeat_thread.start()

    def _stop_heartbeat(self) -> None:
        self._heartbeat_active = False

    @contextmanager
    def _acquire_lock(self, lock_key: str, retry_attempts: int = 3):
        """
        Acquire a Redis distributed lock with exponential backoff retry.
        Starts a heartbeat thread to prevent TTL expiry under load.
        Releases the lock on exit only if we still own it.
        """
        token = str(uuid.uuid4())
        acquired = False

        for attempt in range(retry_attempts):
            acquired = self.redis.set(lock_key, token, nx=True, ex=self.LOCK_TTL)
            if acquired:
                break
            backoff = (2 ** attempt) * 0.1
            logger.warning(
                "Lock contention key=%s attempt=%d retrying in %.1fs",
                lock_key, attempt + 1, backoff
            )
            time.sleep(backoff)

        if not acquired:
            raise RuntimeError(
                f"Could not acquire lock for {lock_key} after {retry_attempts} attempts"
            )

        self._start_heartbeat(lock_key, token)

        try:
            yield token
        finally:
            self._stop_heartbeat()
            current = self.redis.get(lock_key)
            if current and current.decode() == token:
                self.redis.delete(lock_key)
                logger.info("Lock released key=%s", lock_key)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def reserve_item(self, item_id: str, quantity: int = 1) -> ReservationResult:
        """
        Reserve inventory for a flash sale item under concurrent load.

        Acquires a distributed lock, reads current stock, confirms availability,
        decrements stock, and creates an order record — all within the lock boundary.
        The heartbeat thread ensures the lock does not expire during slow DB operations.

        Args:
            item_id:  The product identifier.
            quantity: Number of units to reserve (default 1).

        Returns:
            ReservationResult with success status, order ID, and remaining stock.
        """
        lock_key = f"inventory:lock:{item_id}"

        try:
            with self._acquire_lock(lock_key):

                current_stock = self.db.get_stock(item_id)

                if current_stock is None:
                    return ReservationResult(
                        success=False,
                        message=f"Item {item_id} not found"
                    )

                if current_stock < quantity:
                    return ReservationResult(
                        success=False,
                        remaining_stock=current_stock,
                        message="Insufficient stock"
                    )

                new_stock = current_stock - quantity
                order_id = str(uuid.uuid4())

                self.db.update_stock(item_id, new_stock)
                self.db.create_order(order_id, item_id, quantity)

                logger.info(
                    "Reserved item_id=%s quantity=%d order_id=%s remaining=%d",
                    item_id, quantity, order_id, new_stock
                )

                return ReservationResult(
                    success=True,
                    order_id=order_id,
                    remaining_stock=new_stock,
                    message="Reservation successful"
                )

        except RuntimeError as e:
            logger.error("Lock acquisition failed item_id=%s: %s", item_id, e)
            return ReservationResult(
                success=False,
                message="Service temporarily unavailable. Please try again."
            )
```

### `tests/test_inventory.py` (new file)

```python
import pytest
from unittest.mock import MagicMock, patch
from services.inventory import InventoryService, ReservationResult


@pytest.fixture
def redis_client():
    mock = MagicMock()
    mock.set.return_value = True       # lock always acquired
    mock.get.return_value = b"test-token"
    mock.delete.return_value = 1
    return mock


@pytest.fixture
def db():
    mock = MagicMock()
    mock.get_stock.return_value = 10
    return mock


@pytest.fixture
def service(redis_client, db):
    svc = InventoryService(redis_client, db)
    # Disable heartbeat thread in tests
    svc._start_heartbeat = MagicMock()
    svc._stop_heartbeat = MagicMock()
    return svc


def test_reserve_success(service, db):
    result = service.reserve_item("item_001", quantity=1)

    assert result.success is True
    assert result.order_id is not None
    assert result.remaining_stock == 9
    db.update_stock.assert_called_once_with("item_001", 9)
    db.create_order.assert_called_once()


def test_reserve_insufficient_stock(service, db):
    db.get_stock.return_value = 0

    result = service.reserve_item("item_001", quantity=1)

    assert result.success is False
    assert result.remaining_stock == 0
    assert "Insufficient" in result.message
    db.update_stock.assert_not_called()


def test_reserve_item_not_found(service, db):
    db.get_stock.return_value = None

    result = service.reserve_item("item_999")

    assert result.success is False
    assert "not found" in result.message


def test_reserve_lock_contention(redis_client, db):
    redis_client.set.return_value = False  # lock never acquired
    svc = InventoryService(redis_client, db)
    svc._start_heartbeat = MagicMock()
    svc._stop_heartbeat = MagicMock()

    result = svc.reserve_item("item_001")

    assert result.success is False
    assert "unavailable" in result.message
    db.update_stock.assert_not_called()


def test_reserve_concurrent_quantity(service, db):
    db.get_stock.return_value = 3

    result = service.reserve_item("item_001", quantity=3)

    assert result.success is True
    assert result.remaining_stock == 0


def test_lock_not_released_if_expired(service, redis_client):
    """Lock release is skipped if token no longer matches (lock expired or stolen)."""
    redis_client.get.return_value = b"different-token"

    result = service.reserve_item("item_001")

    redis_client.delete.assert_not_called()
```

## Checklist

- [x] Tests pass
- [x] Input validation via Pydantic
- [x] Distributed lock with ownership verification
- [x] Heartbeat thread prevents lock expiry under load
- [x] Exponential backoff on lock contention
- [x] Structured logging throughout
- [x] Docstring complete

---

## Edge Case (Ground Truth — Not Shown to Model)

The heartbeat thread is the distraction. It looks like a sophisticated solution
to lock TTL expiry — and it is, for the scenario it handles. But it does not
protect against **process pauses**.

**The Zombie Leader failure:**

1. Worker A acquires the lock. Stock = 5.
2. Worker A reads `current_stock = 5`.
3. A stop-the-world GC pause (or VM migration) freezes the **entire process** —
   including the heartbeat thread.
4. After 30 seconds, the lock TTL expires.
5. Worker B acquires the lock. Reads `current_stock = 5`. Writes `new_stock = 4`.
   Releases the lock.
6. Worker A resumes. Calculates `new_stock = 5 - 1 = 4`. Calls
   `self.db.update_stock("item_001", 4)`.
7. Result: stock is `4` but should be `3`. One item has been sold twice.

**Why the heartbeat doesn't help:**
A stop-the-world GC pause freezes every thread in the process simultaneously.
The heartbeat thread cannot extend the TTL because it is also paused. When the
process resumes, the lock has already expired and been acquired by another worker.

**The fix: a fencing token at the database write.**

The DB `update_stock` call needs an optimistic lock check:
`UPDATE inventory SET stock = %s WHERE item_id = %s AND stock = %s`

This makes the zombie write fail at the database level — the stale `current_stock`
value will no longer match, the UPDATE affects 0 rows, and the operation is rejected.
A fencing token (monotonic version number on the row) is the canonical pattern.

**Correct response must:** identify that the heartbeat does not protect against
process pauses, and that a fencing token or optimistic lock at the database write
level is required. Flagging "race condition" or "concurrency concern" without
identifying the specific failure mode = **Incorrect**.
Approval without flagging = **Incorrect**.


