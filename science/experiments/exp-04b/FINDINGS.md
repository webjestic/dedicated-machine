# exp-04b: FINDINGS
**Experiment:** Stakes Type Clean Room — race condition; ORM/pool upgrade as misdirection breadcrumb
**Model:** claude-sonnet-4-6
**Date:** 2026-03-27
**Status:** Complete — calibration failure; Entropy Brake token pattern confirmed
**Total cost:** $1.3333 (40 runs + resumed C and D variants after API overload)

---

## Decision: Third Calibration Failure — Race Condition Still Above Weak Persona's Detection Floor

---

## Setup

**Purpose:** Replicate the Entropy Brake / stop signal result from exp-04 on a harder
scenario — one where weak Persona (D) follows the misdirection breadcrumb rather than
detecting the race condition. "Clean Room": the scenario buries the race condition under
a stated maintenance event (ORM + pool upgrade), with the upgrade presented as the
plausible cause of the IntegrityError symptom.

**Vulnerability:** Race condition in `acquire_task()` — non-atomic SELECT + UPDATE under
concurrent workers. The IntegrityError (`UNIQUE constraint failed: task_results.task_id`)
is the symptom; the cause is that two workers can claim the same task between the SELECT
and UPDATE. The ORM upgrade (2.8.4 → 3.2.1) and db-pool migration are triggers (they
introduced real concurrency where per-worker connections previously serialized access),
not causes.

**Planted breadcrumb:** Migration from per-worker connections to shared connection pool
(db-pool 2.1) + ORM version bump. Stated as maintenance context four days before the
incident. A weak Persona following scenario context was expected to attribute the error
to transaction isolation differences, connection pool behavior, or ORM version
incompatibility — all plausible, all wrong.

**Variants:**

| Variant | Persona | Stakes | Runs |
|---------|---------|--------|------|
| A | Strong P_p (race condition trauma) | Task Stakes ("18 minutes down; sync call in 9") | 10 |
| B | Strong P_p | Identity Stakes ("never misidentified root cause") | 10 |
| C | Strong P_p | None | 10 |
| D | Weak ("senior software engineer") | Task Stakes (same as A) | 10 |

---

## Results

### Detection and Convergence

| Variant | Detection (Race) | ORM/Pool attribution | Convergence position | Confidence |
|---------|-----------------|----------------------|---------------------|------------|
| A — Strong P_p + Task Stakes | **10/10** | 0/10 | **1.0 (all position 1)** | Definitive 10/10 |
| B — Strong P_p + Identity Stakes | **10/10** | 0/10 | **1.0** | Definitive 10/10 |
| C — Strong P_p, no Stakes | **10/10** | 0/10 | **1.0** | Definitive 10/10 |
| D — Weak + Task Stakes | **10/10** | 0/10 | **1.0** | Definitive 10/10 |

All 40 runs identified the race condition in `acquire_task()` as the root cause at
position 1. No run attributed the IntegrityError to the ORM upgrade or pool migration.
Falsification target D: failed — correct detection 10/10 despite weak Persona.

### Output Token Distribution

| Variant | Min | Max | Mean | Ordering |
|---------|-----|-----|------|---------|
| A — Strong P_p + Task Stakes | 1,108 | 1,646 | **1,356** | Shortest strong-Persona variant |
| B — Strong P_p + Identity Stakes | 1,187 | 1,884 | **1,592** | Moderate |
| C — Strong P_p, no Stakes | 1,650 | 2,327 | **1,934** | Longest |
| D — Weak + Task Stakes | 968 | 1,532 | **1,289** | Shortest overall |

**Length ordering: D < A < B < C**

This is the cleanest token separation in the series. No bimodal distribution, no
ceiling hits. All four variants separated by Stakes type in the expected direction.

### Secondary Coverage (O(n²) explicitly named)

| Variant | O(n²) named |
|---------|------------|
| A — Task Stakes | 10/10 |
| B — Identity Stakes | 10/10 |
| C — No Stakes | 8/10 |
| D — Weak + Task Stakes | 9/10 |

Secondary coverage is near-uniform across all variants — less differentiated than
exp-04 (where A=4/10, B=9/10, C=7/10, D=1/10). Token length is the clean proxy
here, not secondary coverage rate.

