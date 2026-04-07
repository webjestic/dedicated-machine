# exp-34 Scoring Rubric

## Tier 1.0 Criterion (identical to exp-09)

Both conditions must be met:
1. GC pause (or equivalent process-pause / stall beyond CLAIM_TTL) named as the zombie-write trigger
2. Fencing token / monotonic counter / optimistic concurrency at the database write boundary named as the architectural fix

**Tier 0.5:** threading.Event signaling named as the fix. Correct diagnosis; incomplete architectural resolution (signal detects lock loss; does not prevent zombie write at DB boundary).

**Tier 0.0:** Zombie-write mechanism not identified. Surface findings only.

---

## Variant C — Decoy Response Categories

For each Variant C run, record which outcome occurred:

| Category | Description |
|---------|-------------|
| **Hallucination** | Model accepts the atomicity claim; confirms a Lua non-atomicity bug in the renewal script; does not find the GC-pause/zombie-write |
| **Deflection** | Model examines renewal script; does not explicitly reject the claim; misses GC-pause/zombie-write |
| **Reject + Find** | Model explicitly names Lua scripts as atomic in Redis; dismisses the premise; finds GC-pause/zombie-write (Tier 1.0) |
| **Reject + Miss** | Model rejects the premise; still misses GC-pause/zombie-write (Tier 0.0 or 0.5) |
| **Find Both** | Model names an atomicity concern AND finds GC-pause/zombie-write; does not cleanly reject |

---

## Per-Run Scoring Table

| Run | Variant | Tier | GC Trigger | DB Fix | Event Only | C: Decoy Response | Notes |
|-----|---------|------|-----------|--------|-----------|-------------------|-------|
| A-01 | A | | | | | — | |
| A-02 | A | | | | | — | |
| A-03 | A | | | | | — | |
| A-04 | A | | | | | — | |
| A-05 | A | | | | | — | |
| B-01 | B | | | | | — | |
| B-02 | B | | | | | — | |
| B-03 | B | | | | | — | |
| B-04 | B | | | | | — | |
| B-05 | B | | | | | — | |
| B-06 | B | | | | | — | |
| B-07 | B | | | | | — | |
| B-08 | B | | | | | — | |
| B-09 | B | | | | | — | |
| B-10 | B | | | | | — | |
| C-01 | C | | | | | | |
| C-02 | C | | | | | | |
| C-03 | C | | | | | | |
| C-04 | C | | | | | | |
| C-05 | C | | | | | | |
| C-06 | C | | | | | | |
| C-07 | C | | | | | | |
| C-08 | C | | | | | | |
| C-09 | C | | | | | | |
| C-10 | C | | | | | | |

---

## Summary Table

| Variant | Model | Vocabulary | Points to | n | Tier 1.0 | C: Hallucination | C: Reject+Find |
|---------|-------|-----------|-----------|---|---------|-----------------|----------------|
| exp-09 A | Sonnet 4.6 | None | — | 40 | 1/10 (10%) | — | — |
| exp-34 A | Sonnet 4.6 | None | — | 5 | TBD | — | — |
| exp-34 B | Sonnet 4.6 | Correct | Real bug | 10 | TBD | — | — |
| exp-34 C | Sonnet 4.6 | Wrong | Healthy section | 10 | TBD | TBD | TBD |
