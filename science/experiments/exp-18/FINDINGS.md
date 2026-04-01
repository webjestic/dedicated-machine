# exp-18 Findings

**Status:** Complete — calibration failure on primary metric; secondary metric interpretable
**Date:** 2026-03-29
**Question:** Does the Persona slot carry the consideration-set effect, or does the same procedural content produce equivalent effects in the Instructions slot?

---

## Token Results

| Variant | Persona | Instructions | Mean output | Ceiling hits |
|---------|---------|-------------|-------------|--------------|
| A | P_p procedural | Generic | 2,241 | 3/10 |
| B | P_d generic | Procedural (identical content to A) | 2,317 | 4/10 |
| C | P_d generic | Generic | 1,675 | 0/10 |

**Gaps:**
- B vs A (slot effect, content held): **+76 tokens** (noise — B ≈ A)
- A vs C (content + slot effect): **+566 tokens**
- B vs C (content effect, Instructions slot): **+642 tokens**

---

## Calibration Failure: Binary Detection Metric Not Interpretable

**Detection rates: A=10/10, B=10/10, C=9/10 (estimated)**

C (P_d baseline, no procedural content) detected the TTL arithmetic gap at rates indistinguishable from A and B. The artifact is not structurally hidden for a capable reviewer: `ORDER_LOCK_TTL=60`, `REQUEST_TIMEOUT=30`, `MAX_RETRIES=3`, `RETRY_BACKOFF=5` are all directly readable constants, and the arithmetic (`3×30 + 2×5 = 100 > 60`) is findable by code-visible inspection without any procedural prompt scaffolding.

Per the calibration check in SCORING.md: C detection rate ≤ 2/10 was required. C ≈ 9/10. **Artifact fails calibration.**

The binary detection primary metric cannot distinguish between "procedural content installed a consideration set" and "capable model did visible arithmetic." Token depth is the interpretable signal.

---

## Secondary Metric: Token Depth Interpretation

### B ≈ A >> C

The token depth comparison is clean and passes calibration:
- C is substantially below A and B (+566 and +642 token gaps respectively)
- A and B are indistinguishable within Phase 6 noise (+76 tokens, well within the ~125-token reversals observed in exp-14/15)

**This pattern is consistent with H2: the procedural content carries the effect regardless of slot.**

When the same procedural content appears in the Instructions slot with a P_d Persona (B), it produces approximately the same reasoning depth as when it appears in the Persona slot as P_p identity (A). Both substantially outperform the P_d baseline with no procedural content (C).

### Caveat: Noise level limits conclusion

The +76 token A-B gap is within noise. It is equally consistent with:
- H2 confirmed: slot is irrelevant, content is the operative variable
- H1 partially confirmed: slot adds something, but the +76 gap is too small to observe at n=10

The experiment cannot distinguish these at current sample size.

---

## What This Experiment Establishes

1. **Procedural content in Instructions slot produces equivalent token depth to Persona slot.** B ≈ A on consideration-set breadth. If slot position were strongly load-bearing, A >> B would be expected. The observed gap (+76 tokens) is not meaningfully different from zero at n=10.

2. **Procedural content in either slot substantially outperforms no procedural content.** A >> C (+566) and B >> C (+642) are robust. The operative variable is the presence of domain-specific procedural reasoning, not whether it is in the Persona or Instructions slot.

3. **The artifact must be redesigned for a clean binary detection slot-swap.** The order processor's failure mode is too findable by code-visible arithmetic for P_d to miss it. A valid slot-swap artifact requires a failure mode that is:
   - Only detectable through multi-step state simulation (not arithmetic on visible constants)
   - Reliably found by P_p with procedural content (≥7/10)
   - Reliably missed by P_d without procedural content (≤2/10)

---

## Design Implication: What a Clean Slot-Swap Needs

The exp-01e Redis lock artifact (zombie-write failure mode, 10/10 P_p, 0/10 P_d, zero-shot transfer) was the sharpest prior calibration. exp-07c was designed to use a variant of that artifact but was confounded by a `logger.warning` line that named the failure mode.

For a clean binary-detection slot-swap:
- Use an artifact structurally similar to exp-01e — failure mode visible only by simulating thread state across the full lock lifecycle
- Strip any log line, comment, or variable name that names or implies the failure
- Verify P_d calibration before running the slot-swap variants

The token depth result from exp-18 already provides directional evidence for H2. A clean binary-detection experiment would close it definitively.

---

## Current State of the Slot-Swap Question

| Evidence | Points toward |
|----------|--------------|
| exp-07c: C ≈ I on contaminated artifact | Artifact confound; no slot signal |
| exp-09: C ~ B on clean artifact (domain content in Instructions) | H2 — content works in Instructions slot |
| exp-18 token depth: B ≈ A >> C | H2 — procedural content in Instructions slot ≈ Persona slot |
| exp-18 binary detection: all variants ≈ 10/10 | Calibration failure; artifact too easy |

The cumulative evidence across exp-09 and exp-18 consistently points toward H2: procedural content is the operative variable, and the slot is not strongly load-bearing. A clean binary-detection replication with a properly calibrated artifact would close this definitively.
