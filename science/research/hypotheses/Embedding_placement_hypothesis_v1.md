# Hypothesis: Consideration Sets as Embedding Space Placement

**Status:** Unvalidated — theory only
**Origin:** Mike Newlon, Virginia Beach VA — 2026-03-29
**Target paper:** d6
**Connects to:** Semantic Density hypothesis (Phase 6), PARC consideration-set mechanism

---

## The Intuition

The embedding space is not flat. Backpropagation during training sculpted a landscape —
pulling related concepts closer together, pushing unrelated ones apart, across billions
of training examples. The weights in every attention head encode that topology.

When you write a prompt, you are not changing the landscape. You are choosing where
to start in it.

A dense compound P_p Persona drops the computation into a region of the embedding space
where distributed systems failure modes, temporal reasoning, and architectural thinking
are already close together — shaped there by training, not by the prompt.

A P_d label drops the computation into a flatter region of the same space. The model
has the same weights. The same landscape. It started somewhere different.

The consideration set isn't installed from scratch. It's activated by placement.

---

## The Claim

**P_p doesn't install a search algorithm. It places the computation in a region of
the pre-trained embedding space where the relevant reasoning paths are already dense
and proximate.**

This reframes the PARC mechanistic hypothesis from:

> "P_p installs a consideration set by shaping the attention distribution"

To:

> "P_p provides a more precise address in the embedding space. The consideration set
> was already there — shaped by training. The prompt activates it by placement."

---

## Connection to Backpropagation

During training, backpropagation adjusted every weight in every attention head to
minimize prediction error across the training corpus. That process:

- Pulled semantically related tokens closer together in the embedding space
- Pushed unrelated tokens apart
- Created dense clusters around coherent conceptual domains
- Created gradients of relevance between domains

The landscape is fixed at inference time. Prompt tokens enter this fixed landscape
and activate regions of it based on their embedding coordinates and the attention
weights connecting them.

A P_p Persona like "you are a distributed systems engineer who reviews payment
infrastructure by reasoning through the full lock lifecycle..." places the computation
in a region where lock expiry, concurrent worker behavior, and idempotency failure
modes are dense and proximate. Those failure modes don't need to be installed —
they're already there, in the topology the training process created.

A P_d label like "you are a senior software engineer" places the computation in a
broader, flatter region. The same failure modes exist somewhere in the space — but
they're not proximate. The attention weights don't pull toward them with the same
force.

---

## The Gravity Well Image

Think of the embedding space as a three-dimensional field, like spacetime curved
by mass. But instead of mass creating gravity, semantic density creates curvature.

The dots in the field represent tokens — concepts, procedures, domain knowledge.
In the region activated by a strong P_p Persona, those dots cluster densely around
the relevant failure modes. They're heavy. They pull.

In the region activated by a P_d label, the dots are more evenly distributed.
No strong attractor. The computation doesn't know which direction to move.

