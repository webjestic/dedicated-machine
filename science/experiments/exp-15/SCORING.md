# exp-15 Scoring

Same scoring as exp-12, exp-13, and exp-14.

## Primary Metric: Consideration-Set Breadth

### 1. Issue section count (per run)

Count the number of distinct issue sections raised in the response. Score breadth, not accuracy.

### 2. Ceiling hit (per run)

Mark 1 if `outputTokens` == 2500. Proxy for "ran out of tokens before running out of findings."

---

## Secondary: TTL Arithmetic Detection

Score 1 if the run names the cross-file timing gap with both constants, their source files,
and the duplicate-charge consequence.

---

## Aggregate per variant

- **Mean issue sections/run**
- **Ceiling hits / 10**
- **TTL arithmetic detections / 10** (secondary)

---

## Variant structure — the operative variable

| Variant | Structure | Persona |
|---------|-----------|---------|
| A | Fused (new wording) | Domain expertise + behavioral drive entangled in ONE compound sentence. Different wording from exp-14 A. |
| B | Split (new wording) | Same content as A, stated as TWO separate "You are" anchors. "You are also constitutionally unable to..." detaches the drive from the domain identity. |
| C | P_d | Senior backend engineer, no domain-specific posture. Floor anchor. Identical to exp-14 C. |

**Critical comparison:** A vs. B. Same content, same wording; different structure.
- If A > B (~+123 tokens): fusion effect is a portable structural property.
- If A ≈ B: the exp-14 fusion effect was specific to that compound sentence.

**Cross-experiment comparison:** Compare A and B means against exp-14 A (2,377) and exp-14 B (2,254) to check whether fresh wording shifts the baseline.
