# exp-20 Findings — Vocabulary-Only Slot-Swap

**Date:** 2026-03-30
**Status:** Complete
**Cost:** $1.1934 (30 runs × claude-sonnet-4-6, temp=0.5)

---

## Result

| Variant | Description | Detection | Mean words | Mean API tokens |
|---------|-------------|-----------|------------|-----------------|
| A | P_p Persona with domain vocabulary (no procedure) | 9/10 | 1,144 | 2,026 |
| B | P_d Persona + same vocabulary in Instructions | 9/10 | 1,150 | 2,309 |
| C | P_d Persona + generic Instructions (baseline) | 0/10 | 981 | 2,143 |

**A vs. B word count gap:** 6 words — within noise floor (~125 tokens per Phase 6).
**A vs. B API token gap:** 283 tokens — B substantially more verbose than A (see below).
**B ceiling hits:** 6/10 | **A ceiling hits:** 2/10

---

## Artifact

Same exp-01e zombie-write artifact as exp-19. Same detection criterion.

**Vocabulary content (A Persona / B Instructions):** Kleppmann, split-brain, zombie-write failure modes, fencing tokens, process isolation boundaries, lock lease expiry. No explicit procedure.

---

## Interpretation

**H2 again corroborated, with two caveats.**

A = B on detection (9/10 each) and on scoring-relevant word count (6-word gap = noise). Slot placement did not add detectable lift when vocabulary was present in either slot.

**Caveat 1 — Vocabulary too directive.** The vocabulary named "zombie-write failure modes" and "fencing tokens" — the failure mode class and the fix class directly. Both variants were handed strong orientation. This is closer to exp-19's explicit procedure than to generic vocabulary (exp-09). The vocabulary specificity is the operative variable, not the slot.

**Caveat 2 — Near-ceiling.** Both A and B reached 9/10. A genuine slot effect of 1-2 runs would be invisible. The ceiling effect objection from exp-19 applies again.

**Vocabulary specificity finding (new):** exp-09 used generic distributed systems vocabulary in Instructions (Kleppmann, split-brain, lease expiry) → null result (C ≈ B). exp-20 used failure-mode-specific vocabulary in Instructions → B = 9/10. The operative distinction is specificity, not slot. This holds across both Persona and Instructions variants.

**API token paradox (new observation):** B produced 283 more mean API tokens than A (2,309 vs. 2,026), with 6/10 ceiling hits vs. A's 2/10. Scoring-relevant word counts were nearly identical (1,150 vs. 1,144). Interpretation: vocabulary in the Instructions slot may act as an output template driver (treats vocabulary list as checklist of things to address → verbose output). Vocabulary in the Persona slot acts as a reasoning filter (installs orientation, produces focused output). Same detection, different output economy. Not yet robustly established — needs exp-21 tracking.

---

## Manual Review Notes

- **A-10 (Score 0 confirmed):** Named "zombie-write vector" and "GC pause" in heartbeat timing context, but fix was Lua atomic release for TOCTOU in lock release (different failure mode). No process-pause → DB-write chain. Correctly Score 0.
- **B-02 (Score 0 confirmed):** Same pattern — TOCTOU + Lua fix, "zombie-write scenario per Kleppmann" used but for lock release concern, not all-threads-paused scenario.
- **C-03 (Score 0 confirmed):** Fix keywords (Lua script) without process-pause scenario.

---

## What this changes in the theory

Confirms the exp-09 → exp-18 → exp-19 → exp-20 progression:
- Generic vocabulary in Instructions → no detection (exp-09)
- Explicit procedure in both slots → A = B = 10/10 (exp-19)
- Directive vocabulary in both slots → A = B = 9/10 (exp-20)

The pattern is consistent: when equivalent content is in both slots, detection is equivalent. The slot is not adding lift beyond the content. Whether this holds when content is less directive and task difficulty prevents ceiling is still open.

---

## What remains open

1. **Vocabulary proximity effect.** Does naming "zombie-write failure modes" anywhere in context (including in the artifact itself) drive detection, or does it need to be in a Persona/Instructions slot? Exp-21A tests this.

2. **Less directive vocabulary at non-ceiling difficulty.** At what specificity level does slot start to matter (if ever)? Exp-21B tests this with less directive vocabulary designed not to ceiling either variant.

3. **Output economy signal.** B API output > A despite same detection. Is vocabulary in Instructions installing enumerative verbosity vs. vocabulary in Persona installing focused search? Track in exp-21.

---

## Next Experiments

**Exp-21A — Vocabulary in artifact (Gemini's question):**
Same artifact with vocabulary injected into the PR description itself. Three variants: A = artifact vocabulary + P_p Persona; B = artifact vocabulary + P_d + generic Instructions; C = no vocabulary anywhere (baseline). Tests whether vocabulary needs a Persona slot or works anywhere in context.

**Exp-21B — Less directive vocabulary, non-ceiling:**
Same artifact. Vocabulary that provides domain orientation without naming the failure mode or fix: "distributed lock protocols, process isolation, lock lifecycle analysis." No "zombie-write" or "fencing token." Tests whether slot matters when vocabulary is less directive.

---

## Files

- `variants/A-pp-vocabulary.md` — P_p Persona with vocabulary
- `variants/B-pd-vocabulary.md` — P_d + vocabulary in Instructions
- `variants/C-pd-baseline.md` — P_d baseline
- `output/` — 30 raw model outputs (A-01 through C-10)
- `review/scores.md` — keyword pre-screen scores
- `review/gemini-results.md` — Gemini results review
- `review/cc-synthesis.md` — CC synthesis
- `review/gemini-synthesis-review.md` — Gemini synthesis challenge
- `review/cc-decision.md` — CC decision (this experiment)
