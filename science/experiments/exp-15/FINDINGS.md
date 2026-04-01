# exp-15 Findings

**Status:** Complete
**Date:** 2026-03-29
**Question:** Is the +123 token fusion effect from exp-14 a portable structural property of grammatical entanglement, or was it specific to that compound sentence?

---

## Token Results

| Variant | Structure | Mean output | Ceiling hits | Min | Max |
|---------|-----------|-------------|--------------|-----|-----|
| A | Fused (new wording) | 2,198 | 1/10 | 1,920 | 2,500 |
| B | Split (new wording) | 2,323 | 4/10 | 1,753 | 2,500 |
| C | P_d baseline | 1,792 | 0/10 | 1,460 | 2,265 |

**Gaps:**
- B vs A (split beat fused): +125 tokens — reversal of exp-14
- B vs C: +530 tokens
- A vs C: +405 tokens

---

## Primary Finding: Fusion Is Not a Portable Structural Property

**A > B did not replicate.** B beat A by +125 tokens — essentially the mirror image of exp-14's +123 token fusion effect, in the opposite direction. The fusion effect is sentence-specific, not a general property of grammatical entanglement.

The cross-experiment ordering makes the mechanism visible:

| Source | Form | Mean output |
|--------|------|-------------|
| exp-14 A | Fused, original sentence | 2,377 |
| exp-15 B | Split, new wording | 2,323 |
| exp-14 B | Split, original wording | 2,254 |
| exp-15 A | Fused, new wording | 2,198 |
| exp-13 B | Split + orthogonal well | 2,065 |
| P_d baselines | — | ~1,650–1,792 |

The rank does not follow a fused > split axis. It follows sentence quality. A high-density split sentence (exp-15 B, 4/10 ceiling) outperforms a lower-density fused sentence (exp-15 A, 1/10 ceiling).

---

## Revised Mechanism: Semantic Neighborhood, Not Grammatical Form

The semantic density hypothesis is not falsified — it is refined. The operative variable is **not** grammatical fusion; it is the **content density of the semantic cluster adjacent to the "You" identity anchor**.

- Fusion can produce density by forcing high-value tokens into close proximity. This is what made exp-14 A effective.
- Fusion does not guarantee density. A fused sentence with less precise or less coherent tokens (exp-15 A) produces a weaker gravity well than a split sentence with higher-density content (exp-15 B).
- A split sentence can produce high semantic density if its wording is precise and domain-coherent.

**Fusion is neither necessary nor sufficient for high semantic density.** That is different from inert — grammatical fusion is a mechanism by which density can be achieved, but it is not the cause.

---

## What "Sentence Quality" Means Mechanistically

The exp-15 B sentence is: *"You are an expert in distributed systems: consensus protocols, fault-tolerant locking, and race conditions across service boundaries. You are also constitutionally unable to let a distributed design pass without tracing every lock acquisition boundary, TTL assumption, and cross-service dependency until each either holds under failure or you have found exactly where it breaks."*

Despite being split, the second anchor is domain-specific — it references lock acquisition boundaries, TTL assumptions, and cross-service dependencies. These tokens are semantically adjacent to the distributed systems vocabulary in the first anchor. The semantic neighborhood is dense even though the identity anchors are formally separated.

The exp-15 A sentence is: *"You are a distributed systems engineer whose expertise in consensus protocols and fault-tolerant locking has produced a near-pathological attention to concurrency: you cannot review distributed code without mentally tracing every lock acquisition boundary, every TTL assumption, and every cross-service dependency..."*

Grammatically fused, but the compound reads more like a character description than an identity installation. The behavioral drive ("near-pathological attention") is attributed to the engineer as a trait, rather than encoded as a reflex. Compare to the exp-14 A sentence's phrasing: *"you are tedious and thorough and rarely let questionable design architectures go unscrutinized. You can't help but try to discover the hidden mysteries..."* — "can't help but" encodes compulsion as a reflex; "near-pathological attention" names it as a trait. That distinction may account for part of the effectiveness gap.

---

## Impact on Semantic Density Hypothesis

The hypothesis requires revision at the mechanism level:

**Original claim:** Thematic coherence of tokens adjacent to identity anchors predicts depth; fusion creates this coherence by entangling themes in a single sentence.

**Revised claim:** Thematic coherence of tokens adjacent to identity anchors predicts depth; fusion is one way to achieve this coherence but is neither necessary nor sufficient. The operative variable is the semantic density of the cluster, which is shaped by:
1. Which tokens are present (domain specificity, behavioral precision)
2. How directly they encode action vs. describe a trait
3. How semantically proximate they are to the domain vocabulary — not whether they are in the same sentence

**The "can't help but" / compulsion-as-reflex pattern** from exp-14 A and B may be a more reliable density mechanism than grammatical fusion. This is worth isolating in a future experiment.

---

## P_p >> P_d: Sixth Confirmation

Every P_p variant substantially outperforms P_d across six tests:

| Weakest P_p variant tested | Experiment | Mean | vs. P_d |
|---------------------------|-----------|------|---------|
| Split + 2 orthogonal wells | exp-13 C | 2,017 | +350 |
| Fused, new wording | exp-15 A | 2,198 | +406 |

The floor of the P_p effect is now well-characterized: even the weakest P_p configurations tested are ~350–400 tokens above P_d. The P_p installation effect on consideration-set breadth is robust regardless of sentence form or wording quality.
