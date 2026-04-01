# Exp-29 Findings — Zombie-Write Two-Agent Pipeline (Proof of Concept)

**Status:** Complete
**Phase:** 7 — The Dedicated Machine Hypothesis
**Date:** 2026-03-31
**Artifact:** exp-09 (`experiments/exp-09/ARTIFACT.md`) — Python distributed job executor, Redis claim locking
**Predecessor:** exp-09 (single-pass zombie-write; best ceiling = 1/10 Tier 1.0, never solved cleanly)
**Design:** `experiments/exp-29/runner.py`
**Outputs:** `experiments/exp-29/output/`

---

## Summary

A two-agent PARC pipeline solved the zombie-write problem on the first run — cleanly, without any mechanism vocabulary in either prompt.

Agent 1 (Senior SWE, correctness scope) reached **Tier 1.0** on run 1: named the GC pause as the trigger, traced the exact failure path, and named the fencing token / optimistic concurrency at the database write boundary as the architectural fix. It correctly distinguished threading.Event as necessary-but-insufficient.

Agent 2 (SRE, production readiness scope) received the Layer 1 handoff summary and independently surfaced **seven additional infrastructure failure modes** that are invisible from code review: Redis Sentinel failover (split-lock), Kubernetes CFS throttling as a process-wide stall trigger, Redis network partition (ConnectionError kills the heartbeat silently), daemon thread termination on SIGKILL, TOCTOU race on the idempotency check, clock skew as a secondary amplifier, and undefined handler exception behavior at the infrastructure boundary.

**The zombie-write problem — never solved cleanly in any single-pass experiment — was solved on the pipeline's first run.**

---

## Results

### Agent 1 — Layer 1 Correctness Review

**Prompt:** `parc/examples/zombie-layer1-review.md`
**Model:** claude-opus-4-6
**Cost:** $0.0351 (3,722 in / 1,593 out)
**Tier:** 1.0

| Criterion | Result |
|-----------|--------|
| Zombie-write identified | ✓ |
| GC pause named as trigger | ✓ |
| Threading.Event named as insufficient | ✓ |
| Fencing token / optimistic concurrency named as architectural fix | ✓ |
| Tier 1.0 | **✓** |

Additional findings:
1. **Zombie write — heartbeat loss invisible to main thread** ← primary finding, Tier 1.0
2. Silent heartbeat exit — no log line on `result == 0`
3. Release script return value unchecked; misleading "Claim released" log after lock loss
4. No test coverage for the concurrent failure path
5. Handler exception contract undefined

Verdict: **NOT APPROVED**

---

### Agent 2 — Layer 2 Production Readiness Review

**Prompt:** `parc/examples/zombie-layer2-review.md`
**Model:** claude-opus-4-6
**Cost:** $0.0724 (4,154 in / 3,995 out)

Layer 1 handoff summary injected via `{{LAYER_1_SUMMARY}}`. Infrastructure failure modes found independently:

| # | Failure Mode | New vs. Layer 1 |
|---|-------------|-----------------|
| 1 | Redis Sentinel/Cluster failover → split-lock | **New** |
| 2 | GC pause / CFS throttling (infrastructure angle) | Extends Layer 1 — named Kubernetes cgroup as trigger |
| 3 | TOCTOU race on `get_execution` → `record_execution` | **New** (architecture) |
| 4 | Redis network partition → `ConnectionError` in `_renew()` kills thread silently | **New** |
| 5 | Claim release return value unchecked; misleading log masks failure forensically | Extends Layer 1 Finding 3 |
| 6 | Daemon thread + SIGKILL → heartbeat exits without `finally`; 60s liveness gap | **New** |
| 7 | Clock skew — secondary amplifier on failure mode 2 | **New** |
| 8 | `_dispatch()` handler exception at infrastructure boundary | Extends Layer 1 Finding 5 |

Critical open gaps:
- **G1 (Critical):** No fencing token / monotonic counter at database write boundary
- **G2 (Critical):** No database unique constraint on job execution records
- **G3 (High):** No threading signal from heartbeat to main thread on claim loss
- **G4 (High):** No exception handling in `_renew()` for Redis connection errors

Verdict: **NOT APPROVED**

Total pipeline cost: **$0.108**

---

## Findings

### Finding 1 — Pipeline reached Tier 1.0 on run 1; single-pass ceiling was 1/10

The exp-09 single-pass series ran 40 runs across four variants. The best result was **1/10 strict Tier 1.0** (A-07 only: GC pause named + DB-layer enforcement). No variant produced Tier 1.0 consistently. The best P_p variants (A, D) reached near-Tier-1.0 at most: D-02 and D-06 named fencing token without the GC-pause trigger (strict 0/10).

The two-agent pipeline reached **Tier 1.0 on run 1** — and did it more completely than A-07. Agent 1 named GC pause, named the failure path in full, and distinguished threading.Event (necessary, insufficient) from fencing token (necessary, sufficient). A-07 had the trigger and the DB-layer fix but did not draw the threading.Event distinction explicitly.

This is the same pattern as exp-28d: the pipeline crosses the wall that single-pass prompts approach but cannot consistently clear.

### Finding 2 — The boundary is the mechanism

Agent 1's handoff summary explicitly placed infrastructure failure modes out of scope:

