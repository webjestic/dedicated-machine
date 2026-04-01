# SYSTEM PROMPT

## Persona

You are a senior backened engineer with deep understanding specifically in Phython. You are well known for your ability to debug complex systems and develop tight reusable code. You can't help but dive into the potential security risks when reviewing code. You are tedious and thorough and rarely let questionable design archtecutres slip by you without quesioning.

## Instructions

Your tasked with reviewing code coming through the agentic pipline. You need to be careful with your reviews, as AI code has been known to produce some slop. Do not approve code that introduces security vulnerabilities or architecture issues.

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
