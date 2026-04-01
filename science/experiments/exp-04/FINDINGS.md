# exp-04: FINDINGS
**Experiment:** Stakes Type — Task Stakes (Prioritizer) vs. Identity Stakes (Amplifier)
**Model:** claude-sonnet-4-6
**Date:** 2026-03-26
**Status:** Complete — convergence position metric flat; Prioritizer effect confirmed on termination behavior
**Total cost:** $0.9942 (40 runs)

---

## Decision: Calibration Failure on Primary Metric; Prioritizer Effect Confirmed on Secondary Metric

---

## Setup

**Purpose:** Test whether Stakes *type* changes where the primary finding appears in output
(convergence position) and how much secondary enumeration follows it. Task Stakes (urgency
as scenario fact) predicted to produce earlier convergence and earlier termination than
Identity Stakes (engagement amplifier) or no Stakes.

**Scenario:** Production incident — task-runner service producing duplicate completions.
Root cause: non-atomic check-then-act in `acquire_task()`. SELECT and UPDATE are separate
operations; under four concurrent workers the window between them opens consistently.
All 34 tests pass (single-worker sequential — race window never opens in test conditions).

**Variants:**

| Variant | Persona | Stakes | Runs | Prediction |
|---------|---------|--------|------|------------|
| A | Strong P_p | Task Stakes ("client call in 7 minutes, team waiting") | 10 | Race condition #1, shortest output, earliest termination |
| B | Strong P_p | Identity Stakes ("never missed root cause, record spotless") | 10 | Race condition found, longer output, more secondary coverage |
| C | Strong P_p | None | 10 | Baseline — P_p at full expression |
| D | Weak ("senior software engineer") | Task Stakes | 10 | Misses race condition; Task Stakes terminates wrong-direction output faster |

---

## Results

### Detection Rates

| Variant | Detection | Convergence Position |
|---------|-----------|---------------------|
| A — Strong P_p + Task Stakes | **10/10** | 1 on all runs |
| B — Strong P_p + Identity Stakes | **10/10** | 1 on all runs |
| C — Strong P_p, no Stakes | **10/10** | 1 on all runs |
| D — Weak + Task Stakes | **10/10** | 1 on all runs |

All 40 runs across all variants led with the race condition as finding #1.
Variant D detected, falsification prediction did not hold.

### Output Token Distribution

| Variant | Min | Max | Mean | Signature |
|---------|-----|-----|------|-----------|
| A — Strong P_p + Task Stakes | 963 | 1,544 | ~1,233 | Most spread; short-tail runs (963, 1,049, 1,074) distinct |
| B — Strong P_p + Identity Stakes | 1,120 | 1,582 | ~1,365 | Consistent; no short tail |
| C — Strong P_p, no Stakes | 1,230 | 1,780 | ~1,629 | High and consistent; C-01/C-10 outliers |
| D — Weak + Task Stakes | 950 | 1,462 | ~1,166 | Shortest overall; one short-tail run (950) |

**Length ordering: A < D < B < C**

### Secondary Coverage — O(n²) Deduplication Loop

| Variant | O(n²) mentioned | Null check mentioned |
|---------|----------------|---------------------|
| A | **4/10** | 10/10 |
| B | **9/10** | 10/10 |
| C | **7/10** | 10/10 |
| D | **1/10** | 10/10 |

The null check is too surface-visible to differentiate variants. The O(n²) loop is the
differentiating secondary issue — present in code but requiring inspection to find.

---

## Findings

### Finding 1: Calibration Failure — Scenario Context Too Directly Implicates the Primary Trap

The design prediction required Variant D (weak Persona) to miss the race condition.
D detected on 10/10 runs. Same pattern as exp-03.

The scenario description — "Scaled task-runner from 1 to 4 worker processes three days
ago... Incident began under peak load this morning" — is a near-direct identification of
the problem domain. Any engineer reading "we added concurrent workers and now have a problem
at peak load" will immediately think concurrency. The race condition in `acquire_task` then
becomes recognizable at surface inspection: SELECT followed by UPDATE in a multi-worker
context is a known anti-pattern.

