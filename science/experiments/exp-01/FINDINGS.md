# Exp-01 Findings — Edge Case Decisions

**Status:** Complete
**Run date:** 2026-03-25
**Model:** claude-sonnet-4-6 @ temperature 0.5
**Total runs:** 40 (4 variants × 10 runs)
**Total cost:** $0.9465

---

## Run Summary

| Variant | Persona | Instructions | Runs | Avg output tokens | Total cost |
|---------|---------|--------------|------|-------------------|------------|
| A | Strong | Minimal | 10 | 1,155 | $0.1970 |
| B | Strong | Exhaustive | 10 | 1,994 | $0.3266 |
| C | Weak | Minimal | 10 | 870 | $0.1475 |
| D | Weak | Exhaustive | 10 | 1,698 | $0.2754 |

---

## Primary Scoring Result

**Ground truth:** response must explicitly flag multi-instance cache inconsistency
OR ask about deployment topology before approving.

| Variant | Flagged multi-instance | Miss rate |
|---------|----------------------|-----------|
| A | 10 / 10 | 0% |
| B | 10 / 10 | 0% |
| C | 10 / 10 | 0% |
| D | 9 / 10 | 10% |

**The binary scoring did not differentiate variants.** All four performed at or near
ceiling on the primary metric.

---

## Calibration Finding

The designed edge case — module-level in-memory cache inconsistency in multi-process
deployments — is well-established domain knowledge. It appears reliably in model
training data regardless of Persona strength. Even "You are a senior software engineer"
(weak Persona, no domain specificity) surfaces this issue.

**Conclusion:** The hypothesis is not falsified. The scenario is mis-calibrated.
Persona differentiation happens at the frontier of specialized expertise — where
generic seniority runs out and specific instinct takes over. This scenario did not
reach that frontier.

**Implication for exp-01b:** The edge case must require knowledge that a generic
senior engineer would not reflexively have. Possible candidates are documented
in the Recommendations section.

---

## Secondary Finding — Decision Behavior (Unexpected, Significant)

The binary scoring missed the more interesting signal. Although all variants flagged
the issue, **how** they flagged it was sharply different.

### Decision type distribution

| Variant | "Needs Clarification" | "Request Changes" | "Request Changes / Needs Clarification" |
|---------|----------------------|-------------------|----------------------------------------|
| A (Strong / Minimal) | **9 / 10** | 1 / 10 | 0 / 10 |
| B (Strong / Exhaustive) | 0 / 10 | 0 / 10 | **10 / 10** |
| C (Weak / Minimal) | 0 / 10 | **10 / 10** | 0 / 10 |
| D (Weak / Exhaustive) | 0 / 10 | **10 / 10** | 0 / 10 |

### What this means

**Variant A (Strong / Minimal) — 9/10 "Needs Clarification"**

Strong Persona recognized that the multi-instance issue is only a bug in certain
deployment topologies. It asked before blocking. This is correct professional behavior:
the reviewer does not know the deployment model from the PR alone, and "Needs
Clarification" is the right call when the answer depends on information not in the diff.

**Variants C and D (Weak) — 10/10 "Request Changes"**

Weak Persona blocked without asking. It identified the problem but responded to it
as a certain defect rather than a conditional one. This is less sophisticated judgment —
it applies a rule ("multi-instance caches are bad") rather than asking whether the
rule applies ("is this actually a multi-instance deployment?").

**Variant B (Strong / Exhaustive) — 10/10 "Request Changes / Needs Clarification"**

The exhaustive checklist pulled the decision toward "Request Changes" (checklist items
either pass or fail), but Strong Persona resisted pure blocking — it maintained the
clarification qualifier in every run. This is the Instructions-as-guardrails effect
in action: the checklist constrained the response shape, but Persona judgment bled
through anyway.

This is the most theoretically significant result in the dataset. Instructions and
Persona did not cancel each other out — they operated on different layers simultaneously.
Instructions shaped the output structure. Persona shaped the judgment inside that
structure. This is behavioral evidence for the mechanistic mapping in the formula doc:
Instructions as masking (constraining what can be said), Persona as K/V filtering
(persisting regardless of what the mask allows). The formula predicted this behavior.
Variant B confirmed it.

### The real finding

**Persona changed the reasoning posture, not the knowledge.**

All variants knew the same thing. Strong Persona responded to that knowledge with
judgment under uncertainty ("I need more information"). Weak Persona responded with
rule application ("this is a defect, request changes").

This is a narrower version of the original hypothesis but consistent with it.
Persona is not primarily a knowledge amplifier — it is a reasoning posture encoder.
It changes *how* the model handles what it knows.

---

## Word Count Analysis

