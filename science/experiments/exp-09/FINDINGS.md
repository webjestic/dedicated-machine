# exp-09 FINDINGS

**Experiment:** Clean slot-swap falsification — P_p vs Instructions-slot domain content on unhinted artifact
**Date:** 2026-03-28
**Model:** claude-sonnet-4-6, temperature 0.5, max_tokens 2500
**Runs:** 40 (n=10 per variant)
**Total cost:** $1.6277

---

## Results Summary

| Variant | Persona | Instructions extras | Ceiling hits | Mean tokens | Tier 1.0 | Tier 0.5 |
|---------|---------|---------------------|-------------|-------------|----------|----------|
| A | P_p — distributed systems engineer | None | 5/10 | 2,362 | 1/10 | 10/10 |
| B | P_d — senior software engineer | None | 0/10 | 1,842 | 0/10 | 10/10 |
| C | P_d — senior software engineer | + domain content | 0/10 | 1,853 | 0/10 | 10/10 |
| D | P_p — distributed systems engineer | + domain content | 2/10 | 2,363 | 0/10 strict | 10/10 |

**Primary binary question result: C ~ B ≠ A**

**Secondary question result: D ≈ A on strict Tier 1.0, D shows 2/10 near-Tier-1.0 (fencing token without GC-pause framing)**

---

## Primary Finding: Persona Is Load-Bearing on Clean Artifact

C (mean 1,853 tokens, 0/10 ceiling) matches B (1,842, 0/10) on every measurable dimension.
A (2,362, 5/10) is clearly distinct.

The few-shot confound from exp-07c/07d — where Instructions-slot domain content produced results equivalent to P_p — does not hold on the clean artifact. Removing the artifact-level hints (checklist item naming the detection behavior) caused C to collapse back to B-level performance.

This is the cleanest result of the series. C ~ B on tokens, ceiling hits, and Tier scoring. The Instructions domain content changed the framing and vocabulary of C's outputs (see below) but did not install the consideration-set depth that distinguishes A from B.

**Interpretation from SCORING.md outcome table:** Persona slot load-bearing; Instructions compensation in exp-07c/07d was artifact-level.

---

## Calibration Observation: Artifact Still Visible at Tier 0.5

All four variants found the zombie-write at 10/10. The clean artifact (unannotated `if result == 0: return` in `_renew()`) was still visible enough for P_d to find the mechanism without P_p's consideration set.

This is a partial calibration failure at Tier 0.5. The goal was for B to score lower than A on mechanism detection — to create a gap where Instructions-slot content could be measured. Instead, all ten B runs found the silent renewal exit. The `if result == 0: return` branch creates a visible dead end in the code that a careful reviewer can notice even without temporal simulation.

The differentiation that remains measurable:
1. **Token volume and ceiling hits** — A (2,362, 5/10) vs B/C (≈1,850, 0/10)
2. **Tier 1.0 framing** — architectural fix naming (GC pause + DB-layer enforcement)
3. **Output structure** — how prominently the gap-during-execution finding is organized

The binary question is still answerable from (1): C ~ B, not C ~ A.

---

## What Each Variant Found

### A (P_p, no extras) — 10/10 zombie-write, 1/10 Tier 1.0

All 10 runs identified `if result == 0: return` in `_renew()` as a silent claim-loss path with no signal to the main thread. All proposed threading.Event or shared flag as the fix (Tier 0.5).

**A-07 reached Tier 1.0:** Explicitly walked the scenario — "a GC pause or network partition causes the renewal to miss → two workers can both pass the `get_execution` check and both attempt to write" — and recommended "upsert-with-conflict or a unique constraint that causes the second writer to fail." Both conditions for Tier 1.0 met: process-pause trigger + DB-layer enforcement as the fix.

GC pause mentions in A across all 10 runs: 4 runs mentioned it, but A-01, A-06, and A-09 placed it in the context of TTL sizing (renewal interval math), not as the zombie-write trigger. Only A-07 named it as the causal mechanism for the dual-write scenario.

Secondary findings (most runs): `_dispatch` exception escapes `execute()` breaking the `JobResult` contract; `get_execution` outside the DB transaction as generic TOCTOU; renewal thread swallows Redis exceptions.

### B (P_d, no extras) — 10/10 zombie-write, 0/10 Tier 1.0

All 10 runs found the silent renewal exit. Most organized it as a medium or high severity finding, typically after a `_dispatch` exception handling issue they rated critical. The renewal silence finding was present but not consistently the primary finding.

No GC pause mentions. No fencing token or DB-layer enforcement mentions. Proposed fixes were consistently threading.Event or shared flag (Tier 0.5).

B-04 and B-08 came closest to Tier 1.0: both named the dual-writer scenario (Redis failover / network partition → second worker acquires → both pass the idempotency check) and both recommended a DB-level unique constraint as the fix. Neither named GC pause. Borderline Tier 0.75.

### C (P_d + Instructions domain content) — 10/10 zombie-write, 0/10 Tier 1.0

All 10 runs found the zombie-write. C's outputs are qualitatively distinguishable from B's: all 10 leads prominently with the gap-during-execution finding, and several (C-04, C-07) explicitly quote or echo the Instructions framing ("the gap between when coordination is lost and when the code learns it"). The Instructions directive shaped how the finding was presented and prioritized.

But the finding depth did not change. C stopped at Tier 0.5 on all 10 runs — threading.Event signaling — same as B. No fencing token mentions. No GC pause as the zombie-write trigger.

