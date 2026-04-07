# exp-33 — Zombie-Write Pipeline on Sonnet 4.6 (exp-29 Replication)

**Replicates:** exp-29 (zombie-write two-agent pipeline proof-of-concept)
**Date:** 2026-04-02
**Model:** claude-sonnet-4-6
**Runs:** 10 (full pipeline each = Agent 1 + Agent 2)
**Artifact:** exp-09/ARTIFACT.md — Python distributed job executor, Redis claim locking
**Runner:** `experiments/exp-33/runner.py` (custom pipeline runner)

---

## Background

exp-29 established that the zombie-write two-agent pipeline solved the problem on the
first run using claude-opus-4-6. The single-pass baseline (exp-09) used claude-sonnet-4-6
and achieved 1/10 Tier 1.0 across 40 runs.

The comparison in d7's Claim 2 table is confounded: pipeline used Opus 4.6; single-pass
baseline used Sonnet 4.6. The pipeline effect and the model-capability effect have not
been separated. exp-32's unanticipated critiques (via B-variant reviewers) flagged this
as a load-bearing confound.

## Primary Question

Does the zombie-write two-agent pipeline reach Tier 1.0 consistently when run on
claude-sonnet-4-6 — the same model as the single-pass baseline?

**If yes:** Claim 2 is clean. The pipeline architecture is doing the work, not the model
upgrade. d7 can be revised to remove the confound disclaimer.

**If no (inconsistent Tier 1.0 on Sonnet):** Claim 2 needs significant revision. The
pipeline effect and model-capability effect cannot be cleanly separated, and the paper
must acknowledge that exp-29's result may be partly a model-capability finding.

## Secondary Questions

1. What is Agent 1's Tier 1.0 consistency across 10 independent runs on Sonnet?
2. When Agent 1 misses Tier 1.0, does Agent 2 independently find the zombie-write fix?
3. How many infrastructure failure modes does Agent 2 surface per run on average?

## Design

**Pipeline (same as exp-29):**
- Agent 1: `parc/examples/zombie-layer1-review.md` — Senior SWE, correctness scope
- Agent 2: `parc/examples/zombie-layer2-review.md` — Senior SRE, production readiness scope
- Handoff: Agent 1's handoff summary injected as `{{LAYER_1_SUMMARY}}` in Agent 2's prompt
- Artifact: exp-09/ARTIFACT.md (same code as exp-29)

**Model change:** claude-opus-4-6 (exp-29) → claude-sonnet-4-6 (exp-33)

**n=10 independent runs** (each run = one Agent 1 call + one Agent 2 call from fresh context)

**Temperature:** 0.5 (same as all PARC experiments)

## Predictions

**Primary prediction:** Agent 1 reaches Tier 1.0 on ≥7/10 runs. Rationale: Sonnet
is capable enough for correctness code review; the P_p Persona installs the consideration
set. If the pipeline effect is architectural, model capability is a secondary variable.

**Null prediction (would support Claim 2 revision):** Agent 1 reaches Tier 1.0 on
≤3/10 runs. This would suggest exp-29's result was partly a model-capability effect
and the pipeline comparison to exp-09's 1/10 single-pass needs reframing.

## Tier 1.0 Criterion

Identical to exp-09 and exp-29:
- Identifies GC pause (or equivalent process-pause) as the zombie-write trigger
- Names fencing token / monotonic counter / optimistic concurrency at DB write boundary as
  the architectural fix
- Distinguishes threading.Event signaling as necessary but insufficient

threading.Event alone = Tier 0.5 (correct diagnosis, incomplete fix).
