# exp-31 — P_p vs P_d Classifier

**Status:** Complete
**Date:** 2026-04-01
**Full record:** `parc/science/experiments/exp-31/findings/FINDINGS.md`

---

## Summary

A one-sentence P_p Persona combined with the PARC compact reference as Context correctly classified persona statements as P_p or P_d across 30 runs and three variants. 30/30 correct. Zero variance.

---

## What Was Tested

Whether the PARC compact reference (parc-reference.md), delivered as Context, is sufficient domain knowledge for a model to distinguish P_p from P_d — and what the decisive variable in the classification actually is.

---

## Results

| Variant | Description | Score | Runs |
|---------|-------------|-------|------|
| A | 5 P_p / 5 P_d, alternating, synthetic | 10/10 | 10 |
| B | 4 P_p / 6 P_d, non-alternating, CW-authored | 10/10 | 10 |
| C | 6 P_p / 4 P_d, sourced from actual experimental variants | 10/10 | 10 |

---

## Key Findings

**1. The reference is sufficient.** The model evaluated against the installed definitions in Context, not training-weight priors. No additional grounding needed.

**2. Mechanism vocabulary is necessary but not sufficient.** The hardest case (exp-28d/A): rich mechanism vocabulary, specific failure modes named, no termination condition. Classified P_d on 10/10 runs. Rule: mechanism vocabulary without a termination condition = P_d.

**3. The termination condition is the decisive variable.** Variants B and C both proved it. Statements 5 vs 6 (exp-27/B vs C): word-for-word identical except one clause — "My implementation is complete only when..." All 10 runs split correctly. The termination condition is the most portable, recognizable P_p marker across model architectures (confirmed: Claude, Grok, Gemini).

**4. Prohibition framing installs a convergence target.** "Do not approve code where..." with a specific structural condition = P_p. The prohibition encodes a verification the model must perform before it can stop. Vague prohibition does not qualify.

**5. Format must prohibit reasoning explicitly when input density is high.** Short variants (A, B) returned clean JSON unprompted. Long variants (C) triggered reasoning prose that consumed the token budget. Adding "Return JSON only. No reasoning, no explanation, no preamble." to Instructions resolved it immediately.

**6. Model-specific sensitivity threshold.** Gemini classified the borderline case (mechanism vocab, no termination) as P_p. Claude and Grok held P_d consistently. This is architecture, not noise.

---

## Tools Produced

- `parc/examples/ispark.md` — working P_p/P_d classifier prompt; reusable for prompt auditing
- `parc/articles/parc-reference.md` — compact PARC reference + findings for practitioners

## Open Threads Generated

- Context as installer — does Context substitute for Persona on recognition tasks?
- Backwards construction method — does building TASK layer first reliably produce P_p?
- Cross-model sensitivity threshold — formal series across Claude, Grok, Gemini on borderline cases
- D, E, F termination conditions — content pipeline personas are P_d by this finding; add termination conditions before further tuning
