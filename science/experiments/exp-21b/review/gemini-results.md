# Exp-21b Gemini Results Review

**Model:** gemini-3-flash-preview (gemini-3-pro-preview at capacity)

---

The null results in **exp-21b** are highly interpretable when viewed alongside the preceding experimental chain (19, 20, 21a). They suggest a **threshold effect** where general domain orientation is insufficient to expand the model's consideration set to include high-entropy failure modes like the zombie-write.

### 1. Interpretability of the Null Result
The result is interpretable as a confirmation of **vocabulary specificity requirements**. In exp-20, naming the failure mode ("zombie-write") and the fix ("fencing token") produced 9/10 detection. In exp-21b, providing the "less directive" orientation (lock lifecycle, process isolation) resulted in 0/10.

The flagged items (A-06, B-02, B-09, B-05) are the smoking gun: the model identified components of the problem (e.g., naming the "pause" or the "fix") but failed to connect them into a coherent causal chain. This indicates that orientation gets the model to the "neighborhood" of the failure, but only specific vocabulary triggers the "search algorithm" required to find the specific "house."

### 2. The Full Matrix (exp-20, 21a, 21b)

| Experiment | Vocabulary Type | Slot | Pragmatic Force | Result |
| :--- | :--- | :--- | :--- | :--- |
| **exp-20** | Directive (Specific) | System Prompt | Directive (Search) | **9/10** |
| **exp-21a** | Directive (Specific) | Artifact (PR) | Assertion (Verify) | **0/10** |
| **exp-21b** | Orientation (Vague) | System Prompt | Directive (Search) | **0/10** |

Together, these experiments form a coherent picture: **Detection requires BOTH specific "what" (vocabulary) AND directive "how" (framing/slot).**

### 3. Mechanism Implication: Specificity vs. Slot
The operative variable is likely the **interaction** between the two.
- **Specificity (a) is necessary:** 21b proves that even in the "strong" System Prompt slot, vague orientation fails.
- **Slot/Pragmatic Force (b) is necessary:** 21a proves that even specific vocabulary fails if it is framed as an authorial assertion in the artifact rather than a directive in the prompt.
- **Conclusion:** The model treats the System Prompt as an *instruction to search* and the Artifact as a *premise to evaluate*. If the instruction is too vague (21b), the search fails. If the premise claims success (21a), the evaluation terminates early.

### 4. Proposed Experiment to Isolate Variables
To isolate **Slot Position** from **Pragmatic Force**, run **exp-22**:
- **Design:** Inject directive vocabulary into the Artifact but with **Interrogative/Directive Force**.
- **Implementation:** Modify the PR description to include an "Open question for reviewer: Does this design prevent zombie-writes through fencing tokens?"
- **Logic:** If this scores > 0, then H2 (Content/Force > Slot) is supported. If it still scores 0, then the Artifact slot itself is a "dead zone" for reasoning, regardless of how the text is framed.

### 5. Threshold Effect
There is a fundamental threshold effect. The zombie-write is not a "natural" reasoning path for the model; it is a "hidden" state. "Orientation" language increases the probability of looking at the lock's temporal properties, but naming the "zombie-write" is the required trigger to bridge the gap from "unreliable heartbeat" to "stale DB write." You must name the ghost to see it.

### 6. Token Count Observation
The B (1113) > A (1048) pattern matches exp-20's API token paradox (B=2309 > A=2026). This suggests a consistent "Instructions-as-checklist" verbosity effect (B) versus "Persona-as-filter" economy effect (A), regardless of whether the detection target is hit.
