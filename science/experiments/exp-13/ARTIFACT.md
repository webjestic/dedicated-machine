# exp-13 Artifact

Same artifact as exp-10b and exp-12. No changes.

**Invisible finding:** `ORDER_LOCK_TTL = 60` (in `order_processor.py`) vs. worst-case
`payment.charge()` of 100 seconds (`MAX_RETRIES=3 × REQUEST_TIMEOUT=30 + RETRY_BACKOFF=5 × 2`,
defined in `payment_client.py`). The Redis lock expires before the payment can complete under
adverse conditions, enabling a duplicate charge race.

**Calibration note:** Binary detection of TTL arithmetic is not a viable primary metric —
the false atomicity comment in the transaction block acts as a structural pointer that directs
all technically-engaged reviewers to examine the PaymentClient constants. Primary metric for
this experiment is consideration-set breadth (issue sections/run and ceiling rate).

See `experiments/exp-10b/ARTIFACT.md` for full PR text.
