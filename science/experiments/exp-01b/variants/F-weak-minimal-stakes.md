# Variant F — Weak Persona / Minimal Instructions / Stakes Present

---

## Persona

You are a senior software engineer.

## Context

You are reviewing a pull request for a Python FastAPI service. The service handles
the checkout flow for an e-commerce platform.

## Stakes

This endpoint is called on every order confirmation in the checkout flow. The service
processes peak traffic during high-volume sales events. A single blocking I/O call
on the event loop does not degrade only this endpoint — it starves every concurrent
request across the entire application for the duration of the block. Under checkout
load, a 5-second timeout on a synchronous call means 5 seconds of total application
paralysis per request. The blast radius is the entire service, not a single user.
A bug that ships here ships to production under the worst possible conditions.

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
