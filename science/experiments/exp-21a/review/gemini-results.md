# Exp-21a Gemini Results Review

**Model:** gemini-3-pro-preview
**Prompt:** See /tmp/exp21a-gemini-review-prompt.txt

---

**Calibration Status:** Clean. Baseline (C=0/10) confirms the zombie-write failure mode remains out-of-distribution for the unconditioned model. The metric is structurally interpretable, but the experimental design contains a fatal flaw that invalidates its primary conclusion.

**1. The Null Result is Confounded by Semantic Framing.**
The null result in exp-21a is not a clean measurement of slot placement; it is the result of a content confound. By placing the vocabulary in the PR description as an *assertion of success* ("prevent zombie-write failure modes... defending against scenarios..."), the experimental design changed the pragmatic force of the words. The model processed the vocabulary as a premise to accept ("the author claims this is handled") rather than a heuristic to apply. This triggers the LLM's documented confirmation bias toward authorial claims, truncating the search algorithm before it can reach the failure mode.

**2. Exp-21a Does Not Challenge H2.**
H2 (content is operative regardless of slot) remains unfalsified. Because you changed both the slot (Instructions → Artifact) and the semantic force (Directive → Assertion), the variables are not isolated. You cannot conclude that the artifact slot suppresses vocabulary activation when the vocabulary was presented as a solved constraint.

**3. Vocabulary Operates via Pragmatic Force, Not Just Presence.**
The contrast between exp-20 (9/10) and exp-21a (0/10) proves that lexical presence alone is not a magic activation key. The operational variable is how the text positions the model relative to the target concept. In the Instructions slot, the vocabulary acts as a search vector. In the artifact PR description, it acts as a search terminator.

**4. Token Gap Does Not Exceed Noise.**
The token deltas (A=1012, B=946, C=908) fall below the established ~125-token noise threshold for Phase 6. The A vs. B gap (66 tokens) is statistically meaningless and does not indicate that P_p (Variant A) installed a deeper consideration set or search algorithm. The model simply produced slightly more verbose shallow analysis.

**5. Next Experiment Proposed: Directive Artifact Placement.**
To actually test H2 and isolate the effect of the artifact slot, you must inject the vocabulary into the artifact with the same directive or interrogative force it possessed in the system prompt.

**Design:** Modify the artifact to include the vocabulary as an unresolved `TODO` comment or an explicit PR reviewer question, rather than a statement of fact.
**Example Injection:** `// TODO: evaluate if this architecture is vulnerable to zombie-write failure modes during GC stop-the-world pauses. Check if lock lease expiry allows fencing token violations at the write layer.`

If this yields high detection rates (matching exp-20), H2 is supported: content governs engagement regardless of the slot. If it yields 0/10, you have isolated the artifact slot as structurally degrading to directive reasoning.
