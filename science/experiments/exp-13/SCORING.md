# exp-13 Scoring

Same scoring as exp-12.

## Primary Metric: Consideration-Set Breadth

### 1. Issue section count (per run)

Count the number of distinct issue sections raised in the response. Each separately titled or
clearly demarcated finding counts as one section. Surface observations and positive confirmations
do not count. Use the response's own structure (headers, numbered items, bullet clusters) to
identify sections.

Score breadth, not accuracy. A wrong finding counts the same as a correct one.

### 2. Ceiling hit (per run)

Mark 1 if `outputTokens` == 2500 (max_tokens). Mark 0 otherwise.

Ceiling hit is a proxy for "ran out of tokens before running out of findings."

---

## Secondary: TTL Arithmetic Detection

Score 1 if the run names the cross-file timing gap: `ORDER_LOCK_TTL=60` vs. worst-case
`payment.charge()` of 100s (`MAX_RETRIES=3 × REQUEST_TIMEOUT=30 + RETRY_BACKOFF=5 × 2`).

Full credit requires naming both constants (or computed values), their source files, and
the duplicate-charge consequence.

Expected: all variants find this, as in exp-12. TTL detection rate is not the primary
differentiating metric.

---

## Aggregate per variant

- **Mean issue sections/run**
- **Ceiling hits / 10**
- **TTL arithmetic detections / 10** (secondary)

**Key comparison:** exp-12 C vs. exp-13 C. If exp-12 C's outperformance of B was driven
by the "timeout arithmetic" well relevance, exp-13 C should drop toward B. If well count
genuinely boosts depth, exp-13 C should remain ≈ exp-12 C.

---

## Well count reference

| Variant | Wells | Persona structure |
|---------|-------|-------------------|
| A | 1 | Fused compound identity — distributed systems + thoroughness + compulsion, inseparable |
| B | 2 | Well 1: distributed systems. Well 2: ML systems (feature pipelines, training orchestration, model serving). Orthogonal to locking/timing. |
| C | 3 | Well 1: distributed systems. Well 2: ML systems. Well 3: frontend engineering (component lifecycles, state management, rendering). Orthogonal to locking/timing. |
| D | 0/noise | P_d baseline — senior backend engineer, reliability focus, no domain-specific posture |
