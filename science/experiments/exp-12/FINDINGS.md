# exp-12 Findings

**Status:** Complete
**Date:** 2026-03-29
**Question:** Does consideration-set depth decrease monotonically with the number of semantic wells in the Persona (A=1 > B=2 > C=3 > D=P_d)?

---

## Token Results (Proxy for Breadth)

| Variant | Wells | Mean output | Ceiling hits | Min | Max |
|---------|-------|------------|--------------|-----|-----|
| A | 1 (fused) | 2,285 | 4/10 | 1,873 | 2,500 |
| B | 2 (dist. systems + security) | 2,183 | 2/10 | 1,827 | 2,500 |
| C | 3 (dist. systems + security + perf.) | 2,344 | 3/10 | 1,911 | 2,500 |
| D | P_d baseline | 1,794 | 0/10 | 1,433 | 2,032 |

---

## Issue Section Count (Spot-Checked)

Full scoring of all 40 runs was not performed. Spot-checks of representative runs:

| Run | Tokens | Sections counted |
|-----|--------|-----------------|
| A-01 | 2,500 (ceiling) | 10 distinct issue sections |
| B-01 | 2,268 | 8 distinct issue sections |
| C-01 | 2,500 (ceiling) | 8+ distinct sections (truncated) |
| D-01 | 1,946 | 8 distinct issue sections |
| D-02 | 1,492 | ~3–4 sections (stopped early) |
| D-05 | 1,433 | ~3–4 sections (stopped early) |

D variance is wide: high-token D runs reach 7–8 sections; low-token runs stop at 3–4. A and C ceiling runs had more to say beyond the 2,500 token limit.

---

## Primary Finding: Predicted Ordering Does Not Hold

**Predicted:** A > B > C > D
**Observed (by mean tokens):** C > A > B >> D
**Observed (by ceiling hits):** A=4 > C=3 > B=2 >> D=0

The strict well-count dilution gradient did not appear. C outperformed B despite having more wells. A and C are statistically indistinguishable from each other on both metrics. The only clean separation is the P_p cluster (A, B, C) vs. the P_d baseline (D).

---

## What Does Hold: P_p >> P_d

All three P_p variants substantially outperform D on both metrics:

- **Mean output gap:** ~490 tokens between D and the weakest P_p variant (B)
- **Ceiling rate:** 0/10 for D; 2–4/10 for each P_p variant
- **Section depth:** D's low-token runs routinely stopped at 3–4 sections; A's lowest run still produced 1,873 tokens

The P_p installation effect on consideration-set breadth is robust across all three well configurations tested. This is the third confirmation of A >> D across exp-10, exp-10b, and exp-12.

---

## The C Confound: Well Relevance vs. Well Count

The failure to find A > B > C is attributable to a design confound in C's Persona:

> "You are a performance engineer who tracks **timeout arithmetic**, resource contention, and latency under failure conditions."

The phrase "timeout arithmetic" directly names the class of reasoning required to find the invisible finding (cross-file TTL arithmetic). This is not a neutral third semantic cluster — it is a task-specific pointer to the finding type. C's third well adds domain-relevant signal rather than diluting the first two.

The experiment intended to hold relevance constant while varying count. It did not. C effectively has one highly focused distributed systems well, one moderately relevant security well, and one well that is directly pointed at the artifact's hidden failure mode. The result — C ≈ A > B — is consistent with well relevance dominating well count.

---

## B vs. A: A Clean(er) Comparison

B's second well (adversarial security: vulnerability hunting, trust boundaries, attack surfaces) is less task-specifically relevant than C's performance engineering well. Security brings attention to the payment/trust boundary and idempotency key absence — finding types that are relevant but not the TTL arithmetic directly.

The A vs. B gap is modest: 102-token mean difference, 2 fewer ceiling hits. This is in the right direction for the dilution hypothesis but is not large enough to be confident. With 10 runs per variant, the difference is not statistically distinguishable from variance.

---

## TTL Arithmetic Detection: All Variants

All four variants — including D — found the cross-file TTL arithmetic in every spot-checked run. This confirms that the false atomicity comment in the artifact is still functioning as a structural pointer: it directs reviewers to examine the payment/DB boundary, and once there, the PaymentClient constants are visible and the arithmetic is findable.

The exp-10b calibration failure diagnosis holds. Binary detection of TTL arithmetic is not a viable metric for this artifact — it is essentially baseline behavior under any technically-engaged Persona.

---

## Interpretation

The data does not support the well-count dilution hypothesis as originally stated: "1 well > 2 wells > 3 wells > P_d." What it does support:

1. **P_p >> P_d is robust.** Any P_p configuration — fused or split, 1–3 wells — substantially deepens the consideration set relative to P_d.

2. **Well relevance confounds well count.** C's third well was domain-specifically relevant to this artifact, making C ≈ A rather than C < A. The experiment cannot distinguish "well count doesn't matter" from "relevance offset the dilution."

3. **The dilution effect, if it exists, is subtle at low well counts.** A > B in the right direction but not by a meaningful margin at n=10. If dilution is real, it requires more runs, better-matched wells, or a wider spread (e.g., 1 well vs. 5+ wells) to detect.

---

## Design Diagnosis and exp-13

The well count hypothesis requires a cleaner experiment:

**Problem:** Wells in exp-12 varied in task relevance, not just count.

**Required control:** All wells must be equally task-relevant (or all equally task-irrelevant). To test pure dilution, additional wells should be drawn from domains that are genuinely orthogonal to the task — not domains that happen to contain vocabulary adjacent to the finding type.

**Design for exp-13 (Well Count — Controlled Relevance):**
- A: 1 well — fused distributed systems identity (same as A here)
- B: 2 wells — distributed systems + an orthogonal domain (e.g., data science / ML systems)
- C: 3 wells — distributed systems + ML systems + a third orthogonal domain (e.g., frontend/UI engineering)
- D: P_d baseline

The orthogonal wells should be technically plausible as an engineer's background but provide no conceptual overlap with distributed locking, payment timing, or timeout arithmetic. The hypothesis: if dilution is real, A > B > C > D. If relevance was the entire story in exp-12, A ≈ B ≈ C > D.
