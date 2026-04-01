# exp-07c SCORING

## Experiment Purpose

Slot-swap falsification test for the P_p/P_d distinction. Tests whether procedural
distributed-systems content drives detection regardless of prompt slot, or whether
Persona identity framing is architecturally load-bearing.

## Calibration History

- **exp-07 (v1):** Code had instance-level heartbeat state, TOCTOU lock release, non-atomic
  DB ops. Obvious bugs overshadowed zombie write. All variants 0/10.
- **exp-07b (v2):** Code had `threading.Event.wait()` misuse (tight-loop heartbeat) and
  `ValidationError` uncaught. Obvious bugs overshadowed zombie write. All variants 0/10.
- **exp-07c (v3):** Both obvious bugs fixed. Only remaining hidden failure mode is the
  process-pause zombie write. Models have no other unambiguous implementation error to find.

## Scenario: Process-Pause Zombie Write

The code is a well-implemented distributed inventory reservation service. All known
implementation bugs have been corrected:

- Heartbeat: `stop_event` starts **cleared**; `while not stop_event.wait(timeout=N)` fires
  every N seconds and exits cleanly when stop_event is set. No tight loop.
- Lock release: Lua script (atomic). Heartbeat extension: Lua script (atomic).
- Database writes: wrapped in `self.db.transaction()`.
- Input validation: Pydantic with `ValidationError` caught and returned as `ReservationResult`.
- Backoff: exponential + jitter.

The **sole remaining structural failure mode** is the process-pause zombie write:

> After acquiring the lock, the process reads `current_stock` **outside** the DB transaction.
> If the process is then paused (OS scheduling, GC stop-the-world, VM migration) for longer
> than `LOCK_TTL` (30s), the heartbeat thread is also paused. The lock expires. Another
> process acquires the lock, reads the same stock value, completes its reservation, and
> commits. When the original process resumes, it is still inside
> `with self._acquire_lock(lock_key):`. The heartbeat detects the token mismatch (result==0)
> and exits, but it has **no channel to abort the main thread**. The main thread continues
> with a stale `current_stock` reading and writes `new_stock` — the same value the second
> process already wrote. Net result: two orders issued, stock decremented only once. Oversell.

The architectural fix requires one of:
- A **fencing token** (monotonically incrementing Redis lock version) passed through to DB
  operations; the DB rejects writes whose token is not the current maximum.
- **DB-level optimistic locking**: a `version` or `etag` field with a conditional update
  (`UPDATE inventory SET stock=?, version=version+1 WHERE item_id=? AND version=?`) that
  fails if another writer committed between the read and the write.

## Scoring Criterion

This experiment requires **two-tier scoring** to distinguish mechanism identification from
implementation patching:

### Score = 1 (P_p behavior)
The output:
1. Identifies the **process-pause / long GC pause / lock-expiry-while-paused** scenario
   as a specific failure mode — not just generic TOCTOU or concurrent access, but the
   scenario where the **lock itself expires** because the process holding it was paused, and
2. Names the architectural fix: **fencing token**, **monotonic counter**, **version field +
   conditional update**, or **optimistic concurrency control** that rejects stale writes.

### Score = 0.5 (partial — recognizes mechanism, proposes weaker fix)
The output identifies the process-pause / lock expiry scenario but proposes only `SELECT FOR
UPDATE` or "move the read inside the transaction" without noting that DB-level row locking
also breaks down under a zombie-write scenario (the DB lock is held inside an uncommitted
transaction that may eventually be committed by the zombie process).

### Score = 0 (P_d behavior)
The output finds `get_stock()` outside the transaction as a generic TOCTOU concern and
recommends `SELECT FOR UPDATE` or moving the read inside the transaction — without naming
the lock-expiry / process-pause mechanism. Correct fix proposed, wrong reason given.

## Expected Outcome Under PCSIEFTR

If the Persona slot is architecturally load-bearing:
- I: score 1 (P_p finds zombie write mechanism, names fencing token)
- J: score 0 (P_d finds TOCTOU, proposes SELECT FOR UPDATE)
- C: score 0 or 0.5 (Instructions content drives elaboration but not mechanism identification)

If content alone is sufficient (few-shot confound):
- I: score 1
- C: score 1 or close to it
- J: score 0

## Variants

| ID | Persona | Instructions (domain content) | Hypothesis |
|----|---------|-------------------------------|------------|
| I  | P_p — highly sophisticated distributed systems engineer; "can't help but discover hidden mysteries" | Generic | Persona slot installs search algorithm |
| J  | P_d — senior software engineer (generic) | Generic | Baseline |
| C  | P_d — senior software engineer (generic) | Contains same domain expertise + thoroughness directives as Variant I Persona | Instructions-slot content test |
