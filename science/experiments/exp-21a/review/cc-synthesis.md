# Exp-21a CC Synthesis

## Results

| Variant | Final Score | Mean tokens |
|---------|-------------|-------------|
| A (P_p, generic persona) | 0/10 | 1012 |
| B (P_d, generic persona) | 0/10 | 946 |
| C (P_d baseline) | 0/10 | 908 |

Calibration passed (C=0/10).

Two A-variant outputs (A-01, A-07) pre-screened as 1 due to "GC pause" + "fencing token" keyword co-occurrence. Manual review confirmed both as false positives: GC pause appeared only as a timing-precision aside ("heartbeat sleep may be delayed by GC pause"), and fencing token appeared as what the code fails to prevent (TOCTOU race framing), not as the recommended DB-layer fix. No output described the zombie-write causal chain or recommended fencing token at the DB write layer. All 30 outputs: Score 0.

## Primary Finding

**Vocabulary in the artifact drives zero detection, even when that vocabulary explicitly names zombie-write failure modes and fencing token violations.**

This is in direct contrast to exp-20, where the same vocabulary in the Instructions slot drove 9/10 detection. The vocabulary is present in both cases; the operative difference is semantic framing:

- **System prompt slot (exp-20):** vocabulary acts as a search directive — "look for these failure modes"
- **Artifact PR description (exp-21a):** vocabulary acts as an assertion of success — "the design claims to address these failure modes"

The model processes authorial claims in the artifact as premises to evaluate (and often accept), not as triggers to search. This terminates the investigation before reaching the gap.

## Gemini Concurs: Design Confound

Gemini identifies the same issue: exp-21a changed two variables simultaneously — slot (Instructions → Artifact) AND pragmatic force (directive → assertion). The variables are not isolated, so exp-21a cannot cleanly test H2 (slot vs. content).

Gemini's formulation: "The operational variable is how the text positions the model relative to the target concept." This is a useful refinement: the effect we're observing in exp-20 may not be about the system prompt slot per se, but about the text being framed as a directive search vector.

## Revised Theory: Pragmatic Force

A cleaner characterization of what we're observing:

**The consideration set is expanded when vocabulary is deployed as a directive search vector (explicit or implicit). The consideration set is not expanded when vocabulary appears as an assertion to verify.**

This is consistent with:
- exp-19: no vocabulary, P_p persona provides implicit search orientation → 10/10 detection
- exp-20: vocabulary in system prompt as explicit orientation → 9/10 detection
- exp-21a: vocabulary in artifact as assertion of what the design prevents → 0/10 detection
- exp-21b (pending): orientation vocabulary in system prompt without naming failure mode

## What exp-21a Does NOT Test

Gemini is correct that exp-21a does not test H2 cleanly. H2 = content is operative regardless of slot. But exp-21a confounds slot with pragmatic force. To test H2 properly, we need vocabulary placed in the artifact with the same directive/interrogative pragmatic force it has in the system prompt.

## Next Experiment Design

Following Gemini's proposed direction: inject vocabulary into the artifact with interrogative/directive framing — as an open question or TODO, not an assertion.

**Proposed exp-22:**
- Same artifact, modified PR description to include: "**Open question for reviewer:** This design does not implement a fencing token at the database write layer. In a scenario where GC pause causes all threads (including the heartbeat) to freeze and the lock expires, would this implementation produce zombie writes?"
- Variant A (P_p generic): no system prompt vocabulary
- Variant B (P_d generic): no system prompt vocabulary
- Variant C (P_d baseline): original artifact (no interrogative)

If A=B >> C: H2 confirmed — content governs regardless of slot, provided it has directive force. Pragmatic force is the operative variable, not slot.
If A=B=C=0: the artifact slot structurally degrades reasoning regardless of pragmatic force framing.

## H1/H2 Status

Neither H1 nor H2 can be adjudicated from exp-21a. The experiment was informative but not in the way intended — it revealed the pragmatic force confound rather than slot effects. This actually advances the research by narrowing what the follow-up experiment needs to test.
