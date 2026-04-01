# Exp-28d Design — Two-Agent Pipeline vs. Single-Pass (Rate Limiter)

**Status:** Complete — see `research/findings/exp-28d.md`
**Phase:** 7 — The Dedicated Machine Hypothesis
**Date:** 2026-03-31
**Predecessor:** exp-28b (single-pass gap-detection; D=2.6/10, Tier 2 items 0% across all variants)
**Prompt templates:** `parc/examples/rate-limiter-design.md`, `parc/examples/rate-limiter-implement.md`

---

## Hypothesis

A two-agent pipeline (dedicated design agent → dedicated implementation agent) crosses the Tier 2 SRE wall that single-pass prompts cannot reach.

**Mechanism:** The design agent's SRE/operational consideration set encodes into the design document. The implementation agent receives that document as its source of truth via Context. The first agent's P_p installs what the second agent's Context carries. The bridge between agents is the artifact.

**Why single-pass fails:** A single-pass prompt asks one machine to hold two incompatible consideration sets simultaneously — engineering (code-complete) and operations (SRE-ready). The machine picks one and terminates there. exp-28b D, the best single-pass variant, reached 2.6/10 and 0% on all five Tier 2 items.

**Why the pipeline should succeed:** The design agent never writes code — its satisfaction condition is a complete operational specification. Tier 2 items (alerting, runbooks, load testing, health checks, incident procedures) are native to the SRE consideration set. They appear in the design doc because the design agent's P_p puts them there. The implementation agent then receives them as requirements, not discoveries.

---

## Variants

### Variant A — Two-Agent Pipeline

**Step 1 — Agent 1 (Design):** `variants/A-pipeline-agent1-design.md`

SRE/operational architect P_p. Produces a complete operational design document. Never writes code. The seven Tier 2 operational items are explicit requirements in the Instructions. Output: `output/A-design-doc.md` (one canonical run).

**Step 2 — Agent 2 (Implement):** `variants/A-pipeline-agent2-implement.md`

Implementation engineer P_p. Receives the Agent 1 design doc as `{{DESIGN_DOC}}`. Compliance-first: cannot begin implementation without producing a requirement checklist derived from the design. Output scored against the operational checklist.

**Run protocol:** Run Agent 1 once to produce the canonical design document. Run Agent 2 n=10 against that design document. Score Agent 2 outputs on the operational checklist.

### Variant B — Best Single-Pass (exp-28b D)

`variants/B-single-pass-D.md` — exact copy of exp-28b Variant D (the user-authored operational-mindset P_p + gap-detection satisfaction condition). n=10. Provides the single-pass ceiling for comparison.

**exp-28b D result:** mean=2.6/10, range 2–3. Tier 2 items: 0% across all 10 runs.

### Variant C — P_d Baseline

`variants/C-pd-baseline.md` — exact copy of exp-28b Variant C. n=10. Calibration anchor.

**exp-28b C result:** mean=0.9/10. Can use exp-28b data directly if recalibration is not needed.

---

## Scoring

Same 10-item operational checklist from exp-28b. Applied to the final output (Agent 2 for pipeline; direct output for B and C).

| # | Item | Tier |
|---|------|------|
| 1 | observability | 1 |
| 2 | alerting_policy | 2 |
| 3 | graceful_degrade | 1 |
| 4 | client_error_guide | 1 |
| 5 | load_test_spec | 2 |
| 6 | env_driven_config | 1 |
| 7 | health_check | 2 |
| 8 | incident_runbook | 2 |
| 9 | memory_audit | 1 |
| 10 | race_condition_tests | 2 |

**Scoring rule:** Score 1 if explicitly named, implemented, or flagged as a production requirement with substance. Score 0 if absent or mentioned in passing without actionable content.

**Primary signal:** Tier 2 detection rate for A vs. B. exp-28b showed 0% on all Tier 2 items across all single-pass variants. Any Tier 2 detection in A is a finding.

---

## Predictions

| Variant | Predicted mean | Tier 2 prediction | Reasoning |
|---------|---------------|-------------------|-----------|
| C | 0.9/10 | 0% | Calibration anchor; use exp-28b data |
| B | 2.6/10 | 0% | exp-28b D ceiling; Tier 2 outside engineering consideration set |
| A | 6–9/10 | >50% on 3+ items | Design agent's SRE P_p installs Tier 2 into the design doc; implementation agent receives as requirements |

**Falsifiable outcomes:**

| Pattern | Interpretation |
|---------|----------------|
| A Tier 2 > 50% on 3+ items | Pipeline architecture crosses the SRE wall; two-agent design vindicated |
| A > B on total score but Tier 2 still 0% | Design doc carries Tier 1 lift but Agent 2 ignores or skips Tier 2 items |
| A ≈ B | Pipeline adds no lift over best single-pass; consideration-set boundary is in Agent 2, not Agent 1 |
| A design doc scores high but A implementation scores low | The gap is in Agent 2's compliance, not Agent 1's design |

---

## Additional Analysis

**Score Agent 1's design document separately** against the operational checklist before running Agent 2. This isolates whether the pipeline failure (if any) is in the design agent or the implementation agent.

If Agent 1 design doc scores 8–10/10 but Agent 2 implementation scores 3/10: the problem is Agent 2's compliance behavior, not the pipeline architecture.

If Agent 1 design doc scores 3/10: the SRE P_p did not install the operational consideration set — re-examine the Persona.

---

## Connection to Prior Work

**exp-28b D (2026-03-30):** Best single-pass. 2.6/10. 0% Tier 2. The upper bound for what a single-pass prompt can reach. exp-28d tests whether the pipeline architecture breaks through this ceiling.

**Phase 6 — Semantic Density:** Each agent gets one well. The agent boundary is where a single-pass prompt would go fat. The design agent's single well is SRE/operational architecture. The implementation agent's single well is faithful implementation from specification.

**dedicated-machine_v2.md — The pipeline implication:** The machine delivers exactly what its satisfaction condition defines. Two agents with two separate satisfaction conditions can cover ground that one agent cannot — not by making one machine smarter, but by giving each machine a different definition of done.

**parc/examples/:** `rate-limiter-design.md` and `rate-limiter-implement.md` are the canonical PARC prompt templates for this pipeline. exp-28d is the empirical validation run.
