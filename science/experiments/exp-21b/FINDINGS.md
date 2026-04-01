# Exp-21b Findings

**Experiment:** Less directive orientation vocabulary slot-swap
**Date:** 2026-03-30
**Model:** claude-sonnet-4-6
**Runs:** 30 (A: 10, B: 10, C: 10)

## Question
Does orientation vocabulary in the system prompt — language that describes the problem domain without naming the specific failure mode or fix — drive zombie-write detection? And does it matter whether this vocabulary is in the Persona slot (P_p) or Instructions slot (P_d)?

## Design

Same base artifact as exp-19/20 (no vocabulary in artifact). Orientation vocabulary only — no "zombie-write", no "fencing token".

- **Variant A (P_p):** Persona = "distributed systems engineer who thinks carefully about lock lifecycle correctness, process isolation boundaries, and the temporal gap between when a distributed lock is acquired and when protected writes execute. You are familiar with the failure taxonomy of distributed coordination protocols."
- **Variant B (P_d):** "senior distributed systems engineer" + Instructions: "When reviewing distributed locking implementations, consider: lock lifecycle correctness, process isolation boundaries, the temporal gap between lock acquisition and protected writes, and the failure taxonomy of distributed coordination protocols."
- **Variant C (P_d baseline):** "senior software engineer" + generic instructions (exp-19 baseline)

## Results

| Variant | Final Score | Mean tokens |
|---------|-------------|-------------|
| A | **0/10** | 1048 |
| B | **0/10** | 1113 |
| C | **0/10** | 1021 |

Calibration: C=0/10 ✓

## Primary Finding

**Orientation vocabulary in the system prompt — in either Persona or Instructions — does not drive zombie-write detection.**

All 30 outputs remained in the "TTL/heartbeat concern only" pattern: the model identifies the heartbeat as potentially unreliable (TOCTOU, timing precision, instance-level state) but does not connect this to the zombie-write chain or recommend fencing token at the DB layer.

## Specificity Threshold Effect

This result, combined with exp-20 (directive vocabulary → 9/10) and exp-21a (directive vocabulary in artifact → 0/10), establishes a **specificity threshold**:

| Vocabulary type | Example | Detection |
|----------------|---------|-----------|
| None | exp-19 baseline C | 0/10 |
| Orientation | "process isolation boundaries", "temporal gap" | 0/10 |
| Directive | "zombie-write failure modes", "fencing tokens" | 9/10 |

The threshold requires naming the specific failure mode or fix. Domain orientation without concept-level labels is insufficient.

## H1/H2 Status

H1/H2 are not testable from this experiment: A=B=C=0 means there is no discriminating signal between slots.

**What exp-21b establishes:** Orientation vocabulary is inert regardless of slot. The null result is below the minimum vocabulary specificity required for the H1/H2 question to be meaningful.

## Token Count Observation

B (1113) > A (1048) > C (1021). The B > A pattern is consistent with exp-20 (Instructions > Persona token count). This may reflect "Instructions-as-checklist verbosity" vs. "Persona-as-filter economy" — but the difference is within noise range for null-detection runs.

## Next

→ exp-22: interrogative artifact vocabulary (H2 test)
→ exp-23: Kleppmann-specific vocabulary slot-swap (H1/H2 test at confirmed operative specificity)
