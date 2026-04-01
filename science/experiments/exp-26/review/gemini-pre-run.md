# Exp-26 Gemini Pre-Run Review

**Date:** 2026-03-30
**Reviewer:** Gemini (adversarial peer review)
**Verdict:** Do not run in current form — fatal objection; redesign required

---

## 1. Calibration Verdict

Partially capable of adjudicating the hypothesis, but only if the base P_p Persona is
properly calibrated to the artifact's difficulty.

- **Strong support:** B ≥ 8/10 and A ≤ 3/10. Satisfaction condition installs a search algorithm that prohibition does not.
- **Null result — floor:** A = B = 0/10. Neither framing crosses the specificity threshold on a clean artifact.
- **Null result — ceiling:** A = B = 10/10. Base P_p ("distributed systems engineer") already primed to find zombie-write without added framing.
- **Falsification:** A > B. Explicit prohibition drives higher detection than goal-oriented Persona — logically undermines the Dedicated Machine hypothesis.

---

## 2. Design Objections

**Variable Entanglement (Slot vs. Force):** The design entangles the Slot (Instructions vs.
Persona) with the Pragmatic Force (Prohibition vs. Satisfaction). PARC has already established
that the Persona slot is the primary determinant of the consideration set. If B > A, you cannot
distinguish whether the gain came from "Goal Architecture" framing or simply from placing the
operative logic in the load-bearing Persona slot rather than the Task Layer.

**The Elaboration Ceiling Constraint:** The prohibition is in the Instructions. Prior findings
(exp-03 series) establish that prohibitions act as an "elaboration ceiling," compressing output
to ~11% of unconstrained depth. This may suppress A's score not by stopping detection, but by
truncating the reasoning required to satisfy the Score 1 criteria.

---

## 3. Fatal Objection: The Specificity/Mechanism Confound

**This experiment as designed is unpublishable.** It replicates the fatal error of exp-22.

Variant B's satisfaction condition contains high-density mechanism vocabulary:
- "lock expired"
- "transferred to another process"
- "application threads were suspended"

Variant A uses vague directive labels:
- "distributed lock vulnerabilities"
- "concurrent write safety issues"

Phase 6 established a strict Specificity Threshold: orientation/directive vocabulary often fails
(0/10); mechanism vocabulary drives ceiling detection (10/10). If B > A, a peer reviewer will
correctly argue that B succeeded because you "named the ghost" — B provides the temporal
simulation blueprint; A provides a generic boundary.

**Required Redesign:** Both A and B must share the exact same vocabulary density.

Proposed parallel phrasing:
- **A (Prohibition):** "Do not approve code where an unbounded process suspension or GC pause could cause the lock to expire, leading to a stale write after threads resume."
- **B (Satisfaction):** "My review is complete only when I confirm that an unbounded process suspension or GC pause cannot cause the lock to expire and lead to a stale write after threads resume."

---

## 4. Persona Critique: Artifact Pointer Confound Relocated

Variant B's satisfaction condition is the Artifact Pointer Confound from exp-24, relocated
to the prompt. By instructing the model to ask "could another process have acquired this lock
while threads were suspended," you are providing a procedural cheat sheet — transforming the
task from Structural Inference to Pattern Recognition.

To truly test Goal Architecture, the satisfaction condition must be higher-level (e.g., "confirm
write-exclusivity is maintained across the entire lifecycle regardless of execution timing")
without handing the model the "GC pause" key.

**Note (CC assessment):** Higher-level satisfaction conditions are orientation-level vocabulary,
which Phase 6 established as below the specificity threshold (0/10). The right resolution is to
match vocabulary density across A and B (Gemini's redesign), not to abstract B's vocabulary
further. Both variants should carry the same mechanism vocabulary; only the pragmatic force should differ.

---

## 5. Scope Re-framing as Secondary Metric

"Decision = Approve after detection" is a high-fidelity signal for the Dedicated Machine
hypothesis. In exp-03b, P_p variants under prohibition re-categorized vulnerabilities as
"implementation-description mismatches" to satisfy the task without defying the prohibition.

However, distinguish from hedging: the scope re-framing signal only holds if the model names
the Bug 2 causal chain AND still chooses to Approve. Score 0.5 (bug named but fix missing)
+ Approve may just be a failure of Persona depth, not deliberate routing behavior.
This distinction is already captured in the current scorer's pre-score=1 condition.

---

## CC Decision

**Fatal objection accepted.** Vocabulary differential between A and B is too wide to permit
a Goal Architecture interpretation.

**Redesign:**
1. Place both prohibition and satisfaction condition in the Persona slot (resolves slot confound)
2. Match vocabulary to Gemini's parallel phrasing — "unbounded process suspension or GC pause...
   lock expire... stale write after threads resume" — in both A and B
3. Only the pragmatic force differs: prohibition vs. satisfaction condition

This makes exp-26 a clean Pragmatic Force test at mechanism vocabulary level, in the Persona slot:
- Same slot
- Same vocabulary density
- Same mechanism description
- Different pragmatic force only

Prediction update: given Phase 6 (mechanism vocabulary drives ceiling regardless of framing in
artifacts), the most likely outcome is A ≈ B at ceiling — "framing doesn't matter when vocabulary
is mechanism-level, even in Persona." That would be a Phase 6 extension, not a Phase 7 finding.
If A and B do diverge, the Dedicated Machine framing gains empirical support.
