# exp-10b SCORING

## Experiment Purpose

Phase 6 — Semantic Density hypothesis first clean test.

Tests whether the *structure* of a P_p Persona — specifically, whether domain concepts are fused
into compound identity sentences (dense gravity well) or listed as separate statements (diluted
wells) — independently affects consideration-set depth, holding semantic content constant.

**Hypothesis:** A dense compound P_p identity (fused themes, compulsion language) installs a
deeper consideration set than an identical P_p whose concepts are distributed across separate,
unfused statements. Content is held constant. Structure is the variable.

**Calibration fix from exp-10:** `payment.charge()` moved inside `self.db.transaction()`,
eliminating the charge-before-commit race that acted as a structural pointer to `PaymentClient`.
The only non-surface finding path is now the cross-file timing arithmetic.

## Artifact

Payment order processor (`services/order_processor.py` + `services/payment_client.py`).
See `ARTIFACT.md`.

**The failure:** `ORDER_LOCK_TTL = 60` (order_processor.py) vs. worst-case `payment.charge()`
duration of 100 seconds (`MAX_RETRIES=3 × REQUEST_TIMEOUT=30 + RETRY_BACKOFF=5 × 2`, defined
in payment_client.py). The lock expires before the payment completes under adverse conditions.

**Why it's invisible:** Every component is individually correct. The lock pattern, idempotency
check, token-verified release, and transactional write (including the charge) are all sound.
The failure is purely in the cross-file arithmetic `60 < 100` and its consequence: Worker A's
lock expires mid-payment, Worker B acquires the lock and passes the idempotency check, both
workers charge the customer.

**Discovery requires:** Reading both files, computing worst-case `charge()` duration, and tracing
the consequence through the distributed timeline. No dead-end branch. No visible pointer.

## Variants

| ID | Persona | Hypothesis |
|----|---------|------------|
| A | Dense P_p — fused compound identity, compulsion language | Baseline: dense well installs full consideration set |
| B | Diluted P_p — same concepts, 5–6 separate unfused statements, no compulsion language | Test: does dilution reduce consideration-set depth? |
| C | P_d — senior software engineer baseline | Lower bound |

## Scoring Criterion

### Score = 1.0 (full architectural finding)
Output:
1. Names the cross-file timing arithmetic explicitly — `ORDER_LOCK_TTL` vs. worst-case
   `payment.charge()` duration — or names the specific adverse scenario (3 payment timeouts
   exhaust the lock window), AND
2. Names the consequence: lock expires mid-payment → second worker passes idempotency check →
   duplicate charge, AND
3. Names the architectural fix: lock heartbeat/renewal during payment, pessimistic locking
   (remove TTL, release only on completion), or DB-layer unique constraint on charge record
   that causes the second writer to fail.

### Score = 0.5 (mechanism found, incomplete)
Output identifies that the lock has no renewal mechanism and could expire during a slow payment,
without computing the specific timing arithmetic or without naming the duplicate-charge consequence
explicitly.

### Score = 0.25 (concern raised, no mechanism)
Output notes the missing renewal/heartbeat as a best-practice concern without connecting it to
the duplicate charge scenario.

### Score = 0 (surface only)
Output validates the lock pattern, approves, or finds only surface issues (input validation,
error handling, long-running transaction concern, test coverage gaps).

**Note on long-running transaction:** A reviewer may flag that `payment.charge()` is called
inside `db.transaction()`, holding an open DB connection during an external HTTP call. This is
a legitimate performance/resource concern but scores 0 — it is a surface observation that does
not require cross-file reasoning and does not reveal the timing race.

## Binary Questions

**Primary:** Does A > B on detection rate?
- A > B: Semantic density is a real variable — well structure affects consideration-set depth
  independently of content
- A ~ B: Content is what matters; well structure is irrelevant to the consideration set

**Secondary:** Does B > C?
- B > C: Diluted P_p retains some consideration-set behavior even without fusion and compulsion
  language — partial well structure still outperforms P_d
- B ~ C: Dilution fully destroys P_p behavior; equivalent to P_d

## Outcome Interpretation

| A vs B | B vs C | Interpretation |
|--------|--------|----------------|
| A > B | B > C | Semantic density is continuous — well structure is a real variable; dilution degrades but does not eliminate P_p behavior |
| A > B | B ~ C | Semantic density is binary — fusion + compulsion language is required; without it, P_p content is inert |
| A ~ B | B > C | Content + domain keywords install consideration set regardless of structure; P_p > P_d is content-driven |
| A ~ B | B ~ C | Neither A nor B outperforms P_d — artifact or Persona calibration failure |
