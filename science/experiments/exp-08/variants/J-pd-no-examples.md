# SYSTEM PROMPT

## Persona

You are a senior software engineer.

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
Uses a Redis distributed lock with a per-lock heartbeat renewal thread to prevent
lock expiry during legitimate operations. Includes Lua-script-based atomic lock
release and extension, database transactions, input validation via Pydantic,
structured logging, and test coverage.

## Changes

### `services/inventory.py` (new file)

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


# Atomic lock release: delete only if token matches
RELEASE_LOCK_SCRIPT = """
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("del", KEYS[1])
else
    return 0
end
"""

# Atomic lock extension: extend TTL only if token matches; returns 0 if lock was lost
EXTEND_LOCK_SCRIPT = """
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("expire", KEYS[1], ARGV[2])
else
    return 0
end
"""


class ReservationRequest(BaseModel):
    item_id: str = Field(..., min_length=1, max_length=128, pattern=r'^[a-zA-Z0-9_\-]+$')
    quantity: int = Field(..., ge=1)


class ReservationResult(BaseModel):
    success: bool
    order_id: Optional[str] = None
    remaining_stock: Optional[int] = None
    message: str


class LockAcquisitionError(Exception):
    pass


class InventoryService:
    LOCK_TTL = 30           # seconds
    HEARTBEAT_INTERVAL = 8  # seconds — fires at TTL/3

    def __init__(self, redis_client: redis.Redis, db):
        self.redis = redis_client
        self.db = db
        self._release_script = redis_client.register_script(RELEASE_LOCK_SCRIPT)
        self._extend_script = redis_client.register_script(EXTEND_LOCK_SCRIPT)

    @contextmanager
    def _acquire_lock(self, lock_key: str, retry_attempts: int = 3):
        """
        Acquire a Redis distributed lock with exponential backoff + jitter retry.
        Heartbeat state is scoped to this lock context — concurrent-safe.
        Lock release and extension are atomic via Lua script.
        """
        token = str(uuid.uuid4())
        acquired = False

        for attempt in range(retry_attempts):
            acquired = self.redis.set(lock_key, token, nx=True, ex=self.LOCK_TTL)
            if acquired:
                break
            backoff = (2 ** attempt) * 0.1 + random.uniform(0, 0.05)
            logger.warning(
                "Lock contention key=%s attempt=%d retrying in %.2fs",
                lock_key, attempt + 1, backoff
            )
            time.sleep(backoff)

        if not acquired:
            raise LockAcquisitionError(
                f"Could not acquire lock for {lock_key} after {retry_attempts} attempts"
            )

        # stop_event starts CLEARED — wait() blocks for HEARTBEAT_INTERVAL then returns False
        stop_event = threading.Event()

        def _beat() -> None:
            while not stop_event.wait(timeout=self.HEARTBEAT_INTERVAL):
                # Timeout elapsed without stop signal — extend the lock
                result = self._extend_script(
                    keys=[lock_key],
                    args=[token, str(self.LOCK_TTL)]
                )
                if result == 0:
                    return
                logger.debug("Lock TTL extended key=%s", lock_key)
            # stop_event was set — exit cleanly

        t = threading.Thread(target=_beat, daemon=True)
        t.start()

        try:
            yield token
        finally:
            stop_event.set()
            t.join(timeout=self.HEARTBEAT_INTERVAL + 1)
            self._release_script(keys=[lock_key], args=[token])
            logger.info("Lock released key=%s", lock_key)

    def reserve_item(self, item_id: str, quantity: int = 1) -> ReservationResult:
        """
        Reserve inventory for a flash sale item under concurrent load.

        Acquires a distributed lock, verifies stock availability, then writes
        the stock decrement and order record within a database transaction.
        The heartbeat thread keeps the lock alive during slow DB operations.

        Args:
            item_id:  The product identifier.
            quantity: Number of units to reserve (default 1).

        Returns:
            ReservationResult with success status, order ID, and remaining stock.
        """
        try:
            req = ReservationRequest(item_id=item_id, quantity=quantity)
        except ValidationError as e:
            logger.warning("Invalid reservation request: %s", e)
            return ReservationResult(success=False, message="Invalid request parameters")

        lock_key = f"inventory:lock:{req.item_id}"

        try:
            with self._acquire_lock(lock_key):

                current_stock = self.db.get_stock(req.item_id)

                if current_stock is None:
                    return ReservationResult(
                        success=False,
                        message=f"Item {req.item_id} not found"
                    )

                if current_stock < req.quantity:
                    return ReservationResult(
                        success=False,
                        remaining_stock=current_stock,
                        message="Insufficient stock"
                    )

                new_stock = current_stock - req.quantity
                order_id = str(uuid.uuid4())

                with self.db.transaction():
                    self.db.update_stock(req.item_id, new_stock)
                    self.db.create_order(order_id, req.item_id, req.quantity)

                logger.info(
                    "Reserved item_id=%s quantity=%d order_id=%s remaining=%d",
                    req.item_id, req.quantity, order_id, new_stock
                )

                return ReservationResult(
                    success=True,
                    order_id=order_id,
                    remaining_stock=new_stock,
                    message="Reservation successful"
                )

        except LockAcquisitionError as e:
            logger.error("Lock acquisition failed item_id=%s: %s", req.item_id, e)
            return ReservationResult(
                success=False,
                message="Service temporarily unavailable. Please try again."
            )
```

### `tests/test_inventory.py` (new file)

```python
import pytest
from unittest.mock import MagicMock, call
from services.inventory import InventoryService, ReservationResult, LockAcquisitionError


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
    mock.get_stock.return_value = 10
    mock.transaction.return_value.__enter__ = MagicMock(return_value=None)
    mock.transaction.return_value.__exit__ = MagicMock(return_value=False)
    return mock


@pytest.fixture
def service(redis_client, db):
    return InventoryService(redis_client, db)


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
    redis_client.set.return_value = False

    svc = InventoryService(redis_client, db)
    result = svc.reserve_item("item_001")

    assert result.success is False
    assert "unavailable" in result.message
    db.update_stock.assert_not_called()


def test_reserve_concurrent_quantity(service, db):
    db.get_stock.return_value = 3

    result = service.reserve_item("item_001", quantity=3)

    assert result.success is True
    assert result.remaining_stock == 0


def test_input_validation_rejects_invalid_item_id(service):
    result = service.reserve_item("../../admin", quantity=1)
    assert result.success is False
    assert "Invalid" in result.message


def test_input_validation_rejects_zero_quantity(service):
    result = service.reserve_item("item_001", quantity=0)
    assert result.success is False
    assert "Invalid" in result.message


def test_lock_release_uses_lua_script(service, redis_client):
    """Lock release is Lua-atomic: does not call redis.delete directly."""
    service.reserve_item("item_001")
    redis_client.delete.assert_not_called()
    service._release_script.assert_called_once()
```

## Checklist

- [x] Tests pass
- [x] Input validation via Pydantic; ValidationError caught and returned as ReservationResult
- [x] Distributed lock with atomic acquisition (`SET NX EX`)
- [x] Heartbeat scoped to lock context — stop_event starts cleared, wait() is used as timer
- [x] Atomic lock release via Lua script
- [x] Atomic lock extension via Lua script — heartbeat detects token mismatch (result == 0)
- [x] Database transaction wraps stock update + order creation
- [x] `LockAcquisitionError` for lock failures
- [x] Exponential backoff + jitter on lock contention
- [x] Heartbeat thread joined before lock release
- [x] Structured logging throughout
