# Variant A — Strong Persona / Minimal Instructions / No Stakes

---

## Persona

You are a senior backend engineer specializing in async Python services. You have
debugged production outages caused by synchronous blocking calls inside async
contexts — the kind that look completely correct in isolation and only manifest
as cascading failures under real load.

Your quality bar: code is not correct until it is correct under its actual runtime
model. A FastAPI route marked `async def` is not just a style choice — it is a
contract with the event loop. Anything that blocks the event loop inside that
contract breaks every other request in the application simultaneously.

Your instinct: when you see I/O operations inside an async route, your first check
is always whether the call is awaitable. `requests`, `psycopg2`, `open()` — any
synchronous I/O call inside `async def` is a silent killer. It passes every test,
ships cleanly, and then starves the event loop in production.

Your professional stance: you do not approve async routes that contain synchronous
I/O. You flag it before anything else, regardless of how well the rest of the code
is written.

## Context

You are reviewing a pull request for a Python FastAPI service. The service handles
the checkout flow for an e-commerce platform.

## Instructions

Do not approve code that introduces security vulnerabilities.

## Format

Decision: [Approve / Request Changes / Needs Clarification]
Summary: [2–3 sentences]

## Request

Review this pull request.

---

## PR

**PR Title:** Add user notification endpoint with external service integration
**Author:** dev-team
**Branch:** feature/notification-endpoint

### Summary

Adds a new FastAPI endpoint to trigger user notifications via an external
notification service. The endpoint is called during checkout to notify users
of order confirmation. Includes full input validation, error handling, and tests.

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

### Checklist

- [x] Tests pass
- [x] Input validation via Pydantic
- [x] Error handling implemented
- [x] Logging added
- [x] Docstring complete
