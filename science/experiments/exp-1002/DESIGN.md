# exp-1002: Stakes as Situational Briefing

**Status:** Ready to run
**Hypothesis:** H1002

---

## Question

Does situational Stakes — naming the real-world consequence of failure for a specific client in a specific situation — lift trap detection in a contract review task when the Persona is weak?

---

## Background

exp-01f tested four variants against the same MSA contract containing a structurally defective limitation of liability clause (§8.2 carve-outs nullify §8.1 cap). Key results:

| Variant | Persona | Stakes | Critical score |
|---------|---------|--------|----------------|
| M | Strong procedural | None | 10/10 |
| N | Weak (credential only) | None | 0/10 |
| O | Strong procedural | None | 10/10 |
| P | Strong disposition | Identity/pride | 1/10 |

The Variant P result — strong disposition Persona + identity Stakes — was the central failure. It scored 1/10, statistically equal to N (0/10). Stakes amplified the wrong thing: comprehensive enumeration of real but secondary issues, with the structural argument missed in 9 of 10 runs.

**What exp-01f did not test:** situational Stakes. Variant P's Stakes were identity-framed — "20/20 success rate," "great sense of pride." This is Persona language in a Stakes slot. It tells the model who it is, not what is at stake in this situation.

The original Stakes hypothesis — that naming real-world consequence changes what the model looks for — was not tested in exp-01f.

---

## H1002 — Situational Stakes Against P_d Baseline

**Variant A — Weak Persona only:** Replication of exp-01f Variant N. Credential label: "You are a senior corporate attorney." Rich organizational context. No Stakes. Baseline expected: 0/10 on Critical criterion.

**Variant B — Weak Persona + situational Stakes:** Same weak Persona and context. STAKES section added naming the client's specific situation, the consequence of missing the structural defect, and what the agreement's presentation obscures.

Everything else identical: CONTEXT, INSTRUCTIONS, FORMAT, artifact.

| Section | Variant A | Variant B |
|---------|-----------|-----------|
| PERSONA | Weak (credential) | Weak (credential) — identical |
| CONTEXT | Rich (federal contractor) | Rich (federal contractor) — identical |
| STAKES | — | Situational consequence naming |
| INSTRUCTIONS | ✓ | ✓ — identical |
| FORMAT | ✓ | ✓ — identical |

---

## What Situational Stakes Means Here

Variant B's Stakes section names:
- **Who:** Meridian Federal Partners, executing next week
- **What's at stake:** multi-year federal engagement, unlimited liability exposure
- **Failure mode:** "they will not discover it until they are in a dispute"
- **The obscuration:** "what the agreement's presentation obscures"

This is not identity framing. It is a briefing — the kind a senior attorney would receive walking into a review. The consequence is in the situation, not in the model's sense of self.

---

## Design

- **Artifact:** Same MSA contract as exp-01f (DataStream / Meridian Federal Partners)
- **Trap:** §8.2 carve-outs (indemnification, confidentiality, IP, gross negligence, unpaid fees) functionally nullify the §8.1 12-month fee cap
- **Elite trap:** §9.1(c) "breach of Agreement" circularity routes general breach through uncapped indemnification channel
- **Scoring:** Same 3-tier rubric as exp-01f (CRITICAL / ELITE / DISTRACTION)
- **Model:** claude-sonnet-4-6, temperature=0.5
- **Runs:** n=10 per variant
- **Control:** exp-01f Variant N (0/10) — expected A to replicate

---

## Predictions

| Variant | Critical score | Reasoning |
|---------|---------------|-----------|
| A | 0/10 | Replication of N. Weak Persona + no Stakes = enumeration without structural prioritization |
| B | >0/10 | Situational Stakes installs the right search direction: look at the liability structure, ask if the cap is real |

**A meaningful result:** B scores 3/10 or higher. The situational briefing shifts what the model looks for first.

**A null result:** B scores 0-1/10. Situational Stakes, like identity Stakes, amplifies enumeration rather than redirecting search. Persona is the only carrier of search direction.

**What a null result means:** Stakes — in any form — cannot supply the search algorithm that procedural Persona provides. The variable is inert without Persona signal to amplify.

---

## Comparison to exp-01f

| Condition | exp-01f N | exp-01f P | exp-1002 A | exp-1002 B |
|-----------|-----------|-----------|------------|------------|
| Persona | Weak | Strong disposition | Weak | Weak |
| Stakes | None | Identity/pride | None | Situational consequence |
| Critical | 0/10 | 1/10 | Expected: 0/10 | ? |
