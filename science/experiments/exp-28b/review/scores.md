# exp-28b Scored Results
**Scoring pass:** keyword pre-screen — operational horizon checklist

> **Score** = number of operational production requirements surfaced (0–10).
> Items: observability, alerting_policy, graceful_degrade, client_error_guide,
> load_test_spec, env_driven_config, health_check, incident_runbook,
> memory_audit, race_condition_tests.
> Calibration target: C (P_d baseline) mean <= 2/10.

## Variant A

**Mean score:** 0.5/10 | **Range:** 0–1 | **Mean tokens:** 1552

| Run | Score | observability | alerting_policy | graceful_degrade | client_error_guide | load_test_spec | env_driven_config | health_check | incident_runbook | memory_audit | race_condition_tests |
|-----|-------|---|---|---|---|---|---|---|---|---|---|
| A-01 | 1/10 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ |
| A-02 | 0/10 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| A-03 | 1/10 | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| A-04 | 1/10 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ |
| A-05 | 0/10 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| A-06 | 0/10 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| A-07 | 1/10 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ |
| A-08 | 1/10 | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| A-09 | 0/10 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| A-10 | 0/10 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

**Item detection rates:**

| Item | Detected | Rate |
|------|----------|------|
| observability | 0/10 | 0% |
| alerting_policy | 0/10 | 0% |
| graceful_degrade | 2/10 | 20% |
| client_error_guide | 0/10 | 0% |
| load_test_spec | 0/10 | 0% |
| env_driven_config | 0/10 | 0% |
| health_check | 0/10 | 0% |
| incident_runbook | 0/10 | 0% |
| memory_audit | 3/10 | 30% |
| race_condition_tests | 0/10 | 0% |

## Variant B

**Mean score:** 1.7/10 | **Range:** 1–3 | **Mean tokens:** 1586

| Run | Score | observability | alerting_policy | graceful_degrade | client_error_guide | load_test_spec | env_driven_config | health_check | incident_runbook | memory_audit | race_condition_tests |
|-----|-------|---|---|---|---|---|---|---|---|---|---|
| B-01 | 3/10 | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ |
| B-02 | 1/10 | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| B-03 | 1/10 | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| B-04 | 2/10 | ✗ | ✗ | ✓ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| B-05 | 1/10 | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| B-06 | 1/10 | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| B-07 | 1/10 | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| B-08 | 2/10 | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ |
| B-09 | 3/10 | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| B-10 | 2/10 | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

**Item detection rates:**

| Item | Detected | Rate |
|------|----------|------|
| observability | 1/10 | 10% |
| alerting_policy | 0/10 | 0% |
| graceful_degrade | 10/10 | 100% |
| client_error_guide | 3/10 | 30% |
| load_test_spec | 0/10 | 0% |
| env_driven_config | 1/10 | 10% |
| health_check | 0/10 | 0% |
| incident_runbook | 0/10 | 0% |
| memory_audit | 2/10 | 20% |
| race_condition_tests | 0/10 | 0% |

## Variant C

**Mean score:** 0.9/10 | **Range:** 0–2 | **Mean tokens:** 1436

| Run | Score | observability | alerting_policy | graceful_degrade | client_error_guide | load_test_spec | env_driven_config | health_check | incident_runbook | memory_audit | race_condition_tests |
|-----|-------|---|---|---|---|---|---|---|---|---|---|
| C-01 | 0/10 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| C-02 | 2/10 | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| C-03 | 0/10 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| C-04 | 1/10 | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| C-05 | 0/10 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| C-06 | 0/10 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| C-07 | 1/10 | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| C-08 | 2/10 | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| C-09 | 1/10 | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| C-10 | 2/10 | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

**Item detection rates:**

| Item | Detected | Rate |
|------|----------|------|
| observability | 0/10 | 0% |
| alerting_policy | 0/10 | 0% |
| graceful_degrade | 4/10 | 40% |
| client_error_guide | 5/10 | 50% |
| load_test_spec | 0/10 | 0% |
| env_driven_config | 0/10 | 0% |
| health_check | 0/10 | 0% |
| incident_runbook | 0/10 | 0% |
| memory_audit | 0/10 | 0% |
| race_condition_tests | 0/10 | 0% |

## Variant D

**Mean score:** 2.6/10 | **Range:** 2–3 | **Mean tokens:** 1675

| Run | Score | observability | alerting_policy | graceful_degrade | client_error_guide | load_test_spec | env_driven_config | health_check | incident_runbook | memory_audit | race_condition_tests |
|-----|-------|---|---|---|---|---|---|---|---|---|---|
| D-01 | 3/10 | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ |
| D-02 | 3/10 | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| D-03 | 3/10 | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| D-04 | 3/10 | ✗ | ✗ | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| D-05 | 2/10 | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| D-06 | 2/10 | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| D-07 | 3/10 | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| D-08 | 3/10 | ✗ | ✗ | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| D-09 | 2/10 | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| D-10 | 2/10 | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

**Item detection rates:**

| Item | Detected | Rate |
|------|----------|------|
| observability | 4/10 | 40% |
| alerting_policy | 0/10 | 0% |
| graceful_degrade | 10/10 | 100% |
| client_error_guide | 9/10 | 90% |
| load_test_spec | 0/10 | 0% |
| env_driven_config | 2/10 | 20% |
| health_check | 0/10 | 0% |
| incident_runbook | 0/10 | 0% |
| memory_audit | 1/10 | 10% |
| race_condition_tests | 0/10 | 0% |

## Summary

| Variant | Mean score | Range | Mean tokens |
|---------|------------|-------|-------------|
| A | 0.5/10 | 0–1 | 1552 |
| B | 1.7/10 | 1–3 | 1586 |
| C | 0.9/10 | 0–2 | 1436 |
| D | 2.6/10 | 2–3 | 1675 |
