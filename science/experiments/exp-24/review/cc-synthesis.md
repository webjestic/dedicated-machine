# Exp-24 CC Synthesis

**Date:** 2026-03-30

## Primary Finding

Mechanism vocabulary in PR summary as an assertion does NOT kill detection.
A=8/10, B=9/10 — models challenged the false technical claim rather than
accepting it. The assertion was explicitly quoted and refuted in all sampled
outputs: "The PR summary frames the heartbeat as a feature. It is actually
the opposite."

## Pragmatic Force — Narrowed

Exp-21a (0/10) vs exp-24 (8-9/10) comparison:

| | Exp-21a | Exp-24 |
|--|---------|--------|
| Vocabulary | Directive labels ("zombie-write", "fencing token") | Mechanism description (GC pause chain) |
| Assertion | Vague outcome ("prevents zombie-write failure modes") | Specific technical claim (TTL + heartbeat ensures validity) |
| Result | 0/10 | 8-9/10 |

The pragmatic force effect is real but bounded: assertional framing kills
detection when the assertion makes a vague outcome claim with no evaluatable
mechanism. When the assertion describes a specific causal mechanism, the model
evaluates it against the code rather than accepting it as a World Layer premise.

Updated model:
- Vague outcome assertion → search terminator
- Mechanism assertion → evaluatable claim (model checks it, finds it wrong)
- Mechanism interrogative → search activator

## H1/H2

A=8/10, B=9/10. Gap within noise (1/10 differential, both at ceiling range).
H2 corroborated for the fifth time. Persona type produces no observable
differential when mechanism vocabulary is present in either slot or the artifact.

## Gemini's Alternative: Training Data Priors ("Spoiler Effect")

The combination of "heartbeat + TTL + GC pause" in the same paragraph may
function as a textual pattern strongly associated with the canonical "wrong
solution" in distributed systems literature. Detection may not require logical
evaluation of the assertion — the pattern may fire regardless of framing.

This is a live alternative to the outcome/mechanism distinction. Cannot be
ruled out from exp-24 data alone.

## Token Pattern

A (1149) < B (1175). Small gap, within noise. No reversal observed — unlike
exp-23 where mechanism vocabulary in Persona drove A > B. Possible reason: the
mechanism vocabulary here is in the artifact (same location for A and B), not
in the Persona or Instructions, so the Persona-as-simulation-engine effect
doesn't apply.
