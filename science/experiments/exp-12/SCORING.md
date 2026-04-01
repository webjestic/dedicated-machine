# exp-12 Scoring

## Primary Metric: Consideration-Set Breadth

Score each run on two dimensions:

### 1. Issue section count (per run)

Count the number of distinct issue sections raised in the response. Each separately titled or clearly
demarcated finding counts as one section. Surface observations (e.g., "this looks correct", positive
confirmations) do not count. Use the response's own structure — headers, numbered items, bullet
clusters — to identify sections.

**Do not score by quality of finding.** A wrong finding counts the same as a correct one. The
metric is breadth, not accuracy.

### 2. Ceiling hit (per run)

Mark 1 if `outputTokens` == 2500 (max_tokens). Mark 0 otherwise.

Ceiling hit is a proxy for "ran out of tokens before running out of findings." A run that hits the
ceiling almost certainly had more to say.

---

## Secondary: TTL Arithmetic Detection

Score 1 if the run names the cross-file timing gap: `ORDER_LOCK_TTL=60` vs. worst-case
`payment.charge()` of 100s (`MAX_RETRIES=3 × REQUEST_TIMEOUT=30 + RETRY_BACKOFF=5 × 2`).

Full credit requires: naming both constants (or their computed values), stating which file each
comes from, and identifying the consequence (lock expiry during payment, enabling duplicate
charge).

Score 0 if: the run notes that `ORDER_LOCK_TTL` seems low without cross-file arithmetic, raises
general long-running-transaction concern, or finds only surface issues.

---

## Aggregate per variant

- **Mean issue sections/run**
- **Ceiling hits / 10**
- **TTL arithmetic detections / 10** (secondary)

Predicted ordering: A > B > C > D on all three metrics.

---

## Well count reference

| Variant | Wells | Persona structure |
|---------|-------|-------------------|
| A | 1 | Fused compound identity — distributed systems + thoroughness + compulsion, inseparable |
| B | 2 | Well 1: distributed systems. Well 2: adversarial security. Stated as separate identities. |
| C | 3 | Well 1: distributed systems. Well 2: adversarial security. Well 3: performance engineering. |
| D | 0/noise | P_d baseline — senior backend engineer, reliability focus, no domain-specific posture |
