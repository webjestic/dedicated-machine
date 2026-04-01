# exp-13 Findings

**Status:** Complete
**Date:** 2026-03-29
**Question:** With relevance controlled (orthogonal second and third wells), does well count predict consideration-set depth? Does A > B > C > D hold?

---

## Token Results

| Variant | Wells | Mean output | Ceiling hits | Min | Max |
|---------|-------|-------------|--------------|-----|-----|
| A | 1 (fused compound) | 2,416 | 3/10 | 2,280 | 2,500 |
| B | 2 (dist. systems + ML systems) | 2,065 | 0/10 | 1,530 | 2,497 |
| C | 3 (dist. systems + ML + frontend) | 2,017 | 0/10 | 1,717 | 2,178 |
| D | P_d baseline | 1,667 | 0/10 | 1,433 | 1,955 |

**Gaps:**
- A vs B: +351 tokens
- B vs C: +47 tokens (noise)
- C vs D: +350 tokens
- A vs D: +749 tokens

---

## Primary Finding: The First Split Is the Loss

The well-count dilution gradient predicted A > B > C > D. The observed ordering is **A >> B ≈ C >> D**.

The B vs. C gap (+47 tokens) is noise — indistinguishable from run-to-run variance. The A vs. B gap (+351) and the C vs. D gap (+350) are large and consistent.

**The loss occurs at the first split, not at each additional well.** Going from 1 fused compound well (A) to 2 unfused wells (B) costs ~350 tokens of mean output. Going from 2 to 3 orthogonal wells (C) costs essentially nothing further. This is not a monotonic dilution gradient — it is a step function: fused compound identity vs. any split configuration.

---

## exp-12 Confound Confirmed

| Variant | exp-12 mean | exp-13 mean | Delta |
|---------|-------------|-------------|-------|
| A | 2,285 | 2,416 | +131 (noise) |
| B | 2,183 | 2,065 | −118 |
| C | 2,344 | 2,017 | **−327** |
| D | 1,794 | 1,667 | −127 (noise) |

A and D are stable across experiments — same Personas, noise-level variation. B dropped modestly when the security well was replaced with the orthogonal ML systems well (security was somewhat task-relevant; ML is not). C dropped 327 tokens — confirming that exp-12 C's "performance engineering / timeout arithmetic" well was functionally pointing at the artifact's finding type, not testing well count. With the relevance confound removed, exp-13 C collapses to exp-13 B.

---

## The Mechanism: Binary Switch, Not Gradient

The data is consistent with a binary switching model rather than a linear dilution model:

**State 1 — Fused compound identity (A):** One coherent gravity well. The model has a single, unified semantic cluster to activate. Consideration-set depth is at its maximum for this Persona's domain expertise.

**State 2 — Any split configuration (B, C):** Two or more unfused identity statements. The model holds multiple lenses without a dominant one. Depth drops to the same lower level regardless of how many additional wells are added beyond the first split.

The practical implication: the distinction that matters is **fused vs. split**, not **one well vs. two wells vs. three wells**. Designing a Persona with 5 separate expertise statements is not meaningfully worse than 2 — the damage is already done at the first split.

---

## P_p >> P_d: Fourth Confirmation

All three P_p configurations substantially outperform D:

- Mean gap (weakest P_p variant C vs. D): +350 tokens
- Ceiling rate: A=3/10; B, C=0/10; D=0/10
- A vs. D gap: 749 tokens

The P_p installation effect on consideration-set breadth is robust regardless of well configuration. This is the fourth consecutive confirmation across exp-10, exp-10b, exp-12, and exp-13.

---

## Revised Well-Count Claim

The original hypothesis — "1 well > 2 wells > 3 wells > P_d" — should be replaced with:

> **"Fused compound identity > any split configuration > P_d."**

The number of wells past the first split does not predict depth. The operative variable is identity coherence — whether the Persona activates one dominant gravity well or distributes attention across multiple unfused clusters. Once split, additional wells are inert.

---

## Impact on Semantic Density Hypothesis

The well-count framing was too coarse. The correct framing is **compound fusion vs. distributed identity**:

- Compound: themes entangled in a single sentence, inseparable at the token level — one well
- Distributed: themes stated as separate "You are X / You are Y" sentences — multiple wells, but the first split is what costs you

This maps directly back to the original semantic density hypothesis: thematic coherence of tokens adjacent to identity anchors. A fused compound sentence produces one coherent cluster; separate sentences produce diluted, competing clusters. The finding is that coherence is binary at the relevant scale: either the identity is fused or it isn't.

**Next experiment (exp-14 — Fusion Test):** Hold domain constant; vary only fusion vs. explicit separation. Same two themes (distributed systems + thoroughness/compulsion) in two forms:
- A: Fused — same as exp-13 A
- B: Separated — "You are an expert in distributed systems: consensus protocols, distributed locking, and race conditions. You are tedious and thorough and rarely let questionable design architectures go unscrutinized. You can't help but try to discover the hidden mysteries that may be embedded in complex or critical code." (same content, split into two "You" statements)
- C: P_d baseline

This directly tests whether the fusion form is doing the work, or whether it is the domain content of the distributed systems expertise that matters regardless of how it is stated.
