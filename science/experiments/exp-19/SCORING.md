# exp-19 Scoring Guide

## Research Question

Does the Persona slot carry the consideration-set effect, or does the same procedural
content produce equivalent binary detection when placed in the Instructions slot?

H1: A >> B — Persona slot is architecturally load-bearing; identical content in
Instructions slot produces lower detection.

H2: A ≈ B >> C — procedural content is the operative variable; slot is not
strongly load-bearing.

---

## Primary Metric: Zombie-Write Detection

A run **detects** the failure mode if it explicitly identifies ALL of:

1. The heartbeat thread does NOT protect against process pauses (GC stop-the-world,
   VM migration, OS scheduler freeze) — because the pause freezes all threads in
   the process simultaneously, including the heartbeat thread

2. A fencing token OR optimistic lock check at the database write level is required
   as the fix (e.g., `UPDATE ... WHERE stock = current_stock`, or a version/token
   column check)

### Score: 1 (detected)

Any of the following qualify as detection:
- Explicit statement that a stop-the-world GC pause (or equivalent) freezes the
  heartbeat alongside the main thread, allowing the lock to expire
- Statement that the write proceeds with stale data after a process pause regardless
  of the heartbeat mechanism
- Naming fencing token, optimistic lock, or version-based write as the fix

**The finding and the fix must both be present.** Naming the failure without the
fix = 0. Naming the fix without the failure = 0.

### Score: 0 (not detected)

- General concurrency concern or race condition without naming process pause scenario
- "Lock can expire" or "TTL too short" without naming simultaneous thread freeze
- Approval without flagging
- Fix suggestion (optimistic lock) without explaining why the heartbeat is insufficient
- Any finding that does not identify the process-pause / all-threads-frozen scenario

---

## Secondary Metric: Consideration-Set Breadth

Output token count as proxy for reasoning depth. Secondary signal — interpretable
even if binary detection calibration fails on one variant.

---

## Calibration Check

Before interpreting B vs. A results, verify:

- **A detection rate ≥ 7/10** — otherwise P_p Persona is insufficient; redesign before concluding
- **C detection rate ≤ 2/10** — otherwise artifact has a code-visible hint; redesign

Historical baseline from exp-01e with this same artifact:
- P_p variants (I, L): 10/10 detection
- P_d variant (J): 0/10 detection

If A calibrates at ≥ 7/10 and C at ≤ 2/10, B is interpretable as a clean slot test.

---

## Scoring Notes

**Do not credit keyword matches alone.** The exp-01e lesson: variant J appeared to
detect by keyword grep (the word "expired" appeared in a test function name) but
scored 0/10 on ground truth. Score only on explicit reasoning about process pauses
and the fix mechanism.

**Partial credit is not defined.** A run either meets all criteria or it doesn't.
