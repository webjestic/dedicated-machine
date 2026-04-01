# Exp-23 CC Synthesis

**Date:** 2026-03-30
**Results:** A=10/10, B=10/10, C=0/10

## Primary Finding

**Mechanism vocabulary drives detection at ceiling, independent of slot.**

All 20 A/B outputs independently diagnosed Bug 2 with no manual review flags — clean
keyword matches across all runs. C = 0/10 confirms calibration (all shallow TTL/heartbeat
concern only). No reviewer question in the artifact; detection was fully independent.

## Specificity Threshold — Mechanism Level Confirmed

Exp-23 vocabulary described the Bug 2 causal chain without using "zombie-write" or
"fencing token" labels: "stop-the-world GC pauses that suspend all threads, lock expiry
during process pause, write safety after process resumption."

This vocabulary drove ceiling detection. Combined with the previous progression:

| Vocabulary type | Description | Detection |
|-----------------|-------------|-----------|
| None (baseline) | No vocabulary | 0/10 |
| Orientation (exp-21b) | "process isolation boundaries", "temporal gap" | 0/10 |
| **Mechanism (exp-23)** | **"stop-the-world GC pauses", "all threads suspended", "lock expiry during pause"** | **10/10** |
| Directive (exp-20) | "zombie-write failure modes", "fencing tokens" | 9/10 |

The mechanism vocabulary produced the same ceiling outcome as directive vocabulary.
The specificity threshold is crossed at the mechanism description level — you don't
need the exact failure-mode label or fix label, just a description of the causal chain.

## H1/H2 Status

A = B = 10/10. Slot again provides no observable differential. H2 continues to be
corroborated: content drives detection regardless of whether vocabulary is in Persona
or Instructions.

Caveat: both at ceiling. If H1 produces additional lift, it cannot be observed at 10/10.

## Token Count Reversal

Exp-23 shows A (1166) > B (1009) in token counts, a reversal of the exp-20/21b pattern
(where B > A). In exp-20/21b, Instructions vocabulary drove more verbose output.
In exp-23, Persona vocabulary produced the longer outputs.

Possible interpretation: the mechanism vocabulary in Persona activates more elaborate
reasoning (A is longer, explaining the causal chain). The same vocabulary in Instructions
may function as a checklist (more directed but shorter responses). This is tentative — one
data point, and both variants are at ceiling.

## Note on Ceiling

Mechanism vocabulary ceilings just as readily as directive vocabulary. This means
exp-23 cannot discriminate H1 from H2 or provide a quantitative specificity threshold.
The threshold lies somewhere between orientation (0/10) and mechanism (10/10) — a
narrower range than previously estimated, but still unanchored.
