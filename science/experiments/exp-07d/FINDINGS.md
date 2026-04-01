# exp-07d FINDINGS

**Experiment:** Slot-swap falsification test — silent artifact (warning line removed)
**Date:** 2026-03-28
**Model:** claude-sonnet-4-6, temperature 0.5, max_tokens 2500
**Runs:** 30 (n=10 per variant)
**Total cost:** $1.3232

---

## Results Summary

| Variant | Persona | Instructions content | Ceiling hits | Mean tokens | Score (strict) |
|---------|---------|---------------------|-------------|-------------|----------------|
| I | P_p — procedural distributed systems engineer | Generic | 7/10 | 2,461 | 0/10 |
| J | P_d — senior software engineer | Generic | 1/10 | 2,092 | 0/10 |
| C | P_d — senior software engineer | P_p domain content (slot-swapped) | 8/10 | 2,477 | 0/10 |

**Binary question result: C ≈ I > J**

---

## Scoring Note

The strict scoring criterion (Score = 1: identifies GC pause / process-pause scenario + names fencing token / optimistic locking) was calibrated for the original zombie-write artifact, where the failure mode required simulating process state across the full lock lifecycle with no code-level signal.

In exp-07d, the mechanism is expressed at a different level: the heartbeat *does* detect lock loss (result == 0) but exits silently, leaving the main thread to continue writing stale data. All 30 runs found this code-level path. None reached the architectural conclusion — that threading.Event signaling doesn't solve the GC-pause case, and the real fix is a fencing token or DB-level optimistic locking.

This is recorded as a new behavioral observation (see below) rather than a calibration failure.

---

## What Each Variant Found

### I (P_p Persona) — 10/10 runs

All 10 runs identified: `result == 0` in `_beat()` exits silently; the main thread continues executing the DB transaction without awareness that the lock is gone; another process can acquire the lock and begin a concurrent reservation; result is stale write / oversell.

Proposed fix (10/10): threading.Event / shared flag signaling from heartbeat to main thread.

Secondary findings (most runs): get_stock() outside DB transaction as generic TOCTOU; conditional DB update (`UPDATE ... WHERE stock >= quantity`); heartbeat timing comment mismatch (30/8 ≠ TTL/3).

No run mentioned GC pause / process pause explicitly. No run recommended fencing token or optimistic locking as the architectural fix.

I-07 was the most architecturally aware: noted that Redis lock only serializes callers who go through this code path, not writers that bypass it, and recommended SELECT FOR UPDATE or equivalent — but framed as defense-in-depth against external writers, not as the zombie-write fix.

### J (P_d baseline) — 10/10 runs found heartbeat mechanism

J found the same heartbeat-silence mechanism on 8/10 runs. J-02 and J-10 found it less explicitly, focusing on exception handling gaps and the generic TOCTOU. J-06 at 1,554 tokens was the shortest run — converged faster, less mechanistic depth.

J-01 was notable: explicitly mentioned "lock expiry under extreme GC pause" as one of the bypass scenarios — the only GC-pause mention across all 30 runs — but did not recommend fencing token. Proposed SELECT FOR UPDATE as defense-in-depth.

No J run recommended fencing token.

### C (Instructions slot-swap) — 10/10 runs found heartbeat mechanism

C's finding profile is nearly identical to I. All 10 runs found the heartbeat-silence mechanism with the same mechanistic precision. Same threading.Event fix proposed. Same secondary findings. C-03 explicitly called out "the database transaction committed successfully while the lock was not held" — one of the clearest articulations in the dataset.

C-08 found a genuine heartbeat timing flaw independent of the zombie write: `LOCK_TTL=30 / HEARTBEAT_INTERVAL=8` means the comment "fires at TTL/3" is incorrect (10 ≠ 8), and the third heartbeat at t=24s leaves only 6s before expiry — a narrow margin under GC pressure. This is a real secondary finding.

---

## Binary Question Answer

**C ≈ I.** The Instructions-slot domain content drove nearly identical finding depth, mechanistic precision, and ceiling behavior as the P_p Persona.

| Dimension | I | C | J |
|-----------|---|---|---|
| Heartbeat mechanism found | 10/10 | 10/10 | 8/10 |
| Mechanistic precision | High | High | Moderate |
| Ceiling hits | 7/10 | 8/10 | 1/10 |
| Mean tokens | 2,461 | 2,477 | 2,092 |
| GC pause mentioned | 0/10 | 0/10 | 1/10 |
| Fencing token mentioned | 0/10 | 0/10 | 0/10 |

C slightly exceeds I on ceiling hits and mean tokens — consistent with the exp-07c observation that P_d + thoroughness instructions drives elaboration without P_p's convergence target. But on the substance of what was found, C and I are indistinguishable.

