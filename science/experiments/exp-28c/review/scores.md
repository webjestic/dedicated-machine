# exp-28c Scored Results
**Scoring pass:** keyword pre-screen — operational horizon checklist

> **Score** = operational production requirements identified in review (0–10).
> **Tier 1** (engineering-adjacent): observability, graceful_degrade,
>   client_error_guide, env_driven_config, memory_audit.
> **Tier 2** (SRE Wall): alerting_policy, load_test_spec, health_check,
>   incident_runbook, race_condition_tests.
> Calibration target: C mean <= 2/10 total, <= 1/10 Tier 2.

## Variant C

**Total:** 2.9/10 | **Tier 1:** 2.8/5 | **Tier 2:** 0.1/5 | **Range:** 2–4 | **Mean tokens:** 1290

| Run | Total | T1 | T2 | observability | alerting_policy | graceful_degrade | client_error_guide | load_test_spec | env_driven_config | health_check | incident_runbook | memory_audit | race_condition_tests |
|-----|-------|----|----|---|---|---|---|---|---|---|---|---|---|
| C-01 | 3/10 | 3/5 | 0/5 | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| C-02 | 3/10 | 3/5 | 0/5 | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| C-03 | 2/10 | 2/5 | 0/5 | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| C-04 | 3/10 | 3/5 | 0/5 | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| C-05 | 3/10 | 3/5 | 0/5 | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| C-06 | 2/10 | 2/5 | 0/5 | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| C-07 | 3/10 | 3/5 | 0/5 | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| C-08 | 4/10 | 3/5 | 1/5 | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ |
| C-09 | 3/10 | 3/5 | 0/5 | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| C-10 | 3/10 | 3/5 | 0/5 | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

**Tier 1 detection rates:**

| Item | Detected | Rate |
|------|----------|------|
| observability | 8/10 | 80% |
| graceful_degrade | 10/10 | 100% |
| client_error_guide | 10/10 | 100% |
| env_driven_config | 0/10 | 0% |
| memory_audit | 0/10 | 0% |

**Tier 2 detection rates:**

| Item | Detected | Rate |
|------|----------|------|
| alerting_policy | 0/10 | 0% |
| load_test_spec | 0/10 | 0% |
| health_check | 1/10 | 10% |
| incident_runbook | 0/10 | 0% |
| race_condition_tests | 0/10 | 0% |

## Summary

| Variant | Total | Tier 1 | Tier 2 | Range |
|---------|-------|--------|--------|-------|
| C | 2.9/10 | 2.8/5 | 0.1/5 | 2–4 |
