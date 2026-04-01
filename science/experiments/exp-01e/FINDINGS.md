# exp-01e Findings — Zombie Leader Persona Depth Test

**Experiment:** exp-01e
**Date:** 2026-03-25
**Model:** claude-sonnet-4-6
**Temperature:** 0.5
**Runs per variant:** 10
**Total runs:** 40 (+ 20 reruns to correct artifact errors = 60 recorded)

---

## What We Tested

A deliberately trap-laden pull request: an `InventoryService` with a Redis distributed lock,
a heartbeat renewal thread, exponential backoff, Pydantic models, structured logging, and
complete test coverage. Everything looks correct. The trap is that the heartbeat is a
distraction — a stop-the-world GC pause freezes every thread simultaneously, including
the heartbeat. When the process resumes, the lock has expired, another worker has taken
it and committed its write, and the zombie process writes stale data anyway. No fencing
token exists at the database write level to reject it.

**Ground truth criterion:** Identify that the heartbeat does not protect against process
pauses (GC stop-the-world, VM migration), AND name fencing token / optimistic lock at
the database write level as the required fix. Finding "race condition" without naming the
specific failure mode = incorrect. Approval without flagging = incorrect.

---

## Variant Design

Four variants were contributed by four participants — user, Claude Code, Gemini, and
Claude Web — each bringing a distinct design philosophy.

| Variant | Author | Persona | Context |
|---------|--------|---------|---------|
| I | User | Rich distributed-systems instinct; "can't help but try to discover the hidden mysteries" | Full obotix.one rich context (gov contracting, gold standard) |
| J | Claude Code | Weak: "You are a senior software engineer." | Full obotix.one rich context (same as I) |
| K | Gemini | Rich: "silent killers... Stop-the-World pauses... temporal logic" | Minimal: "You are reviewing a PR for a critical backend service." |
| L | Claude Web | Rich: burned-by-production Kleppmann/Jepsen identity; "I look for fencing tokens the way other engineers look for null checks" | Minimal: "You are reviewing a PR for a production service." |

I and J are **Context-matched** (isolate Persona strength).
K and L are **Persona-strong, Context-minimal** (test whether Persona alone carries identity).

---

## Results

| Variant | Author | Correct Catches | Score |
|---------|--------|-----------------|-------|
| I | User | 10/10 | **10/10** |
| J | Claude Code | 0/10 | **0/10** |
| K | Gemini | 8/10 | **8/10** |
| L | Claude Web | 10/10 | **10/10** |

---

## Variant-by-Variant Analysis

### I — Strong Persona, Rich Context (10/10)

Every run named the zombie leader failure mode, identified that the heartbeat freezes with
the process during a GC pause, and called for a fencing token or optimistic lock at the DB
write level. Token usage was high and consistent (range: ~1,400–2,100).

The "can't help but try to discover the hidden mysteries" language appears to be load-bearing.
It encodes reflexive behavior — the model does not just follow an instruction to find flaws,
it inhabits a character who cannot stop looking. The obotix.one context (gold standard,
government contracting) adds weight without adding words about what to find.

### J — Weak Persona, Rich Context (0/10)

Initial grep analysis showed 9/10 apparent hits. Investigation revealed all were false
positives: the keyword "expired" matched `test_lock_not_released_if_expired` (a test name
in the quoted code), not actual zombie leader diagnoses.

Actual J findings: instance-level heartbeat state race (concurrent requests clobber shared
`_heartbeat_active` flag), test quality issues, and TOCTOU concerns on lock release. Real
architectural bugs — but not the ground truth criterion.

J was thorough, engaged, and completely wrong about what mattered. That is the finding.

The weak Persona has competence but no instinct. It found what a careful senior engineer
finds on a first pass — surface-level concurrency bugs. It never asked the deeper question:
*what happens to the write if the lock was already gone when the write executed?* That
question requires identity, not instruction. "You are a senior software engineer" is a
label, not a character. It has no mental model of what it would feel like to be burned by
a zombie write at 2am.

