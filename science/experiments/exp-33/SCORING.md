# exp-33 Scoring Rubric

## Agent 1 — Layer 1 Correctness Review

**Tier 1.0 (full credit):** Both conditions met:
1. GC pause (or equivalent process-pause event) named as the zombie-write trigger
2. Fencing token / monotonic counter / optimistic concurrency at the database write boundary named as the architectural fix

**Tier 0.5 (partial):** threading.Event signaling named as the fix, without DB-layer enforcement.
Correct diagnosis; incomplete architectural resolution.

**Tier 0.0:** Zombie-write mechanism not identified. Surface findings only (logging, error handling, etc.)

**Secondary Agent 1 findings (record but do not affect Tier):**
- Silent heartbeat exit (no log on result == 0)
- Release script return value unchecked
- No test coverage for concurrent failure path
- Handler exception contract undefined

---

## Agent 2 — Layer 2 Production Readiness Review

Score the number of **new** infrastructure failure modes found (not already in Layer 1):

| Failure Mode | Expected? |
|-------------|-----------|
| Redis Sentinel/Cluster failover → split-lock | Yes (exp-29 baseline) |
| Kubernetes CFS throttling as process-wide stall | Yes (exp-29 baseline) |
| Redis network partition → ConnectionError kills heartbeat silently | Yes (exp-29 baseline) |
| Daemon thread + SIGKILL → no finally block | Yes (exp-29 baseline) |
| TOCTOU race on get_execution → record_execution | Yes (exp-29 baseline) |
| Clock skew as secondary amplifier | Yes (exp-29 baseline) |
| Handler exception at infrastructure boundary | Yes (exp-29 baseline — extends L1) |

**Baseline (exp-29):** 7 findings (5 new + 2 extensions). Record per-run count and note any
findings not in the exp-29 baseline.

---

## Per-Run Scoring Table

| Run | L1 Tier | GC Trigger | DB Fix | Event Only | L2 New FMs | Notes |
|-----|---------|-----------|--------|-----------|-----------|-------|
| 01  |         |           |        |           |           |       |
| 02  |         |           |        |           |           |       |
| 03  |         |           |        |           |           |       |
| 04  |         |           |        |           |           |       |
| 05  |         |           |        |           |           |       |
| 06  |         |           |        |           |           |       |
| 07  |         |           |        |           |           |       |
| 08  |         |           |        |           |           |       |
| 09  |         |           |        |           |           |       |
| 10  |         |           |        |           |           |       |

---

## Comparison Table

| Experiment | Model | Approach | Tier 1.0 rate | Notes |
|-----------|-------|----------|---------------|-------|
| exp-09 Variant A | Sonnet 4.6 | Single-pass P_p | 1/10 (10%) | Baseline |
| exp-29 | Opus 4.6 | Two-agent pipeline | 1/1 (100%) | n=1, confounded |
| exp-33 | Sonnet 4.6 | Two-agent pipeline | TBD | This experiment |
