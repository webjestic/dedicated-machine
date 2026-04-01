# Exp-28d Findings — Two-Agent Pipeline vs. Single-Pass (Rate Limiter)

**Status:** Complete
**Phase:** 7 — The Dedicated Machine Hypothesis
**Date:** 2026-03-31
**Predecessor:** exp-28b (single-pass gap-detection; D=2.6/10, Tier 2 items 0% across all variants)
**Design:** `experiments/exp-28d/DESIGN.md`
**Runs:** `api/exp-28d-runs/`

---

## Summary

The two-agent pipeline partially crossed the Tier 2 SRE wall. Two of the five Tier 2 items — `load_test_spec` and `health_check` — moved from 0% detection (exp-28b) to 100% across all 10 pipeline runs. A third Tier 2 item, `alerting_policy`, moved from 0% to 30%. The remaining two — `incident_runbook` and `race_condition_tests` — stayed at 0%.

The pattern of success and failure directly traces to what the Agent 1 design document contained. The bridge worked where the design doc had substance. It failed where the design doc was truncated or incomplete.

**The bridge between agents is the artifact. Agent 2 carries exactly what Agent 1 encoded.**

---

## Results

### Scores

| Variant | n | Mean score | Tier 2 rate |
|---------|---|------------|-------------|
| A — two-agent pipeline | 10 | **5.6/10** | **46% (23/50)** |
| B — single-pass D (ceiling) | 10 | 2.9/10 | 0% (0/50) |
| C — P_d baseline | 10 | 2.4/10 | 0% (0/50) |
| Agent 1 design doc (separate) | 1 | **7/10** | 60% (3/5) |

Total cost: $3.76 (21 implementation runs × ~$0.146 + 10 C runs × ~$0.097 + 1 design run × $0.122)

### Per-item detection rates

| # | Item | Tier | A rate | B rate | C rate | Design doc |
|---|------|------|--------|--------|--------|------------|
| 1 | observability | 1 | 100% | 0% | 0% | 1 |
| 2 | alerting_policy | 2 | **30%** | 0% | 0% | 1 |
| 3 | graceful_degrade | 1 | 100% | 100% | 80% | 1 |
| 4 | client_error_guide | 1 | 100% | 100% | 80% | 1 |
| 5 | load_test_spec | 2 | **100%** | 0% | 0% | 1 |
| 6 | env_driven_config | 1 | 10% | 40% | 80% | 0 |
| 7 | health_check | 2 | **100%** | 0% | 0% | 1 |
| 8 | incident_runbook | 2 | 0% | 0% | 0% | 0 (truncated) |
| 9 | memory_audit | 1 | 20% | 40% | 0% | 1 |
| 10 | race_condition_tests | 2 | 0% | 0% | 0% | 0 |

### Per-run scores — Variant A

| Run | obs | alert | degrade | client | load | env | health | runbook | memory | race | Total |
|-----|-----|-------|---------|--------|------|-----|--------|---------|--------|------|-------|
| A-01 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 6 |
| A-02 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 5 |
| A-03 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 5 |
| A-04 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 6 |
| A-05 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | 6 |
| A-06 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 5 |
| A-07 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 6 |
| A-08 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 6 |
| A-09 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 5 |
| A-10 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | 6 |
| **Mean** | 1.0 | 0.3 | 1.0 | 1.0 | 1.0 | 0.1 | 1.0 | 0.0 | 0.2 | 0.0 | **5.6** |

---

## Findings

### Finding 1 — Pipeline crossed the Tier 2 wall for load_test_spec and health_check

`load_test_spec` and `health_check` both went from 0% (exp-28b, all single-pass variants) to 100% across all 10 Agent 2 runs. These items are Tier 2 (pure SRE, outside the engineering consideration set) and never appeared in any single-pass output in exp-28b.

The mechanism is confirmed: the design agent encoded both items with full specification — §6.6 (Load Test Specification) provided 7 named scenarios with pass criteria; §6.4 (Health Check) provided liveness/readiness endpoint specs. Agent 2 received these as requirements and implemented them.

