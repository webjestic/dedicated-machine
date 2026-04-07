# exp-33 — Zombie-Write Pipeline on Sonnet 4.6 (exp-29 Replication)

**Replicates:** exp-29 (zombie-write two-agent pipeline, claude-opus-4-6, n=1)
**Date:** 2026-04-02 | Model: claude-sonnet-4-6 | 10 full pipeline runs | Cost: $1.14
**Full record:** `experiments/exp-33/findings/FINDINGS.md`

## Summary

Replication of exp-29 on claude-sonnet-4-6 (matching the exp-09 single-pass baseline
model) at n=10. Resolves the model discrepancy confound that exp-32 identified as a
load-bearing structural gap in Claim 2.

**Result: 10/10 Tier 1.0.** Every Agent 1 output named the GC pause as the zombie-write
trigger, the fencing token at the database write boundary as the architectural fix, and
explicitly distinguished threading.Event signaling as necessary but insufficient.

**Claim 2 is clean.**

## Comparison Table

| Experiment | Model | Approach | n | Tier 1.0 rate |
|-----------|-------|----------|---|---------------|
| exp-09 Variant A | Sonnet 4.6 | Single-pass P_p | 40 | 1/10 (10%) |
| exp-29 | Opus 4.6 | Two-agent pipeline | 1 | 1/1 (100%) |
| exp-33 | Sonnet 4.6 | Two-agent pipeline | 10 | 10/10 (100%) |

## Key Findings

**1. Pipeline effect is architectural, not a model upgrade.**
Model capability is held constant (Sonnet 4.6 throughout). Architecture is the sole
variable. 10/10 Tier 1.0 on the pipeline vs. 1/10 on single-pass at the same model.

**2. exp-29 was not a high-draw first run.**
n=10 with 0 misses confirms the pipeline reliability is structural, not variance.

**3. The boundary remains the mechanism.**
Agent 2 finds 6+ infrastructure failure modes per run — including several not present
in exp-29's Opus run. The handoff's explicit out-of-scope statement activates the SRE
consideration set. Two satisfaction conditions in sequence cross a horizon no single
consideration set can reach.

## Implications for d7

The §9.9 model discrepancy revision can be updated to report exp-33 and retire the
confound disclaimer. Claim 2 can now be stated with model held constant across the
comparison.
