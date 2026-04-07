# exp-1000c: Surgical Fixes — Denial and Falsification Fragments

**Status:** Complete — Tier 0.5 (4/6). H1c partially supported. See findings/FINDINGS.md.
**Hypothesis:** H1c

---

## Question

Do two surgical fixes to exp-1000b — sharpening the denial instruction in
Agent I and adding falsification fragment format to Agent D — push the pipeline
from Tier 0.5 (4/6) to Tier 1.0 (6/6)?

---

## Background

exp-1000b scored Tier 0.5 (4/6). Gates 2, 3, 5, 6 cleared. Gates 1 and 4
failed on form, not content:

- **Gate 1 (Denial):** Agent I accepted an immersive scene-setting opening
  as a valid gap. The gate requires an explicit denial — the wrong assumption
  named and stripped in the first line. "Gap" is broader than "denial."

- **Gate 4 (Falsification):** The falsification existed but two moves were
  combined per sentence. The gate requires one move per line, no connecting
  tissue. No agent in the pipeline had this assignment.

exp-1000c makes exactly two changes. Everything else is held constant.

---

## H1c — Two Surgical Fixes

**Change 1 — Agent D extended:** Falsification fragment format added as
instruction 3. D now handles filter words, narrative intrusion, AND
falsification fragments. Termination condition updated to include fragments.

**Change 2 — Agent I sharpened:** Denial definition tightened. "Creates a gap"
replaced with "names and strips a wrong assumption — not through contrast, not
through scene, not through implication." The form is explicit: "The [X] is not
[Y]." or equivalent direct denial.

All other agents unchanged from exp-1000b.

| Agent | Change |
|-------|--------|
| A | Unchanged |
| B | Unchanged |
| C | Unchanged |
| D | **Extended** — adds falsification fragment format as instruction 3 |
| E | Unchanged |
| F | Unchanged |
| G | Unchanged |
| H | Unchanged |
| I | **Sharpened** — denial definition now explicit, not just "gap" |
| J | Unchanged |

---

## Design

- **Artifact:** ARTIFACT.md (same PARC article throughout 1000 series)
- **Scoring:** SCORING.md — 6 binary gates against Mike-01.md benchmark
- **Model:** claude-sonnet-4-6, temperature=1
- **Runs:** n=1 per variant (pipeline — not a statistical experiment)
- **Control:** exp-1000b (Tier 0.5, 4/6)
- **Target:** Tier 1.0 (6/6)
