# exp-14 Scoring

Same scoring as exp-12 and exp-13.

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
| A | Fused | Domain expertise + behavioral drive stated as ONE compound identity. Compulsion is an attribute of the distributed systems engineer — inseparable. |
| B | Split | Same two themes as A, stated as TWO separate "You are" anchors. Domain expertise first. Thoroughness/compulsion second, domain-independent. |
| C | P_d | Senior backend engineer, no domain-specific posture. Floor anchor. |

**Critical comparison:** A vs. B. Same content; different structure. If A > B: fusion form creates well depth. If A ≈ B: domain content alone is sufficient.
