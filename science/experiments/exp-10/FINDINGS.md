# exp-10 Findings

**Status:** Complete — calibration failure; primary metric invalid
**Date:** 2026-03-28
**Hypothesis:** Semantic Density (Phase 6 first test)
**Primary question:** Does dense compound P_p (A) outperform diluted P_p (B) on detection rate for an invisible cross-file timing failure?

---

## Raw Results

| Variant | Persona type | TTL arithmetic found | Gateway idempotency key | Lua sentinel (result=0) | Mean output (words) |
|---------|-------------|----------------------|------------------------|------------------------|---------------------|
| A | Dense P_p (fused compound, compulsion language) | ~8/10 | 9/10 | 4/10 | ~1,214 |
| B | Diluted P_p (same content, 5–6 unfused statements, no compulsion) | ~7/10 | 5/10 | 3/10 | ~1,010 |
| C | P_d baseline (senior software engineer) | ~8/10 | 6/10 | 0/10 | ~1,038 |

**"TTL arithmetic found"** = output explicitly computes worst-case `payment.charge()` duration (3×30 + 2×5 = 100s) and names the 60 < 100 timing gap.

---

## Primary Metric: Invalid Due to Calibration Failure

The target metric for this experiment was whether A > B on detection of the cross-file timing gap (`ORDER_LOCK_TTL = 60` < worst-case `payment.charge()` of 100s). Detection rates across all three variants were approximately equal — the experiment cannot answer the semantic density question.

**The confound:** The artifact contained an unintended second bug — `payment.charge()` was called outside `self.db.transaction()`. This charge-before-commit race is code-visible (readable in `order_processor.py` without cross-file reasoning) and creates an obvious pointer: any reviewer who correctly flags it as critical will naturally examine `payment_client.py` to understand the charge operation. That examination exposes `REQUEST_TIMEOUT = 30`, `MAX_RETRIES = 3`, `RETRY_BACKOFF = 5` — and from those three constants, the 60 < 100 arithmetic follows immediately.

The intended difficulty was: *cross-file arithmetic with no structural pointer*. The charge-before-commit bug provided the pointer. The invisible failure became visible-by-domino.

**Consequence:** All three variants found the TTL issue at near-equal rates. The consideration-set difference between dense P_p (A) and diluted P_p (B) cannot be measured when the artifact provides a guided path to the finding.

This is the same class of calibration error as the `if result == 0: return` branch in exp-07 through exp-09 — a code-visible feature that guided the model to the target finding independent of Persona.

---

## Secondary Findings: A > B > C on Depth

While the primary metric failed, secondary issue detection shows a consistent A > B ≈ C pattern that mirrors prior P_p vs P_d results:

**Gateway idempotency key** (payment retries without a stable key to the gateway can cause double-charges at the gateway layer, independent of the lock):
- A: 9/10
- B: 5/10
- C: 6/10

**Lua sentinel treated as error** (if `_release_script` returns 0, it means the token didn't match — indicating TTL expiry stole the lock mid-critical-section; this should be logged as an error, not silently ignored):
- A: 4/10
- B: 3/10
- C: 0/10

The Lua sentinel finding is the subtlest in the artifact — it requires reading the Lua release script, understanding that `return 0` means no-match, and connecting that to the TTL-expiry scenario. C found it 0/10. A found it 4/10. This is the consideration-set depth signal, visible in secondary findings even though the target metric was swamped.

A's outputs also show broader remediation depth: two-phase payment flows (PENDING → COMPLETE), outbox patterns, saga references. B and C outputs generally stop at "increase the TTL."

---

## Interpretation

The token depth difference (A outputs average ~20% longer than B and C) is accounted for by secondary issue identification — A runs consistently find more issues and develop richer remediation proposals. This is consistent with a deeper consideration set. But because the primary target finding was found by all variants, the semantic density hypothesis cannot be confirmed or falsified from this data.

The experiment does not rule out semantic density as a variable. It rules out this artifact as a discriminating test.

---

## Outcome Cell

Per SCORING.md outcome table:

> **A ~ B | B ~ C → "Neither A nor B outperforms P_d — artifact calibration failure or consideration set not activated for this scenario"**

Verdict: **Artifact calibration failure**. The secondary finding pattern (A > B > C on gateway idempotency key, Lua sentinel) suggests the consideration set was activated — A is finding more than B and C — but the primary metric was neutralized by the visible pointer.

---

## Artifact Redesign Required: exp-10b

To test the semantic density hypothesis cleanly, the artifact must have **one finding path** — the cross-file timing arithmetic — with no visible structural pointer to `payment_client.py`.

**Required fix:** Move `payment.charge()` inside `self.db.transaction()`, or otherwise eliminate the charge-before-commit bug so no single file contains a reviewable flaw that motivates looking at `PaymentClient`. The TTL arithmetic should be the only non-surface finding available.

**Keep everything else:** The `ORDER_LOCK_TTL = 60` vs 100s worst case is a well-calibrated invisible failure. The `services/payment_client.py` cross-file structure is correct. Only the charge-before-commit bug needs to be fixed.

**Variants:** Same A / B / C structure. Same scoring rubric.

---

## Notes for Phase 6 Synthesis

This is the first exp-10 run (call it exp-10a). The calibration failure is informative:
- It confirms the domino-pointer pattern that contaminated exp-07 through exp-09 is not limited to single-file artifacts
- It demonstrates that even a cross-file invisible failure becomes visible if another bug acts as a structural pointer
- The secondary findings (A > B > C on Lua sentinel) are the cleanest glimpse at semantic density's real signal so far

The hypothesis remains unvalidated. exp-10b is the correct next step.
