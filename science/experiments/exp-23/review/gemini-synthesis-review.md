# Exp-23 Gemini Synthesis Review

**Model:** gemini-cli default
**Date:** 2026-03-30

## Objection: Procedural Leakage and Pattern-Matching Confound

**Objection:**
The mechanism vocabulary in exp-23 provides a step-by-step causal blueprint of the target
failure: "stop-the-world GC pauses that suspend all threads, lock expiry during process pause,
write safety after process resumption." This may transform the task from a discovery problem
(consideration-set activation) into a pattern-matching problem (GC pause trigger → memorized
failure chain). If the model is simply pattern-matching, the H2 corroboration is trivial:
pattern-matching fires regardless of whether the keyword is in Persona or Instructions.

**Why it matters:**
1. The jump from 0/10 (orientation) to 10/10 (mechanism) may not identify a reasoning
   threshold but semantic saturation — the point where the prompt becomes a literal instruction
   to check for a specific bug.
2. If pattern-matching is operative, the P_p simulation engine / P_d checklist handler
   distinction cannot be inferred from token counts alone.
3. The 157-token delta (A > B) may be a register artifact: Persona framed as "thinking
   carefully about X" biases toward verbosity (performing the identity), not a structural
   cognitive architecture difference.

**What resolves it:**
A de-patterned causal probe: replace explicit mechanism triggers with abstract system
properties (e.g., "distributed coordination overhead," "non-atomic execution windows,"
"state-lease temporal decoupling"). If P_p outperforms P_d on this blind task, the
simulation engine hypothesis is supported; if A = B, it is a verbosity artifact.

## CC Assessment

Objection accepted as significant but not fatal. The H2 finding (A = B at 10/10) remains
robust across exp-19, exp-20, exp-21b, and exp-23 — four independent corroborations. The
pattern-matching critique does not invalidate H2 corroboration; it questions whether the
detection mechanism is search (H2) or recognition (pattern-match). Both are compatible
with H2's claim that content drives detection regardless of slot.

The P_p simulation engine / P_d checklist handler interpretation is held as tentative.
The token count reversal (A > B for mechanisms, B > A for labels) is an observation
requiring replication.

Conclusion narrowed: "Mechanism vocabulary drives ceiling detection in both slots" —
confirmed. "P_p integrates mechanism vocabulary differently than P_d" — tentative,
requires follow-up.