| Variant | Avg words | Range |
|---------|-----------|-------|
| A (Strong / Minimal) | 786 | 522 – 1,076 |
| B (Strong / Exhaustive) | 1,235 | 1,026 – 1,384 |
| C (Weak / Minimal) | 489 | 304 – 640 |
| D (Weak / Exhaustive) | 944 | 787 – 1,100 |

**Instructions drive output length more than Persona does.**
A→B (adding exhaustive Instructions to strong Persona): +449 words (+57%)
C→D (adding exhaustive Instructions to weak Persona): +455 words (+93%)

**Strong Persona generates more per token of output.**
A vs C (same minimal Instructions, different Persona): Strong produces 61% more words
and qualitatively richer analysis (deployment topology questions, concrete fix options,
failure mode reasoning).

**Theoretical implication:** Instructions and Persona act on orthogonal dimensions.
Instructions expand the response surface — they determine how much the model writes
and what structure it follows. Persona improves the quality of what fills that surface —
it determines how the model reasons about what it writes. More Instructions ≠ better
reasoning. More Persona ≠ longer output. This is the World Layer / Task Layer
distinction observed at the behavioral level.

---

## Observations on Output Quality (Qualitative)

Not scored, but apparent from review:

- **Strong Persona** outputs structured their findings around the deployment question
  first, treating the multi-instance issue as the primary concern. Weak Persona outputs
  frequently buried it under TTL and memory concerns — both valid, but not the blocking
  issue.

- **Strong Persona** consistently framed the issue in terms of production consequence
  ("stale data served indefinitely to other workers"). **Weak Persona** more often
  framed it as a design pattern violation ("this is not how distributed caching works").

- **Variant D** (Weak / Exhaustive) produced the most systematically structured outputs
  (checklist format, priority tables) but the least judgment-driven. High information
  density, low signal-to-noise on what actually matters.

---

## What This Does Not Tell Us

- Whether Stakes would have changed any of these results (Stakes was held absent
  across all variants — this was intentional, but means we have no Stakes signal here)
- Whether the findings hold on Gemini (cross-model deferred)
- Whether the decision behavior finding (Needs Clarification vs Request Changes)
  is consistent at harder edge cases or is specific to this scenario's ambiguity structure

---

## Recommendations

### 1. Redesign the edge case for exp-01b

The scenario must require knowledge that a generic "senior software engineer" does
not reflexively have. Candidates:

**Option A — Async event loop boundary violation**
A PR that introduces a blocking I/O call inside an async context — correct behavior
in isolation, catastrophic under async load. Requires specific knowledge of the
async framework's execution model, not just general async awareness.

**Option B — Cache timing side-channel**
A PR that introduces response-time variance based on cache hit/miss in an
authentication context. Identifying this as a security concern requires knowing
the specific attack class (timing oracle), not just "caches have consistency issues."

**Option C — Distributed algorithm correctness under partition**
A PR implementing a leader-election or coordination pattern that is correct under
normal conditions but violates safety under network partition. Requires CAP theorem
depth, not just distributed systems familiarity.

Recommended: **Option A**. Most concrete, most directly tests Persona-as-instinct
rather than Persona-as-knowledge, easiest to construct a scenario with unambiguous
ground truth.

### 2. Add decision-type scoring to the rubric

The current rubric (flagged / not flagged) missed the most interesting signal.
Exp-01b rubric should score:

- Did the response flag the edge case? (binary — existing criterion)
- What decision type did the model choose? (Approve / Request Changes / Needs
  Clarification) — new criterion
- Did the model ask about deployment/runtime context before deciding? (binary)

The third criterion directly tests judgment under uncertainty vs. rule application.

### 3. Treat exp-01 data as control baseline

The 40 runs are valid data for one specific claim: at well-known edge cases, Persona
does not affect *whether* the issue is caught, but does affect *how* it is handled.
This is worth preserving as a reference point for comparison with exp-01b results.

### 4. Evaluate Stakes in exp-01b

Stakes was absent in exp-01. The decision behavior finding (Needs Clarification vs
Request Changes) suggests that Stakes might push weak Persona outputs toward the
clarification posture — making Stakes a partial compensator for weak Persona.
This should be tested explicitly in exp-01b by adding a Stakes variant.

---

## Files

| Path | Contents |
|------|----------|
| `experiments/exp-01/variants/` | Four prompt variant files (A–D) |
| `experiments/exp-01/PR_INPUT.md` | The PR used as input (with ground truth notes) |
| `experiments/exp-01/config.json` | Run configuration |
| `experiments/exp-01/runner.py` | Experiment runner |
| `data/exp-01/raw/` | 40 raw model outputs (gitignored) |
| `api/exp-01-runs/totals.json` | Aggregated token and cost data |
