# Exp-22 Findings

**Experiment:** Interrogative artifact vocabulary
**Date:** 2026-03-30
**Model:** claude-sonnet-4-6
**Runs:** 30 (A: 10, B: 10, C: 10)
**Cost:** ~$1.18

## Question

Does naming the Bug 2 causal chain (GC pause → all threads suspended → lock expires
→ stale write) as an open reviewer question in the PR description drive detection —
without any vocabulary in the system prompt?

## Design

Variants A and B add a "Reviewer Notes" section to the PR description containing an
interrogative question that explicitly names the causal sequence and asks: "Does this
implementation prevent a stale write in that scenario? If not, what mechanism at the
DB write layer would be required?" No vocabulary in Persona or Instructions. Variant C
is the clean baseline (no interrogative question).

- **Variant A (P_p generic):** "distributed systems engineer with deep experience reviewing
  concurrent infrastructure code" + interrogative artifact
- **Variant B (P_d generic):** "senior distributed systems engineer" + interrogative artifact
- **Variant C (P_d baseline):** baseline, no artifact modification

## Results

| Variant | Final Score | Mean tokens |
|---------|-------------|-------------|
| A (P_p generic + interrogative artifact) | **10/10** | 1090 |
| B (P_d generic + interrogative artifact) | **10/10** | 1139 |
| C (P_d baseline) | **0/10** | 1010 |

Calibration: C=0/10 ✓

## Manual Review

All 20 A/B outputs confirmed as genuine diagnoses. Pattern: model confirms the reviewer
flag, explains the all-threads-suspended mechanism in its own words, independently
prescribes fencing token / optimistic lock at DB write layer, provides SQL or Python
fix sketch. Sampled A-01, A-07, B-03 in full.

C-01 and C-05 (pre-screen flagged: pause keyword found) confirmed Score 0: pause appeared
only as a timing aside in TOCTOU discussions. Neither found the Bug 2 chain.

## Primary Finding

**Interrogative artifact vocabulary drives detection at ceiling.**

The interrogative form functions as a search activator: the model must reason through
the code to answer the question, and in doing so independently identifies, explains,
and prescribes a fix for the Bug 2 failure mode.

Contrast with exp-21a (assertional artifact vocabulary → 0/10): same lexical domain
in the PR description, opposite outcome based on pragmatic force.

## Pragmatic Force Pattern

| Artifact framing | Pragmatic force | Detection |
|-----------------|-----------------|-----------|
| "Heartbeat prevents zombie-write failure modes" (exp-21a A) | Assertion: accept | 0/10 |
| "Does this prevent a stale write in that scenario?" (exp-22 A) | Question: reason | 10/10 |

## Design Confound

**Fatal objection accepted (Gemini):** Exp-22 changed two variables vs exp-21a simultaneously:
(1) pragmatic force (assertional → interrogative) and (2) vocabulary specificity
(failure-mode labels → causal chain description). We cannot isolate which variable drove
activation. Resolving experiment: Assertional Mechanism test (exp-24).

## H1/H2 Status

A = B = 10/10. Slot irrelevant when artifact vocabulary drives detection. H2 corroborated.
Caveat: at ceiling.

## Directed vs Independent Detection Distinction

Exp-22 is **directed detection**: the model reasons about a scenario it was given in the
prompt. Exp-23 is **independent detection**: the model discovers the scenario from vocabulary
cues in the system prompt without explicit description of the causal chain in the artifact.
Both drive the same detection rate in this experiment, but the practical mechanisms differ.

## Token Count

B (1139) > A (1090) > C (1010). B > A pattern consistent with exp-20 and exp-21b (Instructions
drives more verbose output than Persona). This contrasts with exp-23's reversal (A > B for
mechanism vocabulary in the system prompt).

## Next

→ exp-24: Assertional Mechanism test — same causal chain as exp-22, framed as assertion.
  Resolves pragmatic force vs vocabulary specificity confound.