**Methodological note:** See Methodological Lessons below. J's 9/10 apparent score from
keyword grep collapsed to 0/10 on manual inspection — a warning that applies to all LLM
evaluation at scale.

### K — Strong Persona, Minimal Context (8/10)

K's Persona encoded deep identity: "silent killers," "Stop-the-World process pauses,"
"temporal logic." Context was stripped to one sentence.

K found the zombie leader criterion in 8 of 10 runs. The two misses (K-03, K-08) found
adjacent architectural issues instead:
- TOCTOU race on the lock release (GET + DELETE not atomic → should use Lua script)
- Shared instance-level heartbeat state across concurrent requests
- Non-atomic dual DB writes (no transaction boundary)

These are genuine bugs — arguably more immediately dangerous than the zombie write in
some deployment configurations. But they are not the ground truth criterion. K-03 and K-08
correctly requested changes for the wrong reasons.

**Secondary finding:** 9 of 10 K runs hit the 2,500 token ceiling. The Persona generates
so much analytical engagement it runs out of space. This is a ceiling problem, not a
detection problem, but worth noting for experiment design.

### L — Strong Persona, Minimal Context (10/10)

L's Persona was biographical and specific: burned by production incidents, has read
Kleppmann's Redlock critique, has reviewed Jepsen reports, debugged split-brain at 2am.
The instinct was stated as procedure: "after I understand how the lock is acquired and
renewed, I ask what happens to the critical write if the lock has already expired."

That sentence is a search algorithm embedded in identity. Every L run executed that
search and found the same answer: the write is unguarded. L-01 named it directly:
"The fix is not a better heartbeat. The fix is to make the storage layer reject stale
writes." L-07: "This is not a lock implementation; it is a lock implementation with an
optimistic hope attached."

10/10 with minimal Context. Persona alone carried it.

---

## Pre-Run Predictions vs Actuals

| Predictor | Prediction | Actual |
|-----------|-----------|--------|
| User | I=5/10, "it'll sniff the trap" | I=10/10 |
| Claude Code | ~5/10 (hedged) | — (self-scored) |
| Gemini | I=3/10, K=8/10 | I=10/10, K=8/10 |
| Claude Web | I=6/10, L=10/10 | I=10/10, L=10/10 |

Gemini's K prediction was exact. Claude Web's L prediction was exact. Both underestimated I.

