# exp-35: Strong CoT Baseline

**Status:** Complete — 2026-04-02
**Result:** A = B = 10/10 Tier 1.0. H0 confirmed.

---

## Question

Can explicit chain-of-thought procedure in the Instructions layer replicate the Tier 1.0
rate produced by a Procedural Persona (P_p)?

## Design

- **Variant A (Strong CoT):** P_d Persona (senior software engineer, no domain vocabulary,
  no termination condition). All procedural content — zombie write vocabulary, GC pause
  trigger, fencing token distinction, explicit reasoning steps, termination condition —
  in Instructions as numbered CoT steps.
- **Variant B (P_p control):** Identical to exp-34 A. P_p with termination condition in
  Persona. Within-experiment anchor.
- **Artifact:** exp-09/ARTIFACT.md (same zombie-write code artifact used across the series)
- **n=10 per variant, claude-sonnet-4-6, temperature=0.5**

## Results

| Variant | Prompt | n | Tier 1.0 |
|---|---|---|---|
| A | P_d + Strong CoT (Instructions) | 10 | **10/10** |
| B | P_p control | 10 | **10/10** |

A = B = 10/10. Strong CoT replicates P_p exactly.

## Key Comparison

| Experiment | Variant | Persona | Procedural content | n | Tier 1.0 |
|---|---|---|---|---|---|
| exp-09 | A | P_d only | None | 40 | **1/10** |
| exp-35 | A | P_d only | Instructions (Strong CoT) | 10 | **10/10** |
| exp-35 | B | P_p | Persona + Instructions | 10 | **10/10** |
| exp-34 | A | P_p | Persona + Instructions | 10 | **10/10** |

## Central Finding

**H0 confirmed. The Persona slot is not load-bearing on this task.**

Moving all procedural content (termination condition, domain vocabulary, explicit reasoning
steps) from the Persona slot to the Instructions layer had no observable effect on Tier
1.0 rate. The content is the mechanism. The slot is irrelevant.

The exp-09 A → exp-34 A gap (1/10 → 10/10) is attributable to **procedural content**,
not to Persona slot identity anchoring. Both exp-35 A (P_d + Strong CoT) and exp-34 A
(P_p) produce 10/10. The content is what changed between exp-09 A and exp-34 A.

## Implication for d8

The paper's mechanism claim must shift from slot-level to content-level:

> **Current (d7):** P_p installs a search algorithm as operative identity — the "identity
> anchoring" mechanism. The Persona slot has a distinct function.
>
> **Revised (d8):** A termination condition and explicit reasoning procedure cause the model
> to adopt convergent search behavior, regardless of which slot they occupy. PARC provides
> a clean architectural structure for delivering this content; the architecture is not the
> mechanism.

Sections requiring revision: §4.2 (P_p/P_d distinction mechanism claim), §9.x
(identity-anchoring framing). §9.9 item 7 added to d7.

## What This Does Not Rule Out

1. **Weaker CoT variants might fail.** Strong CoT was the most favorable alternative —
   explicit steps, domain vocabulary, termination condition. A vaguer instruction would
   not replicate P_p.
2. **Task-specificity.** This artifact has a well-defined termination criterion. In tasks
   with more ambiguous termination, Persona slot anchoring may provide more lift.
3. **Structural compression advantage.** P_p encodes the same procedure more compactly
   in Persona. At token limits or for less capable models, this compression may matter.
