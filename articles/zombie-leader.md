# The Zombie Leader Problem
### Why good code fails in production, and why a single prompt can't tell you

---

Here is a pull request that will pass your code review.

It is well-engineered. Atomic lock operations via Lua script. Token-verified release — the worker can only release its own lock, not someone else's. Background heartbeat thread that renews the lock during long-running jobs. Exponential backoff with jitter on contention. Pydantic input validation. Database transaction wrapping execution record and job completion. A test suite that covers contention, idempotency, and the atomic Lua path.

The checklist is comprehensive. Everything is checked. The tests pass.

And it has a bug that will fire a job twice.

Not on every run. Not even frequently. Under a specific timing sequence — a GC pause, a slow external call, a moment of process stall — two workers will both believe they own the same job and both execute it. If the job sends an alert, both alerts go out. If it charges a payment, it charges twice. If it triggers an external action, it triggers twice.

The code is correct. The system is not.

---

## What a Zombie Write Is

The job executor works like this: a worker acquires a Redis lock before processing a job. The lock has a TTL — it expires automatically if the worker disappears. To handle long-running jobs, a background heartbeat thread renews the TTL every 15 seconds. When the job finishes, the worker releases the lock.

The vulnerability is in what happens when the renewal fails.

Here is the sequence:

1. **Worker A** acquires the lock. Token = `abc-123`. TTL = 60 seconds. Heartbeat thread starts.

2. A garbage collection pause — or a slow external call, or a CPU throttle from the container runtime — holds Worker A's process for 65 seconds. The lock's TTL expires. Redis deletes it.

3. **Worker B** sees the lock is gone. Worker B acquires the lock. Token = `xyz-789`. Worker B starts executing the job.

4. Worker A's process resumes. The heartbeat fires. It tries to renew the lock:
   ```python
   if redis.call("get", KEYS[1]) == ARGV[1] then   # "abc-123" != "xyz-789"
       return redis.call("expire", ...)
   else
       return 0                                       # silent exit
   end
   ```
   The token doesn't match. The Lua script returns `0`. The heartbeat thread exits:
   ```python
   if result == 0:
       return
   ```

5. **Worker A's main thread continues executing the job.** It has no way to know the heartbeat exited. Threading.Event isn't watching the heartbeat. The heartbeat doesn't signal anything. The main thread is already past lock acquisition — it's inside the `with self._claim_job()` block, and the heartbeat exit doesn't propagate.

6. Both Worker A and Worker B complete the job. Both write their execution records. Both fire their side effects.

This is a zombie write. Worker A is dead — it lost the lock — but it doesn't know it. It keeps going. It walks through the system like a process that hasn't been informed of its own death.

The fix is a fencing token at the database write boundary: a monotonic counter or version number that the database enforces, so that a stale write cannot succeed even if the code didn't catch the lock loss. Without it, the code and the database are operating on a shared assumption — "whoever holds the lock is current" — that the environment can silently invalidate.

---

## Why It Passes Review

The code is doing everything a correctness-focused review asks for.

The Lua scripts are atomic — no TOCTOU at the Redis layer. The token check means only the holder can release or renew. The database transaction wraps both the execution record and the job completion marker. The idempotency check (`get_execution` before `_dispatch`) catches the case where a job was already completed. The tests cover contention and verify the Lua path is used.

A reviewer asking "does this code do what it claims?" will find that it does. The claim acquisition is correct. The renewal logic is correct. The release is correct. The token verification is correct. Everything the checklist names has been addressed.

The question "what does a GC pause do to this code?" is not a correctness question. It's an infrastructure question. It lives outside the correctness review's scope — not because the reviewer is lazy, but because that's the right scope for a correctness review. Correctness and infrastructure readiness are different concerns, and a review that tries to hold both simultaneously tends to do neither well.

The gap is real. The gap is intentional. The problem is that no one is covering the other side of it.

---

## Forty Runs, Four Variants

