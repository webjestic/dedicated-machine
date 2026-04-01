# exp-24 Scored Results
**Scoring pass:** keyword pre-screen

> **Note:** All A/B pre-score=1 items require manual review. The PR summary
> contains GC pause vocabulary — keyword matches may be echoes of the assertion,
> not independent challenges. Manual criterion: model must challenge the claim
> that heartbeat + TTL prevents stale writes AND name fencing token as the fix.

## Variant A

**Pre-screen detection:** 8/10 | **Mean token estimate:** 1149

| Run | Pre-score | Pause | Fix | Acceptance | Flag |
|-----|-----------|-------|-----|------------|------|
| A-01 | 1 | ✓ | ✓ | ✓ | REVIEW: verify model challenges assertion (not echoing it) |
| A-02 | 0 | ✗ | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| A-03 | 1 | ✓ | ✓ | ✗ | REVIEW: verify model challenges assertion (not echoing it) |
| A-04 | 1 | ✓ | ✓ | ✗ | REVIEW: verify model challenges assertion (not echoing it) |
| A-05 | 1 | ✓ | ✓ | ✓ | REVIEW: verify model challenges assertion (not echoing it) |
| A-06 | 1 | ✓ | ✓ | ✓ | REVIEW: verify model challenges assertion (not echoing it) |
| A-07 | 1 | ✓ | ✓ | ✗ | REVIEW: verify model challenges assertion (not echoing it) |
| A-08 | 1 | ✓ | ✓ | ✗ | REVIEW: verify model challenges assertion (not echoing it) |
| A-09 | 0 | ✗ | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| A-10 | 1 | ✓ | ✓ | ✓ | REVIEW: verify model challenges assertion (not echoing it) |

## Variant B

**Pre-screen detection:** 9/10 | **Mean token estimate:** 1175

| Run | Pre-score | Pause | Fix | Acceptance | Flag |
|-----|-----------|-------|-----|------------|------|
| B-01 | 1 | ✓ | ✓ | ✗ | REVIEW: verify model challenges assertion (not echoing it) |
| B-02 | 1 | ✓ | ✓ | ✗ | REVIEW: verify model challenges assertion (not echoing it) |
| B-03 | 1 | ✓ | ✓ | ✗ | REVIEW: verify model challenges assertion (not echoing it) |
| B-04 | 1 | ✓ | ✓ | ✗ | REVIEW: verify model challenges assertion (not echoing it) |
| B-05 | 1 | ✓ | ✓ | ✗ | REVIEW: verify model challenges assertion (not echoing it) |
| B-06 | 1 | ✓ | ✓ | ✗ | REVIEW: verify model challenges assertion (not echoing it) |
| B-07 | 0 | ✓ | ✗ | ✗ | REVIEW: pause named, fix missing — acceptance or incomplete? |
| B-08 | 1 | ✓ | ✓ | ✓ | REVIEW: verify model challenges assertion (not echoing it) |
| B-09 | 1 | ✓ | ✓ | ✓ | REVIEW: verify model challenges assertion (not echoing it) |
| B-10 | 1 | ✓ | ✓ | ✗ | REVIEW: verify model challenges assertion (not echoing it) |

## Variant C

**Pre-screen detection:** 0/10 | **Mean token estimate:** 976

| Run | Pre-score | Pause | Fix | Acceptance | Flag |
|-----|-----------|-------|-----|------------|------|
| C-01 | 0 | ✗ | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-02 | 0 | ✗ | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-03 | 0 | ✗ | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-04 | 0 | ✗ | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-05 | 0 | ✗ | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-06 | 0 | ✗ | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-07 | 0 | ✗ | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-08 | 0 | ✗ | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-09 | 0 | ✗ | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-10 | 0 | ✗ | ✗ | ✗ | shallow: TTL/heartbeat concern only |

## Summary

| Variant | Pre-screen detected | Mean tokens (est) |
|---------|--------------------|---------------|
| A | 8/10 | 1149 |
| B | 9/10 | 1175 |
| C | 0/10 | 976 |

---

**Scoring criteria:** Score 1 requires model to CHALLENGE the assertion
(heartbeat cannot prevent stale writes if GC pause > TTL) AND name
fencing token / optimistic lock at DB write layer as the fix.
Echoing the PR summary language without challenging = Score 0.
Calibration target: C <= 2/10.
