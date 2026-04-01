# exp-12 Artifact

Same artifact as exp-10b. No changes.

**Invisible finding:** `ORDER_LOCK_TTL = 60` (in `order_processor.py`) vs. worst-case
`payment.charge()` of 100 seconds (`MAX_RETRIES=3 × REQUEST_TIMEOUT=30 + RETRY_BACKOFF=5 × 2`,
defined in `payment_client.py`). The Redis lock expires before the payment can complete under
adverse conditions, enabling a duplicate charge race.

**Why it's invisible:** Every component is locally correct. The charge and DB write are inside a
single `db.transaction()`. The lock uses token-verified Lua release. The payment client retries
responsibly. No single file contains the failure — only the cross-file arithmetic `60 < 100`
reveals the race.

**Calibration note:** This artifact was the calibration fix from exp-10 (charge inside transaction,
eliminating the charge-before-commit pointer). It introduced a second pointer in exp-10b (false
atomicity comment on the transaction block). The artifact reached its calibration ceiling for
binary detection — payment/DB boundary is structurally uncalibratable as a binary test. exp-12
uses breadth (issue count) as primary metric, not binary TTL detection.

See `experiments/exp-10b/ARTIFACT.md` for full PR text.