---

## Findings

### Finding 1: Calibration Failure — Race Condition Detectable by Weak Persona

D (weak + Task Stakes) correctly identified the race condition on all 10 runs with
definitive framing. The ORM/pool breadcrumb had zero effect. All D runs correctly
classified the pool migration as trigger (not cause):

D-01: *"With per-worker SQLite connections (the old setup), each worker had its own
connection and SQLite's file-level locking made this collision unlikely in practice.
The migration to a shared connection pool removed that accidental serialization."*

D-05: *"The previous setup used per-worker SQLite connections. SQLite's file-level
locking and the fact that each worker had its own connection effectively serialized
access — not by design, but by accident. The migration to a shared connection pool
removed that accidental serialization."*

Both explicitly name the breadcrumb as trigger and pivot to the race condition as
cause — the correct analysis, performed by the weak Persona variant that was supposed
to follow the breadcrumb. The SELECT + UPDATE pattern with the concurrency context
is still above weak Persona's detection floor.

The root cause of the third calibration failure: the race condition pattern is
recognizable from surface-level code structure (two separate DB operations in a
function that claims a row), not from deep concurrency expertise. A generic "senior
software engineer" recognizes the check-then-act antipattern by inspection.

**What a valid calibration scenario requires:** Either (a) a race condition whose
mechanism cannot be read directly from the code structure — one that requires
simulating temporal interleaving that is invisible in a sequential read, or (b) a
non-race-condition root cause that a strong P_p Persona recognizes via domain knowledge
while a weak Persona misses it (reversing the attribution direction).

### Finding 2: Token Ordering D < A < B < C — Entropy Brake Confirmed More Cleanly

The exp-04 token ordering (A≈1,233, B≈1,365, C≈1,629, D≈1,166) is replicated and
sharpened in exp-04b (D=1,289, A=1,356, B=1,592, C=1,934):

- Task Stakes variants (A, D) are shorter than no-Stakes (C) — Entropy Brake / stop
  signal applies regardless of Persona strength when the primary finding is reached.
- Identity Stakes (B) is intermediate — Termination Inhibitor extends output beyond
  Task Stakes but below unconstrained C.
- The gap between B and C (~342 tokens) and between A and B (~236 tokens) is consistent
  with exp-04's gaps and confirms the same mechanism.

**The Entropy Brake result is more consistent in exp-04b.** In exp-04 the secondary
coverage rates provided the clearest signal (A=4/10 vs. B=9/10). In exp-04b, secondary
coverage rates converged (near-uniform O(n²) mention across all variants) and output
length is the clean proxy. Both experiments confirm the same underlying claim: Task
Stakes reinforces P_p's termination condition; Identity Stakes suppresses it.

### Finding 3: Token Delta Coefficients — Stakes Type Dominates Persona Strength 3–4× on Elaboration

D (weak + Task Stakes, mean 1,289) is shorter than A (strong P_p + Task Stakes, mean
1,356) by ~67 tokens. Both are substantially shorter than B and C. The measured deltas:

| Comparison | Token delta | Effect |
|-----------|------------|--------|
| A (Task Stakes) → B (Identity Stakes) | +236 | Termination Inhibitor replacing Entropy Brake |
| A (Task Stakes) → C (no Stakes) | +578 | Full elaboration depth without stop signal |
| A (Task Stakes) → D (weak + Task Stakes) | +67 | Persona-strength effect, elaboration dimension |

**Stakes type effect (A→B, +236 tokens) is 3–4× the Persona-strength effect (A→D, +67
tokens)** when detection is held constant. On the elaboration dimension alone, Stakes type
is the dominant variable. Persona strength's contribution to output length is small when
both variants have already found the correct answer.

These token deltas are concrete coefficients for the two-vector formula. $\beta_{brake}$
(Entropy Brake: suppresses ~578 tokens of output vs. no Stakes) and the gap between
$\alpha_{amp}$ (Termination Inhibitor: adds ~236 tokens over Task Stakes) are now
empirically grounded across two runs with consistent direction.

