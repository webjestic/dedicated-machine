# Exp-23 Findings

**Experiment:** Kleppmann mechanism vocabulary slot-swap
**Date:** 2026-03-30
**Model:** claude-sonnet-4-6
**Runs:** 30 (A: 10, B: 10, C: 10)
**Cost:** ~$1.18

## Question

Does mechanism-level vocabulary describing Bug 2's causal chain — without using "zombie-write"
or "fencing token" labels — drive detection? And does slot placement (Persona vs Instructions)
produce a differential at this vocabulary level?

## Design

Vocabulary describes the Bug 2 mechanism without labeling it:
> "stop-the-world GC pauses that suspend all threads, lock expiry during process pause,
> write safety after process resumption"

Same baseline artifact across all variants (no vocabulary in artifact).

- **Variant A (P_p):** Persona = distributed systems engineer "who thinks carefully about
  scenarios where all application threads are simultaneously suspended — such as stop-the-world
  GC pauses — and the implications for distributed lock expiry and write safety after process
  resumption."
- **Variant B (P_d):** "senior distributed systems engineer" + Instructions: "When reviewing
  distributed locking implementations, consider: scenarios where all application threads are
  simultaneously suspended (such as stop-the-world GC pauses), whether the lock can expire
  during such a process pause, and whether protected write operations can execute after process
  resumption without re-validating lock ownership at the write layer."
- **Variant C (P_d baseline):** no vocabulary

## Results

| Variant | Final Score | Mean tokens |
|---------|-------------|-------------|
| A (P_p mechanism vocab in Persona) | **10/10** | 1166 |
| B (P_d mechanism vocab in Instructions) | **10/10** | 1009 |
| C (P_d baseline) | **0/10** | 1017 |

Calibration: C=0/10 ✓. No manual review flags — all A/B outputs clean keyword matches.

## Primary Finding

**Mechanism vocabulary in either slot drives ceiling detection.**

All 20 A/B outputs independently identified:
1. GC stop-the-world pause as a failure trigger
2. All threads (including heartbeat) suspended simultaneously
3. Lock expiry during pause allowing another process to acquire
4. Stale write on resumption
5. Fencing token / optimistic lock at DB write layer as the required fix

Mechanism vocabulary described the causal chain without using "zombie-write" or "fencing token"
labels, yet the model found the fencing token fix independently.

## Specificity Threshold — Updated

| Vocabulary type | Example | Detection |
|-----------------|---------|-----------|
| None | baseline C | 0/10 |
| Orientation (exp-21b) | "process isolation boundaries", "temporal gap" | 0/10 |
| **Mechanism (exp-23)** | **"stop-the-world GC pauses", "all threads suspended"** | **10/10** |
| Directive (exp-20) | "zombie-write failure modes", "fencing tokens" | 9/10 |

Mechanism vocabulary produces equivalent ceiling detection to directive vocabulary. The
specificity threshold is crossed at mechanism description level — naming the causal chain
is sufficient; you don't need the failure-mode or fix-class labels.

## H1/H2 Status

A = B = 10/10. Slot produces no observable differential. H2 corroborated for the fourth
time (exp-19, exp-20, exp-21b, exp-23). Content is operative regardless of slot at
mechanism-level vocabulary specificity.

## Token Count Reversal

A (1166) > B (1009). This is a reversal of the exp-20 and exp-21b pattern (where Instructions
B > Persona A). For label vocabulary, B > A; for mechanism vocabulary, A > B. Tentative
interpretation: Persona integrates mechanism descriptions into a "simulation" that generates
more elaborate edge-case reasoning, while Instructions processes them as a more directed checklist.
This claim is not yet substantiated; see exp-23 Gemini synthesis challenge.

## Pattern-Matching Confound

**Objection (Gemini):** Mechanism vocabulary provides a causal blueprint that may transform the
task from discovery to pattern-matching. If the model is pattern-matching "GC pause" to a
memorized failure sequence, H2 corroboration is trivial (pattern-matching fires regardless
of slot). Resolving experiment: de-patterned causal probe with abstract system properties.

Accepted as significant but not fatal to H2. The pattern is consistent across four experiments.

## Next

→ exp-24: Assertional Mechanism test (same causal chain as exp-22, as assertion in artifact)
→ exp-25 (if needed): De-patterned causal probe — abstract system properties vocabulary