The zombie-write problem became a benchmark. We ran it forty times across four prompt variants — different Persona constructions, different gap-detection conditions — and scored each output against a strict criterion (Tier 1.0): name the GC pause as the trigger *and* name the fencing token / optimistic concurrency as the architectural fix.

| Variant | Tier 1.0 rate | What it reached |
|---------|--------------|-----------------|
| A — domain P_p | 1/10 | Named GC pause + fencing token, once |
| B — A + gap detection | 0/10 strict | Named fencing token without the GC trigger |
| C — P_d baseline | 0/10 | Threading.Event signaling, no structural fix |
| D — operational P_p + gap detection | 0/10 strict | Same as B |

The expert Persona (A) knew about fencing tokens. It knew about GC pauses. It produced the correct finding once in ten runs. The other nine runs named threading.Event as the fix — correct diagnosis, wrong layer.

Why? The correctness reviewer's consideration set terminates at the engineering boundary. Threading.Event is an engineering fix: make the code respond to heartbeat failure. Fencing token is an architectural fix: make the database enforce exclusivity even when the code doesn't know it's a zombie. The first fix is inside the implementation. The second fix is outside it.

The expert correctness reviewer will reach threading.Event most of the time because it's available within the engineering consideration set. Fencing token requires stepping outside that consideration set into infrastructure and database architecture. That step is what the correctness frame doesn't install.

---

## The Two-Prompt Solution

The insight is that the zombie-write problem isn't one review — it's two. A correctness review and an infrastructure review. Each requires a different consideration set. And a single machine trying to hold both consideration sets simultaneously never holds the second one reliably enough to find the fix every time.

The pipeline assigns one consideration set to each agent.

**Layer 1 — The Correctness Reviewer:**

```
You are a senior software engineer with deep experience in backend systems,
distributed coordination, and Redis. You have reviewed hundreds of pull requests
for systems running at scale. Your reviews are systematic: you trace execution
paths, identify race conditions, verify atomicity, and confirm error handling.
You do not approve code until you have confirmed it does what it claims under
concurrent load.

Your review is complete only when you have named every correctness issue...
At the end of every review you produce a tight handoff summary: what this
review covered, what was found, and what remains out of scope for a correctness
review.
```

Notice the last line: *what remains out of scope for a correctness review.* The Persona requires Agent 1 to produce an explicit boundary statement. Not as a footnote — as a required output. Agent 1 cannot be done without naming what it didn't cover.

The Instructions reinforce this:

```
4. Do not speculate beyond correctness — infrastructure failure modes are
   out of scope for this review.
5. End with a handoff summary for the production readiness reviewer: what
   this review covered, issues found and addressed, and a one-line statement
   of what this review explicitly does not cover.
```

Agent 1 produced exactly this:

> *"This review does not cover infrastructure-level failure modes (Redis cluster failover, network partitions, database availability), deployment topology, performance under load, or operational runbook readiness."*

That sentence is the bridge. Everything Agent 1 said it wasn't covering became Agent 2's scope.

**Layer 2 — The SRE:**

```
You are a senior SRE with a decade of experience operating distributed systems
in production. You have been on the calls — the ones that happen at 3am when a
system that passed code review still produced incorrect results. You know the
pattern: the code was correct. The infrastructure did something the code didn't
account for. The gap was never in the code itself.

Your job now is pre-production. You review systems before they ship — specifically
to find the failure modes that exist outside the code.
```

The SRE Persona installs a completely different consideration set. The question is no longer "does this code do what it claims?" The question is "what does the environment do to this code?" Those questions have different answers — and reach different failure modes.

The Instructions make the scope explicit:

```
4. Pay particular attention to failure modes where the locking mechanism
   believes it is operating correctly but the underlying guarantee has already
   been invalidated by an event outside its control.
```

That's the zombie-write pattern stated directly. The locking mechanism believes it is operating correctly. The guarantee has been invalidated by an event outside its control. The SRE's job is to find exactly that class of failure.

---

## What the Pipeline Found

