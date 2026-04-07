# exp-1000d Findings — Full Structural Gate at Agent I

**Status:** Complete
**Result:** Tier 1.0 (6/6 gates)
**H1d:** Supported

---

## Score

| Gate | Criterion | Result |
|------|-----------|--------|
| 1 | Denial landed | PASS |
| 2 | Verdict stated | PASS |
| 3 | Inside the finding | PASS |
| 4 | Falsification shown | PASS |
| 5 | Operative variable | PASS |
| 6 | CTA earned | PASS |

**Total: 6/6 — Tier 1.0**

Control (exp-1000c): 4/6 — Tier 0.5
Benchmark (content-pipeline A→B→C→D): 6/6 — Tier 1.0

---

## Trajectory

| Exp | Score | Key change |
|-----|-------|------------|
| exp-1000 | 0/6 | No structural agents |
| exp-1000b | 4/6 | Scaffold at top of funnel |
| exp-1000c | 4/6 | Denial sharpened; fragment format assigned to D |
| exp-1000d | 6/6 | All structural gates consolidated into I |

---

## What Worked

Consolidating all four structural assignments into Agent I, which runs after
all prose editing is complete:

1. **Denial** — "The credential is not the mechanism." First line, explicit,
   strips the wrong assumption directly.

2. **Verdict** — "Attention is." 2 words, isolated paragraph, white space
   before and after.

3. **Falsification fragments** — Assigned at I (position 9), nothing downstream
   overwrites it except J (language standards only, which does not reformat
   structure). Clean fragment format survived to final output:
   ```
   The intuitive fix: make the credential stronger.

   Tested.
   Added seniority markers.
   Added compulsion framing — "cannot help but," "constitutionally unable to."
   Watched output collapse to baseline anyway.
   ```

4. **CTA** — Names the unanswered question ("what semantic neighborhood density
   means at the token level — and why fusion outperforms split when vocabulary
   is identical"), points to the article, does not explain what's there.

---

## Key Architectural Finding

**Fragment format does not survive prose-editing passes.**

Assigning structural format to an agent early in the pipeline (exp-1000c: D at
position 4) produces the format, but six subsequent prose-editing agents
(E through J) reconstruct it as prose. The format must be applied after prose
editing is complete.

**The correct architecture: structure after craft.**

Craft agents (A–H) produce the experience. The structural gate (I) installs the
architecture. The language gate (J) enforces standards without reformatting
structure.

---

## Pipeline Architecture — Final Form

| Stage | Agents | Job |
|-------|--------|-----|
| Scaffold | A, B, C | Immersion, voice, suspense |
| Craft | D, E, F, G, H | Filter, show/tell, sensory, rhythm, specificity |
| Structure | I | Denial + verdict + fragments + CTA |
| Gate | J | Language standards |

---

## Cost

Total: $0.1120 (10 runs × 1 each, sonnet-4-6, temp=1)
Total across 1000 series: ~$0.67 (exp-1000 through exp-1000d)
