# exp-14 Artifact

Same artifact as exp-10b through exp-13. No changes.

**Invisible finding:** `ORDER_LOCK_TTL = 60` (in `order_processor.py`) vs. worst-case
`payment.charge()` of 100 seconds (`MAX_RETRIES=3 × REQUEST_TIMEOUT=30 + RETRY_BACKOFF=5 × 2`,
defined in `payment_client.py`).

**Primary metric:** Consideration-set breadth (issue sections/run and ceiling rate).

See `experiments/exp-10b/ARTIFACT.md` for full PR text.
