# exp-1001: Stakes as Voltage — Consequence Naming

**Status:** Ready to run
**Hypothesis:** H1001

---

## Question

Does consequence naming in a STAKES section independently raise output depth beyond what a strong Persona alone achieves — specifically on operational items that historically land at 0% in single-agent runs?

---

## Background

The rate-limiter experiments (exp-20 series) established that single-agent prompts with a strong SRE Persona scored **2.6/10** on a 10-item operational checklist. Five items — alerting policy, load test spec, health check, incident runbook, race condition handling — landed at **0% across all variants**. The two-agent pipeline lifted this to 5.6/10 by installing a second machine scoped to the operational layer.

The rate-limiter-design.md example pairs a strong Persona with a consequence-naming STAKES section:

> *"An operational requirement left out of this document is an operational requirement left out of the system. Not a gap to fill later. A production incident waiting to happen."*

This pairing was never isolated. It is unknown whether the STAKES section contributes independently or whether the Persona carries the full effect.

---

## H1001 — Stakes as Independent Variable

**Variant A — Persona only:** Strong SRE architect Persona, no STAKES section. All other sections identical to B.

**Variant B — Persona + stakes:** Same Persona. STAKES section added: consequence naming only — names what an omission produces, not what the machine should do.

Everything else held constant: CONTEXT, TONE, INSTRUCTIONS, FORMAT, REQUEST, artifact.

| Section | Variant A | Variant B |
|---------|-----------|-----------|
| PERSONA | ✓ (SRE architect) | ✓ (identical) |
| CONTEXT | ✓ | ✓ (identical) |
| STAKES  | — | ✓ (consequence naming) |
| TONE    | ✓ | ✓ (identical) |
| INSTRUCTIONS | ✓ | ✓ (identical) |
| FORMAT  | ✓ | ✓ (identical) |

---

## Design

- **Artifact:** ARTIFACT.md — rate-limiter requirements (180 RPS sustained, 400 RPS peak, Redis, multi-instance)
- **Scoring:** SCORING.md — 10 binary items, mean score per variant
- **Model:** claude-sonnet-4-6, temperature=0.5
- **Runs:** n=10 per variant
- **Control:** Historical single-agent baseline — 2.6/10 (exp-20 series)
- **Sensitivity target:** Five items at historical 0% — alerting policy, load test spec, health check, incident runbook, race condition handling

---

## What a Positive Result Looks Like

Variant B scores meaningfully higher than Variant A, with the delta concentrated in the five sensitivity-target items. At least two of the five items move from near-zero in A to >50% in B.

## What a Null Result Looks Like

A and B score similarly. The strong Persona already installs the effect the STAKES section was hypothesized to add. Stakes as voltage is not an independent variable at this Persona strength.

---

## Next Experiments (Conditional)

- **exp-1001b:** If H1001 supported — test stakes with a weak Persona (P_d baseline). Does consequence naming lift a weak Persona?
- **exp-1001c:** If H1001 supported — test quantified stakes ("180 RPS, 3am, six months from now") vs. consequence naming. Is specificity the operative variable within stakes?
- **exp-1001-null:** If null result — test stakes with instructions stripped. Does stakes substitute for instructions when Persona is strong?
