# exp-07b SCORING

## Experiment Purpose

Slot-swap falsification test for the P_p/P_d distinction. Tests whether procedural distributed-systems
content drives detection regardless of prompt slot, or whether Persona identity framing is
architecturally load-bearing.

## Scenario: Process-Pause Zombie Write

The code is a well-implemented distributed inventory reservation service with a Redis lock and
heartbeat. All common implementation bugs have been addressed:

- Heartbeat state is per-lock-context (threading.Event, not instance vars)
- Lock release is atomic (Lua script, not GET + DELETE)
- Database operations are wrapped in a transaction
- Input validation is present (Pydantic, LockAcquisitionError)
- Heartbeat thread is joined before lock release

The ONLY remaining structural failure mode is the **process-pause zombie write**:

> A process holding the lock is paused (OS scheduling, GC stop-the-world) for longer than
> LOCK_TTL (30s). The heartbeat thread is also paused — it cannot renew the lock. The lock
> expires. Another process acquires the lock and completes its reservation. When the first
> process resumes, it is still inside `with self._acquire_lock(lock_key):`. The heartbeat
> detects lock loss (extend_script returns 0) but has no channel to abort the main thread.
> The main thread continues executing `update_stock` and `create_order` — a zombie write
> that races with the second process's committed write.

The fix requires one of:
- A **fencing token** (Redis lock version counter) passed through to DB operations; DB
  enforces monotonic ordering with a conditional update
- **DB-level optimistic concurrency** (version/ETag field + conditional `UPDATE ... WHERE version=N`)

## Binary Scoring Criterion

**Score = 1** if the output:
1. Identifies the process-pause or long-pause scenario as a failure mode, AND
2. Names the specific remedy: fencing token, monotonic counter, or DB-level optimistic locking

A response that finds other issues (e.g., heartbeat observability, TTL ratio, test coverage gaps)
without identifying the zombie write scores **0**.

A response that identifies "lock can expire during operation" without naming the fencing token
or optimistic locking fix scores **0** — identifying the mechanism is required, not just the symptom.

## Result Interpretation

| Outcome | Interpretation |
|---------|----------------|
| C ≈ I (both high) | Few-shot confound is real: procedural content drives detection regardless of slot. Persona slot is not architecturally special — content density is the load-bearing variable. |
| C ≈ J (both low), I high | Persona identity framing is load-bearing. Same content in Instructions does not install the search algorithm. Framework claim strengthened. |
| C partial (between I and J) | Both mechanisms contribute. Persona slot amplifies procedural content; content in Instructions provides partial signal. Framework needs refinement. |

## Variants

| ID | Persona | Instructions (domain content) | Hypothesis |
|----|---------|-------------------------------|------------|
| I  | P_p — highly sophisticated distributed systems engineer; "can't help but discover hidden mysteries" | Generic | Persona slot installs search algorithm |
| J  | P_d — senior software engineer (generic) | Generic | Baseline: neither slot has domain content |
| C  | P_d — senior software engineer (generic) | Contains same domain expertise + thoroughness directives as Variant I Persona | Instructions slot with same content |
