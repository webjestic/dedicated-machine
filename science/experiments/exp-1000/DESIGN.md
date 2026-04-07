# exp-1000: Interleaved Author/Voice Pipeline

**Status:** Complete — Tier 0 (0/6). H1 not supported. See findings/FINDINGS.md.
**Hypothesis:** H1

---

## Question

Does an interleaved pipeline — where each agent applies one author-style rule
paired with one complementary voice rule — produce higher benchmark scores than
a sequential layer approach (author-style layer first, voice layer second)?

---

## Background

The content-pipeline prototype (parc/examples/content-pipeline/) established a
sequential four-agent pipeline (A→B→C→D) achieving Tier 1.0 on the 6-gate
scoring rubric against the Mike-01.md benchmark. That pipeline applies
author-style rules first, with voice compression last.

The hypothesis here: author rules and voice rules are not additive — they are
multiplicative when applied together. The observational lens (voice) determines
*what* to show; show don't tell (author) determines *how* to show it. Pairing
them in the same agent produces more coherent output than applying them in
separate sweeps.

---

## H1 — Interleaved Pipeline

Each agent receives one author-style rule paired with one voice rule selected
for complementary function. Nine agents. A is fattest; each subsequent agent
narrows one dimension. I is the final structural gate.

| Agent | Author rule | Voice rule | Shared job |
|-------|-------------|------------|------------|
| A | Write the post | Immersion principle | Frame from the start |
| B | No content loss | Voice identity | Install who is writing |
| C | Filter word prohibition | Narrative intrusion | Presence and absence |
| D | Show don't tell | Observational lens | What to show, through whose eyes |
| E | Sensory layering | Speech patterns & dialect | Texture — feel and sound |
| F | Suspense architecture | Suspense via hindsight | Tension |
| G | Sentence variation | Narrative distance | Rhythm and proximity |
| H | Specificity/grounding | Signature similes | Concrete detail through voice |
| I | Language standards | Best practices (opening/cliffhanger) | Final gate |

---

## Design

- **Artifact:** ARTIFACT.md (same PARC article used in content-pipeline)
- **Scoring:** SCORING.md — 6 binary gates against Mike-01.md benchmark
- **Model:** claude-sonnet-4-6, temperature=1
- **Runs:** n=1 per variant (pipeline — not a statistical experiment)
- **Control:** content-pipeline A→B→C→D (Tier 1.0, sequential)

---

## What exp-1000b, 1000c... will test

- **exp-1000b:** Remove two middle agents — does the tier hold with 7?
- **exp-1000c:** Swap pairings — different author/voice combinations
- **exp-1000d:** Sequential vs. interleaved head-to-head (same rules, different order)
- **exp-1000e:** Reduce to minimum agents that still produce Tier 1.0