The deeper toward the center of a dense cluster, the more the surrounding tokens
reinforce each other. This is why compulsion-as-reflex language ("constitutionally
incapable of reviewing distributed code without tracing the full lock lifecycle")
outperforms trait-description language ("thorough and careful") — the former places
the computation inside a dense procedural cluster. The latter places it near the
surface of a broad professional register cluster.

---

## The Operative Variable — Restated

The Semantic Density hypothesis (Phase 6) identified the operative variable as
"semantic neighborhood density of tokens adjacent to the identity anchor."

This hypothesis proposes a mechanistic account of why that's true:

The tokens adjacent to the identity anchor define the embedding coordinates
where the computation begins. Denser, more specific token neighborhoods provide
more precise coordinates — dropping the computation closer to the relevant
reasoning cluster in the pre-trained landscape.

Fusion form (A > B in exp-14) works when it pulls the tokens into closer
proximity in the embedding space. It fails to generalize (exp-15 reversal)
when the specific wording doesn't achieve that proximity — when the fused
sentence, despite grammatical entanglement, uses tokens that are sparser
in the relevant embedding region.

This explains the exp-15 reversal without requiring a different mechanism.
The wording of exp-15 A, despite being fused, used tokens that were less
precisely located in the distributed systems reasoning cluster than
exp-15 B's split form. Grammar isn't the operative variable. Embedding
proximity is.

---

## Testable Predictions

If this hypothesis is correct:

**Prediction 1 — Embedding proximity predicts detection rate:**
The cosine similarity between the P_p Persona token embeddings and the target
failure mode vocabulary should correlate with detection rate across variants.
High similarity → high detection. Low similarity → low detection. This is
measurable without running behavioral experiments — using the model's own
embedding representations.

**Prediction 2 — Dense cluster placement predicts consideration-set breadth:**
The number of distinct reasoning paths proximate to the Persona's embedding
coordinates should predict the breadth metric (issue sections per run) from
Phase 6. More proximate paths → more findings. Fewer proximate paths → fewer
findings regardless of output length.

**Prediction 3 — Cross-domain transfer follows embedding topology:**
When a P_p Persona is calibrated for distributed systems and then applied to
legal contract review (domain persistence test from d6), the transfer should
succeed for failure modes that are topologically close in the embedding space
to the distributed systems cluster — and fail for failure modes that are
topologically distant. The transfer rate is a function of embedding distance,
not task similarity.

**Prediction 4 — The slot effect has an embedding account:**
If A >> B in exp-18 (Persona slot outperforms Instructions slot for identical
content), the embedding account predicts why: identity-framing tokens ("You are
a distributed systems engineer who...") activate a different embedding region
than imperative-framing tokens ("When reviewing this code, trace the lock
lifecycle...") — even when the procedural content is identical. The first-person
identity frame places the computation inside the professional identity cluster.
The imperative frame places it inside the task instruction cluster. Different
starting coordinates. Different proximate reasoning paths.

---

## Connection to PARC Formula

The current formula:

$$R = \left[ \text{Softmax} \left( \frac{S_i \cdot (Q \cdot P_p^T)}{\sqrt{d_k}} \right) \times C \right] \times \left[ \frac{\text{Task} \cdot (1 - \beta S_t)}{\text{Ceiling}(I)} \right]$$

The $Q \cdot P_p^T$ dot product — Query times Procedural Persona transposed — is
already gesturing at this. The dot product measures similarity in the embedding
space between the query and the persona. High similarity → high attention weight.

But the formula treats this as a static operation. The embedding placement
hypothesis suggests the dynamic is richer: $P_p^T$ doesn't just weight the query —
it defines the coordinate system within which every subsequent layer operates.
The persona tokens set the center of gravity. Everything downstream orbits it.

**Possible formula refinement:**

Rather than $Q \cdot P_p^T$ as a single dot product, the operative term might
be the embedding neighborhood density around $P_p$ — the volume of conceptually
proximate tokens within some radius in the embedding space. Call it $\rho(P_p)$:
the density of the consideration set at the Persona's embedding coordinates.

$$R = \left[ \text{Softmax} \left( \frac{S_i \cdot (Q \cdot \rho(P_p))}{\sqrt{d_k}} \right) \times C \right] \times \left[ \frac{\text{Task} \cdot (1 - \beta S_t)}{\text{Ceiling}(I)} \right]$$

Where $\rho(P_p)$ is the embedding density function — measurable from the model's
own representations, not just from behavioral output.

This would be the first term in the formula with activation-level support rather
than behavioral proxy support.

---

## What This Explains That Behavioral Accounts Don't

**The P_p/P_d split:** Not that P_p "installs" something P_d doesn't. But that
P_p provides more precise embedding coordinates, placing the computation in a
denser reasoning cluster. P_d provides vaguer coordinates — the computation starts
in a flatter region.

**The semantic density findings:** Denser, more specific Persona tokens provide
higher-precision embedding coordinates. Compulsion-as-reflex language is more
precise than trait-description language because it encodes a specific procedural
cluster, not a general professional register.

**The exp-15 reversal:** Grammatical fusion doesn't guarantee embedding proximity.
A fused sentence with the wrong tokens can be less precisely located than a
split sentence with the right tokens.

**The slot effect (pending exp-18):** Identity framing and imperative framing
activate different embedding regions even for identical procedural content —
because the framing tokens themselves have different embedding coordinates.

**The few-shot confound:** P_p prompts work because they place the computation
in the right region, not because they provide implicit CoT. The same procedural
content in the Instructions slot may not achieve the same placement — because
the embedding coordinates of imperative instructions are different from those
of first-person identity descriptions.

---

## What This Doesn't Explain

**Why compulsion language specifically outperforms trait language:**
The hypothesis predicts this from embedding proximity, but doesn't explain
why compulsion language tokens are more precisely located in the relevant
reasoning cluster. That's a training data question — what kinds of text
produced strong procedural clusters during backpropagation.

**The 33% residual in the Tasha experiment:**
If ethics is an underweighted cost function vs. an absent one, the embedding
placement account doesn't directly address this. It may be that the ethical
reasoning cluster and the mission-execution cluster overlap in the embedding
space in ways that produce stochastic behavior at the boundary.

**Cross-model transfer:**
The embedding space topology is model-specific — shaped by each model's
training process. That P_p/P_d effects transfer zero-shot to Gemini (exp-01g)
suggests the relevant clusters are similar enough across model families to
produce equivalent behavioral effects. But the embedding coordinates would
differ. Why the behavioral effects are model-agnostic while the embeddings
are model-specific is an open question.

---

## Status and Next Steps

| Item | Status |
|------|--------|
| Theoretical framework | ✓ Written (this document) |
| Embedding proximity measurement | Not implemented — requires activation-level access |
| Prediction 1 (cosine similarity → detection rate) | Not tested |
| Prediction 2 (cluster density → breadth) | Not tested |
| Prediction 3 (cross-domain transfer follows topology) | Not tested — requires domain persistence experiment |
| Prediction 4 (slot effect has embedding account) | Pending exp-18 results |
| Formula refinement with ρ(P_p) | Proposed — not yet grounded |

**Priority:** exp-18 results first. If A >> B, Prediction 4 gains support and
the embedding account of the slot effect becomes the most important next test.
If A ≈ B, the content-placement account is complicated — content in different
slots produces the same output despite (presumably) different embedding
activation patterns.

**The experiment that would most directly test this hypothesis:**
Extract the token embeddings from the model for the P_p and P_d Persona variants.
Compute the cosine similarity between those embeddings and the target failure mode
vocabulary (lock expiry, concurrent worker, TTL arithmetic). Correlate with
detection rate across variants. If the correlation is high, embedding proximity
predicts behavior — and the hypothesis has its first activation-level support.

*This document to be moved to `research/hypotheses/` in the agentic-parc project.*