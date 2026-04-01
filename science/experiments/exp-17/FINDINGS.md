# exp-17 Findings

**Status:** Complete
**Date:** 2026-03-29
**Question:** Is the compulsion-as-reflex linguistic pattern ("constitutionally unable to X without Y") a portable P_p amplifier independent of domain vocabulary, or is domain vocabulary the operative variable?

---

## Token Results

| Variant | Persona type | Mean output | Ceiling hits | Min | Max |
|---------|-------------|-------------|--------------|-----|-----|
| A | Compulsion-as-reflex + domain vocabulary | 2,074 | 2/10 | 1,417 | 2,500 |
| B | Trait/habit description + domain vocabulary | 2,261 | 3/10 | 1,914 | 2,500 |
| C | Compulsion-as-reflex, no domain vocabulary | 1,756 | 0/10 | 969 | 2,361 |
| D | P_d baseline | 1,772 | 0/10 | 1,463 | 2,139 |

**Gaps:**
- B vs A (register effect, domain vocabulary held): **B > A by +187 tokens** (reversal — expected A > B)
- C vs D (compulsion framing without domain vocabulary vs. P_d): **+16 tokens (noise)**
- A vs D (domain vocabulary effect, compulsion framing): **+302 tokens**
- B vs D (domain vocabulary effect, trait framing): **+489 tokens**

---

## Primary Finding: Domain Vocabulary Is the Operative Variable; Compulsion Framing Is Not

### 1. Compulsion framing without domain vocabulary = P_d floor

C ≈ D (+16 tokens). The compulsion-as-reflex structure — "cannot read code without mentally simulating every execution path until you have found exactly where it does not hold" — produces no amplification whatsoever when domain-specific vocabulary is stripped out. Compulsion framing is not a portable amplifier. It requires domain content to activate.

**Note on C-02:** C-02 ran 969 tokens (the shortest output in the experiment). This is an outlier — consistent with what a P_d-floor variant produces under low-engagement conditions. Without C-02, C mean ≈ 1,843, which puts C ~71 tokens above D. This does not change the conclusion: even in the best-case reading, compulsion-without-domain-vocabulary is only marginal above P_d, not meaningfully amplified.

### 2. Compulsion framing with domain vocabulary is weaker than trait framing with the same vocabulary

B > A by +187 tokens. The trait/habit variant ("your reviews are comprehensive and methodical: when examining a locking implementation you trace lock lifecycles... and you verify whether designs hold under failure conditions") outperforms the compulsion variant ("constitutionally unable to review a locking implementation without tracing the full lifecycle of every lock...").

This is the third consecutive reversal on a framing hypothesis:
- exp-14: A (fused) > B (split) by +123 tokens
- exp-15: B (split, fresh wording) > A (fused, fresh wording) by +125 tokens — reversal
- exp-17: B (trait) > A (compulsion) by +187 tokens — reversal

The compulsion-as-reflex framing is not the operative variable. When controlled for domain vocabulary, it does not consistently outperform the simpler trait description.

### 3. Domain vocabulary is necessary AND sufficient

| What's present | Mean | vs. P_d |
|----------------|------|---------|
| Domain vocab + compulsion framing (A) | 2,074 | +302 |
| Domain vocab + trait framing (B) | 2,261 | +489 |
| Compulsion framing, no domain vocab (C) | 1,756 | −16 (noise) |
| P_d baseline (D) | 1,772 | — |

Domain vocabulary adjacent to the "You" anchor is what activates the consideration-set mechanism. The linguistic register through which it is expressed — compulsion vs. habit vs. trait — is secondary and not consistently directional across experiments.

---

## Revised Mechanism: Semantic Content, Not Linguistic Register

The Semantic Density hypothesis holds but in a narrower form:

**What was hypothesized:** Dense semantic neighborhood adjacent to the "You" anchor activates the consideration set; the compulsion-as-reflex register further amplifies this by encoding procedural behaviors as reflexes rather than choices.

**What the data shows:** Dense semantic neighborhood adjacent to the "You" anchor activates the consideration set. The register through which it is expressed is not a reliable amplifier — it can be positive, negative, or neutral depending on wording and context.

**The operative variable is the semantic content of the domain vocabulary, not the linguistic frame around it.**

This connects directly to the few-shot confound (exp-06, §7.3 of the paper): what makes P_p work is the procedural reasoning embedded in domain-specific vocabulary, not the identity framing structure around it. The compulsion-as-reflex language is a stylistic marker that often co-occurs with high-quality domain vocabulary in practice — which is why it was observable across Phase 6 — but it is not independently operative when controlled.

---

## Cross-Experiment Rank (Updated Through exp-17)

| Persona form | Source | Mean output |
|-------------|--------|-------------|
| Fused compound, original wording | exp-14 A | 2,377 |
| Split same-content, fresh wording | exp-15 B | 2,323 |
| Split same-content, original | exp-14 B | 2,254 |
| Trait + domain vocabulary | exp-17 B | 2,261 |
| Fused compound, fresh wording | exp-15 A | 2,198 |
| Compulsion + domain vocabulary | exp-17 A | 2,074 |
| Split orthogonal (1 orthogonal well) | exp-13 B | 2,065 |
| Split 2 orthogonal wells | exp-13 C | 2,017 |
| Compulsion, no domain vocabulary | exp-17 C | 1,756 |
| P_d baseline | exp-17 D / exp-14 C | ~1,750 |

The rank does not follow compulsion vs. trait. It does not follow fused vs. split. The top six configurations all contain domain-specific vocabulary adjacent to the "You" anchor. The bottom two do not have it (C) or are P_d (D).

**The consistent signal across all of Phase 6 is: domain-specific vocabulary in the Persona is what separates P_p performance from P_d. Everything above that threshold — fusion form, compulsion framing, split form, trait framing — produces variance that has not been directionally stable across experiments.**

---

## What This Closes

1. **Compulsion-as-reflex as the operative variable: falsified.** It is not portable. Without domain vocabulary, it collapses to P_d floor. With domain vocabulary, it is outperformed by the simpler trait form.

2. **Semantic Density hypothesis: confirmed in narrower form.** The operative variable is the semantic content density (domain vocabulary adjacent to the "You" anchor), not the grammatical or linguistic register through which it is expressed.

3. **Phase 6 summary:** Six experiments establish that P_p >> P_d across all configurations tested (minimum gap: domain vocabulary required; maximum gap: +489 tokens in exp-17 B). The within-P_p structure (fusion vs. split, compulsion vs. trait) produces variance but no stable gradient. Any P_p variant with domain-specific vocabulary in the Persona substantially outperforms P_d; the specific framing of that vocabulary does not produce consistent directional effects at n=10.

---

## What Remains Open

The within-P_p variance (range from ~2,017 to ~2,377 across Phase 6) is real but unpredictable from the linguistic features tested. The candidates that have not been directly isolated:

1. **Specificity of procedural content:** The explicit reasoning steps embedded in the Persona ("trace lock acquisition through the heartbeat renewal cycle, then ask what happens to the pending write if a GC pause freezes the heartbeat thread between renewal attempts") have not been varied independently of domain vocabulary and framing. These steps are the implicit CoT hypothesis made specific — and they have never been controlled in Phase 6.

2. **Density of domain vocabulary vs. generality of procedural steps:** A Persona with maximal domain vocabulary but generic procedural steps (B: "trace lock lifecycles") vs. one with fewer domain terms but highly specific procedural steps has not been tested.

These questions map directly onto the paper's primary open confound (§7.3): the slot-vs-content question. exp-17 provides the clearest evidence yet that content (domain vocabulary) is the operative variable. The question is what within "content" matters most.