The two-agent pipeline was run once — a proof-of-concept, not a controlled trial. Agent 1 reached Tier 1.0 on the first run: named the GC pause as the trigger, traced the full failure path, and named the fencing token at the database write boundary as the architectural fix. Cleaner than any of the 40 single-pass runs.

Agent 2 received the Layer 1 handoff summary — the list of what the correctness review covered, and the explicit out-of-scope statement. Agent 2 independently surfaced seven additional infrastructure failure modes that appeared in none of the 40 single-pass runs:

- **Redis Sentinel failover → split-lock:** During a Redis failover, two workers can simultaneously believe they hold the lock.
- **Kubernetes CFS throttling:** The container runtime can pause the process for longer than LOCK_TTL without a GC event — a process-wide stall the heartbeat cannot prevent.
- **`ConnectionError` in `_renew()` kills the heartbeat silently:** If Redis is briefly unreachable during renewal, the thread exits without signaling the main thread.
- **Daemon thread + SIGKILL:** If the process receives SIGKILL (or `kubectl delete pod --force`), the daemon heartbeat exits without the `finally` block running. The lock stays claimed for 60 seconds.
- **TOCTOU on `get_execution` → `record_execution`:** Two workers can both read `None` from `get_execution` before either commits, then both proceed to execute.
- **Clock skew:** A secondary amplifier on the GC pause scenario — clock drift between workers affects which lock appears to be current.
- **Handler exception at the infrastructure boundary:** An unhandled exception in `_dispatch()` propagates out of the `with` block and into the `finally`, where the claim is released — but the database may or may not have recorded the execution depending on where the exception was thrown.

None of these appeared in any single-pass output across 40 runs.

Why? The SRE's consideration set contains these failure modes. The correctness reviewer's does not. The pipeline didn't make one machine smarter — it gave each consideration set its own machine.

---

## The Mechanism

The agent boundary is not a convenience. It is the mechanism.

Agent 1's handoff summary contains an explicit out-of-scope statement. That statement defines Agent 2's scope. The failure modes Agent 1 said it wasn't covering became the failure modes Agent 2 was looking for. The boundary between the two consideration sets is load-bearing — it is the bridge that connects them.

This is what the Dedicated Machine framing predicts. Each machine terminates at the nearest state its satisfaction condition registers as complete. Agent 1's satisfaction condition is "every correctness issue named, handoff summary produced." Agent 2's satisfaction condition is "every infrastructure assumption validated." The gap in single-pass prompts exists because one machine cannot hold both satisfaction conditions simultaneously — it terminates at the first one it reaches.

The pipeline doesn't close the gap by making the machine smarter. It closes the gap by making the second satisfaction condition the starting point of a different machine.

---

## Reading the Prompts

Both prompts are in `parc/examples/`. The code being reviewed is in `experiments/exp-09/ARTIFACT.md`.

Three things worth noticing when you read them:

**The out-of-scope instruction in Layer 1 is doing double duty.** Instruction 4 says "do not speculate beyond correctness — infrastructure failure modes are out of scope for this review." This keeps Agent 1 on its own job. But it also seeds the handoff — the model knows it's producing a document that will be handed to another reviewer, and the out-of-scope statement is explicitly required in the output format.

**Layer 2's Persona is not the correctness reviewer with more knowledge.** It's a different identity entirely. The SRE's opening isn't "you know distributed systems." It's "you have been on the calls — the ones that happen at 3am when a system that passed code review still produced incorrect results." That framing installs a different set of salient failure modes before the code is even read.

**The pipeline produces two verdicts: NOT APPROVED.** Both. The correctness reviewer finds the zombie write and rejects the PR. The SRE finds seven more infrastructure failure modes and rejects it again. The code doesn't ship. That is the correct outcome.

---

*This article is based on `parc/examples/zombie-layer1-review.md`, `parc/examples/zombie-layer2-review.md`, the artifact at `experiments/exp-09/ARTIFACT.md`, and the experimental findings in `experiments/exp-29/FINDINGS.md`.*