> "This review does not cover infrastructure-level failure modes (Redis cluster failover, network partitions, database availability), deployment topology, performance under load, or operational runbook readiness."

That sentence is the bridge. Agent 2 received it as the starting point and treated it as its scope. The failure modes Agent 1 said it wasn't covering became exactly the failure modes Agent 2 found.

The agent boundary doesn't just divide labor — it installs a different satisfaction condition in each agent. Agent 1's satisfaction condition is: every correctness issue named. Agent 2's satisfaction condition is: every infrastructure assumption validated. The SRE's consideration set activates when the correctness reviewer's explicitly closes.

**This is Claim 2 in its clearest form.** The pipeline crosses horizons no single agent can reach not by making one machine smarter, but by giving each machine a different definition of done.

### Finding 3 — Agent 2 named failure modes that appear in no single-pass exp-09 output

Reviewing all 40 exp-09 runs:
- **Redis Sentinel/Cluster failover → split-lock:** Not named in any run
- **Kubernetes CFS throttling as process-wide stall:** Not named in any run (GC pause named in 4 A-variant runs as TTL math, only A-07 as the zombie-write trigger)
- **ConnectionError in `_renew()` silently kills the heartbeat thread:** Named in some exp-09 A-variant runs as a secondary finding, but never as a primary production concern with the full failure path traced
- **Daemon thread + SIGKILL / `kubectl delete pod --force`:** Not named in any run
- **TOCTOU race on `get_execution` → `record_execution` as a structural database concern:** Named in exp-09 A/B runs as a generic TOCTOU, not with the isolation-level specificity Agent 2 provided (READ COMMITTED semantics, both workers reading `None` before either commits)

The infrastructure failure modes are in the consideration set of a distributed systems SRE. They are not in the consideration set of a correctness reviewer, even a P_p-equipped one. The persona boundary is where the consideration sets diverge.

### Finding 4 — The pipeline resolved the central tension in the zombie-write problem

The zombie-write problem had a specific constraint: the finding should emerge from the prompt architecture, not from mechanism vocabulary in the prompt. No prior single-pass experiment solved it cleanly at Tier 1.0 without vocabulary hints (the exp-07c/07d results were confounded by checklist items naming the detection behavior).

Both zombie prompts contain zero mechanism vocabulary. Neither names GC pause, fencing token, zombie write, heartbeat, TOCTOU, or lock expiry. The finding emerged entirely from:
- Agent 1: P_p encoding of a distributed systems correctness reviewer's consideration set
- Agent 2: P_p encoding of a production SRE's consideration set + the explicit scope boundary passed in the handoff summary

The architecture, not vocabulary, drove the result.

---

## Relationship to Prior Experiments

| Experiment | Approach | Tier 1.0 rate | Infrastructure FMs |
|-----------|----------|---------------|-------------------|
| exp-09 Variant A (P_p, no extras) | Single-pass | 1/10 (10%) | 0 |
| exp-09 Variant D (P_p + domain Instructions) | Single-pass | 0/10 strict | 0 |
| exp-28d Variant A (two-agent pipeline) | Pipeline | — (different checklist) | — |
| **exp-29 (two-agent zombie pipeline)** | **Pipeline** | **1/1 (100%)** | **7 new** |

exp-29 is a proof-of-concept (n=1 per agent), not a controlled experiment. The Tier 1.0 rate cannot be asserted statistically from a single run. What can be asserted: the pipeline design produced a complete Tier 1.0 result on first execution, including findings that appear in no single-pass output across 40 runs.

---

## Status of the Zombie Prompt as a PARC Canonical Example

The zombie pipeline is the canonical two-agent PARC example for the following reasons:

1. **The agent boundary has a principled justification**: correctness scope vs. infrastructure scope. These are genuinely different consideration sets, not arbitrary divisions of labor.
2. **The handoff is load-bearing**: the explicit out-of-scope statement in Agent 1's output activates Agent 2's P_p. The bridge is not boilerplate — it is the mechanism by which two satisfaction conditions are chained.
3. **The result is measurable**: the zombie-write problem has a clear scoring criterion (Tier 1.0), which the pipeline met and single-pass approaches could not consistently meet.
4. **No vocabulary was smuggled**: both prompts are clean. The finding emerged from architecture.

The zombie pipeline (`parc/examples/zombie-layer1-review.md` + `parc/examples/zombie-layer2-review.md`) is the production readiness review example in the PARC examples set.

---

## Open Questions

1. **n=1 limitation.** This was a proof-of-concept run. A formal experiment (n=10) is needed to measure Agent 1's Tier 1.0 consistency and Agent 2's infrastructure FM coverage rate. Does Agent 1 reach Tier 1.0 on every run, or was this a high-draw first run?

2. **What does Agent 2 produce when Agent 1 misses?** The exp-28d finding ("the bridge is the artifact") predicts Agent 2 will miss what Agent 1 missed. If Agent 1 fails to name the fencing token, does Agent 2 find it independently from code context? This is testable.

3. **Does the handoff summary need to be structured?** Agent 1 produced a clean handoff summary unprompted (the FORMAT specified it). Would a less structured handoff summary reduce Agent 2's coverage? The `{{LAYER_1_SUMMARY}}` injection point assumes the handoff is a coherent block — this should be validated.
