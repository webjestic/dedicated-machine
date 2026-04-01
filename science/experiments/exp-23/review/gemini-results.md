# Exp-23 Gemini Results Review

**Model:** gemini-cli default
**Date:** 2026-03-30

## Calibration Verdict: SUCCESS

C=0/10 confirms Bug 2 remains outside the consideration set of a generic senior
engineer Persona. A and B both at 10/10 demonstrate that providing the *physics* of
the mechanism (suspension, expiry, resumption) is a high-potency trigger equivalent
to the directive labels used in exp-20.

## Primary Interpretation: The "Slot-Type Reversal"

The most significant finding is the **token depth reversal** (A > B in exp-23,
vs B > A in exp-20/21b):

- **Exp-20 (Labels: "zombie-write", "fencing tokens"):** B (Instructions) > A (Persona).
  Labels act as checklist items that the instruction-following agent expands upon.
- **Exp-23 (Mechanism descriptions):** A (Persona) > B (Instructions). Mechanism
  descriptions act as "mental models" that the Persona identity integrates into its
  simulation engine.

This supports: **P_p is a simulation engine; P_d is a checklist handler.** When the
prompt provides the *physics* of a failure (mechanism) rather than just its *name*
(label), Persona uses it to generate a more exhaustive set of edge cases (A-01 extends
"GC pause" to VM live migration, container CPU throttling, SIGSTOP) whereas Instructions
stays closer to the examples provided.

## Confounds and Fatal Objections

**Ceiling Compression:**
Both A and B at 10/10 — cannot conclude A is more *reliable* than B, only more
verbose. The task is "solved" by both; differential appears only in elaboration.

**Efficiency counter-argument:**
B may be more *efficient*, reaching 10/10 detection with fewer tokens. However, the
qualitative difference (A's generalization to non-obvious suspension vectors) suggests
A is running a higher-fidelity simulation rather than being merely verbose.

## What This Leaves Open

- **The "missing middle" specificity:** Between orientation (0/10) and mechanism (10/10)
  there is a vocabulary level where a detection differential between A and B might be
  observable. This is the critical experiment for H1/H2.
- **Instructional fatigue limit:** At what complexity level does mechanism vocabulary in
  Instructions fail to remain salient while Persona still integrates it?
- **API token paradox stability:** Does the B > A (labels) vs A > B (descriptions) reversal
  hold across different model families, or is this Sonnet-specific?
