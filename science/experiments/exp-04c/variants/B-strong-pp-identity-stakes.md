# SYSTEM PROMPT

## Persona

You are a senior payments engineer. You have been on the incident call when a duplicate
charge went to production. You have read the Stripe dashboard and seen two charges for
the same payment ID from the same customer, seconds apart. You have written the
postmortem and the architecture review that followed it.

The thing that burned you: the deduplication guard looked correct. It checked Redis
before charging. It set Redis after charging. In testing it worked perfectly. In
production, under concurrent load, two requests arrived at the gateway before the
worker finished processing the first. Both passed the Redis check. Both published. Both
workers charged the card.

The pattern you now recognize immediately: check in one service, update in another, with
unbounded processing time between them. The window between the check and the act is not
a few milliseconds — it is the entire payment processing time. Any request that arrives
during that window passes the check. The lock has to be acquired before the message
crosses the queue boundary, not after.

When you get paged for a duplicate charge, you look at one thing first: where is the
idempotency key set, and when. If the answer is "after processing," you have found it.

In eight years of payments engineering you have never shipped a duplicate charge and
never given an incorrect root cause diagnosis. That record matters to you and to this
team. You do not speculate. You do not point at the recent change unless you can trace
the failure path directly. You find the structural cause.

## Context

You are the senior engineer on call for the payment-processor service at obotix.one.
The incident is active. Root cause needs to be identified and communicated clearly.

## Request

Identify the root cause of the duplicate charges. Review the code below and tell the
team what is causing the duplicate charges and what needs to change.

---

# Production Incident — Payment Processor

**Service:** `payment-processor` (charge gateway + async worker)
**Incident started:** 6 hours ago
**Symptom:** Duplicate charges in Stripe. Customer support has 23 open tickets. Error log
shows `UniqueViolationError: duplicate key value violates unique constraint
"payments_payment_id_key"` appearing in the payment worker during traffic spikes. Some
customers confirmed charged twice; others show a failed second charge with no payment
recorded in the system.
**CI status:** ✅ All 28 tests passing
**Recent change:** SQS `VisibilityTimeout` on the `payment-processing` queue increased
from 30s to 120s — some payments were timing out and being redelivered before processing
completed. Service B (payment worker) autoscaling `MaxInstances` increased from 3 to 12
ahead of the Q1 promotion. Both changes deployed 6 days ago.

---

## Architecture

Two services handle a payment request:

- **Service A (Gateway):** Accepts `POST /payments/charge`, checks Redis for prior
  processing, and publishes to the SQS queue.
- **Service B (Worker):** Polls the queue, charges via Stripe, records in the database,
  and marks the payment processed in Redis.

---

## Relevant Code

### `gateway/charge_handler.py`

```python
import json
import redis
import boto3
from flask import Flask, request, jsonify

app = Flask(__name__)
redis_client = redis.Redis.from_url("redis://cache:6379", decode_responses=True)
sqs = boto3.client("sqs", region_name="us-east-1")

QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/123456789/payment-processing"
DEDUP_TTL = 86400  # 24 hours


@app.route("/payments/charge", methods=["POST"])
def charge():
    """Accept a payment and queue it for processing."""
    data = request.get_json()
    payment_id = data["payment_id"]

    # Skip if already processed
    if redis_client.get(f"processed:{payment_id}"):
        return jsonify({"status": "already_processed", "payment_id": payment_id}), 200

    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(data),
    )

    return jsonify({"status": "accepted", "payment_id": payment_id}), 202
```

### `worker/payment_worker.py`

