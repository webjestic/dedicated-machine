# exp-1001b: Stakes as Voltage — Weak Persona (P_d Baseline)

**Status:** Ready to run
**Hypothesis:** H1001b

---

## Question

Does consequence naming in a STAKES section lift output depth when the Persona is weak (P_d baseline) — specifically on the operational items that require mechanism-level consideration sets?

---

## Background

exp-1001 found that consequence naming stakes produced no lift against a strong Persona — and actually reduced coverage (7.0/8 vs. 7.8/8 for Persona only). The strong Persona's mechanism vocabulary ("paged at 3am," "replayed events," "rotated secrets") already installed the full consideration set. Stakes was redundant.

The open question: does stakes compensate for a weak Persona? If the gravity well is shallow, does consequence naming provide the missing voltage?

---

## H1001b — Stakes Against P_d Baseline

**Variant A — Weak Persona only:** P_d baseline — credential label only. "You are a senior backend engineer. You are thorough and experienced." No mechanism vocabulary, no failure-mode framing, no operational anchors. Everything else identical to B.

**Variant B — Weak Persona + stakes:** Same P_d Persona. STAKES section added: same consequence naming as exp-1001B.

Everything else held constant: CONTEXT, TONE, INSTRUCTIONS, FORMAT, REQUEST, artifact.

| Section | Variant A | Variant B |
|---------|-----------|-----------|
| PERSONA | P_d baseline | P_d baseline (identical) |
| CONTEXT | ✓ | ✓ (identical) |
| STAKES  | — | ✓ (consequence naming) |
| TONE    | ✓ | ✓ (identical) |
| INSTRUCTIONS | ✓ | ✓ (identical) |
| FORMAT  | ✓ | ✓ (identical) |

---

## Design

- **Artifact:** ARTIFACT.md — same webhook receiver spec as exp-1001
- **Scoring:** SCORING.md — same 8-item rubric as exp-1001
- **Model:** claude-sonnet-4-6, temperature=0.5
- **Runs:** n=10 per variant
- **Control:** exp-1001 Variant A (strong Persona, 7.8/8)
- **Sensitivity target:** Items 5–8 (replay protection, dead-letter, alerting, secret rotation)

---

## What a Positive Result Looks Like

B scores meaningfully higher than A on items 5–8. Stakes compensates for the missing mechanism vocabulary in the Persona. Consequence naming is a voltage amplifier for shallow gravity wells.

## What a Null Result Looks Like

A and B score similarly. Stakes does not add signal regardless of Persona strength. Consequence naming is not an independent variable.

## What an Interesting Middle Result Looks Like

B lifts some sensitivity-target items but not all. Stakes partially compensates — it adds some voltage but cannot fully substitute for mechanism vocabulary.

---

## Comparison to exp-1001

| Condition | exp-1001 A | exp-1001 B | exp-1001b A | exp-1001b B |
|-----------|-----------|-----------|------------|------------|
| Persona | Strong (P_p) | Strong (P_p) | Weak (P_d) | Weak (P_d) |
| Stakes | None | Consequence naming | None | Consequence naming |
| Expected score | High | High | Low | ? |