**Token distribution confirms:** C (mean 1,853) ≈ B (1,842). The Instructions domain content neither added elaboration depth nor installed the P_p search algorithm. It functioned as a template for organizing and framing the output, not as a behavior installer.

C-04 is the most explicit example of Instructions content affecting framing without affecting depth: it quotes the Instructions prompt verbatim as "the question I apply to every distributed coordination review" and then answers it at exactly the threading.Event level.

### D (P_p + Instructions domain content) — 10/10 zombie-write, 0/10 strict Tier 1.0

All 10 runs found the zombie-write. D closely tracks A on tokens (D mean 2,363, A mean 2,362) and ceiling hits (D 2/10, A 5/10). Adding Instructions domain content to P_p slightly reduced ceiling hits — consistent with the termination-anchor effect observed in exp-08.

**Near-Tier-1.0 observations:**

D-02 and D-06 named fencing token explicitly: "for full closure, the database transaction itself would need to verify claim ownership... without a fencing token written into the DB row." Both also walked the dual-writer scenario. Neither named GC pause as the trigger — both attributed the claim loss to Redis eviction or network partition.

Strict Tier 1.0 requires both the process-pause scenario AND the DB-layer fix. D-02 and D-06 have the fix without the specific trigger, placing them at approximately 0.75. This is a different flavor of near-Tier-1.0 than A-07, which had the trigger without the fencing token label.

**D does not clearly exceed A at strict Tier 1.0** (0/10 strict vs 1/10). The additive gain from Instructions + P_p is marginal and takes a different form than expected — fencing token naming increases, but the GC-pause framing that characterizes the deepest finding does not.

---

## Binary Question Answer

**Primary (C~A or C~B?): C ~ B.** The Instructions domain content did not install P_p behavior on the clean artifact.

| Dimension | A | C | B |
|-----------|---|---|---|
| Zombie-write | 10/10 | 10/10 | 10/10 |
| Tier 1.0 | 1/10 | 0/10 | 0/10 |
| Mean tokens | 2,362 | 1,853 | 1,842 |
| Ceiling hits | 5/10 | 0/10 | 0/10 |

C falls with B on all dimensions. The Instructions-slot compensation in exp-07c/07d was artifact-level, not structural.

**Secondary (D>A or D≈A?): D ≈ A.** Instructions domain content does not extend the P_p ceiling when added to P_p. The same termination-anchor effect observed in exp-08 applies: ceiling hits dropped (5/10 → 2/10), tokens nearly unchanged. D shows 2/10 near-Tier-1.0 (fencing token named), A shows 1/10 strict Tier-1.0 (GC-pause named). Not a clear improvement.

| Dimension | D | A |
|-----------|---|---|
| Tier 1.0 (strict: GC-pause + fencing) | 0/10 | 1/10 |
| Near Tier 1.0 (fencing token named) | 2/10 | 0/10 |
| Tier 0.5 | 10/10 | 10/10 |
| Mean tokens | 2,363 | 2,362 |
| Ceiling hits | 2/10 | 5/10 |

---

## New Observation: Instructions Content as Output Template, Not Behavior Installer

C's outputs are consistently better-organized around the primary finding than B's. The Instructions directive ("ask one more question... simulate the full lifecycle under an adverse timing scenario") shaped the structure and vocabulary of the output — C reviews lead with the gap-during-execution finding and frame it prominently.

But this is template installation, not consideration-set expansion. C found the same thing B found, presented it more directly, and stopped at the same tier. The Instructions content told the model *where to put its answer* and *how to frame it*, but not *how deep to go* once it got there.

This is consistent with the two-layer model. Instructions are Task Layer — they install procedure, structure, and framing. Persona is World Layer — it installs the consideration set that determines what the model is capable of finding. The Instructions directive in C redirected P_d's attention to the right location but could not install the depth that P_p's identity encoding provides.

---

## Relationship to exp-07c/07d and exp-08

The few-shot confound resolution:

| Experiment | Artifact | C result | Interpretation |
|-----------|---------|---------|----------------|
| exp-07c | Contaminated (instructions name fail path) | C ≈ I | Instructions installs P_p — but artifact was hinted |
| exp-07d | Contaminated (checklist names heartbeat detection) | C ≈ I | Same — artifact-level |
| exp-09 | Clean (no checklist hint, unannotated `if result == 0`) | C ~ B | Artifact-level confound confirmed; Instructions cannot install P_p independently |

The exp-07c/07d result — Instructions-slot domain content ≈ P_p — was a confounded measurement. On a clean artifact, the Instructions directive reduced to a framing template. Persona remained the load-bearing behavior installer.

**Complete slot comparison through exp-09:**

| Experiment | Slot | Content type | Result vs. B |
|-----------|------|--------------|-------------|
| exp-07c/07d | Instructions | P_p domain knowledge (contaminated) | ≈ A (matched P_p) |
| exp-09 | Instructions | P_p domain knowledge (clean) | ~ B (no lift) |
| exp-08 | Examples | Mechanism demonstrations | ~ B (no lift) |
| exp-08 (K) | AXIOMS | Descriptive formula | ~ B (no lift) |
| exp-08 (L) | AXIOMS | Procedural bootstrap | ~ B on tier (bootstrapped but shallow) |

On a clean artifact: no non-Persona slot installs P_p consideration-set behavior. Persona is the load-bearing installer.
