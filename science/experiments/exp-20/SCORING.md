# exp-20 Scoring Rubric

## Primary Metric: Binary Zombie-Write Detection

Same detection criterion as exp-19 and exp-01e.

**Score 1 — Detection** requires ALL of:
1. Process-pause scenario named: the heartbeat thread cannot renew the lock because
   all threads in the holding process are simultaneously paused (GC stop-the-world,
   VM migration, OS scheduler pause, JVM/runtime safepoint)
2. Fix identified at the database write level: fencing token, optimistic lock,
   compare-and-swap, or conditional UPDATE (WHERE version = X or WHERE stock = X)

**Score 0 — Non-detection** for any output that:
- Only identifies TTL too short / heartbeat interval too long (TTL/heartbeat concern)
- Names process pause without naming the correct fix
- Names the fix without the process-pause scenario
- Finds the TOCTOU in lock release without the process-pause scenario

## Calibration

- A (P_p vocabulary): target ≥ 5/10 (lower bar than exp-19; no explicit procedure)
- C (P_d baseline): target ≤ 2/10

Note: A target is lower than exp-19 (≥ 7/10) because vocabulary-only orientation
is expected to produce lower detection than explicit procedure. If A fails to exceed
≥ 3/10, the vocabulary content may not be providing meaningful orientation and
results will be difficult to interpret.

## Key Distinction from exp-19

exp-19 variants A and B both contained explicit procedure:
- "trace the full lock lifecycle"
- "ask what happens if all threads simultaneously paused"
- "look for fencing token or optimistic lock at DB write level"

exp-20 variants A and B contain vocabulary orientation only:
- domain concepts named (Kleppmann, split-brain, zombie-write, fencing token,
  process isolation, lease expiry)
- NO procedural instruction about what to trace, ask, or look for

The question: does placement of vocabulary orientation in the Persona slot (A)
vs. the Instructions slot (B) produce different detection rates?

## Scoring Notes

Manual review required for any REVIEW-flagged items.
Do not credit vocabulary keyword matches alone — the model must demonstrate the
causal chain: process pause → heartbeat cannot renew → lock expires → write executes
on stale lock → fix is at the write layer, not the lock layer.
