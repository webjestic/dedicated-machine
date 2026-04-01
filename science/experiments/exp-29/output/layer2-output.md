

**Layer 1 coverage:** The correctness review confirmed the zombie-write failure mode — heartbeat thread exits silently on lock loss, main thread continues unaware — and prescribed fencing tokens at the database write boundary as the architectural fix, with threading signals as a necessary but insufficient complement.

---

## Infrastructure Failure Modes

### 1. Redis Sentinel/Cluster failover causes split-lock

**Trigger:** Redis primary fails. Sentinel promotes a replica. The replica has not yet received the `SET NX EX` replication for Process B's claim — or has not yet expired Process A's key due to clock skew between nodes.

**Failure path:** Process A holds a claim on the old primary. Primary dies. Sentinel promotes a replica that either (a) never received Process A's key (Process A's claim vanishes — another worker can claim immediately while A is still executing), or (b) still holds a stale copy of Process A's key with a different TTL clock base. In either case, two workers can simultaneously believe they hold exclusive claims on the same job. Both execute. Both write results. The idempotency check (`db.get_execution`) is a read-then-write with no atomicity guarantee — both workers read `None`, both proceed, both record.

**Why protection cannot live here:** This is the distributed consensus problem that Redis explicitly does not solve. `SET NX EX` on a single Redis node is not a distributed lock — it is a best-effort lease. Redlock across independent Redis instances mitigates but does not eliminate this. The only protection that survives this failure is a fencing mechanism at the database: a conditional write that fails if a prior execution has already been recorded, enforced by a unique constraint or compare-and-swap, not by a read-then-write sequence.

**Required protection:** Database-level unique constraint on `(job_id, completion_marker)` or an atomic compare-and-swap (e.g., `INSERT ... WHERE NOT EXISTS` or row-level versioning). Must reject the second write, not merely detect it after the fact.

---

### 2. GC pause / process stall exceeds CLAIM_TTL — the zombie-write (infrastructure angle)

**Trigger:** Stop-the-world GC pause, OS-level memory pressure (swapping), CPU throttling in a cgroup-constrained container (Kubernetes CPU limits causing CFS throttling), or a slow external call in `_dispatch()` causes the entire process — including the heartbeat thread — to stall for longer than `CLAIM_TTL` (60s).

**Failure path:** This is the Layer 1 finding from the infrastructure side. The heartbeat thread is not a separate process — it shares the GIL, shares the cgroup, shares the memory space. Any event that stalls the process stalls the heartbeat. The claim expires. Another worker acquires it. When the original process resumes, the heartbeat thread fires, gets `result == 0`, and exits silently (no log line, no exception, no signal to the main thread). The main thread was frozen too — it resumes exactly where it stopped, with no mechanism to detect that its claim is gone. It completes the job. It writes the result. The `db.get_execution` check may or may not catch this depending on timing — if the second worker hasn't committed yet, the check passes and both write.

**Why protection cannot live here:** The heartbeat thread cannot signal the main thread during a process-wide stall because both are stalled. Even after the stall, there is no check-before-write in the main thread. The `with self._claim_job(req.job_id)` context manager yields control and never checks the claim again. The main thread has no awareness of claim state after acquisition.

**Required protection (two layers):**
- **Layer A (necessary, insufficient):** `threading.Event` set by the heartbeat on `result == 0`, checked by the main thread before the database write. This catches the case where the heartbeat detects loss before the main thread writes, but does not catch the case where both threads were stalled simultaneously.
- **Layer B (necessary, sufficient):** Fencing token / monotonic counter at the database write boundary. The token is obtained at claim time and must be validated by the database at write time. If a newer token has been issued (by a second worker acquiring the same claim), the write is rejected.

---

### 3. The idempotency check is a TOCTOU race, not a protection

**Trigger:** Two workers pass the `db.get_execution()` check concurrently. Neither has committed yet.

**Failure path:**
```
Worker A: db.get_execution("job-001") → None     ← check passes
Worker B: db.get_execution("job-001") → None     ← check passes (A hasn't committed)
Worker A: db.record_execution(...)                ← writes
Worker B: db.record_execution(...)                ← also writes
```

This is not a timing edge case. This is the *expected* failure path when two workers hold (or believe they hold) concurrent claims due to any of the above failure modes. The check and the write are not atomic. The read isolation level determines whether Worker B's read sees Worker A's uncommitted write — under READ COMMITTED (the default for PostgreSQL), it does not.

**Why protection cannot live here:** The locking code controls the read and the write, but it does not control the isolation guarantee between them. The gap is between `get_execution` and `record_execution` — that gap is exactly where a second worker's write lands.

**Required protection:** Database unique constraint on `job_id` in the execution table (or the completion marker table). This transforms the race from "both succeed" to "one succeeds, one gets a constraint violation." The application must handle this violation gracefully (catch the IntegrityError, treat it as "job already completed," do not retry).

