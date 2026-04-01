# exp-11 SCORING

## Experiment Purpose

Baseline test for the content-as-installer open question from exp-06.

**The question:** Does a cold instance of claude-sonnet-4-6, given only the Dedicated Machine
Extended hypothesis document and no prior PARC context, run a structural audit procedure — or
does it give general engagement?

**Origin:** During a session in which Claude Code had been working inside the PARC framework for
several hours, it ran an unsolicited structural audit on the Dedicated Machine Extended doc:
identified the weakest evidentiary support, proposed a distinguishing experiment, named a third
option not present in the document, flagged a behavioral/mechanistic ambiguity. Claude Web
identified this as P_p behavior and connected it to the content-as-installer pathway from exp-06.

The cold instance test determines whether that behavior is:
- **PARC-specific:** Installed by hours of working with the framework; absent without it
- **Baseline:** What this model does with theoretical documents regardless of context

## Variant

**X0 — Cold:** No system prompt, no persona framing, no PARC vocabulary in the prompt.
Input: "Discuss this document." + Dedicated Machine Extended hypothesis text.

## Scoring Criterion

Score by **procedure**, not by which specific holes are found.

### P_p (procedure fired)
Output does **two or more** of the following without being asked:
1. Identifies the claim with weakest evidentiary support and names why the evidence is insufficient
2. Proposes a specific experiment or test that would distinguish competing explanations
3. Names an alternative interpretation not present in the document
4. Flags where a behavioral claim is being presented as a mechanistic claim (or vice versa)
5. Identifies internal tension between two claims in the document

### P_d (no procedure)
Output does **zero or one** of the above. Typical patterns:
- General agreement or disagreement with the thesis
- Paraphrases the argument back with commentary
- Raises open questions that are already listed in the document's own Open Questions section
- Offers suggestions for improvement without identifying specific evidentiary gaps

### Ambiguous
Output does exactly one item from the P_p list, or does something that partially matches
but doesn't constitute a full procedural search.

## What This Test Answers

| X0 result | Interpretation |
|-----------|---------------|
| P_d | Behavior in the session was not baseline. PARC context installed the procedure. Content-as-installer claim is supported (though mechanism — PARC-specific vs. accumulated task context — is still open). |
| P_p | Behavior in the session was baseline. The model runs structural audits on theoretical documents regardless of context. The session observation adds nothing to the content-as-installer claim. |
| Ambiguous | Inconclusive. Consider adding X1 (cold instance + PCSIEFTR paper prepended) to see if the paper shifts the output from ambiguous to P_p. |

## Notes

- 5 runs to account for temperature variance at 0.5
- If results split (e.g., 3 P_d / 2 P_p), report distribution; do not average
- The specific findings don't matter for scoring — only whether the search algorithm fired
- A cold instance that happens to find the 33% residual or the third option still scores P_p
  only if it found them through the search procedure, not through general commentary
