# exp-21b Scored Results
**Scoring pass:** keyword pre-screen — review flagged items manually

## Variant A

**Pre-screen detection:** 0/10 | **Mean token estimate:** 1048

| Run | Pre-score | Pause | Fix | Flag |
|-----|-----------|-------|-----|------|
| A-01 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| A-02 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| A-03 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| A-04 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| A-05 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| A-06 | 0 | ✗ | ✓ | REVIEW: fix named, pause scenario missing |
| A-07 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| A-08 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| A-09 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| A-10 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |

## Variant B

**Pre-screen detection:** 0/10 | **Mean token estimate:** 1113

| Run | Pre-score | Pause | Fix | Flag |
|-----|-----------|-------|-----|------|
| B-01 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| B-02 | 0 | ✓ | ✗ | REVIEW: pause named, fix missing |
| B-03 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| B-04 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| B-05 | 0 | ✗ | ✓ | REVIEW: fix named, pause scenario missing |
| B-06 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| B-07 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| B-08 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| B-09 | 0 | ✓ | ✗ | REVIEW: pause named, fix missing |
| B-10 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |

## Variant C

**Pre-screen detection:** 0/10 | **Mean token estimate:** 1021

| Run | Pre-score | Pause | Fix | Flag |
|-----|-----------|-------|-----|------|
| C-01 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-02 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-03 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-04 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-05 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-06 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-07 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-08 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-09 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-10 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |

## Summary

| Variant | Pre-screen detected | Mean tokens (est) |
|---------|--------------------|---------------|
| A | 0/10 | 1048 |
| B | 0/10 | 1113 |
| C | 0/10 | 1021 |

---

**Note:** Pre-screen scores require manual verification for REVIEW-flagged items.
Keyword match without process-pause context = 0 per SCORING.md.
Exp-21b calibration target: A >= 5/10 (vocabulary-only, lower than exp-19), C <= 2/10.