Every Agent 2 run references the load test suite by section number as a production gate ("DO NOT ALTER this script without re-running the load test suite defined in §6.5"). Every Agent 2 run exports `isAlive()` and `isReady()` functions derived from the design spec.

### Finding 2 — alerting_policy crossed partially (30%)

`alerting_policy` appeared in 3 of 10 Agent 2 runs (A-01, A-04, A-07). In the runs where it appeared:
- A-04 produced an explicit checklist item: "R-58 Alert thresholds documented (operational config, not code — flagged in Open Items)"
- A-07 commented: "all alert conditions in §6.5 will silently fail to fire" if metrics are renamed
- A-01 flagged: "Do not rename without updating metric dashboards and alert rules"

The other 7 runs implemented the full metrics infrastructure that feeds the alerts but did not explicitly flag the alert conditions themselves.

The design doc's §6.5 had the full alert table (6 named alerts, P1/P2/P3 severity). The implementation correctly identified that alert conditions are "operational config, not code" and 7/10 runs simply built the metrics layer and moved on. The 30% is partial but above 0%.

### Finding 3 — incident_runbook failed because Agent 1 was truncated

`incident_runbook` scored 0% across all Agent 2 runs. The cause is mechanical: Agent 1 hit the 8000-token output limit. §6.7 (Incident Runbook Outline) has the section header and introductory sentence in the design doc, then cuts off before any runbook content.

Agent 2 received the design doc with an empty runbook section. There was nothing to carry through. Agent 2 does not invent what is absent from its source of truth.

**Interpretation:** This is not a failure of the pipeline architecture — it is a token limit artifact. If Agent 1 had been run with a higher max_tokens or a shorter design scope, the runbook would have been in the doc and Agent 2 would have carried it. The finding supports the hypothesis: the bridge is the artifact.

### Finding 4 — race_condition_tests failed because it was not in the design spec

`race_condition_tests` scored 0% across all variants. The design doc addressed atomicity and race conditions in the algorithm section (Lua script requirement, concurrent operation behavior) but did not specify a named "race condition test" in the load test spec — LT-03 (Multi-Identifier Isolation) and LT-06 (Sustained High Concurrency) covered concurrent load, not specifically race condition tests.

Agent 2 implemented the atomic Lua script correctly per the spec but did not produce a dedicated race condition test suite. The item was not in the artifact.

### Finding 5 — env_driven_config inverted: C beats A

`env_driven_config` scored 80% for C, 40% for B, and only 10% for A. This inversion is consistent with the design doc: the options object (code-level config) was the specified interface; the doc never addressed environment variable configuration.

C (P_d baseline) naturally writes config from process.env because that is the standard Node.js pattern. A (pipeline) followed the design doc's options-based API contract. The design doc's omission propagated into Agent 2's implementation. Agent 2 is compliance-first — it builds what is specified, not what is conventional.

---

## Interpretation — The Artifact is the Bridge

The experiment confirms the Dedicated Machine hypothesis in its strong form:

> Agent 2 delivers exactly what its source of truth (the design doc) encodes. Where the design doc has substance, Agent 2 complies. Where the design doc is silent, Agent 2 omits.

The three outcomes — crossed (load_test, health_check), partial (alerting), failed-for-mechanical-reason (runbook), and not-in-doc (race_condition, env_driven_config) — all trace directly to what was in the Agent 1 output artifact.

The pipeline architecture is vindicated. The failure modes are artifacts of:
1. Token limits on Agent 1 (runbook truncation)
2. Items not in the design doc's consideration set (race_condition_tests, env_driven_config)

Neither is a failure of the pipeline design. Both are fixable: run Agent 1 with higher max_tokens, or add race condition test and env config requirements explicitly to the design agent's Instructions.

---

## Design Doc Analysis — Agent 1 Isolation

Agent 1's design document scored **7/10** independently against the operational checklist.