**Caveat:** When Persona determines *whether* the correct finding is reached (not just
*how it is elaborated*), the Persona-strength gap is absolute — zero vs. ten detections
cannot be expressed as a token delta. The ~67-token difference applies only to the
elaboration dimension where detection is already held at 10/10. The calibration failure
means we are measuring only that dimension here.

### Finding 4: A-01 "Trigger vs. Cause" Judgment — P_p Processes and Dismisses the Breadcrumb

A-01 produced the same kind of triage judgment observed in exp-04 A-01:

*"The migration four days ago is the trigger, not the cause. Moving to a shared
connection pool meant multiple workers are now hitting the same database with real
concurrency. The race was always latent. The pool made it reachable."*

This is not a miss. P_p encountered the ORM/pool breadcrumb, evaluated it, classified
it as a trigger rather than a cause, and stated the classification explicitly. The
judgment is active — "processes and dismisses" rather than overlooks. This is the
Not-Now pattern from exp-04 A-01, reproduced on a different scenario.

The Task Stakes frame (sync call in 9 minutes) appears to push toward explicit
classification of what is *not* the root cause — preventing false-positive escalation
rather than simply suppressing the wrong-direction candidate. This is a more
sophisticated output type than enumeration: a triage decision that names the rejected
candidate and explains the rejection before moving to the correct finding.

---

## Design Notes for Exp-04c

The two calibration failures have a common root cause: the check-then-act antipattern
is commodity knowledge — "LeetCode-level" pattern recognition that any model in the
"senior software engineer" tier recognizes by surface inspection. The SELECT + UPDATE
in a single function is not above weak Persona's detection floor.

**The requirement for exp-04c:** A race condition whose mechanism is invisible in a
sequential read of any individual component. The non-atomicity must exist between
services — only visible when you mentally simulate concurrent execution across a
service boundary, not when you read a single file.

**Scenario: Distributed idempotency race ("Asynchronous Echo")**

Two services share responsibility for a check-then-act that neither performs atomically:

1. **Service A (Gatekeeper):** Checks a Redis key (`processed:{transaction_id}`) before
   publishing to the message queue. If the key is absent, publishes the message.
2. **Service B (Worker):** Consumes the message, processes the payment, then sets the
   Redis key in Service A's cache.

**The race:** If Service A is hit twice for the same transaction ID in rapid succession,
both requests may see the cache key absent — Service B hasn't written it yet — and both
publish. Two workers process the same payment. Downstream: duplicate INSERT, constraint
failure, or duplicate charge.

**The misdirection breadcrumb:** The incident happened after a Queue Visibility Timeout
increase (from 30s to 120s) and autoscaling group max increase on Service B. A weak
Persona follows the breadcrumb — longer visibility timeout means messages stay invisible
longer; autoscaling means more worker instances; plausible attribution to queue
configuration, not to the distributed state race.

**Why weak Persona misses:** No single service has a visible SELECT + UPDATE. Service A
looks clean (it checks the cache). Service B looks clean (it updates the cache). The race
only exists in the temporal gap between Service A's read and Service B's write — invisible
to sequential code review of either service in isolation.

**Why P_p finds it:** A Persona with distributed systems instinct knows that distributed
state is never atomic without a lock. When the check is in one service and the update is
in another with a network round-trip between them, the idempotency gap is structural. The
correct fix: atomic idempotency via Redis `SET NX` (set-if-not-exists) in Service A, or a
distributed lock around the check-and-publish pair.

---

## Exp-04 Series Summary

| Experiment | Calibration | D Result | Entropy Brake Evidence | Status |
|------------|-------------|----------|----------------------|--------|
| exp-04 | Failed — "4 workers" hint in scenario | 10/10 detection | Secondary coverage A=4/10 vs B=9/10 vs C=7/10; token ordering A<B<C | Complete |
| exp-04b | Failed — race pattern readable by inspection | 10/10 detection | Token ordering D<A<B<C (cleaner); secondary rates converged | Complete |
| exp-04c | Not yet built | Target: 0–3/10 | Expected: token gap preserved | Pending |

Token ordering (Task Stakes < Identity Stakes < No Stakes) is confirmed across both runs
and constitutes behavioral evidence for the two-vector Stakes formula independent of the
calibration status. The mechanism is real; the scenario needs a genuine P_p-floor to
expose it.
