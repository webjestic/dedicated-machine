# Exp-21a Findings

**Experiment:** Vocabulary in artifact (PR description)
**Date:** 2026-03-30
**Model:** claude-sonnet-4-6
**Runs:** 30 (A: 10, B: 10, C: 10)

## Question
Does directive vocabulary placed in the PR description of the artifact drive zombie-write detection, even when system prompt slots contain no vocabulary?

## Design

Same base artifact as exp-19/20 (distributed inventory reservation with heartbeat-based Redis lock).

Key modification: the PR Summary in the artifact contains: *"Uses a Redis distributed lock with a heartbeat renewal thread to prevent zombie-write failure modes caused by process isolation boundary violations and lock lease expiry. The heartbeat is designed to keep the lock alive during slow DB operations, defending against scenarios where lock expiry could allow a fencing token violation at the write layer."*

- **Variant A (P_p generic):** Persona = "distributed systems engineer with deep experience reviewing concurrent infrastructure code" (no vocabulary)
- **Variant B (P_d generic):** Persona = "senior software engineer" + generic instructions (no vocabulary)
- **Variant C (P_d baseline):** Clean baseline with original artifact (no vocabulary anywhere)

## Results

| Variant | Final Score | Pre-screen | Mean tokens |
|---------|-------------|------------|-------------|
| A | **0/10** | 2/10 (both false positives) | 1012 |
| B | **0/10** | 0/10 | 946 |
| C | **0/10** | 0/10 | 908 |

Calibration: C=0/10 ✓

### False Positive Analysis (A-01, A-07)
Pre-scorer detected "GC pause" + "fencing token" in these outputs. Manual review confirmed Score 0: GC pause appeared as a timing-precision aside ("heartbeat sleep may be delayed by GC pause"), not as the zombie-write causal chain. Fencing token appeared as what the TOCTOU race fails to prevent, not as the recommended DB-layer fix. Neither output described the zombie-write chain or recommended fencing token at DB write layer.

## Primary Finding

**Vocabulary in the artifact — even when it names zombie-write failure modes and fencing token violations explicitly — does not drive detection.**

This is in direct contrast to exp-20, where the same vocabulary in system prompt Instructions drove 9/10. The operative difference is pragmatic force:
- **System prompt (exp-20):** vocabulary functions as a directive search vector
- **Artifact PR description (exp-21a):** vocabulary functions as an authorial assertion (claims the design addresses these concerns)

The model processes the PR description's claims as premises to accept ("author says this prevents zombie-writes"), not as directives to investigate ("check for zombie-write failure modes").

## Design Confound (accepted)

Exp-21a changed two variables simultaneously: slot (Instructions → Artifact) AND pragmatic force (directive → assertion). H1/H2 cannot be adjudicated. The next experiment (exp-22) will inject directive/interrogative vocabulary into the artifact to isolate the slot variable from the force variable.

## Implication

The consideration-set expansion mechanism requires not just specific vocabulary but specific vocabulary deployed with directive pragmatic force. Assertional vocabulary in the artifact is insufficient, regardless of Persona type.

## Next

→ exp-22: interrogative artifact vocabulary test