---

### 4. Redis network partition — renewal succeeds locally but claim is externally invisible

**Trigger:** Network partition between the application and Redis. Varies based on direction:
- **App → Redis broken:** Renewal fails. Heartbeat gets an exception (not `result == 0` — a `ConnectionError`). The heartbeat's `while not stop_event.wait()` loop has no exception handling. The thread dies with an unhandled exception. The main thread is not notified. Execution continues. Claim expires.
- **App → Redis intermittent:** Some renewals succeed, some fail. Timing-dependent: if the gap between successful renewals exceeds `CLAIM_TTL`, the claim expires while the heartbeat thread is retrying.

**Failure path:** In both cases, the claim expires in Redis while the main thread continues executing. Another worker claims the job. Duplicate execution.

**Why protection cannot live here:** The `_renew` function has no try/except around the Lua script call. A `redis.ConnectionError` or `redis.TimeoutError` will terminate the thread silently (daemon thread — no unhandled exception propagation to the main thread). The main thread has no way to know.

**Required protection:**
- **Immediate:** Exception handling in `_renew()` that (a) logs the failure, (b) retries with backoff for transient errors, (c) sets a signal to the main thread after N consecutive failures or after the elapsed time since last successful renewal approaches `CLAIM_TTL`.
- **Architectural:** Same fencing token at the database. The renewal failure is a signal that the claim *may* be lost, but only the database can enforce that the write is rejected.

---

### 5. Claim release after loss masks the failure

**Trigger:** Claim expires (any cause). Heartbeat exits. Main thread completes execution. `finally` block runs: `stop_event.set()`, `t.join()`, then `self._release_script(keys=[claim_key], args=[token])`.

**Failure path:** The release script checks the token — it won't match (another worker holds the claim now). It returns 0. **This return value is not checked.** The code then logs `"Claim released job_id=%s"` unconditionally. In production, the operator sees "Claim released" in the logs and believes the system operated correctly. The duplicate execution is invisible in the log stream.

**Why this matters operationally:** When the duplicate execution is eventually detected (double payment, double notification), the investigation will start with the logs. The logs will show a clean lifecycle: claimed → renewed → released. The release was a no-op, but the log says otherwise. This delays diagnosis by hours or days.

**Required protection:** Check the return value of the release script. If it returns 0, log at WARN or ERROR: "Claim release failed: token mismatch — claim was lost during execution, job_id=%s. Execution results may be duplicated." This is not a correctness fix. It is an observability fix. Without it, the correctness failure is also an operational invisibility failure.

---

### 6. Daemon thread semantics — process exit kills heartbeat without claim release

**Trigger:** Worker process receives SIGKILL (OOM killer, `kubectl delete pod --force`, systemd stop timeout exceeded), or crashes (segfault in a C extension, stack overflow). Process exits immediately.

**Failure path:** The heartbeat thread is a daemon thread (`daemon=True`). On process exit, daemon threads are terminated without running `finally` blocks. The claim is never released. It persists in Redis for up to `CLAIM_TTL` (60 seconds). During that window, no other worker can claim the job. After TTL expiry, another worker claims it and re-executes.

**Outcome:** This is not necessarily a correctness violation — it's a liveness issue (60-second delay before the job can be retried). However: if the process crashed *after* the database write but *before* returning, the job is already completed. When the next worker picks it up after TTL expiry, the idempotency check (`db.get_execution`) should catch it — *if* the first worker's transaction committed before the crash. If the crash happened between `record_execution` and `commit`, the transaction is rolled back, the job is not recorded, and the retry is correct behavior.

**Gap:** The 60-second liveness delay is acceptable but should be documented. The interaction between crash timing and transaction commit is correct *only if* the database transaction is actually atomic (i.e., `self.db.transaction()` is a real transaction with commit-on-exit semantics and rollback-on-exception). This is an assumption about the `db` interface that is not verified by any test.

**Required protection:** Integration test or contract test that verifies `db.transaction()` actually provides atomicity. If it doesn't, a crash between `record_execution` and `mark_job_complete` leaves the database in an inconsistent state (execution recorded, job not marked complete), and the retry worker will see `get_execution` return a result and skip the job — which may or may not be correct depending on whether the first execution's side effects were committed.

---

### 7. Clock skew between application host and Redis — TTL semantics diverge

**Trigger:** Redis uses its own clock for TTL expiry. If the application host's clock runs slow relative to Redis, the application's `RENEWAL_INTERVAL` (15 seconds by wall clock) may be 16-17 seconds of Redis time. Over multiple renewal cycles, drift accumulates.

