# exp-35 Design: Strong CoT Baseline

## Research Question

Can explicit chain-of-thought procedure in the Instructions layer replicate the Tier 1.0
rate produced by a Procedural Persona (P_p)?

PARC claims that P_p's effect comes from installing a termination condition and verification
procedure as part of the model's operative identity — not merely from providing good
instructions. Every paper reviewer will ask: "What if you just wrote explicit CoT steps?
Would you get the same result without the persona machinery?"

exp-35 answers this directly.

---

## Background

| Experiment | Variant | Persona | Instructions | n | Tier 1.0 |
|---|---|---|---|---|---|
| exp-09 | A | P_d (credential + disposition) | Generic | 40 | 1/10 |
| exp-34 | A | P_p (termination in identity) | Generic + termination condition | 10 | 10/10 |

The gap (1/10 → 10/10) between exp-09 A and exp-34 A has three potential explanations:

1. **Identity anchoring (PARC claim):** The termination condition in the Persona slot installs
   as operative identity — "I am someone who does not approve code until I can name X." The
   Persona slot has a distinct function that Instructions cannot replicate.

2. **Content is the mechanism:** The domain vocabulary (zombie write, GC pause, lock TTL,
   heartbeat) and the termination criterion are what cause the output. Whether they live in
   Persona or Instructions is irrelevant.

3. **PCSIEFTR format effect:** exp-09 used an older format; exp-34 used PCSIEFTR. The format
   change, not the Persona content, accounts for the gap.

exp-35 controls for explanations 2 and 3 by holding content and format constant while moving
the procedural content from Persona to Instructions.

---

## Hypotheses

**H0 (CoT equivalence):** Strong CoT A = P_p B. Tier 1.0 rate is equivalent. The content
(procedure + termination condition) is the mechanism; the slot is irrelevant. PARC's P_p
is structurally equivalent to explicit chain-of-thought prompting.

**H1 (Persona slot is load-bearing):** Strong CoT A << P_p B. Moving the procedural content
to Instructions substantially reduces Tier 1.0 rate. The Persona slot has a distinct
identity-anchoring function that explicit CoT cannot replicate.

---

## Variants

### Variant A: Strong CoT

**Design principle:** Take ALL of the procedural content from exp-34 A's P_p and move it
to the Instructions layer. Leave only a pure P_d credential in Persona.

- **PERSONA:** Dispositional only — senior software engineer, no domain vocabulary, no
  termination condition, no procedure description.
- **INSTRUCTIONS:** Explicit numbered chain-of-thought steps containing:
  - The exact domain vocabulary that was in the P_p (zombie write, GC pause, lock TTL,
    heartbeat thread exit, fencing token)
  - An explicit step-by-step reasoning procedure
  - The termination condition ("complete when you can confirm or name the zombie-write scenario")

This is the most favorable version of the CoT alternative. If this fails, weaker CoT
variants would also fail.

### Variant B: P_p (control)

Identical to exp-34 A — the P_p that produced 10/10 Tier 1.0. Provides a within-experiment
anchor so any run-to-run variation is visible.

---

## Scoring

**Tier 1.0 (same criterion as exp-09, exp-34):**
- GC pause (or equivalent process stall) named as the zombie-write trigger
- Fencing token / optimistic concurrency at the DB write boundary named as the architectural fix
- threading.Event signaling distinguished as necessary but insufficient (Tier 0.5)

**Below Tier 1.0:**
- Finds the zombie-write scenario but names only threading.Event as the fix → Tier 0.5
- Does not find the zombie-write scenario → Tier 0

---

## Predictions

| Outcome | Interpretation |
|---|---|
| A << B (e.g., A ≤ 3/10, B = 10/10) | Persona slot is load-bearing. Identity anchoring is the mechanism. CoT in Instructions cannot replicate P_p. |
| A ≈ B (both ≥ 8/10) | Content is the mechanism. PARC reduces to structured CoT. Paper's architectural claims require qualification. |
| A intermediate (4–7/10) | Partial effect. Persona slot amplifies but does not fully determine the procedure. |

---

## Why this matters for d8

The paper currently claims P_p installs a search algorithm as operative identity, distinct
from "good instructions." If Strong CoT replicates P_p's result, that claim is falsified and
the paper must be rewritten to argue for content-level rather than structural-level effects.

If Strong CoT fails to replicate, the paper has a clean falsification datapoint:
same content, same format, different slot → different outcome. This is the strongest
available evidence for the identity-anchoring mechanism claim.
