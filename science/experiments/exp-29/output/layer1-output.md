

## Findings

**1. Zombie write — heartbeat loss is invisible to the main execution thread**

**Failure path:**

Worker A acquires the claim for `job-042` and begins executing a slow handler (or hits a GC pause, network stall, or any delay exceeding `CLAIM_TTL` of 60 seconds). The claim expires in Redis. Worker B acquires the same claim key with a new token and begins executing the same job. Worker A's heartbeat thread fires `_renew()`, the Lua script returns `0` (token mismatch — the lock no longer belongs to A), and the heartbeat thread silently returns. The main thread in Worker A has no mechanism to observe this. It continues execution: it calls `_dispatch()`, gets a result, opens a database transaction, writes the execution record, and marks the job complete. Worker B does the same. The job runs twice.

For jobs with side effects — sending alerts, issuing payments, triggering external actions — this is a correctness violation. The idempotency check (`db.get_execution`) does not protect against this because both workers pass it before either commits: Worker A checked before its pause, and Worker B checks after acquiring its own valid claim and sees no prior completion.

This is the central defect in the PR.

**Required fix (two layers, both needed):**

**(a) Immediate signal — necessary but not sufficient.** When `_renew()` observes `result == 0`, it must signal the main thread. A `threading.Event` (e.g., `lost_event.set()`) that the main thread checks before every irreversible operation (before `_dispatch()`, before `db.transaction()`) is the minimum viable coordination. This catches the common case where the heartbeat detects loss before the main thread commits.

**(b) Architectural fix — required for actual correctness.** The threading signal has a race window: the lock can expire *between* the last successful heartbeat and the next check in the main thread. The main thread cannot poll its way to safety. The correct fix is a **fencing token** (monotonic counter or epoch number) attached to the claim and threaded through to every write. The database transaction must validate the fencing token at write time (optimistic concurrency control): `UPDATE ... WHERE job_id = ? AND fence_token = ?`. If another worker has claimed with a higher token, the write fails. This is the only mechanism that makes the commit itself atomic with respect to lock ownership. Without fencing, there is always a window between "check lock" and "commit write" where ownership can change.

---

**2. Silent heartbeat exit — no logging, no observability**

**Failure path:** When `_renew()` gets `result == 0` and returns, there is no log entry. In production, the operator has no signal that a claim was lost during execution. Debugging zombie writes or duplicate job executions becomes forensically difficult.

**Required fix:** Log at `WARNING` or `ERROR` level when the renewal script returns `0`, including `job_id` and the worker's token. This is a one-line fix but operationally critical.

---

**3. `_release_script` called unconditionally in `finally` after lock loss**

**Failure path:** After the heartbeat exits due to token mismatch, the lock is now held by another worker (Worker B) with a different token. The `finally` block in `_claim_job` calls `self._release_script(keys=[claim_key], args=[token])`. Because the Lua release script is token-verified, this call is *safe* — it will return `0` and not delete Worker B's lock. However, it logs `"Claim released job_id=..."` unconditionally, which is misleading: the claim was not released, it was already lost. This is a minor observability issue, not a correctness bug, but the log line creates false confidence during incident investigation.

**Required fix:** Check the return value of `_release_script`. Log differently for "released" vs. "claim already lost."

---

**4. No test coverage for the critical concurrent failure mode**

The test suite mocks Redis such that the renewal script always returns `1`. There is no test where `_renew_script` returns `0` during execution. The zombie-write scenario is entirely untested.

**Required fix:** Add a test where the renewal mock returns `0` mid-execution and verify that the executor either aborts, raises, or otherwise prevents the write from completing.

---

**5. `_dispatch` exception during `execute` is unhandled — lock released but job state is indeterminate**

**Failure path:** If `_dispatch()` raises any exception other than `ValueError` (e.g., a handler raises `RuntimeError` or `ConnectionError`), the exception propagates out of the `with self._claim_job(...)` block. The `finally` block releases the claim. The `execute` method does not catch this — it propagates to the caller. The job is neither recorded as completed nor marked as failed in the database. Whether this is a bug depends on the contract: if the caller retries, it will pass the idempotency check (`get_execution` returns `None`) and re-execute, which is likely the desired behavior. But the current code does not make this contract explicit, and there is no `db.mark_job_failed()` path. This is a design gap, not a zombie-write, but it should be explicitly decided.

**Required fix:** Document the retry contract for handler exceptions, or add explicit failure recording.

---

**Correctness verdict:** NOT APPROVED

The main execution thread has no visibility into heartbeat failure. After lock expiry, a worker continues executing and writing as if it still holds the claim. Under real concurrency with GC pauses, slow handlers, or network stalls, this produces duplicate job execution — the exact class of bug this locking system exists to prevent. The threading signal (Finding 1a) is necessary for fast-path detection; the fencing token / optimistic concurrency check at write time (Finding 1b) is necessary for closing the race completely.

---

**Handoff summary for production readiness review:**

This review traced the full lock lifecycle — acquisition, heartbeat renewal, main-thread execution, and release — under concurrent worker scenarios. The critical finding is that heartbeat thread loss (caused by lock expiry during GC pause, slow I/O, or any delay exceeding TTL) is invisible to the main execution thread, which continues to completion and writes results, enabling duplicate job execution. The required architectural fix is a fencing token validated at database write time (optimistic concurrency control); a threading signal from heartbeat to main thread is a necessary but insufficient complement. Four additional issues were identified: silent heartbeat exit with no logging, misleading release logging after lock loss, missing test coverage for the concurrent failure path, and an undefined contract for handler exceptions. This review does not cover infrastructure-level failure modes (Redis cluster failover, network partitions, database availability), deployment topology, performance under load, or operational runbook readiness.