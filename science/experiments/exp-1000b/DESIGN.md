# exp-1000b: Corrected Calibration — Scaffold + Interleaved Pipeline

**Status:** Complete — Tier 0.5 (4/6). H1b partially supported. See findings/FINDINGS.md.
**Hypothesis:** H1b

---

## Question

Does a pipeline that installs structural scaffold at the top of the funnel
(A–C), then applies interleaved craft+voice refinement (D–H), then enforces
structural and language gates (I–J) produce Tier 1.0 output against the
Mike-01.md benchmark?

---

## Background

exp-1000 tested a pure interleaved author/voice pipeline (9 agents, A–I) and
scored Tier 0 (0/6 gates). Root cause: craft quality and structural architecture
are independent axes. The interleaved pipeline optimized craft but assigned no
agent to structural roles — denial/verdict, falsification fragments, operative
variable, CTA. All 6 gates failed.

exp-1000b is corrected calibration. The interleaved pairing hypothesis is
preserved in the craft stage (D–H), but structural scaffold is installed first.

---

## H1b — Scaffold + Interleaved Pipeline

Three stages: scaffold (wide rim of funnel), craft+voice refinement (interleaved),
structural and language gates.

| Agent | Role | Job |
|-------|------|-----|
| A | Foundation | Distill article into LinkedIn post — immersion principle, reader inside the experience |
| B | Voice identity | Install the narrator — clinical, precise, without judgment. Protect all content. |
| C | Suspense/structure | Plant tension architecture — suspense signal before outcome, one hindsight sentence |
| D | Filter intrusion | Cut filter words — replace with sensation, action, fact. Place one narrative intrusion at the pivot. |
| E | Show don't tell | Show emotions as mechanism and outcome. Camera lens throughout. |
| F | Sensory + dialect | Add one non-visual sense per sensory-thin moment. Tune narrator vocabulary domain. |
| G | Rhythm + distance | Break flat sentence rhythm. Install one deliberate close/far distance shift. |
| H | Specificity + similes | Replace category nouns with particulars. Place one signature simile. |
| I | Opening + CTA | Fix opening if it doesn't create a gap. Plant CTA naming the unanswered question. |
| J | Final gate | Language standards — passive, nominalization, hedges, throat-clearing. Fix what fails. |

**Tone across all agents:** First person. Punchy. Precise. Cold. Dark Humor.

---

## Design

- **Artifact:** ARTIFACT.md (same PARC article used in content-pipeline and exp-1000)
- **Scoring:** SCORING.md — 6 binary gates against Mike-01.md benchmark
- **Model:** claude-sonnet-4-6, temperature=1
- **Runs:** n=1 per variant (pipeline — not a statistical experiment)
- **Control:** content-pipeline A→B→C→D (Tier 1.0, sequential)
- **Previous:** exp-1000 (Tier 0 — no structural agents)

---

## What exp-1000c, 1000d... will test

- **exp-1000c:** Swap pairings — different author/voice combinations in D–H
- **exp-1000d:** Sequential vs. interleaved head-to-head (same rules, different order)
- **exp-1000e:** Reduce to minimum agents that still produce Tier 1.0
- **exp-1000f:** Bullet vs. prose in CONTEXT — does formatting change output?
