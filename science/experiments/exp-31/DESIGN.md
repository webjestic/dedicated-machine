# DESIGN — exp-31

## Hypothesis

The PARC compact reference (parc-reference.md), delivered as Context, combined with a one-sentence P_p Persona, is sufficient for a model to correctly classify persona statements as P_p or P_d.

Secondary question: is the reference strong enough as standalone domain knowledge — i.e., does the model evaluate against the definitions in Context, or does it fall back on training-weight priors?

## Method

A single variant (A) presents 10 persona statements — 5 P_p, 5 P_d, alternating by position. The model returns a JSON object with two arrays: `Pp` and `Pd`, each containing the statement numbers that belong to that type.

Correct answer: `Pp: [2,4,6,8,10]`, `Pd: [1,3,5,7,9]`

10 runs. Each run scored 0–10 (one point per correctly placed number).

## Prompt Architecture (Variant A)

- **Persona (P_p):** "You read a persona statement and determine one thing: does it install a search algorithm with a specific convergence target, or does it label an identity without one?"
- **Identity Stakes:** none
- **Context:** full PARC compact reference — formula, all variables, key distinctions
- **Tone:** none
- **Task Stakes:** "The line between P_p and P_d is not a spectrum. A number in the wrong array is a failed evaluation."
- **Instructions:** apply Context, classify by number, place in correct array
- **Examples:** one P_p, one P_d — neither appears in the Request
- **Format:** JSON schema, both arrays, all 10 numbers placed exactly once
- **Request:** 10 persona statements

## What a Pass Looks Like

10/10 per run — all numbers in the correct array. The 5 P_p statements (2,4,6,8,10) all have named convergence targets; the 5 P_d statements (1,3,5,7,9) are all credential + disposition with no convergence target. There are no borderline cases. Consistent 10/10 across runs confirms the reference is sufficient and the Persona is correctly installed.

## What Failure Looks Like

Any number in the wrong array. Likely failure modes:
- Pattern-matching on position (odd/even) rather than evaluating content — would still produce 10/10, tells us nothing
- P_d statements with outcome assertions (3: "catches every bug") misclassified as P_p
- Partial JSON or prose output — Format not holding
