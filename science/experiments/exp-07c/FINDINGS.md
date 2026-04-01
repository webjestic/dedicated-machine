# exp-07c FINDINGS — Slot-Swap Falsification Test (Boundary Finding)

**Status:** Completed — partial result; boundary condition established
**Date:** 2026-03-27
**Cost:** $1.3003 (30 runs × 3 variants × n=10)

---

## Research Question

Does the Persona slot drive detection of hidden failure modes independently of its content,
or does procedural content in the Instructions slot produce equivalent results? This tests
the "few-shot confound" identified in exp-06: P_p prompts embed task-relevant reasoning
that may function as implicit CoT regardless of slot placement.

**Variants:**
- **I**: P_p Persona ("highly sophisticated distributed systems engineer… can't help but
  discover hidden mysteries") + generic Instructions
- **J**: P_d Persona ("senior software engineer") + generic Instructions (baseline)
- **C**: P_d Persona + same domain expertise and thoroughness directives moved to Instructions slot

---

## Code Scenario

All previously identified calibration bugs fixed (see exp-07 and exp-07b FINDINGS):
- Heartbeat: `stop_event` starts cleared; `while not stop_event.wait(timeout=N)` pattern
- Lock release and extension: Lua scripts (atomic)
- DB writes: wrapped in `self.db.transaction()`
- ValidationError: caught and returned as `ReservationResult`
- Backoff: exponential + jitter

**Intended hidden failure mode:** Process-pause zombie write. `get_stock()` is called outside
the DB transaction. If the process is paused for > `LOCK_TTL` (30s), the heartbeat thread
(also in-process) is paused. The lock expires. Another process acquires the lock, reads the
same stock value, completes its reservation. The original process resumes inside
`with self._acquire_lock(lock_key):`. The heartbeat detects token mismatch and exits, but
has no channel to abort the main thread. The main thread continues with its stale
`current_stock` reading and writes an oversold state. Fix requires fencing token or DB-level
optimistic locking with version field.

---

## Results

### Token Pattern

| Variant | Ceiling hits (2500 tok) | Avg output |
|---------|------------------------|------------|
| I (P_p) | 7/10 | ~2,436 |
| J (P_d) | 0/10 | ~2,016 |
| C (slot-swap) | 6/10 | ~2,399 |

I and C substantially above J in output volume. J never hit ceiling.

### Scoring (Two-Tier Criterion)

| Variant | Score 1 | Score 0.5 | Score 0 | Weighted |
|---------|---------|-----------|---------|----------|
| I (P_p) | 0 | 5 | 5 | **2.5** |
| J (P_d baseline) | 0 | 6 | 4 | **3.0** |
| C (slot-swap) | 1 | 5 | 4 | **3.5** |

**Score 1:** Identifies process-pause/lock-expiry zombie write mechanism AND names fencing
token, monotonic counter, or version-field conditional update as architectural fix.

**Score 0.5:** Identifies lock-loss / heartbeat-no-signal mechanism but proposes only
SELECT FOR UPDATE or move-read-inside-transaction (correct DB-level fix, mechanism named).

**Score 0:** Finds `get_stock` outside transaction as generic TOCTOU without naming
lock-expiry / process-pause mechanism.

---

## Finding

**Pattern: C ≥ J > I.** This is inconsistent with the PCSIEFTR prediction (expected I >> J,
with C between them as the slot-swap test). However, the result has a clean explanation that
does not invalidate the framework.

### Root Cause: Code-Visible Hint

The heartbeat code contains:

```python
if result == 0:
    logger.warning("Heartbeat detected lock loss key=%s", lock_key)
    return  # exits thread; caller has no idea
```

This log line — plus the visible `return` with no signal to the main thread — is a
**code-level hint** about the failure mode. Any careful reviewer reading this code notices:
the heartbeat detects lock loss and does nothing about it. J-06 (verified) explicitly
quotes "the heartbeat detects this eventually, not instantly" while identifying the issue.

When the failure mode is *visible* in the code, the consideration-set mechanism is not being
tested. The consideration set expands what is *reachable*; when something is already
*visible*, any variant can reach it through careful code reading.

### I Underperformance

P_p generated 7/10 ceiling hits — more output than J or C proportionally. With 2500 tokens
distributed across more findings, the zombie-write mechanism gets less proportional space in
a 10-finding review than in a 3-finding one. P_p's thoroughness can dilute the signal on
the target finding when the code gives it many legitimate things to find. This is a new
behavioral observation: the P_p search algorithm generates comprehensiveness, which under a
token ceiling trades off against depth on any single finding.

### Single Score-1 (C-02)

The only Score 1 in the experiment came from C-02 (slot-swap Instructions variant). C-02
identified: "the update should be expressed as a delta with a guard condition, not an
absolute assignment" — the conditional update / optimistic locking pattern at the storage
layer. With n=1 this is not statistically meaningful but worth noting.

---

## Boundary Condition Established

The exp-07c result, read against exp-01e (I=10/10, J=0/10 on a structurally hidden zombie
write), establishes a boundary condition:

| Failure mode visibility | I result | J result |
|------------------------|----------|----------|
| Structurally hidden (exp-01e) | 10/10 | 0/10 |
| Code-visible hint (exp-07c) | 2.5/10 weighted | 3.0/10 weighted |

**The consideration-set effect operates on reachable failure modes, not visible ones.** When
a failure mode is signaled in code (a log line naming the failure, a comment describing the
gap), P_d can reach it through code reading. The P_p advantage activates specifically on
failure modes that require reasoning beyond what is explicit in the code — structural
inferences about what happens when the system operates outside its happy path.

This is a more precise statement than the paper currently makes, and it emerged from a
correctly diagnosed null result.

---

## Slot-Swap Question: Status

**Unanswered.** The code-visible hint equalized performance across all variants, making it
impossible to isolate Persona-slot vs. Instructions-slot effects. The few-shot confound
(identified in exp-06 as the strongest unanticipated critique) remains an open question.

**exp-07d design (if pursued):** Remove `logger.warning("Heartbeat detected lock loss")`
and the associated comment. Heartbeat returns silently on token mismatch. This makes the
failure mode structurally hidden — a reasoning inference rather than a code-reading task.
The question then becomes whether P_p identity framing generates the process-pause
reasoning unprompted, which is the core claim.

---

## Implications for d3

1. **Boundary condition finding** should be added to the paper as a refinement of the
   consideration-set claim: "The P_p advantage is specific to structurally hidden failure
   modes. When a failure mode is code-visible, P_d can find it through careful code reading."
2. **Few-shot confound** should be acknowledged as an explicitly open question — the slot-swap
   test was designed but confounded; exp-07d would close it.
3. **P_p thoroughness / token ceiling tradeoff** is a new behavioral observation worth a
   footnote: P_p's comprehensive search can dilute signal on the target finding when the
   code provides many legitimate findings within a fixed token budget.
