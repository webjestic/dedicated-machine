# Exp-22 Gemini Synthesis Review

**Model:** gemini-cli default
**Date:** 2026-03-30

## Fatal Objection: The Mechanism Resolution Confound

**Objection:**
The synthesis attributes exp-22's success (A=10/10, B=10/10) to interrogative framing
(pragmatic force), but the experiment changed TWO variables simultaneously compared to
exp-21a: (1) pragmatic force (assertional → interrogative) and (2) vocabulary specificity
(failure-mode labels → causal chain description). Exp-21a used "zombie-write failure modes"
and "fencing token violation" as labels; exp-22 used "stop-the-world GC, all threads
suspended, lock expires, resumes and writes." These are not equivalent vocabulary at the
same specificity level.

If mechanism-level vocabulary is what drove detection — regardless of framing — then the
pragmatic force theory ("assertional vocabulary is inert") may be misinterpreting a
vocabulary specificity effect as a pragmatic force effect.

**Why it matters:**
If causal specificity (not pragmatic force) drives activation, then an assertion with
mechanism-level vocabulary would also produce 10/10. This would invalidate the claim that
"assertional artifact vocabulary acts as a search terminator."

**What resolves it:**
An "Assertional Mechanism" test: place the same causal chain from exp-22 in the PR summary
as an assertion rather than a question:
> "This implementation prevents stale writes during stop-the-world GC pause scenarios where
> all threads including the heartbeat are simultaneously suspended and the lock expires during
> the pause. A fencing token at the DB write layer ensures write safety after process
> resumption."

If this yields 0/10 → pragmatic force is the operative variable, confirmed.
If this yields 10/10 → vocabulary specificity is the operative variable; exp-22's success
was vocabulary, not interrogation.

## CC Assessment

Fatal objection accepted. Exp-22 cannot isolate pragmatic force from vocabulary specificity.
The result (interrogative mechanism → 10/10) is established, but the mechanistic interpretation
is not yet adjudicated.

Conclusion narrowed: "Interrogative artifact with mechanism-level vocabulary drives detection
at ceiling" — this is established. "Interrogative framing is the operative variable" — this
remains unconfirmed due to confound.
