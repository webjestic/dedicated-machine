# exp-32 — PARC Self-Review on parc_d7.md

**Replicates:** exp-06 (pcsieftr_d2.md)
**Date:** 2026-04-02 | Model: claude-sonnet-4-6 | 10 runs | Variants: A (P_p), B (P_d)
**Full record:** `experiments/exp-32/findings/FINDINGS.md`

## Summary

Replication of exp-06 (PARC self-review) on parc_d7.md. Same two variants: A (P_p academic
reviewer, 6-step procedural audit) and B (P_d generic researcher). Central question: does
d7's explanatory framing constitute content-as-installer — does a P_d reviewer find the
same structural gaps as a P_p reviewer because the paper explains the mechanism explicitly
enough that careful reading gets you there?

**Answer: Yes, partially.** The A−B gap collapsed from 0.5 (exp-06) to 0.2 (exp-32).
P1 and P2 — the paper's most prominent claims — were found by every run of both variants
(5/5 A, 5/5 B). The content installed the consideration set on the claims the paper named.
The procedural audit's advantage survives only on criteria the paper did not name (P5:
component symmetry, 1/5 A vs 0/5 B).

## Primary Criteria Results

| Criterion | A Rate | B Rate |
|-----------|--------|--------|
| P1 — Dedicated Machine as assertion (§1.2 commitment violated) | 5/5 | 5/5 |
| P2 — Claim 2 n=1 (pipeline on first run, acknowledged in §9.9) | 5/5 | 5/5 |
| P3 — Horizon Blindness as distinct mechanism (no experiment isolates it) | 0/5 | 0/5 |
| P4 — Slot-swap resolves slot confound, not CoT confound | 5/5 | 5/5 |
| P5 — Component symmetry (Tone stub; Examples/Format/Request underdeveloped) | 1/5 | 0/5 |
| **Mean** | **3.2/5 (64%)** | **3.0/5 (60%)** |

exp-06 comparison: A=3.0/5, B=2.5/5, gap=0.5. exp-32: A=3.2/5, B=3.0/5, gap=0.2.

## Key Findings

**1. Content-as-installer confirmed — with a limit.**
d7 explains the Dedicated Machine hypothesis, names the n=1 limitation in §9.9, and
acknowledges the slot-swap/CoT tension in §9.5. Every reviewer — P_p and P_d alike —
arrived at those gaps. The paper installed the consideration set by naming its own problems.
The limit: P5 (component symmetry) was not named by d7, and only A found it (1/5 A, 0/5 B).

**2. Self-disclosure = detection rate.**
P1, P2, P4 were all 5/5 for both variants because d7 named them explicitly. P5 was
1/5 A, 0/5 B because d7 didn't name it. This is a measurable relationship: the paper
installs proportionally to how explicitly it names its own gaps.

**3. P3 was 0/10 across both variants.**
Horizon Blindness as a distinct mechanism was not identified by any run. Either d7
integrates it smoothly enough into the Dedicated Machine framing that reviewers treat
them as one claim, or it is crowded out by more prominent gaps.

**4. B found unanticipated critiques not in SCORING.md.**
- exp-29 model version discrepancy (Opus vs. Sonnet) — load-bearing confound in Claim 2
- exp-28d independence issue (10 Agent 2 runs fed from one Agent 1 run = not independent)
- Missing strong CoT baseline (the critical unrun experiment given H2)
- Dedicated Machine / Variant F inconsistency (DM predicts rules leak; F's output gate is a rule that doesn't)

**5. All 10 runs: Major Revision.** (exp-06: all Reject or Major Revision)
d7's honest self-disclosure softened verdicts without changing the structural critique.

## Revision Priorities for d7 (pre-submission)

These are structural gaps identified by exp-32 that are not currently named in §9:

1. **Dedicated Machine falsifiability** — add at least one experimental result that would
   disconfirm the framing as opposed to the CoT/content-quality alternative
2. **exp-29 model discrepancy** — pipeline on Opus 4.6 vs. single-pass baseline on
   Sonnet 4.6; the comparison is confounded by model capability, not just architecture
3. **exp-28d independence** — all 10 Agent 2 runs share one Agent 1 output; not
   independent observations; the 10-run count does not support variance estimates
4. **Variant F paradox** — DM predicts rule-based constraints leak (B=20%); Variant F
   is an output-gate rule that achieves 0%; the paper does not address this internal
   inconsistency

## What Requires New Experiments Before d8

- **exp-29 Sonnet replication** (n=10): run the zombie-write pipeline on claude-sonnet-4-6
  (matching the single-pass baseline model). If Tier 1.0 survives, Claim 2 is clean.
  If it doesn't, Claim 2 needs significant revision.
- **Strong CoT baseline**: procedurally equivalent content in Task Layer vs. P_p Persona.
  This is the critical missing experiment given H2. Without it, the paper cannot distinguish
  PARC from structured CoT.
