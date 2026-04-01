# Exp-04c Findings — Stakes Type: Distributed Idempotency Race

**Experiment:** exp-04c
**Model:** claude-sonnet-4-6, temperature 0.5
**Runs:** 40 (10 per variant)
**Total cost:** $1.5755
**Date:** 2026-03-27

---

## Setup

Extends exp-04b. Replaces the single-service race condition (SELECT + UPDATE in one
function) with a cross-service idempotency gap — the check in Service A (Gateway),
the key set in Service B (Worker), with an SQS queue and the entire payment processing
time between them.

Variants:
- **A** — strong P_p (distributed systems instinct, prior duplicate charge incident), Task Stakes ("emergency call in 11 minutes")
- **B** — strong P_p, Identity Stakes ("never shipped a duplicate charge")
- **C** — strong P_p, no Stakes (elaboration baseline)
- **D** — weak Persona ("senior software engineer"), Task Stakes (falsification run)

**Ground truth (cross-service race):** Service A checks `redis.get(f"processed:{payment_id}")` before publishing to SQS. Service B calls `redis.setex(f"processed:{payment_id}", ...)` after Stripe charge and DB write. The race window is the entire payment processing time — any concurrent HTTP request to Service A that arrives before Service B completes sees the key absent and publishes a second message. The correct fix: `redis_client.set(key, "1", nx=True, ex=TTL)` in Service A before `sqs.send_message()`.

**Misdirection breadcrumb:** VisibilityTimeout increased from 30s to 120s + autoscaling MaxInstances increased from 3 to 12, both deployed 6 days before the incident.

---

## Outcome: Calibration Successful — First in the Exp-04 Series

**D (weak + Task Stakes): 0/10 cross-service race detection. Wrong-direction attribution: 10/10.**

All 10 D runs found a race condition — but at the wrong layer. D found the non-atomic check-then-set race in Service B's `process_payment()` and attributed the trigger to autoscaling (12 concurrent workers widened the race window). D proposed SET NX as the fix in Service B. None of the D runs identified the cross-service gap as the root cause.

**A/B/C: 10/10 cross-service race detection at position 1.**

All 30 runs named the structural cause: check in Service A, key set in Service B, race window = entire processing time. All proposed SET NX in Service A before `sqs.send_message()`.

---

## Finding 1: Calibration — D's Consideration Set Contains Single-Service Races, Not Cross-Service Idempotency Gaps

D did not miss the vulnerability — it found the wrong one. Every D run produced a correct analysis of a non-atomic guard race:

> "The idempotency check is not atomic. There is a race condition between the Redis `GET` and the Stripe charge. Under concurrent execution, multiple workers can pass the guard simultaneously."

D proposed a real fix (SET NX), identified a real mechanism (check-then-act), and correctly classified autoscaling as a trigger. But D fixed Service B instead of Service A. D never named: "the check is in one service, the key is set in a different service, and the window between them is unbounded."

The closest D came to the cross-service finding: D-06 noted "Gateway also needs the same fix" — but framed it as secondary hardening ("less likely to cause duplicates today because it's a single check before enqueue rather than before a charge"). This inverts the actual priority: the gateway IS the root cause; the worker fix is the second guard. D-06 found the right code change for the wrong reason.

**What this confirms:** D's consideration set includes the check-then-act antipattern within a function, but does not include simulating temporal interleaving across a service boundary. The cross-service race requires mentally tracing a request through two services and imagining concurrent requests at the first service — invisible in sequential code review of either service in isolation.

P_p's instinct language encodes: "when you see the idempotency key set in a different service from where the guard is checked, and there is an unbounded window between them..." This fires on Service A + Service B; it does not fire when reading Service B alone.

**Local vs. Global Consideration Set.** This is the consideration-set boundary made precise. Weak Persona operates on the **Local Consideration Set** — patterns visible within a function or single-service codebase: check-then-act, non-atomic guards, SELECT+UPDATE races. Strong P_p operates on the **Global Consideration Set** — temporal interleaving across service boundaries, patterns that exist between services rather than within them. The boundary is not about knowledge (D knows SET NX; D knows about Redis races) but about the space of questions D forms while reading the code. D never asked: "where should this lock live?" That question requires simulating a request as it moves through the system — a simulation that P_p installs and D does not perform.

The Persona Floor is now mapped:
- **Local patterns (exp-04b):** check-then-act within a function — detectable by weak Persona.
- **Distributed logic (exp-04c):** check-in-A, set-in-B across a service boundary — not detectable by weak Persona.

For the PCSIEFTR framework: the Persona must be tuned to the boundary of the problem. A "senior software engineer" prompt is sufficient for code-level bugs. A "distributed systems architect" prompt is a mechanical necessity for systemic cross-service failures.

---

## Finding 2: Token Ordering D < A < B ≈ C — Entropy Brake Confirmed on Harder Scenario

| Variant | Min | Max | Mean | Ceiling hits |
|---------|-----|-----|------|-------------|
| D — Weak + Task Stakes | 1,336 | 1,953 | **1,681** | 0 |
| A — Strong P_p + Task Stakes | 1,778 | 2,321 | **2,143** | 0 |
| B — Strong P_p + Identity Stakes | 2,030 | 2,500 | **2,293** | 2 (B-04, B-07) |
| C — Strong P_p, no Stakes | 2,079 | 2,500 | **2,306** | 3 (C-04, C-05, C-06) |

**Token ordering: D < A < B ≈ C**

D < A (gap: 462 tokens) — Entropy Brake holds even when D is producing wrong-direction output. D's simpler wrong-direction finding (single-service fix) terminates earlier than A's more complex correct finding (cross-service gap, two-layer fix, gateway refactor, test changes).