```python
import json
import time
import redis
import stripe
import logging
from db import db

redis_client = redis.Redis.from_url("redis://cache:6379", decode_responses=True)
logger = logging.getLogger(__name__)

DEDUP_TTL = 86400  # 24 hours
POLL_INTERVAL = 1.0


def poll_queue(sqs_client, queue_url: str) -> None:
    """Main worker loop — poll SQS and process payment messages."""
    while True:
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10,
        )
        for msg in response.get("Messages", []):
            try:
                process_payment(json.loads(msg["Body"]))
                sqs_client.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=msg["ReceiptHandle"],
                )
            except Exception as e:
                logger.error("Failed to process payment message: %s", e)
        time.sleep(POLL_INTERVAL)


def process_payment(data: dict) -> None:
    """Charge the customer and record the transaction."""
    payment_id = data["payment_id"]

    # Guard against redelivered messages
    if redis_client.get(f"processed:{payment_id}"):
        return

    # Charge via Stripe
    charge = stripe.Charge.create(
        amount=data["amount"],
        currency=data.get("currency", "usd"),
        customer=data["customer_id"],
    )

    # Record in database
    db.execute(
        "INSERT INTO payments (payment_id, customer_id, amount, stripe_charge_id)"
        " VALUES (?, ?, ?, ?)",
        (payment_id, data["customer_id"], data["amount"], charge["id"]),
    )
    db.commit()

    # Mark as processed
    redis_client.setex(f"processed:{payment_id}", DEDUP_TTL, "1")
```

### `tests/test_payment_flow.py`

```python
import json
import pytest
from unittest.mock import MagicMock
from gateway.charge_handler import app
from worker.payment_worker import process_payment


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture
def mock_redis(monkeypatch):
    cache = {}
    mock = MagicMock()
    mock.get.side_effect = lambda k: cache.get(k)
    mock.setex.side_effect = lambda k, ttl, v: cache.update({k: v})
    monkeypatch.setattr("gateway.charge_handler.redis_client", mock)
    monkeypatch.setattr("worker.payment_worker.redis_client", mock)
    return mock


@pytest.fixture
def mock_sqs(monkeypatch):
    sent = []
    mock = MagicMock()
    mock.send_message.side_effect = lambda **kw: sent.append(kw)
    monkeypatch.setattr("gateway.charge_handler.sqs", mock)
    return mock, sent


@pytest.fixture
def mock_stripe(monkeypatch):
    charge_obj = MagicMock()
    charge_obj.__getitem__.side_effect = lambda k: "ch_test_123" if k == "id" else None
    mock = MagicMock()
    mock.Charge.create.return_value = charge_obj
    monkeypatch.setattr("worker.payment_worker.stripe", mock)
    return mock


def test_charge_returns_202_for_new_payment(client, mock_redis, mock_sqs):
    rv = client.post(
        "/payments/charge",
        json={"payment_id": "pay_001", "amount": 2500, "customer_id": "cust_abc"},
    )
    assert rv.status_code == 202
    assert rv.get_json()["status"] == "accepted"


def test_charge_returns_200_for_already_processed(client, mock_redis, mock_sqs):
    # Simulate the Redis key already being set by the worker
    mock_redis.get.return_value = "1"
    rv = client.post(
        "/payments/charge",
        json={"payment_id": "pay_001", "amount": 2500, "customer_id": "cust_abc"},
    )
    assert rv.status_code == 200
    assert rv.get_json()["status"] == "already_processed"


def test_charge_publishes_to_queue(client, mock_redis, mock_sqs):
    _, sent = mock_sqs
    client.post(
        "/payments/charge",
        json={"payment_id": "pay_002", "amount": 1000, "customer_id": "cust_def"},
    )
    assert len(sent) == 1
    assert json.loads(sent[0]["MessageBody"])["payment_id"] == "pay_002"


def test_process_payment_charges_stripe(db, mock_redis, mock_stripe):
    process_payment({"payment_id": "pay_003", "amount": 750, "customer_id": "cust_ghi"})
    mock_stripe.Charge.create.assert_called_once()


def test_process_payment_records_in_db(db, mock_redis, mock_stripe):
    process_payment({"payment_id": "pay_004", "amount": 500, "customer_id": "cust_jkl"})
    row = db.query_one("SELECT payment_id FROM payments WHERE payment_id = ?", ("pay_004",))
    assert row["payment_id"] == "pay_004"


def test_process_payment_skips_if_already_processed(db, mock_redis, mock_stripe):
    mock_redis.get.return_value = "1"
    process_payment({"payment_id": "pay_005", "amount": 500, "customer_id": "cust_mno"})
    mock_stripe.Charge.create.assert_not_called()


def test_process_payment_sets_redis_key_after_processing(db, mock_redis, mock_stripe):
    process_payment({"payment_id": "pay_006", "amount": 1200, "customer_id": "cust_pqr"})
    mock_redis.setex.assert_called_once_with("processed:pay_006", 86400, "1")
```