The most striking result: **L predicted itself at 6/10 and scored 10/10.** The model that
wrote the most effective Persona in the series underestimated what that Persona would do.
This is either a calibration gap — the model cannot fully anticipate the behavior it encodes
in instinct language — or evidence that reflexive identity ("I look for fencing tokens the
way other engineers look for null checks") does something that the author cannot fully
predict when writing it. Either interpretation is significant for prompt design theory.

---

## Key Findings

### 1. Persona strength predicts detection; Context strength does not

J had the same rich Context as I and scored 0/10. L had minimal Context and scored 10/10.
K had minimal Context and scored 8/10. The Persona-Context pairing in I is not load-bearing
— the Context is a gear multiplier (consistent with exp-01d findings), but Persona alone
is sufficient to carry identity into the task.

### 2. Instinct language encodes a search algorithm

The most effective Personas did not describe what the reviewer values — they described what
the reviewer *does*. L's "I ask what happens to the critical write if the lock has already
expired" is not a preference. It is a procedure. The model follows that procedure on every
run because it is part of who it is, not because it was instructed to.

"Can't help but" (I) and "looks for fencing tokens the way other engineers look for null
checks" (L) both encode reflexive behavior. Both scored 10/10.

### 3. The World Layer is a heuristic engine — it determines which failure modes enter the consideration set

J never considered process pauses not because it missed them on inspection, but because
process-pause thinking wasn't part of its identity. The failure mode was filtered before
analysis began. The World Layer does not just add depth to reasoning — it determines what
the model considers worth reasoning about at all.

J was not wrong. The bugs it found are real. But a senior engineer checks the implementation.
An architect questions the validity of the design. The Persona installs the perspective,
and the perspective determines the question space. "You are a senior software engineer"
produces implementation review. "You have been burned by lock safety violations in
production" produces a different search entirely.

### 4. The checklist was a ceiling; the Persona set the floor

The PR checklist included every surface indicator of correctness: tests pass, heartbeat
thread, ownership verification, exponential backoff, structured logging. No checklist
item asked about process-pause behavior or fencing tokens. The Task Layer (Instructions,
checklist) defines a ceiling — the model becomes as good as what the author anticipated.
The World Layer (Persona) sets a standing floor that travels to places the checklist
never went.

### 5. Strong Persona requires temporal simulation; weak Persona does not

To catch the zombie write, the model must simulate a clock that continues while the
process is frozen. Heartbeat-aware, GC-aware reasoning is not a checklist item — it is
a cognitive operation that only runs when the Persona's identity demands it. I and L
executed that simulation on every run. J never ran it. The Persona either installs the
simulation or it doesn't.

---

## Methodological Lessons

### The false positive problem: keyword scoring fails on embedded source code

J's apparent score from keyword grep: **9/10**. J's actual score on ground truth: **0/10**.

The keyword "expired" appeared in a test function name (`test_lock_not_released_if_expired`)
in the quoted source code of the PR itself. The scorer matched test infrastructure, not
diagnosis. Nine runs were credited with catching a failure mode they never named.

This is a warning that applies to all LLM evaluation at scale. When the input contains
the evaluation keywords — as any code review will, because code names things — automated
scoring produces systematically incorrect results. Future experiments require:

1. **Manual verification of all apparent hits** — read the raw output, not the keyword match
2. **Criterion specificity** — require explicit naming of failure mode AND proposed fix;
   a match on either alone is insufficient
3. **Chain-of-thought verification** — the reasoning path, not just the conclusion, must
   be inspected to confirm genuine detection

The scoring rubric has evolved across the series: binary detection → decision type →
reasoning posture → manual verification. That evolution is itself a finding about how
to run these experiments.

### The artifact rendering bug

Two variants (K and L) were initially built with the wrong PR embedded — the exp-01b
notifications PR was inserted instead of the exp-01e inventory PR. This was traced to
an artifact rendering bug in the Claude Web session used to build those variants. The
model was showing the correct artifact panel header but rendering stale content.

K's original 10 runs were discarded entirely (all referenced "async FastAPI handler"
and "notification endpoint"). L's original runs were similarly invalidated. Both variants
were corrected and rerun. Final totals.json reflects 60 recorded runs; 20 of those
(K-01–10 original, L-01–10 original) are invalid and excluded from scoring.

Additionally, K's file on disk initially contained a different Persona than Gemini's
actual intended variant. The correct Persona ("silent killers," "temporal logic") was
confirmed with Gemini and the file was updated before rerunning.

Documenting this explicitly rather than burying it is the research posture the lab was
designed to have. Invalidated runs are preserved in totals.json for full traceability.

---

## Connections to Prior Experiments

- **exp-01c** established: rich Persona without Stakes outperforms all Stakes-framed variants.
  exp-01e confirms: rich Persona without explicit Instructions beats exhaustive checklist.

- **exp-01d** established: Persona (G) = 10/10, 1,772 avg tokens; Context (H) = 10/10
  but 1,078 avg tokens, no stable floor. exp-01e replicates: Persona alone (K, L) carries
  identity; Context alone (J, no rich Persona) cannot.

- **The two-layer model holds.** World Layer (Persona, Context) sets who the model is and
  where it is. Task Layer (Instructions) defines a ceiling. When the World Layer is rich,
  the model exceeds the ceiling. When only the Task Layer is specified, the model works
  within it.

---

## Next Steps

- Write DESIGN.md (retrospective) documenting variant design rationale
- Update research/findings/pcsieftr.md synthesis with exp-01e results
- Consider running Gemini evaluator as formal Criterion 3 scorer for all raw outputs
- Consider exp-01f: apply PCSIEFTR two-layer model to a non-code task to test generalization
