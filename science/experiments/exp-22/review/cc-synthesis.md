# Exp-22 CC Synthesis

**Date:** 2026-03-30
**Results:** A=10/10, B=10/10, C=0/10

## Primary Finding

**Interrogative artifact vocabulary drives detection at ceiling.**

All 20 A/B outputs independently diagnosed Bug 2: explained the all-threads-suspended
mechanism, identified the stale write consequence, and prescribed a fencing token or
optimistic lock at the DB write layer. Manual review confirmed diagnosis (not echoing)
for sampled outputs. C = 0/10 confirms calibration.

## Pragmatic Force Confirmed

Exp-21a (assertional artifact vocabulary) → 0/10.
Exp-22 (interrogative artifact vocabulary) → 10/10.

Same lexical content in the artifact (names the GC pause, the all-threads-suspended
mechanism, the stale write) produces opposite detection outcomes based solely on
pragmatic force:

| Artifact framing | Pragmatic force | Detection |
|-----------------|-----------------|-----------|
| "Heartbeat prevents zombie-write failure modes" (exp-21a) | Assertion: accept as true | 0/10 |
| "Does this prevent a stale write in that scenario?" (exp-22) | Question: reason and answer | 10/10 |

The assertional form functions as a search terminator: the model accepts the claim and
does not investigate the mechanism. The interrogative form functions as a search activator:
the model must reason through the code to answer the question, and in doing so independently
identifies and diagnoses the failure mode.

## H1/H2 Status

A = B = 10/10. Slot provides no differential lift when vocabulary is in the artifact.
H2 corroborated again: content operative regardless of slot. However, caution is warranted:
both variants are at ceiling. The slot differential may be unobservable at 10/10.

## Qualification: Directed vs Independent Detection

Exp-22 differs from exp-20 and exp-23 in one important respect: the interrogative question
explicitly names the causal scenario. The model is reasoning about a scenario it was given,
not discovering it from code inspection alone. This is still meaningful detection — the model
must confirm the flaw is real, explain the mechanism, and prescribe the correct fix — but it
is directed detection rather than independent discovery.

The practical distinction:
- **Directed detection (exp-22):** Model confirms and explains a scenario described in the prompt.
- **Independent detection (exp-20, exp-23):** Model discovers the scenario from vocabulary cues alone.

Both are valuable. Directed detection has direct applications to reviewer checklists and
audit prompts. Independent detection is what the PARC consideration-set hypothesis predicts.

## Revised Artifact Vocabulary Theory

Vocabulary in the artifact can serve as a detection vector IF framed interrogatively:
1. Assertional framing → premise accepted → search terminated (exp-21a)
2. Interrogative framing → open question → search activated → Bug 2 diagnosed (exp-22)

This extends the pragmatic force finding: it is not that artifact vocabulary is inert — it
is that assertional artifact vocabulary is inert. Interrogative artifact vocabulary is
as effective as directive system-prompt vocabulary.
