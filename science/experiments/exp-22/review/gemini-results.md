# Exp-22 Gemini Results Review

**Model:** gemini-cli default
**Date:** 2026-03-30

## Calibration Verdict: CALIBRATED

C=0/10 vs A/B=10/10 is absolute. Manual confirmation that models are not merely
echoing but synthesizing original code fixes validates that the artifact is activating
latent reasoning capability rather than inducing "stochastic parrot" effects.

## Primary Interpretation: Pragmatic Activation via Interrogative Pressure

Pragmatic force is the primary gatekeeper for the Bug 2 consideration set:
- **Assertion (exp-21a) fails** because the model treats the description as ground-truth
  premise to accept ("this happened") rather than a problem to solve.
- **Interrogation (exp-22) succeeds** because it frames the causal chain as an open
  question, forcing the model to resolve the contradiction between the claim and the
  code's safety.
- **Persona independence:** A=B suggests that once the interrogative artifact installs
  the specific failure mode in context, the P_p/P_d architectural difference becomes
  irrelevant. The artifact acts as a "manual override" for the search algorithm.

## Confounds and Fatal Objections

**The "Hint" Confound:**
The interrogative artifact is essentially a high-fidelity hint. While it proves the
model *can* reason about the mechanism, it does not prove the model *will* reason
about it in a "wild" PR review. We are measuring "reasoning capacity under extreme
guidance" rather than "autonomous detection."

**The "Contradiction Trigger" objection:**
Does the interrogative framing work because it's a question, or because it introduces
a logical tension? The model must check if the code prevents the described scenario.
If it doesn't, the model finds the bug. This has not isolated "interrogation" from
"specific keyword injection." Would a vague question ("Is this safe?") work? Prior
baselines suggest not.

## What This Leaves Open

- **Minimum viable interrogative:** Does it require naming "GC pause," or is "Could a
  thread suspension invalidate our lock?" sufficient?
- **"Why" of assertional failure:** Why does P_d ignore an assertion of the bug but
  solve an interrogation? Suggests "Truth-Bias" — information in artifact is treated
  as "solved state" rather than "to-be-verified state."
- **Generalization:** Does the interrogative artifact technique transfer to non-concurrency
  bugs, or is Bug 2 uniquely sensitive?
