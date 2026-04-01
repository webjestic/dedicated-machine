# Exp-21a Gemini Synthesis Challenge

## CC Synthesis Claim
CC concluded: vocabulary in the artifact acts as a "search terminator" (assertion framing), not a "search vector" (directive framing). The null result is a pragmatic force confound, not a clean slot measurement. H1/H2 unadjudicated. Next step: inject vocabulary into artifact with interrogative framing (exp-22).

## Gemini Challenge

**The pragmatic force explanation is plausible but over-specified.** CC asserts that the vocabulary acts as a "search terminator" because the PR description frames zombie-write/fencing-token as solved constraints. This is a reasonable hypothesis. However, there is a simpler explanation: the model may simply lack the ability to perform second-order critique — "the author CLAIMS this is handled; let me verify whether the code actually implements it." If so, the null result is not about pragmatic force per se, but about a general limitation in defect verification against stated author intent.

**The two explanations have different experimental implications:**
- If pragmatic force is the confound: interrogative artifact framing (exp-22) will restore detection.
- If second-order critique is the limitation: interrogative framing will also fail, because the limitation is in the model's inability to scrutinize author claims regardless of framing.

**The proposed exp-22 design is the right test and will resolve this ambiguity.**

**Confirmed fatal objection:** Variables are not isolated in exp-21a. Slot AND pragmatic force changed simultaneously. The null result cannot be attributed to slot alone, and H2 remains unfalsified.

## CC Decision
Fatal objection accepted. The conclusion is narrowed:

> **Exp-21a conclusion:** Vocabulary placed in the artifact as assertions of what the design prevents does not drive zombie-write detection, regardless of Persona type. This is consistent with a pragmatic force confound (assertion vs. directive), but the alternative explanation (second-order critique limitation) cannot be ruled out. The next experiment (exp-22) will distinguish these.

H1/H2 remain open. Exp-22 is confirmed as the next step.
