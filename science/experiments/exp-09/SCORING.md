# exp-09 SCORING

## Experiment Purpose

Clean falsification of the few-shot confound. exp-07c/07d showed that
Instructions-slot domain content (C) produced findings equivalent to P_p (I) on
the silent zombie-write artifact. Both experiments had calibration contamination:
code comments and PR checklist items pointed toward the failure mechanism, making
it accessible without the P_p search algorithm.

exp-09 tests the same slot-swap on a clean artifact where:
- The PR description covers the happy path only
- No checklist item names the detection or signaling behavior
- The code has `if result == 0: return` but no comment explaining its failure-mode semantics
- Discovery requires simulating a process pause to reach the architectural finding

## Artifact

Distributed job executor service (`services/job_executor.py`). See `ARTIFACT.md`.

The zombie-write analog: Process A claims a job and begins execution. A GC pause
holds the process longer than CLAIM_TTL. The claim expires. Process B claims and
begins the same job. Process A's renewal fires, returns 0 (token mismatch), the
renewal thread exits silently. Process A's main thread continues, completing
execution and recording the job as done. Both processes complete: the job runs twice.

## Variants

| ID | Persona | Instructions | Hypothesis |
|----|---------|-------------|------------|
| A | P_p — highly sophisticated distributed systems engineer | Generic | Baseline: P_p installs consideration set |
| B | P_d — senior software engineer | Generic | Baseline: should score lower on Tier 1.0 |
| C | P_d — senior software engineer | + domain content | The test: does Instructions-slot domain content substitute for Persona on clean artifact? |
| D | P_p — highly sophisticated distributed systems engineer | + domain content | Does Instructions domain content extend P_p ceiling? |

## Instructions Domain Content (Variants C and D)

The domain content added to the Instructions slot encodes the P_p search procedure
without the identity framing. It tells the model *what to do* (search for mid-operation
coordination failure) without encoding *who to be*:

> When reviewing distributed coordination code: after you confirm that claim
> acquisition, renewal, and release mechanics are correct on the surface, ask one
> more question. If this coordination mechanism were to fail silently during
> execution — not at acquisition, not at release, but in the gap between — would
> the protected code know? Simulate the full lifecycle under an adverse timing
> scenario. The failure mode is not in the acquisition path. It is not in the
> release path. It lives in the gap between when coordination is lost and when the
> code learns it.

## Scoring Criterion

### Score = 1.0 (architectural finding)
Output identifies:
1. The process-pause / long GC pause / claim-expiry-while-paused scenario as a
   specific failure mode — not just generic TOCTOU, but the scenario where the
   **claim expires** because the process holding it was paused, AND
2. Names the architectural fix: **fencing token**, **monotonic counter**,
   **version field + conditional update**, or **optimistic concurrency control**
   that rejects stale writes at the DB layer.

### Score = 0.5 (mechanism found, incomplete fix)
Output identifies the renewal-silence / claim-loss signaling gap and proposes
threading.Event or shared flag — correct mechanism diagnosis, incomplete
architectural fix. (threading.Event doesn't survive a process pause.)

### Score = 0.25 (mechanism found, no fix)
Output identifies the renewal-silence mechanism without a concrete fix.

### Score = 0 (surface only)
Output finds `get_execution()` outside the transaction as a generic TOCTOU or
finds no structural issue.

## Binary Questions

**Primary:** Does C match A or B?
- C ~ A: Instructions-slot domain content installs P_p behavior even on clean artifact
  → slot position is not architecturally significant; content type is
- C ~ B: Persona slot is load-bearing on clean artifact
  → Instructions compensation in exp-07c/07d was artifact-level, not structural

**Secondary:** Does D exceed A?
- D > A on Tier 1.0: domain content in Instructions extends P_p ceiling
- D ≈ A: P_p already saturated; Instructions domain content adds elaboration, not depth

## Outcome Interpretation

| C result | D result | Interpretation |
|----------|----------|----------------|
| C ~ A | D ≈ A | Instructions installs P_p; P_p already saturated |
| C ~ A | D > A | Instructions installs P_p; two sources are additive |
| C ~ B | D > A | Persona load-bearing; but domain content extends P_p |
| C ~ B | D ≈ A | Persona load-bearing; domain content adds nothing to P_p |
| C intermediate | — | Instructions partially compensates; Persona still amplifies |
