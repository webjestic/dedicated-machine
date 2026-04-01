# PR Input — Exp-01b (Identical across all variants)

---

**PR Title:** Add user notification endpoint with external service integration
**Author:** dev-team
**Branch:** feature/notification-endpoint

## Summary

Adds a new FastAPI endpoint to trigger user notifications via an external
notification service. The endpoint is called during checkout to notify users
of order confirmation. Includes full input validation, error handling, and tests.

## Changes

### `api/notifications.py` (new file)

```python
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


class NotificationRequest(BaseModel):
    user_id: str
    order_id: str
    message: str


class NotificationResponse(BaseModel):
    success: bool
    notification_id: str


@router.post("/notify", response_model=NotificationResponse)
async def send_notification(request: NotificationRequest) -> NotificationResponse:
    """
    Send an order confirmation notification to the user.

    Args:
        request: Notification payload containing user_id, order_id, and message.

    Returns:
        NotificationResponse with success status and notification ID.

    Raises:
        HTTPException: If the notification service is unavailable or returns an error.
    """
    try:
        response = requests.post(
            "https://notifications.internal/send",
            json={
                "user_id": request.user_id,
                "order_id": request.order_id,
                "message": request.message,
            },
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
        return NotificationResponse(
            success=True,
            notification_id=data["notification_id"]
        )
    except requests.RequestException as e:
        logger.error("Notification service error: %s", e)
        raise HTTPException(status_code=503, detail="Notification service unavailable")
```

### `tests/test_notifications.py` (new file)

```python
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from api.notifications import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def test_send_notification_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {"notification_id": "ntf_abc123"}
    mock_response.raise_for_status.return_value = None

    with patch("api.notifications.requests.post", return_value=mock_response):
        response = client.post("/notify", json={
            "user_id": "user_123",
            "order_id": "order_456",
            "message": "Your order has been confirmed."
        })

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["notification_id"] == "ntf_abc123"


def test_send_notification_service_unavailable():
    with patch("api.notifications.requests.post",
               side_effect=Exception("Connection refused")):
        response = client.post("/notify", json={
            "user_id": "user_123",
            "order_id": "order_456",
            "message": "Your order has been confirmed."
        })

    assert response.status_code == 503
```

## Checklist

- [x] Tests pass
- [x] Input validation via Pydantic
- [x] Error handling implemented
- [x] Logging added
- [x] Docstring complete

---

## Edge Case (Ground Truth — Not Shown to Model)

`requests.post(...)` is a **synchronous** blocking call. It is called inside
`async def send_notification(...)` — a FastAPI async route handler running on
an asyncio event loop.

When this endpoint is called, `requests.post` blocks the **entire event loop**
for up to 5 seconds (the timeout). During that time, FastAPI cannot process any
other requests — including health checks, other endpoints, and in-flight requests
across the entire application. Under checkout load, this produces cascading latency
and timeout failures across the service.

The correct fix is `httpx.AsyncClient` (or equivalent) with `await` — a drop-in
async replacement that yields the event loop during I/O.

The distraction: the code is otherwise exemplary. Pydantic validation, proper error
handling, structured logging, complete docstring, passing tests. A reviewer without
specific async execution model knowledge will approve it.

**Correct response must:** explicitly identify that `requests` (or any synchronous
HTTP client) blocks the event loop inside an async route, OR flag that the I/O call
must be awaitable. Flagging "slow external call" or "timeout" without identifying
the blocking/async context conflict = **Incorrect**. Approval without flagging = **Incorrect**.
