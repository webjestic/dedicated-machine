# exp-07d SCORING

## Experiment Purpose

Clean falsification test for the P_p/P_d distinction and the few-shot confound.

exp-07c established a new behavioral observation but could not answer the slot-swap
question: C's edge over I was explained by I's P_p comprehensiveness diluting the
critical finding under a token ceiling — not by C finding the zombie write mechanism.
The confound was a `logger.warning("Heartbeat detected lock loss")` line that labeled
the failure mode directly, allowing code reading to substitute for structural inference.

exp-07d removes the hint. The failure mode is silent again.

## What Changed from exp-07c

Single change to the artifact: `_beat()` no longer contains:

```python
if result == 0:
    # Token mismatch: lock expired and was re-acquired by another caller
    logger.warning("Heartbeat detected lock loss key=%s", lock_key)
    return
```

It now contains only:

```python
if result == 0:
    return
```

No other changes. Same variants. Same scoring. Same n.

## New Behavioral Observation from exp-07c (to watch for in exp-07d)

exp-07c revealed that P_p comprehensiveness is a double-edged sword under a token ceiling:
the search algorithm finds *everything*, spreading token budget across many findings and
diluting the critical one. C's Instructions-slot content drove thoroughness without
installing the full P_p search algorithm — resulting in a more focused (if shallower) review.

Watch for this in exp-07d results: if I again shows ceiling hits with the zombie write
finding buried, that confirms the comprehensiveness trade-off is real and independent of
the hint confound. If I sharpens onto the zombie write without ceiling pressure, the
exp-07c result was an artifact of the hint (everyone found it, I kept looking for more).

## Scenario: Process-Pause Zombie Write (Silent)

The code is a well-implemented distributed inventory reservation service. All known
implementation bugs have been corrected. The heartbeat's `result == 0` branch now exits
silently — no log message, no comment labeling the scenario.

The **sole remaining structural failure mode** is the process-pause zombie write:

> After acquiring the lock, the process reads `current_stock` **outside** the DB transaction.
> If the process is then paused (OS scheduling, GC stop-the-world, VM migration) for longer
> than `LOCK_TTL` (30s), the heartbeat thread is also paused. The lock expires. Another
> process acquires the lock, reads the same stock value, completes its reservation, and
> commits. When the original process resumes, it is still inside
> `with self._acquire_lock(lock_key):`. The heartbeat's `result == 0` check detects the
> token mismatch and returns — but it has **no channel to abort the main thread**. The main
> thread continues with a stale `current_stock` reading and writes `new_stock` — the same
> value the second process already wrote. Net result: two orders issued, stock decremented
> only once. Oversell.

Detection now requires structural inference: the reviewer must simulate the process-pause
scenario across the full lock lifecycle. No code-level signal points toward it.

## Scoring Criterion

### Score = 1 (P_p behavior)
The output:
1. Identifies the **process-pause / long GC pause / lock-expiry-while-paused** scenario
   as a specific failure mode — not just generic TOCTOU, but the scenario where the
   **lock expires** because the process holding it was paused, and
2. Names the architectural fix: **fencing token**, **monotonic counter**, **version field +
   conditional update**, or **optimistic concurrency control** that rejects stale writes.

### Score = 0.5 (partial)
The output identifies the process-pause / lock expiry scenario but proposes only
`SELECT FOR UPDATE` or "move the read inside the transaction" without noting that
DB-level row locking also breaks down under a zombie-write scenario.

### Score = 0 (P_d behavior)
The output finds `get_stock()` outside the transaction as a generic TOCTOU concern and
recommends `SELECT FOR UPDATE` or moving the read inside the transaction — without naming
the lock-expiry / process-pause mechanism. Correct fix proposed, wrong reason given.

## Binary Question

| Outcome | Interpretation |
|---------|---------------|
| C ~ I (high score) | Few-shot confound is real — procedural content in Instructions slot is sufficient; Persona slot is not architecturally load-bearing |
| C ~ J (low score) | Persona slot is architecturally load-bearing — content alone does not install the consideration set |
| C intermediate (0.3–0.7) | Partial slot effect — content contributes, but identity framing amplifies |

## Variants

| ID | Persona | Instructions (domain content) | Hypothesis |
|----|---------|-------------------------------|------------|
| I  | P_p — highly sophisticated distributed systems engineer; "can't help but discover hidden mysteries" | Generic | Persona slot installs search algorithm |
| J  | P_d — senior software engineer (generic) | Generic | Baseline — should score ~0 |
| C  | P_d — senior software engineer (generic) | Contains same domain expertise + thoroughness directives as Variant I Persona | The test — does content in Instructions substitute for Persona identity? |
