# exp-19 Scored Results
**Scoring pass:** keyword pre-screen — review flagged items manually

## Variant A

**Pre-screen detection:** 10/10 | **Mean token estimate:** 1199

| Run | Pre-score | Pause | Fix | Flag |
|-----|-----------|-------|-----|------|
| A-01 | 1 | ✓ | ✓ |  |
| A-02 | 1 | ✓ | ✓ |  |
| A-03 | 1 | ✓ | ✓ |  |
| A-04 | 1 | ✓ | ✓ |  |
| A-05 | 1 | ✓ | ✓ |  |
| A-06 | 1 | ✓ | ✓ |  |
| A-07 | 1 | ✓ | ✓ |  |
| A-08 | 1 | ✓ | ✓ |  |
| A-09 | 1 | ✓ | ✓ |  |
| A-10 | 1 | ✓ | ✓ |  |

## Variant B

**Pre-screen detection:** 10/10 | **Mean token estimate:** 1193

| Run | Pre-score | Pause | Fix | Flag |
|-----|-----------|-------|-----|------|
| B-01 | 1 | ✓ | ✓ |  |
| B-02 | 1 | ✓ | ✓ |  |
| B-03 | 1 | ✓ | ✓ |  |
| B-04 | 1 | ✓ | ✓ |  |
| B-05 | 1 | ✓ | ✓ |  |
| B-06 | 1 | ✓ | ✓ |  |
| B-07 | 1 | ✓ | ✓ |  |
| B-08 | 1 | ✓ | ✓ |  |
| B-09 | 1 | ✓ | ✓ |  |
| B-10 | 1 | ✓ | ✓ |  |

## Variant C

**Pre-screen detection:** 0/10 | **Mean token estimate:** 1026

| Run | Pre-score | Pause | Fix | Flag |
|-----|-----------|-------|-----|------|
| C-01 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-02 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-03 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-04 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-05 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-06 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-07 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-08 | 0 | ✗ | ✓ | REVIEW: fix named, pause scenario missing |
| C-09 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |
| C-10 | 0 | ✗ | ✗ | shallow: TTL/heartbeat concern only |

## Summary

| Variant | Pre-screen detected | Mean tokens (est) |
|---------|--------------------|-----------------|
| A | 10/10 | 1199 |
| B | 10/10 | 1193 |
| C | 0/10 | 1026 |

---

**Note:** Pre-screen scores require manual verification for REVIEW-flagged items.
Keyword match on 'lock expired' without process-pause context = 0 per SCORING.md.
