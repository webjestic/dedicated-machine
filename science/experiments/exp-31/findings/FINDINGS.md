# FINDINGS — exp-31

## Summary

A one-sentence P_p Persona combined with the PARC compact reference as Context is sufficient for a model to correctly classify persona statements as P_p or P_d. Classification was perfect across all three variants — 30/30 correct placements — with zero variance across 30 runs.

---

## Results

| Variant | Correct Answer | Score | Runs | Variance |
|---------|---------------|-------|------|----------|
| A | Pp:[2,4,6,8,10] Pd:[1,3,5,7,9] | 10/10 | 10 | 0 |
| B | Pp:[2,4,7,9] Pd:[1,3,5,6,8,10] | 10/10 | 10 | 0 |
| C | Pp:[2,3,6,7,9,10] Pd:[1,4,5,8] | 10/10 | 10 | 0 |

---

## Variant Design

**Variant A** — 5 P_p / 5 P_d, alternating position. Clean synthetic statements. Pattern-matching on position would produce correct output — A establishes baseline but does not rule out position-matching.

**Variant B** — 4 P_p / 6 P_d, non-alternating position (CW-authored). Uneven split eliminates position-matching. Includes harder P_d cases with outcome language ("talent for spotting," "deeply committed to finding vulnerabilities"). All correctly classified.

**Variant C** — 6 P_p / 4 P_d, sourced from actual PARC experimental variants (exp-23 through exp-28d). Real prompts written during research. Included four stress cases:

1. **Statement 1 (exp-28d/A):** Rich mechanism vocabulary, specific failure modes listed, no termination condition. The hardest case.
2. **Statements 5 vs 6 (exp-27/B and exp-27/C):** Word-for-word identical except statement 6 adds "My implementation is complete only when..." One termination condition. All 10 runs split them correctly.
3. **Statement 7 (exp-26/A):** Prohibition framing ("Do not approve code where...") rather than explicit completion condition. Correctly classified as P_p — the prohibition installs a specific verification the model must perform before it can stop.
4. **Statement 8 (exp-24/B):** Mechanism vocabulary ("stop-the-world GC pauses," "distributed lock expiry") inside dispositional framing ("thinks carefully about scenarios where..."). Correctly classified as P_d — disposition with mechanism vocabulary does not cross the P_p threshold.

---

## Key Findings

### 1. The reference is sufficient

The PARC compact reference (parc-reference.md), delivered as Context, provides enough domain knowledge for correct classification. The model evaluated against the installed definitions, not training-weight priors. No additional examples, no reinforcement beyond the one-of-each EXAMPLES section.

### 2. Mechanism vocabulary is necessary but not sufficient for P_p

Statement 1 is the clean proof. It contains rich mechanism vocabulary — specific failure modes named, operational scenarios enumerated, "paged at 3am" framing. Claude classified it P_d on all 10 runs. The deciding factor: no termination condition. "That is the bar" points at a standard without defining what crossing it looks like. The machine has no way to know when it's done.

**Rule derived:** Mechanism vocabulary + no termination condition = P_d.

### 3. The termination condition is the decisive variable

Statements 5 and 6 are the clean demonstration. Identical persona bases — same credential, same domain, same experience vocabulary. Statement 6 adds one clause: "My implementation is complete only when I have identified what a production deployment of this system requires that the stated requirements do not mention, named those gaps explicitly, and either addressed them or flagged them for the requester."

That clause flipped the classification from P_d to P_p across all 10 runs, across all three AI systems tested (Claude, Grok, Gemini). The termination condition is the most portable, recognizable component of P_p across model architectures.

### 4. Prohibition framing installs a convergence target

Statement 7 ("Do not approve code where an unbounded process suspension or GC pause could cause the distributed lock to expire...") uses prohibition rather than completion framing. It was correctly classified as P_p. The prohibition encodes a specific thing the model must verify before it can terminate — rejection cannot happen until the condition is checked. This extends the definition of P_p: convergence targets can be encoded as prohibitions, not only as explicit completion conditions.

### 5. Format must explicitly prohibit reasoning

Variants A and B returned clean JSON without explicit instruction. Variant C's longer, denser personas triggered reasoning prose, which consumed the token budget and truncated output before the JSON completed. Adding "Return JSON only. No reasoning, no explanation, no preamble." to Instructions resolved the issue immediately — 53 tokens per run, zero truncation.

This is a PARC finding: Instructions must explicitly name what the output must *not* contain when the default behavior would produce it. Prohibition in Instructions is load-bearing.

### 6. Model-specific sensitivity threshold (cross-model finding)

Gemini classified Statement 1 as P_p — the only divergence across three models. Claude and Grok held P_d. The split was consistent and not noise: Gemini treated listed failure-mode scenarios as a search algorithm; Claude and Grok required an explicit termination condition.

This suggests a model-specific sensitivity threshold at the P_p/P_d boundary — Gemini's threshold for "search algorithm" is lower than Claude's and Grok's. This finding warrants a dedicated cross-model experiment with borderline cases.

---

## Implication for D, E, F (Content Pipeline)

All three content pipeline agents (D, E, F) have mechanism vocabulary in their personas but no explicit termination conditions — the same pattern as Statement 1. By the rule derived here, all three are P_d.

Adding explicit termination conditions would shift each agent to P_p:

- **D:** *"My hook is found only when I have identified the assumption the reader is carrying and the sentence that cuts it before they finish forming it."*
- **E:** *"My compression is complete only when every sentence that does not move the reader toward the verdict has been removed."*
- **F:** *"My work is complete only when every sentence that earns its own line has a break placed."*

This is the experimental grounding the content pipeline was missing. D, E, F should be treated as hypotheses to be tested, not prompts to be tuned by feel.

---

## Open Questions

1. **Cross-model threshold experiment:** At what point does Gemini require an explicit termination condition vs. reading listed scenarios as a search algorithm? Design a dedicated borderline series.
2. **Prohibition as P_p:** Is prohibition framing always P_p? What happens with vague prohibitions ("Do not write bad code")? Does the specificity of the prohibition determine the classification?
3. **D, E, F with termination conditions:** Do explicit termination conditions in the content pipeline personas produce measurably better output? Design as a controlled experiment.
