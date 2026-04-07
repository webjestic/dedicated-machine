# exp-34 — The Mechanism Decoy

**Date:** 2026-04-02
**Model:** claude-sonnet-4-6
**Runs:** A=5 (replication check), B=10, C=10
**Artifact:** exp-09/ARTIFACT.md — Python distributed job executor, Redis claim locking
**Runner:** Standard runner (`runner.py parc/science/experiments/exp-34`)

---

## Background

d7 §9.8 names the Artifact Pointer Confound: when "Mechanism Vocabulary" is present in
a prompt — GC pause, fencing token, zombie write — does it work by installing a reasoning
algorithm (P_p installs a search mode), or by providing GPS coordinates (vocabulary narrows
the search space to where the answer already lives)?

The prior experiments (exp-09 through exp-28b) could not answer this cleanly because the
vocabulary always pointed toward real bugs. The pointer account and the reasoning account
make identical predictions when the coordinates are correct: model finds bug. They diverge
only when the coordinates are wrong.

This experiment was independently derived by Chrome Gemini (Gemini built into Chrome's
browser sidebar) from a cold read of d7 via the GitHub repo, then refined here. Gemini
labeled it "Experiment 25" — it was reading the paper's internal experiment numbering, not
the full roadmap.

---

## Primary Question

Does mechanism vocabulary install a reasoning algorithm, or does it point the model's
attention to where the answer lives?

**Pointer account:** If correct vocabulary improves detection (B > A) and wrong vocabulary
causes hallucination or deflection (C < A, or C hallucinates), vocabulary is GPS —
efficiently directing attention, not installing a search algorithm.

**Reasoning account:** If wrong vocabulary is rejected and the real bug is still found
(C = A on Tier 1.0, explicit decoy rejection in output), vocabulary is installing an
alert mode — a verification stance that allows the model to evaluate claims against
structural reality rather than simply following coordinates.

---

## The Decoy

**Target:** The Lua renewal script (`RENEW_CLAIM_SCRIPT`) — the healthy part of the codebase.

**False claim:** The script may not execute atomically under high Redis connection
saturation — the `GET` and `EXPIRE` operations may not be atomic.

**Why this is specifically wrong:** Redis Lua scripts are always atomic. No other command
can interleave during Lua execution, regardless of connection load. This is a core Redis
guarantee. An expert in Redis knows this immediately. The code uses Lua scripts precisely
to get atomicity.

**Why it's a good decoy:** It sounds authoritative. It uses real Redis terminology
(`GET`, `EXPIRE`, atomicity). It targets a real section of code. It frames the claim as
prior analysis (authority framing). It points at the renewal path — the healthy mechanism
— and away from the main-thread gap (the real bug: no visibility into heartbeat exit).

**Decoy placement:** Instructions layer. Framed as "a prior review flagged..." — the task
itself is shaped around investigating the wrong place.

---

## Variants

### A — Control (P_p, no vocabulary)

P_p Staff SRE with deep Redis background. No mechanism vocabulary in any slot. No
direction toward any specific code section. Replicates exp-09 Variant A conditions.

Run n=5 as a within-experiment replication check. Reference exp-09 Variant A (n=40,
1/10 Tier 1.0) as the full baseline.

### B — True Pointer (P_p + correct vocabulary)

Same P_p. Instructions add: trace what happens to the main thread when the heartbeat
exits, specifically under a GC pause / process-stall scenario. Name the fencing token
at the DB write boundary. Vocabulary points at the real bug.

Tests: does correct vocabulary improve detection above A's 1/10 baseline?

### C — Decoy (P_p + wrong vocabulary in Instructions)

Same P_p. Instructions embed the false atomicity claim as a "prior review finding" to
investigate. The task directs attention to the renewal script and away from the main-thread
zombie-write gap.

**This is the critical variant.** Tests: does the model accept the false premise
(hallucinate an atomicity bug) or reject it (identify Lua atomicity as guaranteed and
look elsewhere)?

---

## Predictions

**B:** Tier 1.0 rate significantly above A's 1/10 (exp-09). Vocabulary pointing at the
real bug should lift detection. Prediction: 5–8/10.

**C — Reasoning account:** Decoy rejected explicitly in ≥6/10 runs. Model names Lua
atomicity as a Redis guarantee, dismisses the premise, finds the GC-pause/zombie-write
independently. Tier 1.0 rate approximately equal to A.

**C — Pointer account:** Decoy accepted in ≥5/10 runs. Model "validates" the atomicity
gap, spends its output on the renewal script, misses the zombie-write. Tier 1.0 rate
below A.

---

## Relationship to d7

This experiment directly addresses the §9.8 falsification question. Results belong in
§9.8 as the empirical resolution of the Artifact Pointer Confound — either narrowing the
claim (vocabulary is efficient pointing, not reasoning-installation) or strengthening it
(P_p installs a verification mode that resists false coordinates).
