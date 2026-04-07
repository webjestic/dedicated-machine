# exp-34 Findings: Mechanism Decoy

**Status:** All variants complete (n=10 each). A = B = C = 10/10 Tier 1.0.

---

## Experiment Summary

exp-34 tests the §9.8 Artifact Pointer Confound: does mechanism vocabulary in the
P_p prompt install a reasoning procedure, or does it merely point at the answer location
(GPS coordinates)?

The test uses Variant C: a **false mechanism claim** embedded in the Instructions layer.
The decoy targets the Lua renewal script (`RENEW_CLAIM_SCRIPT`) with the claim that `GET`
followed by `EXPIRE` "may not execute atomically under high Redis connection saturation."
This claim is specifically wrong — Redis Lua scripts are unconditionally atomic — and it
points away from the real bug (silent heartbeat exit / zombie write via GC pause).

If the model follows GPS coordinates, it would hallucinate or deflect toward the Lua script
section. If the model has installed verification mode, it would find the real bug and dismiss
or correct the false claim.

---

## Variant C Results (n=10)

**Model:** claude-sonnet-4-6
**Cost:** $0.3995 (37,530 input / 19,128 output tokens)

### Outcome distribution

| Outcome | Count | Description |
|---|---|---|
| **Reject + Find** | **10/10** | Dismissed decoy, found real bug at Tier 1.0 |
| Hallucination | 0/10 | Accepted false claim, missed real bug |
| Deflection | 0/10 | Examined wrong section, no explicit reject |
| Reject + Miss | 0/10 | Dismissed decoy, failed Tier 1.0 |
| Find Both | 0/10 | Named both Lua issue and zombie-write |

### Tier 1.0 criteria met (all 10 runs)

All 10 runs satisfied the full Tier 1.0 criterion:

- **GC pause named as trigger** ✓ (all runs)
- **Fencing token / optimistic concurrency at DB write boundary named as architectural fix** ✓ (all runs)
- **threading.Event distinguished as insufficient (Tier 0.5)** ✓ (all runs)

### Decoy dismissal (all 10 runs)

Every run explicitly dismissed the Lua atomicity claim as "not a real failure path."
The dismissal structure was consistent across all 10 runs:

- Finding 1: The zombie-write bug (real, primary)
- Finding 2: Prior Review's Atomicity Concern — Dismissed (the decoy)

Representative dismissal language across runs:

> "Redis executes Lua scripts atomically with respect to all other Redis commands. [...]
> Connection saturation affects queuing of commands before execution begins; it does not
> cause interleaving within a script." (C-01, C-02, C-03, C-04, C-06, C-07, C-08, C-09)

> "The prior review's concern is technically misstated. Lua scripts in Redis execute
> atomically with respect to other Redis commands." (C-05)

> "The prior review may have been gesturing at, but named incorrectly: The real gap is
> not within the script — it is the temporal gap *before* the script runs." (C-10)

---

## Variant B Results (n=10)

**Model:** claude-sonnet-4-6
**Cost:** ~$0.41 (37,430 input / 19,198 output tokens, 10 runs)

### Outcome distribution

| Outcome | Count | Description |
|---|---|---|
| **Tier 1.0** | **10/10** | GC pause ✓, fencing token ✓, threading.Event insufficient ✓ |
| Below Tier 1.0 | 0/10 | — |

### Result

**10/10 Tier 1.0** — same as Variant C. Every run: GC pause named as trigger, fencing token /
optimistic concurrency at DB boundary named as architectural fix, threading.Event distinguished
as detection mechanism (Tier 0.5) not prevention.

No run discussed Lua atomicity (nothing to dismiss — no decoy present). Several runs went
deeper on secondary findings: `_dispatch()` executing outside any fencing boundary, idempotency
check TOCTOU, missed-renewal detection, release-script logging. Core finding structure was
uniform.

**B = C = 10/10.** The direction of the vocabulary (correct pointer vs. false pointer) did not
change the outcome. The mechanism being named was not what created the result.

---

## Analysis

### Primary result

The decoy failed completely. P_p did not follow the GPS coordinates embedded in the
Instructions layer. Every run found the real bug, characterized it correctly to Tier 1.0,
and dismissed the false claim with a technically accurate rejection.

This is strong evidence **against** the GPS-coordinates hypothesis. If vocabulary in P_p
were functioning as a location pointer (directing attention to where the prior review said
the problem was), we would expect at minimum some rate of hallucination or deflection toward
the Lua script section. We observed zero.

### Rejection mechanism — a limiting observation

The decoy was rejected correctly, but the rejection mechanism is domain-knowledge-based,
not purely code-structural.

Redis Lua atomicity is a well-documented guarantee — it appears in the official Redis
documentation, is discussed extensively in distributed systems literature, and is present
in training data at high density. The model can dismiss the claim from stored knowledge
("Redis Lua scripts are always atomic") without tracing the code execution to verify it.

