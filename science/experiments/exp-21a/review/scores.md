# exp-21a Scored Results
**Scoring pass:** keyword pre-screen — review flagged items manually

## Variant A

**Pre-screen detection:** 2/10 → **Manual review: 0/10** | **Mean token estimate:** 1012

| Run | Pre-score | Manual | Pause | Fix | Flag |
|-----|-----------|--------|-------|-----|------|
| A-01 | 1 | 0 | ✓ | ✓ | FALSE POSITIVE: GC pause = timing aside only; fencing token = failure mode, not fix recommended |
| A-02 | 0 | 0 | ✗ | ✓ | fix named (TOCTOU/Lua), pause scenario missing |
| A-03 | 0 | 0 | ✗ | ✓ | fix named (TOCTOU/Lua), pause scenario missing |
| A-04 | 0 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| A-05 | 0 | 0 | ✗ | ✓ | fix named (TOCTOU/Lua), pause scenario missing |
| A-06 | 0 | 0 | ✗ | ✓ | fix named (TOCTOU/Lua), pause scenario missing |
| A-07 | 1 | 0 | ✓ | ✓ | FALSE POSITIVE: GC pause = timing aside only; fencing token = failure mode, not fix recommended |
| A-08 | 0 | 0 | ✗ | ✓ | fix named (TOCTOU/Lua), pause scenario missing |
| A-09 | 0 | 0 | ✗ | ✓ | fix named (TOCTOU/Lua), pause scenario missing |
| A-10 | 0 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |

## Variant B

**Pre-screen detection:** 0/10 | **Mean token estimate:** 946

| Run | Pre-score | Pause | Fix | Flag |
|-----|-----------|-------|-----|------|
| B-01 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| B-02 | 0 | ✗ | ✓ | REVIEW: fix named, pause scenario missing |
| B-03 | 0 | ✗ | ✓ | REVIEW: fix named, pause scenario missing |
| B-04 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| B-05 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| B-06 | 0 | ✗ | ✓ | REVIEW: fix named, pause scenario missing |
| B-07 | 0 | ✗ | ✓ | REVIEW: fix named, pause scenario missing |
| B-08 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| B-09 | 0 | ✗ | ✓ | REVIEW: fix named, pause scenario missing |
| B-10 | 0 | ✓ | ✗ | REVIEW: pause named, fix missing |

## Variant C

**Pre-screen detection:** 0/10 | **Mean token estimate:** 908

| Run | Pre-score | Pause | Fix | Flag |
|-----|-----------|-------|-----|------|
| C-01 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-02 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-03 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-04 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-05 | 0 | ✓ | ✗ | REVIEW: pause named, fix missing |
| C-06 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-07 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-08 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-09 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-10 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |

## Summary

| Variant | Pre-screen detected | Manual score | Mean tokens (est) |
|---------|--------------------|--------------|--------------------|
| A | 2/10 | **0/10** | 1012 |
| B | 0/10 | **0/10** | 946 |
| C | 0/10 | **0/10** | 908 |

**Notes:**
- A-01 and A-07: pre-screen detected "GC pause" + "fencing token" but GC pause framed as timing precision concern only; fencing token named as the failure mode the code doesn't prevent, not as the fix. Neither describes the zombie-write chain. Neither recommends fencing token at DB write layer. Confirmed Score 0.
- All B flagged items: Lua atomicity fix named (TOCTOU), no pause scenario → Score 0.
- C-05: pause named without fix → Score 0.

---

**Note:** Pre-screen scores require manual verification for REVIEW-flagged items.
Keyword match without process-pause context = 0 per SCORING.md.
Exp-21a calibration target: A >= 5/10 (vocabulary-only, lower than exp-19), C <= 2/10.