**Failure path:** With `CLAIM_TTL = 60` and `RENEWAL_INTERVAL = 15`, there's a 4x safety margin per renewal. Clock skew of even several seconds is unlikely to cause expiry under normal conditions. However: if the renewal thread is delayed by GC *and* clock skew compounds, the effective safety margin shrinks. This is a secondary amplifier of failure mode #2, not an independent failure mode.

**Required protection:** No independent fix needed, but the TTL/renewal ratio (4:1) should be documented as an operational parameter. The standard recommendation is at least 3:1. The current 4:1 is adequate but leaves no room for further reduction.

---

### 8. `_dispatch()` handler exception behavior is undefined at the infrastructure boundary

**Trigger:** The job handler (obtained from `self.db.get_handlers()`) throws an exception — timeout calling an external API, database error inside the handler, or any unhandled exception.

**Failure path:** The exception propagates up through `execute()`. The `_claim_job` context manager's `finally` block runs — it releases the claim. The database transaction context manager's `__exit__` runs — behavior depends on the `db.transaction()` implementation. If it rolls back, no execution is recorded. The job remains unprocessed and available for retry. If it does *not* roll back (e.g., partial commit), the state may be inconsistent.

**Critical gap:** The exception from `_dispatch()` propagates through `execute()` **without being caught** (there is no except clause for general exceptions — only `ClaimError` and `ValidationError`). This means the caller receives an unhandled exception. Depending on the calling framework (Celery, FastAPI, custom worker loop), this may crash the worker, trigger a retry, or be silently swallowed.

**Required protection:** `execute()` should catch exceptions from `_dispatch()` and return a `JobResult` with `claimed=True` and a failure message, or explicitly re-raise with context. The current behavior — letting handler exceptions propagate as unhandled — means the caller cannot distinguish "job failed" from "system error." More importantly, the `finally` block releases the claim even though the job is not complete, allowing another worker to retry immediately. Whether retry is correct depends on whether the handler's side effects are idempotent — a contract that is nowhere defined.

---

## Open Gaps

| # | Gap | Severity | Status |
|---|-----|----------|--------|
| G1 | No fencing token / monotonic counter at database write boundary | **Critical** | Not implemented |
| G2 | No database unique constraint on job execution (TOCTOU race on `get_execution` → `record_execution`) | **Critical** | Not implemented |
| G3 | No threading signal from heartbeat to main thread on claim loss | **High** | Not implemented |
| G4 | No exception handling in `_renew()` — Redis connection errors kill heartbeat silently | **High** | Not implemented |
| G5 | Claim release return value unchecked; "Claim released" logged unconditionally | **Medium** | Not implemented |
| G6 | Heartbeat exits silently on `result == 0` — no log line, no signal | **Medium** | Not implemented |
| G7 | Handler exceptions propagate unhandled; no contract on handler idempotency for retries | **Medium** | Not implemented |
| G8 | `db.transaction()` atomicity is assumed but not tested | **Medium** | Not verified |

---

## Production Readiness Verdict: NOT APPROVED

This system provides a well-structured single-node mutual exclusion mechanism with correct Lua-script-based atomic operations for claim acquisition, renewal, and release. Under the assumption that Redis is a single reliable node, that processes are never stalled, and that no two workers ever execute concurrently for the same job, it works correctly.

That assumption does not hold in production. The system has **two critical gaps** that, independently, permit duplicate job execution with no detection or prevention:

**First**, the heartbeat thread's loss of the claim (whether by process stall, GC pause, Redis failover, or network partition) is completely invisible to the main execution thread. The main thread will complete execution and write results after the claim has been acquired by another worker. There is no signal, no check, and no interruption. This is a known gap from the Layer 1 review and is confirmed from the infrastructure side: the heartbeat thread shares the process's fate (GC, cgroup throttling, OOM) and cannot serve as an independent watchdog.

**Second**, the idempotency check (`get_execution` returning `None`) is a read-then-write race. Under concurrent execution — which is precisely the scenario this system exists to prevent — both workers read `None` and both write. No database constraint prevents the second write.

Before this ships, the following must be in place:

1. **Database unique constraint** on job execution records, keyed on `job_id`. This is the minimum viable protection. It converts duplicate writes from silent corruption to a detectable, catchable constraint violation.
2. **Fencing token validated at the database write boundary.** The claim token (or a monotonic counter derived from it) must be passed through to the database transaction and validated as part of the write condition. This is the only mechanism that survives all identified failure modes — process stalls, Redis failover, network partitions, and TOCTOU races.
3. **Exception handling in the heartbeat thread** for Redis connection errors, with logging and a signal to the main thread.
4. **The release return value must be checked** and a warning logged on mismatch. Without this, the production team cannot diagnose duplicate execution from logs.

Items 1 and 2 are ship-blockers. Items 3 and 4 are required before any on-call team can operate this system. Without them, the first duplicate execution will be discovered by a customer, not by monitoring.