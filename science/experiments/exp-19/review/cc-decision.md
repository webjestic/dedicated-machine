# CC Decision — exp-19

## Gemini's objection

Ceiling effect: A and B both hit 10/10. Any latent slot advantage is unobservable at this task difficulty. The "content is operative" conclusion may be prematurely broad.

## Response

The objection is correct and I accept it — but it does not change the recommendation, it narrows the claim.

What the data establishes: when procedural content is explicit and sufficient for the task, slot placement does not add detectable lift. B = A is a real finding. The ceiling effect is not a confound — it's part of what makes this a clean H2 corroboration. If content alone can drive 10/10 detection, that is evidence that content is operative.

What the data cannot establish: whether the slot provides lift on harder tasks where neither variant ceilings. Gemini is right that this question is still open.

The conclusion is narrowed as follows:

> **Revised claim:** For tasks where explicit procedural content is sufficient to ceiling detection, slot placement (P_p vs P_d + Instructions) does not provide additional architectural lift. The Persona slot may still be load-bearing when task difficulty exceeds what explicit procedure can cover.

## Recommendation (revised)

Record exp-19 as H2 corroboration under the calibrated ceiling condition. Do not generalize to "slot never matters." The novel synthesis question — does slot matter when content cannot fully specify the procedure? — is the right target for exp-20.

**Exp-20 design (confirmed):** Strip instructions to domain vocabulary only. Remove explicit procedure from both A and B. If slot matters for orientation without procedure, it should appear here. This directly addresses Gemini's "what resolves it."