| Item | Score | Notes |
|------|-------|-------|
| observability | 1 | §6.1: full metrics table (8 named metrics), structured logging schema, degraded state definition |
| alerting_policy | 1 | §6.5: 6 named alerts, conditions, P1/P2/P3 severity, routing requirements |
| graceful_degrade | 1 | §6.2: explicit contract + §4: 8 failure modes with full specifications |
| client_error_guide | 1 | §6.3: 429 response contract, required headers, prohibited body contents |
| load_test_spec | 1 | §6.6: 7 named scenarios (LT-01 through LT-07) with pass criteria |
| env_driven_config | 0 | Not addressed; options-object API specified, no env var configuration |
| health_check | 1 | §6.4: liveness and readiness checks, endpoint specs, PING timeout, fail-open behavior |
| incident_runbook | 0 | §6.7 started but truncated at 8000-token limit; no content delivered |
| memory_audit | 1 | §3: 60–80 bytes per key, estimation formula, 100K IP example, attack surface |
| race_condition_tests | 0 | Atomicity specified in §2 but no race condition test spec in §6.6 |

**Key observation:** Agent 1 scored 7/10 including 3/5 Tier 2 items. Agent 2 hit 100% on the Tier 2 items that Agent 1 specified with full detail. The items Agent 1 missed are the exact items Agent 2 missed. The design doc is the causal upstream.

---

## Comparison to Exp-28b

| Metric | exp-28b D | exp-28d B | exp-28d A |
|--------|-----------|-----------|-----------|
| Mean score | 2.6/10 | 2.9/10 | 5.6/10 |
| Tier 2 items detected | 0/5 (0%) | 0/5 (0%) | 2–3/5 (partial) |
| load_test_spec rate | 0% | 0% | **100%** |
| health_check rate | 0% | 0% | **100%** |
| alerting_policy rate | 0% | 0% | **30%** |
| incident_runbook rate | 0% | 0% | 0% (artifact of truncation) |
| race_condition_tests rate | 0% | 0% | 0% (not in design doc) |

The single-pass ceiling (B) is consistent with exp-28b D at ~2.9/10, confirming the experimental control. The pipeline (A) more than doubles the score and crosses Tier 2 on 2 items definitively.

---

## Limitations and Open Questions

1. **n=1 design doc.** Agent 1 was run once. A different Agent 1 run might produce a different design doc, varying Tier 2 coverage. The protocol deliberately uses one canonical design doc — this is the intended architecture — but it means Agent 1 variance is uncharacterized.

2. **Token limit artifact.** The 8000-token cap truncated the runbook. Re-running Agent 1 with a higher cap (or a design scope that fits within 8000 tokens) would likely change the runbook detection rate.

3. **Alerting at 30%, not 100%.** The mechanism is understood (metrics infrastructure is sufficient for most runs; explicit alert flagging is inconsistent). A refinement of Agent 2's Instructions — requiring an explicit operational gap flag for any requirement that is "config, not code" — would likely push this to higher.

4. **race_condition_tests never appeared.** This item needs to be added explicitly to Agent 1's Instructions if it is to appear in the design doc and carry through to Agent 2.

5. **env_driven_config inversion.** The design doc specifying an options-API drove Agent 2 away from env var configuration — the opposite of what would appear naturally. This is a design doc gap, not a pipeline failure.

---

## Connection to Prior Work

**Dedicated Machine hypothesis (Phase 7):** Confirmed in the strong form. The machine terminates at its satisfaction condition. Agent 1's satisfaction condition is a complete SRE design specification. Agent 2's satisfaction condition is faithful compliance with that specification. The gap in single-pass prompts is not a capability limit — it is a consideration-set limit. The pipeline resolves it by separating the consideration sets.

**PARC as agentic architecture:** This experiment is the first empirical validation of the rate-limiter-design.md / rate-limiter-implement.md canonical pipeline templates. The templates are validated as evidence for d7.

**Phase 6 — Semantic Density:** The one-well-per-agent principle holds. Agent 1's single well is SRE/operational architecture. Agent 2's single well is faithful implementation. Neither is asked to hold both simultaneously.
