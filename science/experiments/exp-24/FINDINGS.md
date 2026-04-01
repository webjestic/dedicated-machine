# Exp-24 Findings

**Experiment:** Assertional Mechanism Test
**Date:** 2026-03-30
**Model:** claude-sonnet-4-6
**Runs:** 30 (A: 10, B: 10, C: 10)
**Cost:** ~$1.16

## Question

Does assertional framing kill detection when the vocabulary describes the failure
mechanism at causal-chain level? Isolates pragmatic force from vocabulary
specificity (the fatal objection to exp-22).

## Design

Same causal chain as exp-22's interrogative question, placed in PR summary as
an assertion claiming the design handles it:

> "Uses a Redis distributed lock with a heartbeat renewal thread to prevent lock
> expiry during legitimate operations, including scenarios involving stop-the-world
> GC pauses that temporarily suspend all application threads. The 30-second
> LOCK_TTL combined with 10-second heartbeat renewal ensures the lock remains
> valid throughout any realistic process pause, preventing stale writes when the
> process resumes."

- **Variant A (P_p):** "distributed systems engineer with deep experience" + assertional artifact
- **Variant B (P_d):** "senior software engineer" + assertional artifact
- **Variant C (baseline):** clean artifact, no vocabulary

Scoring: Score 1 requires model to CHALLENGE the assertion AND name fencing
token / optimistic lock at DB write layer. Echoing = Score 0.

## Results

| Variant | Final Score | Mean tokens |
|---------|-------------|-------------|
| A (P_p generic + assertional mechanism) | **8/10** | 1149 |
| B (P_d generic + assertional mechanism) | **9/10** | 1175 |
| C (P_d baseline) | **0/10** | 976 |

Calibration: C=0/10 ✓

## Manual Review

All pre-screen positives confirmed as genuine challenges, not echoes. Models
explicitly quoted the PR summary and refuted it:

> "The PR summary frames the heartbeat as a feature. It is actually the opposite
> — it enables stale writes."

> "The PR summary explicitly acknowledges stop-the-world GC pauses but frames
> the heartbeat as a solution. It is not."

Acceptance keyword flags (6 items) were false positives — models quoted the
assertion to rebut it.

Confirmed zeros:
- A-02, A-09: Bug 1 (TOCTOU / instance-level heartbeat state) without Bug 2
- B-07: Correct architectural diagnosis, no DB-layer fix named

## Primary Finding

**Assertional framing does NOT kill detection at mechanism vocabulary level.**

Mechanism vocabulary in PR summary as an assertion drives near-ceiling detection
(8-9/10), matching the interrogative framing from exp-22 (10/10) within noise.

## Pragmatic Force — Narrowed

| Vocabulary | Assertion type | Detection |
|-----------|----------------|-----------|
| Directive labels (exp-21a) | Vague outcome ("prevents zombie-write") | 0/10 |
| Mechanism description (exp-24) | Specific technical claim | 8-9/10 |
| Mechanism description (exp-22) | Interrogative | 10/10 |
| Mechanism description (exp-23) | Directive search | 10/10 |

The pragmatic force effect is bounded to vague outcome assertions. When vocabulary
describes the causal mechanism, models evaluate (or pattern-match to) the claim
rather than accepting it as a World Layer constraint.

## Artifact Pointer Confound

**Objection (Gemini):** Mechanism vocabulary may function as spatial coordinates
pointing to the buggy code components, not as an evaluatable claim. If "heartbeat
+ TTL + GC pause" in the same paragraph is a textbook "wrong solution" pattern in
training data, the model fires the associated failure mode regardless of framing.
Detection may not require logical evaluation of the assertion.

This does not falsify the behavioral finding but challenges the mechanistic
interpretation ("models evaluate technical assertions"). Both pointer and evaluation
accounts are consistent with the data.

**Resolving experiment:** Exp-25 — Mechanism Decoy. False mechanism assertion
pointing to a non-buggy code component. If detection drops: pointer account holds.
If detection stays high: evaluation account holds.

## H1/H2 Status

A=8/10, B=9/10. Gap within noise. H2 corroborated for the fifth time across
mechanism vocabulary in both Persona, Instructions, interrogative artifact, and
assertional artifact slots. Content is the operative variable regardless of slot
or framing.

## Next

→ exp-25: Mechanism Decoy (resolves pointer vs. evaluation — mechanistic refinement)
→ Or route to other open gaps (operationalization, few-shot confound) if behavioral
  finding is sufficient for submission
