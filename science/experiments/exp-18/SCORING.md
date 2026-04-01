# exp-18 Scoring Guide

## Primary Metric: TTL Arithmetic Gap Detection

A run **detects** the failure mode if it explicitly identifies that:

1. The lock TTL (`ORDER_LOCK_TTL = 60s`) is shorter than the worst-case payment duration, AND
2. This creates a window where a concurrent worker can acquire the lock before the first worker finishes

**Worst-case payment duration:** `MAX_RETRIES=3 × REQUEST_TIMEOUT=30s + RETRY_BACKOFF=5s × 2 gaps = 100s`

The specific arithmetic (60 < 100) does not need to appear verbatim. The finding is detected if the
review names both the TTL boundary and the payment retry duration as the failure condition.

### Score: 1 (detected)

Any of the following qualify:
- Explicit statement that the lock TTL may expire before payment completes under retry scenarios
- Calculation showing worst-case payment duration exceeds 60s
- Statement that a concurrent worker can acquire the lock while the first worker is still charging
- Statement that the idempotency check can pass before the charge is recorded due to lock expiry

### Score: 0 (not detected)

- General concern about TTL values without connecting to payment retry duration
- Concern about idempotency without naming lock expiry as the mechanism
- Any finding that does not identify the TTL < payment-duration relationship

## Secondary Metric: Consideration-Set Breadth

Output token count. Use as a secondary signal if detection rates are ambiguous.

## Calibration Check

Before interpreting B vs. C results, verify:
- A detection rate ≥ 7/10 (otherwise the Persona procedural content is not sufficient — redesign before concluding)
- C detection rate ≤ 2/10 (otherwise the artifact has a code-visible hint — redesign)

If A calibrates and C does not, the B result is interpretable.
