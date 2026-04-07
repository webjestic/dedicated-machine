# exp-1000d: Full Structural Gate — All Four Jobs to Agent I

**Status:** Complete — Tier 1.0 (6/6). H1d supported. See findings/FINDINGS.md.
**Hypothesis:** H1d

---

## Question

Does consolidating all four structural assignments into Agent I — denial,
verdict, falsification fragments, and CTA — allow the pipeline to reach
Tier 1.0 (6/6)?

---

## Background

exp-1000c scored Tier 0.5 (4/6). Gate 1 fixed, Gate 2 broke, Gate 4 persistent.

Root causes identified:
- **Gate 2 (Verdict):** No agent installs a ≤5-word isolated verdict paragraph.
  When I rewrote the opening denial, the verdict slot was consumed.
- **Gate 4 (Falsification):** Fragment assignment in D (position 4) was
  overwritten by six subsequent prose-editing passes (E–J). Format does not
  survive prose editing.

Solution: move all structural assignments to Agent I, which runs after all
prose editing is complete. Nothing downstream overwrites I's output except J
(language standards only — J does not reformat structure).

---

## H1d — Full Structural Gate at I

**Change 1 — Agent D restored:** Falsification fragment instruction removed.
D returns to exp-1000b: filter words + narrative intrusion only.

**Change 2 — Agent I extended:** Now handles four structural jobs in order:
1. Denial — name and strip wrong assumption in first line
2. Verdict — ≤5-word isolated paragraph immediately after denial
3. Falsification fragments — reformat intuitive fix into one move per line
4. CTA — name the unanswered question, point to the answer

All other agents unchanged from exp-1000c.

| Agent | Change |
|-------|--------|
| A | Unchanged |
| B | Unchanged |
| C | Unchanged |
| D | **Restored** — back to filters + intrusion only |
| E | Unchanged |
| F | Unchanged |
| G | Unchanged |
| H | Unchanged |
| I | **Extended** — denial + verdict + falsification fragments + CTA |
| J | Unchanged |

---

## Design

- **Artifact:** ARTIFACT.md (same PARC article throughout 1000 series)
- **Scoring:** SCORING.md — 6 binary gates against Mike-01.md benchmark
- **Model:** claude-sonnet-4-6, temperature=1
- **Runs:** n=1 per variant (pipeline — not a statistical experiment)
- **Control:** exp-1000c (Tier 0.5, 4/6)
- **Target:** Tier 1.0 (6/6)