This creates an alternative explanation for the result: the model rejected the decoy not
because P_p installed verification mode, but because the specific false claim happened to
be falsifiable from training data alone. A harder decoy — one that is plausible-wrong in
a way that requires code-structural verification rather than fact-recall — would more
cleanly isolate the mechanism.

This is a calibration note, not a disconfirmation. The GPS-coordinates hypothesis predicts
hallucination or deflection; we got neither. The Tier 1.0 rate (10/10) and the correct
prioritization (real bug first, decoy dismissed second) are consistent with installed
verification mode. But the strength of the evidence depends on whether the decoy was
hard enough.

### B = C: direction of vocabulary is irrelevant

Variant B provided the correct pointer (true mechanism vocabulary, directing attention
to the GC pause / heartbeat exit path). Variant C provided a false pointer (directing
attention to the wrong code section). Both produced 10/10 Tier 1.0.

This is a strong result. The vocabulary direction had no effect on outcome. A correct
pointer didn't help; a false pointer didn't hurt. This is inconsistent with the GPS-
coordinates hypothesis in either direction. Neither the true pointer (B) nor the false
pointer (C) changed where the model looked or what it found.

The remaining question is whether P_p alone (Variant A, no vocabulary) produces the same
result. If A ≈ 10/10, the vocabulary adds nothing and P_p is the mechanism. If A is low
(near exp-09 A's ~1/10), vocabulary matters but direction doesn't — the model benefits
from mechanism framing but not from location.

### Structural finding (Variant C)

All 10 C runs followed the same output structure: real bug identified first (Finding 1),
decoy dismissed second (Finding 2). No run inverted this ordering or led with the Lua
script section. This ordering is itself a signal: the model was not drawn toward the
explicitly flagged section as its primary investigative target.

---

---

## Variant A Results (n=10)

**Model:** claude-sonnet-4-6
**Cost:** ~$0.47 (36,730 input / 23,603 output tokens, 10 runs)

### Outcome distribution

| Outcome | Count | Description |
|---|---|---|
| **Tier 1.0** | **10/10** | GC pause ✓, fencing token ✓, threading.Event insufficient ✓ |
| Below Tier 1.0 | 0/10 | — |

### Result

**10/10 Tier 1.0** — same as B and C. P_p with no vocabulary, no direction, and no decoy
produces the same outcome as P_p with correct vocabulary and P_p with a false decoy.

This is the decisive result. A = B = C = 10/10. Vocabulary is inert. The P_p termination
condition is the mechanism.

---

## Comparison Table

| Experiment | Variant | Prompt | n | Tier 1.0 |
|---|---|---|---|---|
| exp-09 | A | baseline (no P_p) | 40 | 1/10 |
| exp-34 | A | P_p, no direction | 10 | **10/10** |
| exp-34 | B | P_p + true pointer | 10 | **10/10** |
| exp-34 | C | P_p + decoy (false Lua claim) | 10 | **10/10** |

A = B = C = 10/10. Vocabulary direction is irrelevant. P_p alone is sufficient and hits
the same ceiling as correct or incorrect vocabulary.

The exp-09 A comparison is the key finding: same model, same artifact, P_p vs. no P_p,
10/10 vs. 1/10.

---

## Resolved Questions

1. **Control (A): resolved.** P_p alone, with no vocabulary and no direction, produces
   10/10 Tier 1.0. A = B = C. Vocabulary is inert. The P_p termination condition is the
   mechanism.

2. **Decoy hardness: resolved.** The decoy had no effect (C = 10/10). However, the
   rejection mechanism in C was domain-knowledge-based (Redis Lua atomicity is a documented
   guarantee). A harder decoy — one that requires code-structural verification to refute
   rather than training data recall — remains a candidate for future calibration. This
   experiment shows the decoy didn't redirect; it doesn't fully characterize the robustness
   boundary.

---

## Verdict

**A = B = C = 10/10 Tier 1.0.**

The mechanism vocabulary hypothesis and the GPS-coordinates hypothesis are both rejected.
P_p alone — no vocabulary, no direction — produces the same outcome as P_p with correct
vocabulary and P_p with a false pointer. The vocabulary content is inert. The P_p termination
condition is the mechanism.

The exp-09 A comparison (same model, same artifact, no P_p → 1/10; P_p → 10/10) is the
direct causal attribution. Architecture is the variable. Vocabulary is not.

**Implication for §9.8 (Artifact Pointer Confound):** The confound is resolved in the null
direction. Mechanism vocabulary does not function as GPS coordinates. It does not function
as an activator either — P_p without vocabulary matches P_p with vocabulary exactly. The
§9.8 confound was real to raise, but the experimental result eliminates it: the effect
belongs to the P_p structure, not to the vocabulary it happened to contain.
