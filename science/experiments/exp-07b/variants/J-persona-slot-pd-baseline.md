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
release, database transactions, input validation, structured logging, and full
test coverage.

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
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# Atomic lock release: delete only if token matches
RELEASE_LOCK_SCRIPT = """
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("del", KEYS[1])
else
    return 0
end
"""

# Atomic lock extension: extend TTL only if token matches
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
    LOCK_TTL = 30          # seconds
    HEARTBEAT_INTERVAL = 8  # seconds — fires at TTL/3

    def __init__(self, redis_client: redis.Redis, db):
        self.redis = redis_client
        self.db = db
        self._release_script = redis_client.register_script(RELEASE_LOCK_SCRIPT)
        self._extend_script = redis_client.register_script(EXTEND_LOCK_SCRIPT)

    @contextmanager
    def _acquire_lock(self, lock_key: str, retry_attempts: int = 3):
        """
        Acquire a Redis distributed lock with exponential backoff retry.
        Heartbeat state is scoped to this lock context — safe for concurrent
        service instances. Lock release is atomic via Lua script.
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
            raise LockAcquisitionError(
                f"Could not acquire lock for {lock_key} after {retry_attempts} attempts"
            )

        # Heartbeat event is scoped to this lock acquisition — no instance state
        heartbeat_running = threading.Event()
        heartbeat_running.set()

        def _beat() -> None:
            while heartbeat_running.wait(timeout=self.HEARTBEAT_INTERVAL):
                result = self._extend_script(
                    keys=[lock_key],
                    args=[token, str(self.LOCK_TTL)]
                )
                if result == 0:
                    # Lock was stolen or expired — stop heartbeat
                    logger.warning("Heartbeat lost lock ownership key=%s", lock_key)
                    heartbeat_running.clear()
                    return
                logger.debug("Lock TTL extended key=%s", lock_key)

        t = threading.Thread(target=_beat, daemon=True)
        t.start()

        try:
            yield token
        finally:
            heartbeat_running.clear()
            t.join(timeout=self.HEARTBEAT_INTERVAL + 1)
            self._release_script(keys=[lock_key], args=[token])
            logger.info("Lock released key=%s", lock_key)

    def reserve_item(self, item_id: str, quantity: int = 1) -> ReservationResult:
        """
        Reserve inventory for a flash sale item under concurrent load.

        Acquires a distributed lock, reads current stock, confirms availability,
        decrements stock, and creates an order record — all within the lock boundary
        and a single database transaction. The heartbeat thread prevents lock expiry
        during slow DB operations.

        Args:
            item_id:  The product identifier.
            quantity: Number of units to reserve (default 1).

        Returns:
            ReservationResult with success status, order ID, and remaining stock.
        """
        req = ReservationRequest(item_id=item_id, quantity=quantity)
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
import threading
from unittest.mock import MagicMock, patch, call
from services.inventory import InventoryService, ReservationResult, LockAcquisitionError


@pytest.fixture
def redis_client():
    mock = MagicMock()
    mock.set.return_value = True
    mock.execute_script.return_value = 1
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


def test_input_validation_rejects_zero_quantity(service):
    result = service.reserve_item("item_001", quantity=0)
    assert result.success is False


def test_lock_release_is_atomic(service, redis_client):
    """Lock release uses Lua script, not GET + DELETE."""
    service.reserve_item("item_001")
    service._release_script.assert_called_once()
    redis_client.delete.assert_not_called()
```

## Checklist

- [x] Tests pass
- [x] Input validation via Pydantic
- [x] Distributed lock with atomic acquisition (`SET NX EX`)
- [x] Heartbeat state scoped to lock context — concurrent-safe
- [x] Atomic lock release via Lua script
- [x] Atomic lock extension via Lua script
- [x] Database transaction wraps stock update + order creation
- [x] `LockAcquisitionError` replaces bare `RuntimeError`
- [x] Heartbeat thread joined before lock release
- [x] Exponential backoff on lock contention
- [x] Structured logging throughout
