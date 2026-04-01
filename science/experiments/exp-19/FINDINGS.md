# exp-19 Findings — Clean Slot-Swap

**Date:** 2026-03-29
**Status:** Complete
**Cost:** $1.2536 (30 runs × claude-sonnet-4-6, temp=0.5)

---

## Result

| Variant | Description | Detection | Mean tokens |
|---------|-------------|-----------|-------------|
| A | P_p Persona (procedure in identity) | 10/10 | 1199 |
| B | P_d Persona + procedural Instructions | 10/10 | 1193 |
| C | P_d Persona + generic Instructions (baseline) | 0/10 | 1026 |

**A vs B gap:** 6 tokens — within noise floor (~125 tokens per Phase 6).

---

## Artifact

Inventory reservation service (exp-01e zombie-write artifact). Redis distributed lock with heartbeat. Failure mode: GC stop-the-world / process pause freezes all threads including heartbeat; lock expires; critical DB write executes on stale lock. Fix: fencing token or optimistic lock at DB write level.

Detection criterion: BOTH (1) process-pause scenario named AND (2) fencing token or optimistic lock at DB write level named as fix. Score 1 = both; Score 0 = anything else.

Calibration baseline from exp-01e: P_p = 10/10, P_d = 0/10. Calibration held in exp-19.

---

## Interpretation

**H2 corroborated (with ceiling caveat).** When procedural content is explicit and sufficient for the task, slot placement does not add detectable lift. B = A on both detection rate and token depth.

The most parsimonious explanation: the procedural content is the operative variable. When it specifies what to look for and what the fix is, the model finds it regardless of whether that content lives in the Persona slot or the Instructions slot.

**Ceiling caveat (per Gemini synthesis challenge):** A and B both hit 10/10. Any latent slot advantage is unobservable at this task difficulty. The conclusion is bounded: slot placement does not add lift *for tasks where explicit procedure is sufficient to ceiling detection*. Whether slot matters when content cannot fully specify the procedure remains open.

**C-08 note:** Pre-screen flagged C-08 for REVIEW (fix keywords matched). Manual review confirmed Score 0 — the fix named was atomic Lua script for non-atomic lock release (different concern), no process-pause scenario named.

---

## What this changes in the theory

Exp-19 is the first clean slot-swap test against this artifact. Prior to this, the strongest objection to H2 was: "we haven't run the same procedural content in both slots cleanly." That gap is closed. B = A.

Revises running synthesis in `pcsieftr.md`:
- Slot-swap now tested under calibrated conditions
- H2 (content as operative variable) corroborated
- H1 (slot is load-bearing) not retired — bounded to tasks where explicit procedure is insufficient

---

## What remains open

1. **Novel synthesis question:** Does slot matter when the task requires synthesis beyond what explicit procedure covers? If the model must *discover* what the failure mode is rather than *apply* a named procedure, does P_p embed better orientation?

2. **Content-as-installer question:** Does procedural content in Instructions install a consideration-set shift (H2a) or act as in-context guidance only (H2b)? Both produce the same output in exp-19.

3. **Weak-content boundary:** At what level of instruction specificity does slot placement start to matter?

---

## Next experiment

**Exp-20 design:** Same zombie-write artifact. Instructions stripped to domain vocabulary only (no explicit procedure). Three variants:
- A = P_p Persona with vocabulary embedded in identity
- B = P_d Persona + vocabulary list in Instructions slot
- C = P_d Persona + generic Instructions (baseline)

If slot matters at all, it should appear when content provides orientation without specifying procedure. This directly addresses the novel synthesis question and Gemini's ceiling-effect objection.

---

## Files

- `variants/A-pp-persona.md` — P_p Persona variant
- `variants/B-pd-instructions.md` — P_d + procedural Instructions
- `variants/C-pd-baseline.md` — P_d baseline
- `output/` — 30 raw model outputs (A-01 through C-10)
- `review/scores.md` — keyword pre-screen scores
- `review/gemini-results.md` — Gemini results review
- `review/cc-synthesis.md` — CC synthesis
- `review/gemini-synthesis-review.md` — Gemini synthesis challenge
- `review/cc-decision.md` — CC decision (this experiment)
