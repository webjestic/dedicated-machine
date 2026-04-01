# Exp-24 Gemini Results Review

**Model:** gemini-cli default
**Date:** 2026-03-30

## Calibration Verdict: INTERPRETABLE

C=0/10 confirms Bug 2 remains outside the consideration set of a generic Persona
on the clean baseline artifact. Any detection in A/B is strictly driven by the
experimental intervention (assertional mechanism vocabulary in PR summary), not
baseline model capability drift.

## Primary Interpretation: Training Data Priors ("The Spoiler Effect")

Gemini's most parsimonious alternative to the researcher's outcome/mechanism
distinction: the vocabulary combination ("heartbeat + TTL + GC pause" in the same
paragraph) is a textual pattern associated with a known failure mode in the
distributed systems literature (Kleppmann, Jepsen). The contradiction between the
terms and the safety claim is loud enough in training data to trigger a safety
violation response that overrides the "accept assertion" heuristic.

The model is not necessarily evaluating a falsifiable claim — it may be
**pattern-matching to a known "wrong solution"** and reporting the associated failure
mode regardless of how the claim is framed.

## Pragmatic Force Status: Narrowing, Not Fatal Objection

Pragmatic force operates most effectively in the absence of contradictory evidence.
It acts as a "stop-word" for search. When the assertion contains the evidence to
refute it (the mechanism), the model's logical verification can pierce the pragmatic
frame. The model believes a "lazy" claim ("this is safe") but is "logical" when
given premises that contradict its internal world-model.

> "Logic > Pragmatics only when the logic is explicitly provided in the prompt."

## Vocabulary Density Confound (Open Question)

Is the operative distinction outcome-assertion vs. mechanism-assertion, or simply
vocabulary proximity to the solution? If the model recognizes "GC pause" as a
high-potency pattern from training data, the detection may not require evaluation of
the assertion at all — the pattern fires regardless.

## Proposed Resolution: Exp-25

**Black-Box Interrogative vs. White-Box Assertion Cross:**
- Variant X: Vague vocabulary ("zombie-write failure modes?") in interrogative frame
  → if 0/10, the term is too weak regardless of force; exp-21a was a vocabulary failure
- Variant Y: Mechanism vocabulary + technical outcome assertion with no explicit
  mechanism ("verified to prevent stale writes caused by stop-the-world GC pauses
  exceeding the lock TTL") → if 0/10, outcome assertion kills even named-problem detection
