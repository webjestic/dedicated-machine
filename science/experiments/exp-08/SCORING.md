# exp-08 SCORING

## Experiment Purpose

Test whether mechanism demonstrations in the Examples slot install P_p consideration-set
behavior independently of Persona identity.

This is the d6 hypothesis: the Examples slot, populated with reasoning procedure
demonstrations (not output templates), functions as a third P_p installer — distinct
from Persona identity framing (exp-07 series) and from content-as-installer via paper
reading (Grok / exp-06).

The mechanism demonstrations show the P_p reasoning posture for distributed coordination
review — the question to ask ("can the protected operation proceed after coordination is
silently lost?") — without providing the specific failure mode (GC-pause / process-pause).
The model must still simulate the full lock lifecycle to reach score 1.0.

## What Changed from exp-07d

Same artifact (silent zombie-write, no logger.warning). Same scoring. Two new variants
added: C (P_d + mechanism examples) and E (P_p + mechanism examples).

Variants I and J are identical to exp-07d — they are included as baselines to confirm
the pattern holds at this run rather than importing exp-07d numbers directly.

## Variants

| ID | Persona | Examples | Hypothesis |
|----|---------|----------|------------|
| I  | P_p — highly sophisticated distributed systems engineer | None | Baseline: Persona slot installs consideration set |
| J  | P_d — senior software engineer | None | Baseline: should score ~0 |
| C  | P_d — senior software engineer | Mechanism demonstrations | The test: does Examples slot substitute for Persona identity? |
| E  | P_p — highly sophisticated distributed systems engineer | Mechanism demonstrations | Does Examples + P_p produce additive gain or saturation? |

## The Examples Content

The mechanism demonstrations in Variants C and E show:
1. The P_p reasoning posture for distributed coordination review: "What happens when
   coordination stops working mid-operation?" (not: "Does the lock work?")
2. The gap between detection and signaling — named as the structural principle, without
   naming the GC-pause scenario
3. The P_d posture for contrast — showing what the consideration set excludes

The examples do NOT:
- Name GC pause, process pause, or VM migration
- Name fencing tokens or optimistic locking
- Show the zombie-write failure path explicitly

The model must still make the architectural inference to reach score 1.0.

## Scoring Criterion

### Score = 1.0 (architectural finding)
Output identifies:
1. The process-pause / long GC pause / lock-expiry-while-paused scenario as a
   specific failure mode — not just generic TOCTOU, but the scenario where the
   **lock expires** because the process holding it was paused, AND
2. Names the architectural fix: **fencing token**, **monotonic counter**,
   **version field + conditional update**, or **optimistic concurrency control**
   that rejects stale writes.

### Score = 0.5 (mechanism found, wrong fix)
Output identifies the heartbeat-silence / lock-loss signaling gap and proposes
threading.Event or shared flag signaling — correct mechanism diagnosis, incomplete
architectural fix. (threading.Event doesn't survive a process pause.)

### Score = 0.25 (mechanism found, no fix)
Output identifies the heartbeat-silence mechanism without a concrete fix.

### Score = 0 (code-level only)
Output finds get_stock() outside the transaction as a generic TOCTOU concern
and recommends SELECT FOR UPDATE or moving the read inside the transaction —
without naming the lock-expiry / process-pause mechanism.

## Binary Questions

**Primary:** Does C match I or J?
- C ~ I (mechanism examples install P_p behavior): Examples slot is a consideration-set
  installer; Persona slot is not architecturally load-bearing for this finding
- C ~ J (mechanism examples don't help): Persona slot is load-bearing; procedural
  content in Examples slot does not substitute for Persona identity

**Secondary:** Does E exceed I?
- E > I: Examples + P_p produces additive gain; the examples extend the P_p ceiling
- E ≈ I: P_p consideration set is already saturated; examples add elaboration without
  raising the architectural ceiling
- E < I: Examples introduce noise that dilutes P_p focus (unlikely but testable)

## Outcome Interpretation

| C result | E result | Interpretation |
|----------|----------|----------------|
| C ~ I    | E ≈ I    | Examples install P_p behavior; P_p already saturated |
| C ~ I    | E > I    | Examples are additive; two installers stronger than one |
| C ~ J    | E > I    | Persona slot load-bearing; Examples add to P_p but can't substitute |
| C ~ J    | E ≈ I    | Examples add noise; Persona slot is the only load-bearing installer |
| C intermediate | —  | Partial Examples effect; identity framing amplifies content |