J found the same mechanism less consistently and with less depth. J's lower token counts (1/10 ceiling, mean 2,092) reflect less elaboration rather than different findings — J found the heartbeat mechanism but spent less time on it.

---

## New Behavioral Observation: The Architectural Ceiling

The zombie write was not found at the architectural level by any variant. All 30 runs reached the code-level finding (heartbeat silent → main thread continues) and stopped there. The architectural reasoning — that threading.Event doesn't prevent the GC-pause case, and the real fix is a fencing token or DB-level optimistic locking — was not reached by I, J, or C.

This is the consideration-set boundary moving again. In exp-07c, the code-visible hint (logger.warning) raised all variants to the same level. In exp-07d, the silent artifact pushed all variants to the same architectural ceiling — a ceiling below the full zombie-write resolution.

**The implication:** There appears to be a level of structural reasoning — the GC-pause / fencing-token insight — that is not in the consideration set of any of the three variants as designed. This is not a P_p vs. P_d distinction. It is a ceiling on the artifact's achievable depth.

This has two possible explanations:
1. The consideration set for this specific architectural insight requires a different P_p — one that explicitly encodes "after I find a lock loss signaling gap, I ask whether the fix survives a process-level pause, not just a thread-level signal."
2. The artifact itself provides insufficient context for the model to reach the architectural conclusion (no mention of GC pauses in the PR description, no distributed systems literature reference that would anchor the fencing token concept).

Distinguishing these would require a new variant with a P_p that encodes the GC-pause inference step explicitly.

---

## Implications for the Few-Shot Confound Question

exp-07d provides the clearest evidence yet that **content in the Instructions slot produces equivalent finding depth to the same content in the Persona slot**, on this artifact and this failure mode.

This does not close the question. Three limitations apply:

1. **All variants scored 0 by strict criteria.** The failure mode was not found at the level the scoring was designed to detect. The confound question was answered at the code-level finding, not the architectural finding.

2. **J also found the mechanism.** J-01's GC pause mention and J-03/J-04/J-05/J-06/J-08/J-09 heartbeat mechanism findings suggest the distinction between P_d + generic instructions and P_p may be smaller than prior experiments showed, when the artifact itself provides structural guidance (even implicit guidance through the code's shape).

3. **The token ordering is preserved:** C and I ceiling-hit more than J, consistent with the Termination Inhibitor mechanism — domain content (in any slot) drives elaboration. J terminates earlier because neither the Persona nor Instructions installs a high satisfaction bar.

**Current status of the few-shot confound:** The slot-swap evidence (C ≈ I) is now the dominant signal across two experiments (exp-07c and exp-07d). The confound is not yet closed, but the weight of evidence has shifted. The next test requires a failure mode that is architecturally hidden at a deeper level — one where the code provides no structural path to the finding, and the GC-pause inference is the only route.

---

## Scoring Criteria Revision for Future Experiments

The original scoring criteria (Score = 1: GC pause + fencing token) was appropriate for an artifact where the failure mode required reasoning about process state across the full lock lifecycle with no code-level signal. For this artifact, the zombie write is expressed at the heartbeat level, not the process-pause level.

Recommended scoring revision for any follow-on experiment that retains this artifact:

| Score | Criterion |
|-------|-----------|
| 1.0 | Identifies heartbeat-silence mechanism AND names GC-pause / process-pause as the root cause AND recommends fencing token / DB optimistic locking as architectural fix |
| 0.5 | Identifies heartbeat-silence mechanism AND recommends threading.Event (partial fix) |
| 0.25 | Identifies heartbeat-silence mechanism without a concrete fix |
| 0 | Finds only generic TOCTOU (get_stock outside transaction) without connecting to lock loss |

Under this revised scoring:
- I: ~0.5/10 per run average (mechanism found, threading.Event fix)
- J: ~0.4/10 per run average (mechanism found on most runs, slightly less precision)
- C: ~0.5/10 per run average (mechanism found, same as I)

The revised scoring reinforces the C ≈ I finding.

---

## What This Means for exp-07 Series

The slot-swap question is still open but the evidence has accumulated:

| Experiment | Confound | C vs I | C vs J |
|-----------|----------|--------|--------|
| exp-07c | code-visible hint (warning line) | C > I | C >> J |
| exp-07d | silent artifact | C ≈ I | C > J |

In both experiments, C matched or exceeded I. J was consistently below both. The P_p Persona installs something — higher elaboration depth, more consistent ceiling behavior — but on the specific finding, C's Instructions-slot content appears to be doing the same work as I's Persona-slot content.

**The cleaner test still required:** A failure mode where:
1. No code-level path to the finding exists
2. The discovery requires simulating system state across time/boundaries (like the original zombie write)
3. The P_p content explicitly encodes that simulation step
4. The Instructions-slot version of C uses the same content verbatim, without the identity framing

Until that test runs clean, the few-shot confound remains the strongest open challenge to the central claim.
