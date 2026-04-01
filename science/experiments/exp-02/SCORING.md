# Exp-02 Scoring Guide

## Track A — Contract Review (Variants A, B, C, D)

Same scoring protocol as exp-01f. The contract and trap are identical.

### The Trap

Section 8.2's carve-outs effectively nullify the Section 8.1 cap in practice. The cap
applies only to the narrow residual category of disputes that do not involve indemnification,
confidentiality, IP, gross negligence, or unpaid fees — which is nearly every meaningful
dispute in a software services engagement.

### Critical — Pass/Fail (floor)

Must:
1. Identify that Section 8.2's carve-outs functionally nullify the Section 8.1 cap
2. Name specifically which carve-outs create the problem (indemnification + IP + confidentiality together)
3. Make the nullification argument — explain that these carve-outs cover nearly all meaningful
   commercial disputes in a software services context, leaving the cap applicable only to a
   narrow residual category

Flagging "broad indemnification" or "review Section 8" without making the nullification
argument = **fails Critical**.
Approving the agreement without flagging = **fails Critical**.

### Elite — Depth Signal (bonus)

The 9.1(c) circularity: Section 9.1(c) indemnifies Client against "Vendor's breach of this
Agreement." Because 8.2(a) carves out all indemnification obligations from the cap, general
breach of contract routes through the uncapped indemnification channel. Any Vendor breach
can be characterized as triggering 9.1(c), bypassing the cap entirely.

### Distraction — Control Pattern

Issues that are legitimate but not the primary risk:
- Missing DPA / cybersecurity standards
- Late fee interest rate (1.5%/month)
- Confidentiality survival period (5 years)
- SOW structure or payment terms
- Warranty disclaimer scope

Flagging Distraction only (no Critical) = **confirmed distraction failure — score 0**.

### Track A Score Summary

| Response pattern | Score |
|-----------------|-------|
| Critical + Elite | 10/10 — full cross-clause audit |
| Critical only | Pass — correct catch, standard depth |
| Distraction only (no Critical) | 0/10 — distraction failure |
| Approval | 0/10 |
| "Review Section 8" without nullification | 0/10 — adjacent miss |

### Track A Comparisons

| Variant | vs. exp-01f | Purpose |
|---------|-------------|---------|
| B (P_p, no Stakes) | Replicates M | Baseline — establishes exp-02 detection rate before Stakes |
| D (P_d, no Stakes) | Replicates N | Baseline — establishes P_d enumeration pattern |
| A (P_p + Stakes) | New | Tests whether Stakes adds measurable depth to P_p |
| C (P_d + Stakes) | Replicates P | Tests whether Stakes amplifies P_d enumeration |

If B ≠ M (detection rate diverges), experimental setup has drifted — reconcile before
interpreting A.

---

## Track B — Factual Accuracy (Variants E, F)

### Ground Truth Answers

**Q1 — Audit Tool Accuracy**
Correct answer: approximately **33%**

Calculation: P(malicious | flagged) = (0.98 × 0.01) / [(0.98 × 0.01) + (0.02 × 0.99)]
= 0.0098 / (0.0098 + 0.0198) = 0.0098 / 0.0296 ≈ 0.331

The intuitively probable wrong answer: ~98% (matching test sensitivity).
A correct answer requires recognizing the base rate dominates at 1% prevalence.
Partial credit: any answer below 50% with a Bayesian framing, even if not numerically precise.

**Q2 — Payment Clause**
Correct answer: **May 1**

Reasoning: Delivery on March 17 (after the 15th) triggers the exception clause. Payment is
due 30 days after the first business day of the following month (April 1). 30 days after
April 1 = May 1.

The intuitively probable wrong answer: April 16 (30 days after March 17, ignoring the clause).
Also wrong: November 30 / any reading that applies the base rule.

**Q3 — Logical Validity**
Correct answer: **No**

Reasoning: The policy establishes "outside counsel review → opinion letter." Receiving an
opinion letter does not allow inference backward to "was reviewed by outside counsel." This
is affirming the consequent — a formal logical fallacy. Other paths to an opinion letter
may exist.

The intuitively probable wrong answer: Yes — the surface reading suggests a bidirectional rule.

**Q4 — Vendor Performance**
Correct answer: **Vendor B** (performing better on delivery reliability)

Reasoning: This is Simpson's Paradox. Vendor B outperforms Vendor A in both sub-categories
(90% vs. 85% for small; 30% vs. 20% for large). Vendor A's higher overall rate (80% vs. 65%)
results from its project mix skewing toward easier small projects. The per-category comparison
is the correct measure of delivery capability.

The intuitively probable wrong answer: Vendor A (higher overall rate = better performer).

**Q5 — Exclusion Clause Scope**
Correct answer: **No, the exclusion is not applicable**

Reasoning: The exclusion clause applies only to "damages arising from use of the software
outside the licensed territory." The crash occurred within the licensed territory — the
exclusion's stated condition is not met. The clause is silent on crashes within the territory;
silence is not coverage.

The intuitively probable wrong answer: Yes or "possibly" — misreading the exclusion as a
general limitation rather than a geographic scope restriction.

---

### Track B Scoring Per Run

Each run receives a score of 0–5 (one point per correct answer).

| Score | Classification |
|-------|---------------|
| 5/5 | Perfect — no confident-wrong answers |
| 4/5 | Strong |
| 3/5 | Mixed |
| 2/5 or below | Dominant error pattern |

**Confident-wrong** = wrong answer stated without uncertainty markers ("The probability is 98%").
**Hedged-wrong** = wrong answer with explicit uncertainty ("I'm not certain, but approximately 98%").
**Correct** = answer within acceptable range with valid reasoning.

Record each question separately. Compute:
- Correct rate per variant (E vs. F)
- Confident-wrong rate per variant
- Per-question breakdown (which questions drop under Stakes presence/absence)

### Track B Purpose

If E (Stakes present) outperforms F (Stakes absent) on confident-wrong suppression: Stakes
sharpens the softmax distribution even without a consideration-set requirement — it is a
general sharpening operator.

If E ≈ F: the sharpening effect only manifests when Persona's K/V filter has already
narrowed the space (requires P_p + consideration-set task). Track A would then be the
primary evidence for Stakes as amplifier.
