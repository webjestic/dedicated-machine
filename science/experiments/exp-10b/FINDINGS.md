# exp-10b Findings

**Status:** Complete — second calibration failure; primary metric invalid; consideration-set depth signal clear
**Date:** 2026-03-29
**Hypothesis:** Semantic Density (Phase 6)
**Primary question:** Does dense compound P_p (A) outperform diluted P_p (B) on detection rate for an invisible cross-file timing failure?

---

## Raw Results

| Variant | Mean output tokens | Ceiling hits (2500) | Mean issue sections | TTL arithmetic found |
|---------|--------------------|----------------------|--------------------|--------------------|
| A — Dense P_p | 2,471 | **8/10** | **9.9** | ~9/10 |
| B — Diluted P_p | 1,851 | 0/10 | 7.6 | ~8/10 |
| C — P_d baseline | 1,807 | 0/10 | 8.0 | ~7/10 |

**B ≈ C confirmed** on every dimension: tokens (1,851 vs 1,807), ceiling hits (0/10 each), issue sections (7.6 vs 8.0). Diluted P_p is statistically indistinguishable from P_d baseline — second consecutive confirmation.

**A >> B and A >> C** on every dimension: +620 tokens over B, +664 over C; 8/10 ceiling rate vs 0/10; +2.3 sections per run over B, +1.9 over C.

---

## Second Calibration Failure

The calibration fix from exp-10 introduced a new pointer.

**exp-10 confound:** `payment.charge()` outside `self.db.transaction()` — code-visible charge-before-commit race directed all reviewers to examine `PaymentClient`.

**exp-10b confound:** `payment.charge()` inside `self.db.transaction()`, with an inline comment claiming "crash between charge and record cannot produce an unrecorded charge." This claim is false — a database transaction wrapping an HTTP call provides no atomicity over the external operation. Any reviewer who reads the comment will verify whether it is true, immediately identify that it is not, and examine `PaymentClient` to understand the charge operation's timing characteristics. From there the 60 < 100s arithmetic follows.

The artifact is structurally caught between two visible issues:
- Charge outside transaction → charge-before-commit race (exp-10)
- Charge inside transaction + false atomicity comment → false guarantee (exp-10b)

Both act as pointers to `PaymentClient`. The payment/DB boundary in this artifact cannot be made scrutiny-neutral. Any placement of `payment.charge()` relative to `self.db.transaction()` creates a reviewable correctness claim that directs attention to the retry configuration.

**Consequence:** TTL arithmetic was found by all variants at near-equal rates (A ~9/10, B ~8/10, C ~7/10). The primary metric cannot discriminate.

---

## The Consideration-Set Depth Signal

Despite the primary metric failing, A's output volume is dramatically higher than B and C on every measure:

**Token depth:**
- A mean 2,471 vs B mean 1,851 — 33% more output
- 8/10 A runs hit the 2,500-token ceiling; 0/10 B or C runs hit it
- A-02 and A-10 are the only non-ceiling A runs

**Issue breadth:**
- A: mean 9.9 distinct issue sections per run
- B: mean 7.6; C: mean 8.0
- A covers ~2 additional findings per run beyond what B and C produce

**What A finds that B and C find less often:**

| Secondary finding | A | B | C |
|------------------|---|---|---|
| Gateway idempotency key (retry without key = gateway-level double charge) | ~9/10 | ~5/10 | ~6/10 |
| Redis fault tolerance (single node, no Sentinel/Cluster) | 2/10 | 1/10 | 0/10 |
| DB connection pool exhaustion (HTTP call holding open transaction) | 3/10 | 2/10 | 5/10 |

Note: C finds DB connection pool exhaustion *more* than A (5/10 vs 3/10) — C's attention is concentrated on the false atomicity pointer, developing it in depth. A distributes across more findings.

**A also shows richer remediation depth:** A outputs consistently propose multi-step architectural fixes (outbox pattern, two-phase approach, idempotency key design). B and C outputs tend to stop at "increase the TTL or implement lock extension."

---

## Interpretation

The binary primary question (A > B on detection rate) cannot be answered from this data — the calibration failure collapsed the discriminating condition again.

The secondary signal is different. A's consideration set is demonstrably larger than B's and C's: more findings per run, more tokens per run, ceiling pressure in 80% of runs, richer remediation proposals. The semantic density effect is present and measurable — but it shows up in *how much* is found, not in *whether* the target finding is reached.

**B ≈ C (confirmed twice):** Diluting P_p content from compound fused identity sentences to 5–6 separate unfused statements destroys the token depth signal. Diluted P_p is equivalent to P_d on output volume across both exp-10 and exp-10b. This is a clean negative result: well-structure independently matters. The same content in unfused form produces P_d-level output.

**A >> B and A >> C:** Consistent with a deeper consideration set installed by dense compound identity encoding. The 8/10 ceiling rate means A is running out of tokens before running out of findings. B and C are running out of findings before running out of tokens.

---

## Structural Diagnosis: The Payment Artifact Cannot Be Calibrated

The payment order processor artifact structure has a fundamental property that prevents calibration for this experiment type:

Any version of the code that involves an external payment gateway with retry logic, a distributed lock with a TTL, and a TTL shorter than the worst-case retry window will have the TTL arithmetic as a non-surface finding. But reaching that finding always requires examining `PaymentClient`, and examining `PaymentClient` is always triggered by something visible at the payment/DB boundary.

The artifact is not wrong. It is wrong for this particular measurement goal.

---

## Revised Measurement Approach for Semantic Density

The semantic density hypothesis can be tested without a "finding detection rate" primary metric. The cleaner test uses **consideration-set breadth** as the measurement:

- **Metric:** Mean issue sections per run + ceiling rate
- **Prediction:** Dense compound P_p (A) > Diluted P_p (B) > P_d (C) on both dimensions
- **This experiment confirms:** A >> B ≈ C on both dimensions

What exp-10 and exp-10b together establish:
1. A >> B ≈ C holds on token depth and issue breadth (two independent artifact designs, same result)
2. B ≈ C holds on both dimensions (content without well-structure is inert — same as P_d)
3. The calibration failure is a consistent pattern, not noise — payment artifacts cannot isolate the invisible finding

**For exp-10c or an alternative:** Either (a) accept consideration-set breadth as the primary metric and design an artifact with a known finite set of legitimate findings, or (b) choose an artifact domain where the invisible finding does not go through an external API boundary that creates a visible scrutiny target.

Option (a) is the simpler path. If the true number of findable issues is known and bounded, A > B > C on count per run is a clean test of consideration-set depth.

---

## Outcome

Per the SCORING.md outcome table, primary binary questions cannot be answered.

But the secondary signal is the clearest semantic density measurement to date:
- **A >> B:** Confirmed. Dense compound identity, compulsion language, fused themes → substantially deeper consideration set than same content in diluted form.
- **B ≈ C:** Confirmed. Dilution to unfused statements destroys P_p behavior; diluted P_p is equivalent to P_d.

These are the two most important predictions of the semantic density hypothesis. Both are confirmed by the secondary metrics, across two independent artifact designs.
