# Exp-24 Gemini Synthesis Challenge

**Model:** gemini-cli default
**Date:** 2026-03-30

## Fatal Objection: The Artifact Pointer Confound

**Objection:** The mechanism vocabulary ("TTL," "heartbeat," "GC pauses") functions
as a high-precision search index that anchors the model's attention to the exact
lines of code containing the bug. The model is not evaluating the assertion against
the code; it is being directed to the bug by the vocabulary functioning as
coordinates.

**Why it matters:** If detection is driven by spatial proximity of vocabulary to
the error rather than logical evaluation of the assertion, then the
outcome/mechanism distinction is a misinterpretation of attention steering. The
"search terminator" effect in exp-21a isn't about pragmatic force — it's about
the absence of a pointer. The model didn't overcome the assertion; the pointer
was stronger than the vague claim.

**What resolves it:** Exp-25: Mechanism Decoy. Provide a false mechanism-level
assertion pointing to a technically relevant but non-buggy part of the causal
chain (e.g., "The atomic sequence incrementer prevents stale writes during
concurrent updates") while the actual bug remains in the TTL/heartbeat logic.

- If detection stays high → model is truly evaluating the system state; the
  synthesis holds.
- If detection drops to ~0/10 → "search terminator" effect is still absolute;
  mechanism vocabulary only worked because it accidentally functioned as a
  directive by naming the buggy components.
