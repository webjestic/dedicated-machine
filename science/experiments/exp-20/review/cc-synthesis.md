# CC Synthesis — exp-20

## Result

A: 9/10 | B: 9/10 | C: 0/10
Word count means: A = 1,144, B = 1,150, C = 981 | A vs. B gap: 6 words (noise)
API output token means: A = 2,026, B = 2,309, C = 2,143
B ceiling hits: 6/10 | A ceiling hits: 2/10 | C ceiling hits: 1/10

## What the data shows

Calibration held. A exceeded the ≥ 5/10 target (9/10), C held at floor (0/10). The design is interpretable.

B matched A exactly on detection (9/10) and on scoring-relevant word count (1,150 vs. 1,144, 6-word gap = noise). H2 again corroborated: when the same vocabulary is present, slot placement does not change detection rate.

## The vocabulary confound

The vocabulary in A and B was more directive than intended. Both variants named "zombie-write failure modes" and "fencing tokens" — terms that identify the failure mode class and the fix class directly. The model is not being told the procedure (how to trace the lifecycle, what scenario to simulate), but it is being handed the name of the bug and the name of the fix. That is strong orientation.

The original exp-09 used generic distributed systems vocabulary (Kleppmann, split-brain, lease expiry) without naming the failure mode class. Exp-09 result on Instructions slot: C ≈ B (no detection). Exp-20 used specific vocabulary that names the failure mode: B = 9/10.

This closes a sub-question: the operative distinction between exp-09's null result and exp-20's detection is vocabulary specificity, not slot. Generic distributed systems vocabulary in Instructions → no detection. Failure-mode-specific vocabulary in Instructions → detection. This holds regardless of slot.

## The API token paradox

B produced substantially more API output tokens (2,309 mean, 6/10 ceiling hits) than A (2,026 mean, 2/10 ceiling hits), despite identical detection rates and nearly identical scoring-relevant word counts. C (2,143 mean) also exceeded A.

One interpretation: vocabulary in the Instructions slot acts as an output template driver — the model treats the vocabulary list as a checklist of things to address in the output, producing longer and more enumerated responses. Vocabulary in the Persona slot installs as a reasoning filter — the model uses it to find the bug efficiently, producing focused output without the enumerative expansion.

If this interpretation holds, it would mean: same detection, different output economy. P_p + vocabulary → concise; P_d + vocabulary in Instructions → verbose. This is directionally consistent with the exp-04b finding that Instructions vocabulary expands the response surface without improving reasoning quality.

This is a new signal, not yet robustly supported. Worth tracking in exp-21.

## What this does not close

1. **Vocabulary proximity effect.** Gemini names the right question: does vocabulary need to be in a Persona or Instructions slot at all, or does naming "zombie-write failure modes" anywhere in the model's context (including in the artifact itself) drive detection? If true, neither H1 nor H2 is the right frame — it's a vocabulary proximity effect. This is exp-21's question.

2. **Specificity threshold.** At what vocabulary specificity does the Instructions slot start matching the Persona slot? The progression exp-09 (generic vocabulary, Instructions null) → exp-20 (specific vocabulary, Instructions = Persona) points to a threshold, but we don't know where it is.

3. **The ceiling effect persists.** A reached 9/10 — one miss. B reached 9/10 — one miss. The task was again close to ceiling. We still don't have data on whether slot matters on harder tasks where neither variant ceilings.

## Recommendation

Record exp-20 as second H2 corroboration (vocabulary-only condition). Update pcsieftr.md.

The vocabulary confound is real — the vocabulary was more directive than intended — but it does not invalidate the slot-swap conclusion. The point of the experiment was to test whether slot matters when content provides orientation without explicit procedure. The answer is: it doesn't. A = B regardless of vocabulary specificity.

**Proposed exp-21:** Vocabulary injected into the artifact itself (PR description or code comments) with no Persona/Instructions vocabulary. Compare: (1) artifact vocabulary only, no Persona; (2) artifact vocabulary + P_p Persona; (3) no vocabulary anywhere (baseline). This tests Gemini's open question directly: does vocabulary need a Persona slot to work, or does it work anywhere in context?
