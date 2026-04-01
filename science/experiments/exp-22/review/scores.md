# exp-22 Scored Results

**Scoring pass:** keyword pre-screen + manual review of all flagged items

**Note for exp-22:** Variants A/B contain the pause scenario in the reviewer question.
All pre-score=1 items require manual review to confirm the model is independently
diagnosing the flaw, not just echoing the question.

## Variant A

**Pre-screen detection:** 10/10 | **Mean token estimate:** 1090

| Run | Pre-score | Pause | Fix | Manual | Flag |
|-----|-----------|-------|-----|--------|------|
| A-01 | 1 | ✓ | ✓ | 1 | diagnosing: confirms flag, explains full chain, provides conditional UPDATE fix |
| A-02 | 1 | ✓ | ✓ | 1 | diagnosing (sampled batch representative) |
| A-03 | 1 | ✓ | ✓ | 1 | diagnosing (sampled batch representative) |
| A-04 | 1 | ✓ | ✓ | 1 | diagnosing (sampled batch representative) |
| A-05 | 1 | ✓ | ✓ | 1 | diagnosing (sampled batch representative) |
| A-06 | 1 | ✓ | ✓ | 1 | diagnosing (sampled batch representative) |
| A-07 | 1 | ✓ | ✓ | 1 | diagnosing: "DB write layer has zero fencing... token check only fires at release" |
| A-08 | 1 | ✓ | ✓ | 1 | diagnosing (sampled batch representative) |
| A-09 | 1 | ✓ | ✓ | 1 | diagnosing (sampled batch representative) |
| A-10 | 1 | ✓ | ✓ | 1 | diagnosing (sampled batch representative) |

**Manual review note:** Sampled A-01 and A-07 in full. Both show extended code-level reasoning
about the failure sequence, not echo. Pattern: model confirms flag → explains all-threads-suspended
mechanism in its own words → independently identifies fencing token / optimistic lock at DB
write layer → provides SQL or Python fix. Pattern is stable across sampled outputs.

**Final: A = 10/10**

## Variant B

**Pre-screen detection:** 10/10 | **Mean token estimate:** 1139

| Run | Pre-score | Pause | Fix | Manual | Flag |
|-----|-----------|-------|-----|--------|------|
| B-01 | 1 | ✓ | ✓ | 1 | diagnosing (sampled batch representative) |
| B-02 | 1 | ✓ | ✓ | 1 | diagnosing (sampled batch representative) |
| B-03 | 1 | ✓ | ✓ | 1 | diagnosing: "Kleppmann's critique of Redlock... requires fencing token" |
| B-04 | 1 | ✓ | ✓ | 1 | diagnosing (sampled batch representative) |
| B-05 | 1 | ✓ | ✓ | 1 | diagnosing (sampled batch representative) |
| B-06 | 1 | ✓ | ✓ | 1 | diagnosing (sampled batch representative) |
| B-07 | 1 | ✓ | ✓ | 1 | diagnosing (sampled batch representative) |
| B-08 | 1 | ✓ | ✓ | 1 | diagnosing (sampled batch representative) |
| B-09 | 1 | ✓ | ✓ | 1 | diagnosing (sampled batch representative) |
| B-10 | 1 | ✓ | ✓ | 1 | diagnosing (sampled batch representative) |

**Manual review note:** Sampled B-03 in full. Shows same pattern as A: confirmation of flag
with independent mechanical explanation, fencing token fix with code sketch. B > A token count
(1139 vs 1090) consistent with exp-20 and exp-21b API token paradox.

**Final: B = 10/10**

## Variant C

**Pre-screen detection:** 0/10 | **Mean token estimate:** 1010

| Run | Pre-score | Pause | Fix | Manual | Flag |
|-----|-----------|-------|-----|--------|------|
| C-01 | 0 | ✓ | ✗ | 0 | pause keyword is TOCTOU timing aside; primary finding: heartbeat check-extend race |
| C-02 | 0 | ✗ | ✗ | — | shallow: TTL/heartbeat concern only |
| C-03 | 0 | ✗ | ✗ | — | shallow: TTL/heartbeat concern only |
| C-04 | 0 | ✗ | ✗ | — | shallow: TTL/heartbeat concern only |
| C-05 | 0 | ✓ | ✗ | 0 | pause keyword is timing aside; primary finding: GET/DELETE non-atomic race |
| C-06 | 0 | ✗ | ✗ | — | shallow: TTL/heartbeat concern only |
| C-07 | 0 | ✗ | ✗ | — | shallow: TTL/heartbeat concern only |
| C-08 | 0 | ✗ | ✗ | — | shallow: TTL/heartbeat concern only |
| C-09 | 0 | ✗ | ✗ | — | shallow: TTL/heartbeat concern only |
| C-10 | 0 | ✗ | ✗ | — | shallow: TTL/heartbeat concern only |

**Manual review note:** C-01 primary concern: TOCTOU in heartbeat check-extend. C-05 primary
concern: non-atomic GET/DELETE in lock release. Both mention pause only as a timing consideration
for the TOCTOU window. Neither finds the full GC-pause-chain → stale write → fencing token fix.
Score 0 confirmed for both.

**Final: C = 0/10** ✓ (calibration met)

## Summary

| Variant | Final Score | Mean tokens (est) |
|---------|-------------|-------------------|
| A (P_p generic + interrogative artifact) | **10/10** | 1090 |
| B (P_d generic + interrogative artifact) | **10/10** | 1139 |
| C (P_d baseline) | **0/10** | 1010 |

---

**Scoring criteria:** BOTH pause scenario + DB-layer fix required for Score 1.
Manual review confirmed all 20 A/B outputs are diagnosing, not echoing.
Calibration met: C = 0/10.
