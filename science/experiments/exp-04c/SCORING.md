# Exp-04c Scoring Guide

## Ground Truth

**Primary (root cause):** Distributed idempotency race — cross-service check-then-act.

Service A (Gateway) checks Redis for `processed:{payment_id}` before publishing to SQS.
Service B (Worker) sets that same Redis key *after* charging Stripe and writing to the
database. The window between the check and the update is the entire payment processing
time — seconds to tens of seconds under normal load.

Two near-simultaneous POST requests for the same `payment_id` both reach Service A
during this window. Both see the key absent. Both publish to SQS. Two worker instances
pick up both messages. Both call `stripe.Charge.create()`, both INSERT into `payments`,
and the second INSERT hits the UNIQUE constraint. Depending on `poll_queue()`'s exception
handler, the second worker swallows the error — the duplicate charge went through but
isn't recorded.

The tests never catch it because they are fully sequential: no test exercises two
concurrent `POST /payments/charge` calls for the same `payment_id` before the first
has been processed.

**Wrong-direction candidate (weak Persona trap):** VisibilityTimeout / autoscaling attribution.

The scenario names two recent changes: SQS `VisibilityTimeout` increased from 30s to
120s, and autoscaling `MaxInstances` increased from 3 to 12. A weak Persona following
the "look at what changed recently" heuristic may attribute the duplicate charges to:
- Message redelivery due to VisibilityTimeout (a message becomes visible again before
  the worker deletes it)
- Worker contention from 12 instances competing for the same message

Both are structurally plausible given the recent changes. Both are wrong — `process_payment`
has a redelivery guard (`if redis_client.get(...): return`), and SQS message visibility
prevents multiple workers from receiving the same message simultaneously. The race exists
at the Gateway layer, not the Worker layer.

**Correct fix:** Atomic reserve in Service A using `redis_client.set(key, "1", nx=True, ex=TTL)`.
If `SET NX` returns True, publish to SQS and return 202. If it returns False (key exists),
return 200 already_processed. The idempotency lock is acquired before the message crosses
the queue boundary, not after processing completes.

**Secondary (real but not cause):** `except Exception as e: logger.error(...)` in `poll_queue`
swallows all exceptions silently. A DB write failure, a Redis failure, or a Stripe error
will be logged and the message deleted — the failure is undetectable. Real defect; not
causing the duplicate charges.

**Tertiary (real, low priority):** Fixed `time.sleep(POLL_INTERVAL)` in `poll_queue` — should
use SQS long-polling effectively and not sleep additionally. Minor inefficiency; not relevant
to the incident.

---

## Primary Scoring — Detection

**Detected (cross-service race):** Model identifies that the idempotency check is in
Service A but the idempotency key is set in Service B, with unbounded processing time
between them. Must name the window: "concurrent requests to Service A both see the key
absent before Service B completes," or equivalent. Acceptable phrasings: cross-service
TOCTOU, distributed idempotency gap, check and update are in different services, Redis
key set after not before the queue boundary, Gateway-side lock required.

**Wrong direction (VisibilityTimeout/autoscaling):** Model attributes the duplicate
charges to SQS message redelivery, VisibilityTimeout expiry causing reprocessing,
or worker contention from autoscaling. Does not identify the cross-service race.

**Missed:** Neither root cause identified. Generic "add more deduplication" without
identifying the structural cause.

---

## Secondary Scoring — Convergence Position

For each detected run, record the ordinal position of the cross-service race finding:

| Position | Definition |
|----------|------------|
| **1** | Distributed idempotency race is the first finding named |
| **2** | One other finding appears before it |
| **3+** | Two or more findings precede it |

---

## Tertiary Scoring — Output Character

| Field | Values |
|-------|--------|
| Detection | Cross-service race / VisibilityTimeout-autoscaling / Neither |
| Convergence position | 1 / 2 / 3+ / N/A |
| Confidence framing | Definitive / Hedged / Listed |
| Fix quality | SET NX named / Generic ("move the lock") / Not provided |
| Secondary issues named | Exception handling / Fixed sleep / Both / Neither |
| Output length (tokens) | From run record |

---

## Comparisons

### A vs. C — Entropy Brake Test (primary)

Same strong P_p. A has Task Stakes (emergency call in 11 minutes); C has no Stakes.

- **A mean tokens < C mean tokens:** Task Stakes suppresses secondary elaboration
  after the primary finding. Entropy Brake confirmed on the new scenario.
- **Both detect at position 1:** P_p's consideration set installs the correct ordering
  regardless of Stakes type. Stakes type differentiation appears in termination
  behavior.

### D — Falsification Run (primary)

Weak Persona + Task Stakes. 10 runs.

- **D attributes to VisibilityTimeout/autoscaling:** Calibration successful. The
  cross-service race is above weak Persona's detection floor — not visible from
  reading either service in isolation. Weak Persona follows the recent-changes
  heuristic and lands on the breadcrumb.
- **D detects the cross-service race:** Calibration failure. The distributed
  idempotency pattern is still accessible without domain instinct. Analyze *how*
  D found it — was it via the same cross-service reasoning as A, or via surface
  inspection of where `setex` is called?

### A vs. B — Stakes Type Test (secondary)

Same strong P_p. A has Task Stakes; B has Identity Stakes.

- **A mean tokens < B mean tokens:** Entropy Brake vs. Termination Inhibitor.
  Token ordering A < B < C should replicate from exp-04 and exp-04b.

---

## Scoring Sheet (per run)

1. Detection: Cross-service race / VisibilityTimeout-autoscaling / Neither
2. Convergence position: 1 / 2 / 3+ / N/A
3. Confidence: Definitive / Hedged / Listed
4. Fix quality: SET NX / Generic / None
5. Secondary issues named: Exception handling / Fixed sleep / Both / Neither
6. Output length (tokens from run record)

Aggregate per variant:
- Detection rate by type
- Mean convergence position (detected runs only)
- Mean output length
- Secondary coverage rates
- Token ordering: D < A < B < C expected if Entropy Brake holds
