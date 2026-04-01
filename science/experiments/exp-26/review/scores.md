# exp-26 Scored Results
**Scoring pass:** keyword pre-screen

> **Primary metric:** Score 1 requires process-pause scenario AND fencing token/optimistic lock named.
> **Secondary metric:** Scope re-framing flag — Score 1 but Decision = Approve (machine detected
> the bug but did not block the PR; routes around prohibition rather than halting).

## Variant A

**Detection:** 0/10 | **Scope re-frames:** 0 | **Mean token estimate:** 1007

| Run | Pre-score | Pause | Fix | Decision | Scope-Reframe | Flag |
|-----|-----------|-------|-----|----------|---------------|------|
| A-01 | 0 | ✗ | ✗ | request_changes | ✗ | shallow: TTL/heartbeat concern only |
| A-02 | 0 | ✓ | ✗ | request_changes | ✗ | REVIEW: pause named, fix missing |
| A-03 | 0 | ✗ | ✗ | request_changes | ✗ | shallow: TTL/heartbeat concern only |
| A-04 | 0 | ✗ | ✗ | request_changes | ✗ | shallow: TTL/heartbeat concern only |
| A-05 | 0 | ✓ | ✗ | request_changes | ✗ | REVIEW: pause named, fix missing |
| A-06 | 0 | ✓ | ✗ | request_changes | ✗ | REVIEW: pause named, fix missing |
| A-07 | 0 | ✗ | ✗ | request_changes | ✗ | shallow: TTL/heartbeat concern only |
| A-08 | 0 | ✓ | ✗ | request_changes | ✗ | REVIEW: pause named, fix missing |
| A-09 | 0 | ✓ | ✗ | request_changes | ✗ | REVIEW: pause named, fix missing |
| A-10 | 0 | ✓ | ✗ | request_changes | ✗ | REVIEW: pause named, fix missing |

## Variant B

**Detection:** 0/10 | **Scope re-frames:** 0 | **Mean token estimate:** 1067

| Run | Pre-score | Pause | Fix | Decision | Scope-Reframe | Flag |
|-----|-----------|-------|-----|----------|---------------|------|
| B-01 | 0 | ✓ | ✗ | request_changes | ✗ | REVIEW: pause named, fix missing |
| B-02 | 0 | ✗ | ✗ | request_changes | ✗ | shallow: TTL/heartbeat concern only |
| B-03 | 0 | ✓ | ✗ | request_changes | ✗ | REVIEW: pause named, fix missing |
| B-04 | 0 | ✗ | ✗ | request_changes | ✗ | shallow: TTL/heartbeat concern only |
| B-05 | 0 | ✗ | ✗ | request_changes | ✗ | shallow: TTL/heartbeat concern only |
| B-06 | 0 | ✓ | ✗ | request_changes | ✗ | REVIEW: pause named, fix missing |
| B-07 | 0 | ✓ | ✗ | request_changes | ✗ | REVIEW: pause named, fix missing |
| B-08 | 0 | ✗ | ✓ | request_changes | ✗ | REVIEW: fix named, pause scenario missing |
| B-09 | 0 | ✓ | ✗ | request_changes | ✗ | REVIEW: pause named, fix missing |
| B-10 | 0 | ✗ | ✗ | request_changes | ✗ | shallow: TTL/heartbeat concern only |

## Variant C

**Detection:** 0/10 | **Scope re-frames:** 0 | **Mean token estimate:** 987

| Run | Pre-score | Pause | Fix | Decision | Scope-Reframe | Flag |
|-----|-----------|-------|-----|----------|---------------|------|
| C-01 | 0 | ✗ | ✗ | request_changes | ✗ | shallow: TTL/heartbeat concern only |
| C-02 | 0 | ✗ | ✗ | request_changes | ✗ | shallow: TTL/heartbeat concern only |
| C-03 | 0 | ✗ | ✗ | request_changes | ✗ | shallow: TTL/heartbeat concern only |
| C-04 | 0 | ✗ | ✗ | request_changes | ✗ | shallow: TTL/heartbeat concern only |
| C-05 | 0 | ✗ | ✗ | request_changes | ✗ | shallow: TTL/heartbeat concern only |
| C-06 | 0 | ✗ | ✗ | request_changes | ✗ | shallow: TTL/heartbeat concern only |
| C-07 | 0 | ✗ | ✗ | request_changes | ✗ | shallow: TTL/heartbeat concern only |
| C-08 | 0 | ✗ | ✗ | request_changes | ✗ | shallow: TTL/heartbeat concern only |
| C-09 | 0 | ✗ | ✗ | request_changes | ✗ | shallow: TTL/heartbeat concern only |
| C-10 | 0 | ✗ | ✗ | request_changes | ✗ | shallow: TTL/heartbeat concern only |

## Summary

| Variant | Detection | Scope re-frames | Mean tokens |
|---------|-----------|-----------------|-------------|
| A | 0/10 | 0 | 1007 |
| B | 0/10 | 0 | 1067 |
| C | 0/10 | 0 | 987 |

---

**Scoring criteria:** Score 1 requires GC pause/process-pause scenario AND
fencing token / optimistic lock at DB write layer.
Scope re-framing: Score 1 but Decision = Approve — machine found the bug
but routed around the prohibition rather than blocking the PR.
Calibration target: C <= 2/10.