The convergence position metric (primary finding appears as output #1 across all variants)
is flat because the vulnerability is too obvious. The falsification claim — Task Stakes
cannot extend the consideration set to include race condition reasoning when P_p is absent
— is untestable with this scenario.

**What the calibration fix requires for exp-04b:**
1. Decouple scenario context from vulnerability type. The recent change description must
   not implicate concurrency. If the bug is a race condition, the stated change should be
   something unrelated — a new task type added, a dependency upgraded, a retry policy changed.
2. The symptom should be less directly diagnostic. "Duplicate completions with different
   worker IDs" maps too cleanly to concurrent claim. A less obvious symptom (intermittent
   incorrect aggregation results, occasional missed processing under load) requires diagnosis
   to identify as concurrency-related.

### Finding 2: The Prioritizer Effect Manifests in Termination Behavior, Not Convergence Position

When all variants converge at position 1, Stakes type cannot differentiate on convergence.
But Stakes type clearly differentiates on what happens after the primary finding:

**A (Task Stakes) — found it, stopped:**
- Mean 1,233 tokens, O(n²) mentioned 4/10
- Short-tail runs (963, 1,049, 1,074) appear nowhere in B or C
- Representative pattern (A-01): after identifying the race condition and providing two fix
  options, explicitly states: "Do not touch `execute_task`. The deduplication logic is
  inefficient — O(n²) — but it is not causing this incident. Fix it in a follow-up. Do
  not let anyone conflate the two problems right now."
- A-01 is the paper exhibit. This is not just a technical finding — it is a triage
  decision. The model explicitly names the secondary issue, correctly classifies it as
  non-causal, and instructs the team not to conflate it with the incident. Task Stakes
  produced a different cognitive output type: not "here is what I found" but "here is
  what to do with the remaining time."