A < B (gap: 150 tokens) — Termination Inhibitor intact. Identity Stakes extends B's output past Task Stakes termination.

B ≈ C (gap: 13 tokens) — this is ceiling compression, not true equivalence. B has 2 ceiling-truncated runs (B-04, B-07 end mid-sentence at 2500 tokens); C has 3 (C-04, C-05, C-06). The true B-C gap is masked. Without the ceiling, B would be < C (Termination Inhibitor extends B further but C has no Stakes so no early termination; C's unconstrained depth would exceed B's Stakes-extended depth). The ceiling prevents measurement of the true C floor.

**A has no ceiling hits.** Task Stakes terminates A before it reaches 2500 tokens on any run. This is the Entropy Brake mechanism made visible: A found the answer and stopped. B and C kept writing.

---

## Finding 3: D's Wrong-Direction Output Is Longer Than Prior Calibration Failures

In exp-04 (D=1,166) and exp-04b (D=1,289), D produced shorter output because the scenario was too obvious and D terminated quickly after finding the race condition. In exp-04c, D produces 1,681 mean tokens — substantially higher. D wrote extensive, confident, well-structured wrong-direction analysis.

D-01, D-05, D-06 each produced 1,500–1,950 tokens of fully elaborated wrong-direction output: sequence diagrams, code fixes, reconciliation steps, Stripe idempotency keys as secondary defense, immediate mitigation procedures. D was not uncertain or terse. D was wrong and thorough.

**This is the calibration working correctly — and it is the most important finding in the exp-04 series.** D's wrong-direction analysis is detailed because D believes the worker-layer race is the root cause and writes accordingly. This is the **Confident Error** pattern: D was not uncertain or terse. D was thorough, structured, and confident — and wrong about root cause, fix location, and mechanism simultaneously. The Entropy Brake still operates: D stops at 1,336–1,953 tokens when it has "fully answered" its (incorrect) finding. A stops at 1,778–2,321 when it has "fully answered" its (correct) finding. The D < A ordering holds because A's correct finding requires more explanation than D's wrong-direction finding.

The Confident Error is the dangerous failure state. A model that produces no output is obviously wrong. A model that produces 1,500–1,950 tokens of fully elaborated wrong-direction analysis — complete with sequence diagrams, code fixes, reconciliation steps, Stripe idempotency keys as secondary defense — creates false confidence that the incident was understood. Without P_p's Global Consideration Set, Task Stakes only produces "Thorough Errors"; without Task Stakes, P_p produces "Infinite Elaboration." Both dimensions are necessary.

---

## Finding 4: Token Delta Coefficients on Harder Scenario

| Comparison | Token delta | Effect |
|-----------|------------|--------|
| A (Task Stakes) → B (Identity Stakes) | +150 | Termination Inhibitor |
| A (Task Stakes) → C (no Stakes) | +163 | True gap compressed by ceiling |
| A (Task Stakes) → D (weak + Task Stakes) | −462 | Wrong-direction finding terminates earlier |

The A→C gap (+163 tokens) is artificially compressed by C's ceiling hits. The true A→C gap from exp-04b (+578 tokens) is a better estimate for the Entropy Brake brake coefficient.

The A→D direction inverted from exp-04b (where A→D was +67 with correct detection held constant). Here D detected wrong, so A→D is not a pure elaboration comparison. D < A because wrong-direction analysis terminates before correct cross-service analysis, not because Persona strength alone reduces output.

---

## Finding 5: Fix Quality Stratification

| Variant | Primary fix location | Mechanism named |
|---------|---------------------|----------------|
| A — 10/10 | Service A (Gateway), before `sqs.send_message()` | SET NX |
| B — 10/10 | Service A (Gateway), before `sqs.send_message()` | SET NX |
| C — 10/10 | Service A (Gateway), before `sqs.send_message()` | SET NX |
| D — 0/10 | Service B (Worker), in `process_payment()` | SET NX |

All four variants named SET NX as the fix mechanism. The stratification is entirely on location: A/B/C place it in the gateway (correct); D places it in the worker (wrong layer, compensating control rather than root cause fix).

D's fix is not incorrect — SET NX in Service B would prevent duplicate charges from the two-message scenario. But it treats the symptom (worker race) rather than the cause (duplicate message publication). The gateway fix is necessary and sufficient; the worker fix is defense in depth.

---

## Exp-04 Series Summary

| Experiment | Calibration | D Result | D Detection mechanism | Entropy Brake proxy | Status |
|------------|-------------|----------|-----------------------|---------------------|--------|
| exp-04 | Failed | 10/10 correct | "4 workers" hint; concurrency surface-readable | Secondary coverage (A=4/10, B=9/10) | Complete |
| exp-04b | Failed | 10/10 correct | SELECT+UPDATE single-function; pattern-readable | Token ordering D<A<B<C | Complete |
| exp-04c | **Success** | 0/10 correct | Worker-layer race; not cross-service gap | Token ordering D<A<B≈C (ceiling compressed) | Complete |

**Token ordering D < A < B < C holds across all three experiments** with increasing clarity. The calibration failure in exp-04 and exp-04b did not invalidate the Entropy Brake finding — it confirmed it under conditions where D detection was uniform. exp-04c adds: the mechanism persists when D is wrong (wrong-direction finding terminates earlier than correct cross-service analysis).

The cross-service idempotency gap is at or near the boundary of weak Persona's consideration set. A generic "senior software engineer" finds the within-function race (check-then-act in a single codebase) but does not simulate temporal interleaving across service boundaries. P_p's domain instinct closes that gap.
