# exp-34 — Mechanism Decoy (§9.8 Artifact Pointer Confound)

**Date:** 2026-04-02 | Model: claude-sonnet-4-6 | 30 runs (A=10, B=10, C=10) | Cost: $1.27
**Full record:** `experiments/exp-34/findings/FINDINGS.md`

## Summary

exp-34 tests the §9.8 Artifact Pointer Confound: does mechanism vocabulary in P_p install
a reasoning procedure, or does it function as GPS coordinates pointing to the answer location?

Three variants on the zombie-write artifact (exp-09/ARTIFACT.md):
- **A:** P_p, no vocabulary, no direction (control)
- **B:** P_p + true pointer (correct vocabulary: GC pause, heartbeat exit, fencing token)
- **C:** P_p + decoy (false Lua atomicity claim — specifically wrong, points away from real bug)

**Result: A = B = C = 10/10 Tier 1.0.**

## Comparison Table

| Experiment | Variant | Prompt | n | Tier 1.0 |
|---|---|---|---|---|
| exp-09 | A | baseline (no P_p) | 40 | 1/10 |
| exp-34 | A | P_p, no direction | 10 | **10/10** |
| exp-34 | B | P_p + true pointer | 10 | **10/10** |
| exp-34 | C | P_p + decoy (false Lua claim) | 10 | **10/10** |

## Key Findings

**1. A = B = C = 10/10. Vocabulary is inert.**
Correct vocabulary, false vocabulary, and no vocabulary produce identical outcomes. The
content of the mechanism vocabulary (direction, correctness) has no effect on Tier 1.0 rate.

**2. P_p is the mechanism.**
exp-34 A (P_p, no vocabulary) vs. exp-09 A (no P_p): same model, same artifact, same
single-pass format. 10/10 vs. 1/10. Architecture is the sole variable. Vocabulary adds
nothing on top of P_p.

**3. §9.8 Artifact Pointer Confound resolved in the null direction.**
The confound asked: is the exp-09 A→B gap (P_p vs. vocabulary) caused by vocabulary
pointing at the bug? No. P_p without vocabulary hits the same ceiling. The vocabulary
observed in prior P_p prompts was present but inert.

**4. Decoy had no effect (Variant C).**
All 10 C runs: found the real zombie-write bug first, dismissed the Lua atomicity false
claim second. No run hallucinated or deflected toward the Lua script section. However,
the dismissal mechanism was domain-knowledge-based (Redis Lua atomicity is documented);
a code-structural-verification decoy remains an open calibration question.

**5. GPS-coordinates hypothesis rejected.**
Correct pointer (B) and false pointer (C) both produced 10/10. The model was not following
vocabulary toward a specific code location. P_p installs a verification search that finds
the bug regardless of where the prompt points.

## Implications for d7/d8

- §9.8 confound can be retired. The pointer confound is resolved in the null direction.
- §9.9 limitations: add exp-34 result; remove §9.8 as an open question.
- The vocabulary-as-activator sub-hypothesis is also ruled out (A = B without vocabulary).
- The result strengthens the core P_p mechanism claim: the termination condition installs
  the search behavior; vocabulary is not the active ingredient.
