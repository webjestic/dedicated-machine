# Hypothesis: Semantic Density in the World Layer

**Status:** Unvalidated — theory only
**Origin:** Emerged from PARC prompt iteration work (2026-03-27)
**Target paper:** d5

---

## The Claim

Prompt semantic density — specifically, the thematic coherence of tokens adjacent to identity-assignment anchors in the World Layer — is a measurable predictor of reasoning quality, independent of prompt length.

A World Layer that installs one dense, compound semantic cluster produces stronger consideration-set effects than a World Layer of equal length that installs multiple weaker, competing clusters.

---

## The Mechanism

### "You" as Identity Assignment Operator

The token "You" in a system prompt is not a pronoun. It is an identity assignment operator. When a model encounters "You are X," it does not process X as a description of a third party — it processes X as self-definition. This changes the register: X is not observed, it is inhabited.

This matters because instruction-tuned models are trained on millions of prompt/response pairs where "You are" precedes an identity. The pattern fires reliably. The self-model activates. Whatever semantic cluster follows "You are" gets pulled into the self region of the embedding space — a qualitatively different neighborhood than the same tokens encountered in the third person.

### Gravity Wells

In high-dimensional embedding space, semantically related tokens cluster together. A prompt does not just reference these clusters — it activates them, drawing them into the attention distribution before the task begins. We call an activated semantic cluster a **gravity well**.

"You" opens a gravity well. The tokens immediately adjacent to it determine which cluster gets pulled into the self-model. The coherence of those tokens determines the density of the well.

**Dense well:** "You are a technological thriller novelist who cannot let a technical detail escape" — *technology*, *thriller*, *novelist*, *compulsion*, *detail* all reinforce a single cluster. The well is deep and directed.

**Diluted wells:** Two sentences that each pull toward different clusters create two competing gravity wells anchored to the same identity. The model must reconcile them. That reconciliation costs precision.

### The Compound Identity

Two themes do not have to mean two wells. If the themes are *entangled* — each defined in relation to the other — they fuse into a single compound well. "You can't help but transform technical content into urgent, dramatic prose" is not two wells (technical + dramatic). It is one well that requires both clusters to exist. The tension between them *is* the identity.

The test: can you remove one theme from the sentence without destroying the identity? If yes, they are separate wells. If the sentence collapses without both, they are fused.

### "You cannot help but" — Compulsion Language

The phrase "You cannot help but X" is a specific class of identity language. It does not describe what the model does — it encodes *automaticity* into the identity. The model does not choose to do X. X is a reflex.

This connects to P_p. "After I understand X, I ask Y" is procedural reflex. "You cannot help but transform technical content into dramatic prose" is behavioral reflex. Both encode what the model *does* as part of *who it is*, without requiring a choice at runtime. This is why they outperform descriptive identity language ("I am a thorough analyst") — description requires enactment as a second step; reflex encodes enactment directly.

---

## The Design Principle

**World Layer maximum: two compound wells.**

One well is ideal. Two wells are acceptable if they are fused into a compound identity. Three or more wells competing for the same identity anchor produces measurable drift — the model cannot commit fully to any single gravity well, and the consideration-set narrows toward the intersection of all three, which is smaller than any one of them.

**In single-pass prompts:** The constraint is real. Two compound wells is the practical ceiling before the World Layer starts producing P_d-like behavior — broad engagement across the wrong neighborhood.

**In multi-agent pipelines (e.g. CrewAI):** Each agent gets one well. The pipeline does the work of combining outputs. Agent specialization is the multi-pass version of prompt leanness. The boundary between agents should be placed where the single-pass prompt would start getting fat — where a third well would appear.

---

## The Analysis Tool (Proposed)

A prompt analysis tool that:

1. Identifies all instances of identity-assignment anchors ("You are," "You cannot help but," "You know," etc.) in the World Layer
2. Maps the semantic neighborhood of each anchor — the 5–10 tokens with highest conceptual proximity
3. Clusters those neighborhoods by theme
4. Flags prompts where a single anchor governs more than two distinct theme clusters
5. Scores thematic coherence across all anchors: high coherence = dense well; low coherence = diluted wells

This tool operationalizes "dense vs. diluted" so it is not an authorial judgment but a measurable property of the prompt.

---

## Testable Predictions

If the semantic density hypothesis is correct:

1. **Dense vs. diluted variant test:** A prompt with one compound two-theme well should outperform a prompt with the same content split across two separate sentences (two single-theme wells) on structurally hidden failure modes. Detection rate is the primary measure; token output distribution is secondary.

2. **Well count test:** Prompts with one well > two wells > three wells on detection rate, holding total word count constant.

3. **Fusion test:** A compound sentence that entangles two themes should outperform two separate sentences expressing the same themes individually, even if total token count is identical.

4. **Repetition saturation test:** Multiple "You" anchors pulling toward different clusters should produce lower detection rates than a single "You" anchor pulling toward a dense cluster, even when the total conceptual content is identical.

---

## Connection to Existing PARC Findings

This hypothesis is an extension of the consideration-set mechanism, not a replacement for it.

- **P_p vs. P_d** is the *what*: procedural identity outperforms dispositional identity.
- **Semantic density** is the *why*: procedural language concentrates the gravity well; dispositional language diffuses it.

d3/d4 demonstrate the behavioral effect. d5 would be the first draft that grounds the behavioral findings in embedding geometry — explaining *why* P_p works at the token level, not just *that* it works.

The few-shot confound (§7.3, d4) is also relevant here: if P_p works because it embeds procedural reasoning in the identity, the semantic density mechanism predicts that the *location* of that reasoning (Persona slot vs. Instructions slot) matters less than the *coherence* of the semantic cluster it activates. This is a new angle on the slot-swap question that exp-07 was designed to address.

---

## Status and Next Steps

| Item | Status |
|------|--------|
| Theoretical framework | ✓ Written (this document) |
| Analysis tool | Proposed — not built |
| Dense vs. diluted variant test | ✓ Designed — exp-10 (order processor, invisible timing failure) |
| Well count test | Not designed |
| Fusion test | Not designed |
| Repetition saturation test | Not designed |
| d5 inclusion | Planned — after experimental validation |

**exp-10 artifact note:** The zombie-write scenario was replaced with a new artifact — an order
processor + payment client where `ORDER_LOCK_TTL=60` < worst-case `payment.charge()` duration
of 100s (cross-file arithmetic, no dead-end branch). The zombie-write variants (exp-07 through
exp-09) showed that even an unannotated `if result == 0: return` is code-visible enough for P_d
to find at Tier 0.5. A truly invisible failure requires no dead-end branch at all — only a timing
gap exposed by cross-component arithmetic.
