# exp-14 Findings

**Status:** Complete
**Date:** 2026-03-29
**Question:** Is fusion form doing the work, or domain content alone? Same themes (distributed systems expertise + thoroughness/compulsion drive), different structure: A fuses them into one compound identity sentence; B states them as two separate "You are" anchors.

---

## Token Results

| Variant | Structure | Mean output | Ceiling hits | Min | Max |
|---------|-----------|-------------|--------------|-----|-----|
| A | Fused compound identity | 2,377 | 4/10 | 2,014 | 2,500 |
| B | Split: domain \| behavioral drive | 2,254 | 2/10 | 1,987 | 2,500 |
| C | P_d baseline | 1,642 | 0/10 | 1,450 | 1,979 |

**Gaps:**
- A vs B (fusion effect, content held constant): +123 tokens
- B vs C (P_p vs P_d, same domain content): +612 tokens
- A vs C (full range): +735 tokens

---

## Primary Finding: Fusion Is Real but Modest; Domain Content Does Most of the Work

**A > B confirmed.** Fusing both themes into one compound identity sentence adds ~123 tokens of mean output above the split form with identical content. Ceiling rate is also higher (4/10 vs 2/10). Fusion form is a real effect.

**B >> C confirmed.** Even with the behavioral drive stated as a separate, domain-independent anchor, the split Persona is +612 tokens above P_d. The domain expertise — "expert in distributed systems: consensus protocols, distributed locking, and race conditions" — installs the consideration-set floor regardless of structural form.

The behavioral drive ("meticulous and thorough, can't help but discover hidden mysteries") amplifies depth when fused with the domain anchor. When separated, it still contributes — B is not the same as an orthogonal split — but contributes less.

**The full model is a gradient, not a binary switch:**

| Persona form | Source | Mean output |
|-------------|--------|-------------|
| Fused compound (domain + drive entangled) | exp-14 A | 2,377 |
| Split same-content (domain \| drive separate) | exp-14 B | 2,254 |
| Split orthogonal (domain \| orthogonal well) | exp-13 B | 2,065 |
| Split 2 orthogonal (domain \| 2 orthogonal) | exp-13 C | 2,017 |
| P_d baseline | exp-14 C / exp-13 D | ~1,650 |

---

## Decomposing the exp-13 "First Split Is the Loss" Finding

exp-13 A vs. exp-13 B showed a +351 token gap at the first split. exp-14 now shows that gap conflated two distinct effects:

| Transition | Effect | Delta |
|-----------|--------|-------|
| exp-14 A → exp-14 B | Fusion form (content held constant) | −123 |
| exp-14 B → exp-13 B | Content relevance (same-domain drive → orthogonal domain) | −189 |
| exp-13 A → exp-13 B (combined) | Both effects together (+ noise) | −351 |

The 351-token loss from exp-13 was approximately half structural (fusion vs. split) and half content relevance (domain-relevant behavioral drive vs. orthogonal domain well). These are separable — exp-14 isolates them.

**Implications for Persona design:**
- Fused compound is the optimal form
- If split is unavoidable, a domain-relevant behavioral drive in the second anchor (exp-14 B form) recovers ~189 tokens vs. an orthogonal second anchor
- An orthogonal second anchor is the worst P_p configuration before falling to P_d level

---

## The exp-13 Binary Switch Model: Refined, Not Overturned

exp-13 found: the first split is the loss; B ≈ C with orthogonal wells. That finding stands. The B ≈ C result was real — once you have split and added an orthogonal well, adding a second orthogonal well costs nothing further (exp-13 B=2065 vs C=2017, +47, noise).

What exp-14 adds: within the split regime, content relevance of the second anchor matters. The binary switch is from fused to split. Within the split regime, a finer gradient exists depending on whether the second anchor is domain-relevant or orthogonal.

**Revised model:**

```
fused compound
    ↓ −123 (structural split)
split + domain-relevant behavioral drive
    ↓ −189 (content relevance: behavioral drive → orthogonal domain)
split + orthogonal well(s)
    ↓ −350 (P_p → P_d; any split P_p vs baseline)
P_d baseline
```

The biggest single step remains P_p → P_d (~350–400 tokens), confirmed across six variants in four experiments.

---

## P_p >> P_d: Fifth Confirmation

Every P_p variant in every experiment substantially outperforms P_d:

| Variant | Experiment | Mean output | vs. P_d |
|---------|-----------|-------------|---------|
| A (fused) | exp-14 | 2,377 | +735 |
| B (split same-content) | exp-14 | 2,254 | +612 |
| A (fused) | exp-13 | 2,416 | +749 |
| B (split orthogonal) | exp-13 | 2,065 | +398 |
| A (fused) | exp-10b | 2,471 | +664 |
| P_d baselines | exp-10b / exp-13 / exp-14 | 1,642–1,807 | — |

The P_p installation effect is robust across Persona configurations, well counts, and fusion forms. The weakest P_p variant tested (exp-13 C, split + 2 orthogonal wells, mean=2017) is still +350 tokens above P_d.

---

## Impact on Semantic Density Hypothesis

The hypothesis — "thematic coherence of tokens adjacent to identity anchors predicts consideration-set depth" — is supported with refinement.

**Supported:** Fusion creates a measurably denser activation cluster. Fused compound > split same-content is a repeatable +123 token effect, holding content exactly constant. The form of the identity statement, not just its content, shapes the gravity well.

**Refined:** Content relevance of the semantic neighborhood matters as much as fusion form. Domain-relevant behavioral drive in a split anchor (exp-14 B) outperforms orthogonal domain content in a split anchor (exp-13 B) by +189 tokens — a larger effect than pure fusion (+123). The density of the semantic cluster is shaped by both structure and content.

**Remaining question:** Does the fusion effect generalize? All fusion tests use the same compound sentence (exp-10b/exp-12/exp-13/exp-14 A). Whether fusion is portable — whether any compound sentence benefits equally from entanglement vs. separation — is untested.