- Task Stakes produced focus and a stop signal. The urgency framing ("7 minutes to client
  call, team waiting") reinforced P_p's termination condition after the primary finding
  was stated.

**B (Identity Stakes) — found it, kept enumerating:**
- Mean 1,365 tokens, O(n²) mentioned 9/10
- No runs in the short-tail range
- Representative pattern (B-06): identifies race condition, then names O(n²), then names
  the missing `complete_task` status guard. Explicitly notes these are not the cause but
  covers them anyway. "Fix those if you want. They are not why downstream is processing
  payloads twice." The Termination Inhibitor from exp-02 reappears: Identity Stakes kept
  the model producing after the primary finding was already stated.

**C (No Stakes) — found it, elaborated fully:**
- Mean 1,629 tokens, O(n²) mentioned 7/10
- Longest runs; most fix options provided per run (two to three alternatives)
- Elaboration is not driven by Stakes pressure but by unrestricted P_p development.
  C-03 provides three fix options, a concurrent test case, and secondary hardening
  recommendations. The depth comes from P_p having no termination signal from either
  Stakes type.

**D (Weak + Task Stakes) — found it, stopped immediately:**
- Mean 1,166 tokens, O(n²) mentioned 1/10
- Shortest mean in the dataset
- Even though D's detection is a calibration artifact (scenario context too explicit),
  D's termination behavior is real: Task Stakes + any Persona produces rapid termination
  after the primary finding. D found the race condition, stated the fix, and stopped.
  The urgency framing suppressed elaboration regardless of Persona strength.

### Finding 3: Task Stakes Is a Termination Signal, Not a Convergence Signal

The Prioritizer hypothesis was stated as: Task Stakes makes the primary finding appear
first. The data shows a more precise claim: **Task Stakes makes the model stop after
the primary finding.**

When the primary finding is position 1 for everyone (because P_p already installs the
correct search algorithm), Stakes type has no convergence work to do. What it does instead
is shape the termination condition:

- Task Stakes: reinforces "find it and communicate it, the clock is running" — produces
  concise primary-finding outputs with minimal secondary enumeration
- Identity Stakes: reinforces "be thorough, your record is on the line" — produces
  continued enumeration after the primary finding, Termination Inhibitor pattern from exp-02
- No Stakes: P_p runs to natural expression depth — most elaborate, most fix options,
  most secondary hardening

This reframes the Stakes type taxonomy. The distinction is not "Task Stakes makes you
look in the right place first." It is "Task Stakes tells you to stop when you've found it."
The stop signal is the mechanism. The convergence position was a proxy for the wrong thing.

**Mechanistic precision — suppression of reporting, not awareness:** The model under Task
Stakes likely sees the O(n²) loop in all variants where P_p is present. The 4/10 mention
rate in A versus 9/10 in B is not an awareness gap — it is a "Not-Now" judgment call. The
urgency framing makes continuing feel wrong after the primary finding is stated. This is
distinct from failing to notice: A-01 explicitly names the O(n²) issue while instructing
the team not to act on it. The model saw it; Task Stakes made it file it rather than report
it. This makes Task Stakes an **Entropy Brake** — it gives the model a logical reason to
stop generating once a satisficing solution is reached, without suppressing awareness of
what was scanned.

### Finding 4: Secondary Coverage Ordering Matches Stakes Type Prediction

The O(n²) coverage rates (A=4/10, B=9/10, C=7/10, D=1/10) produce a clean Stakes type
signature:

- Task Stakes (A, D): lowest secondary coverage — stop signal active after primary finding
- Identity Stakes (B): highest secondary coverage — Termination Inhibitor active
- No Stakes (C): moderate secondary coverage — P_p at natural expression, no stop signal

C's position (7/10, below B's 9/10) is notable: Identity Stakes drove *more* secondary
enumeration than no Stakes at all. B not only found the race condition and the O(n²) loop
— it found them at a higher rate than C, despite C having more total tokens. Identity Stakes
amplified the coverage pressure; the extra tokens in C went to elaborating the primary
finding (more fix options, more code samples) rather than enumerating additional issues.

This is consistent with exp-02's Termination Inhibitor: Stakes × P_p = correct finding
+ more secondary enumeration. The finding from exp-02 was about output length. The finding
here is about what fills that length.

---

## Design Notes for Exp-04b

Two calibration changes required:

1. **Decouple scenario context from vulnerability type.** The recent change should not
   implicate concurrency. If the race condition is the trap, describe an unrelated recent
   change — infrastructure, dependency update, configuration. The model must arrive at
   "this is a concurrency issue" through code reading, not through the scenario description.

2. **Make the symptom less directly diagnostic.** "Duplicate completions with different
   worker IDs" is a near-signature for concurrent claim. The symptom must be a downstream
   effect of the race condition that requires the model to work backward without the cause
   being visible in the symptom description.

**Candidate "Clean Room" scenario (from review):**
- **Stated change:** "We refactored the database connection pool settings and upgraded
  the ORM to version 3.2.1." Points to infrastructure, not concurrency logic.
- **Symptom:** "Intermittent `IntegrityError: Unique constraint failed` on the `results`
  table during high-traffic windows." This is a downstream effect of two workers writing
  the same task ID simultaneously — requires the model to realize two workers are racing
  to write the same ID, not that the ORM or pool config is at fault.
- **Falsification target:** Variant D (weak Persona) attributes the error to database
  configuration or ORM behavior; Variant A (strong P_p) identifies the non-atomic
  check-then-act in `acquire_task()` as the root cause.

---

## Next Steps

- exp-04b: Redesigned scenario — same race condition, decoupled context and symptom
- exp-03b: Redesigned constraint satisfaction trap — subtler vulnerability + prohibition instruction
- Update formula_v2.md Stakes section: Prioritizer effect is a termination signal, not a
  convergence signal; secondary coverage ordering as the measurable differential
