# exp-1000 Findings — Interleaved Author/Voice Pipeline

**Status:** Complete
**Result:** Tier 0 (0/6 gates)
**H1:** Not supported

---

## Score

| Gate | Criterion | Result |
|------|-----------|--------|
| 1 | Denial landed | FAIL |
| 2 | Verdict stated | FAIL |
| 3 | Inside the finding | FAIL |
| 4 | Falsification shown | FAIL |
| 5 | Operative variable | FAIL |
| 6 | CTA earned | FAIL |

**Total: 0/6 — Tier 0**

Control (content-pipeline A→B→C→D): Tier 1.0 (6/6)

---

## What the Output Actually Produced

The final output (I-01.md) is high-quality prose. It is immersive, specific, and
uses mechanism vocabulary. It has sensory texture, suspense architecture, and a
consistent narrator. Every craft dimension the pipeline was designed to apply is
present and working.

None of it cleared a single structural gate.

---

## Root Cause

**Craft quality and structural architecture are independent variables.**

The nine-agent interleaved pipeline optimized for craft — immersion, voice
identity, filter removal, showing vs. telling, texture, tension, rhythm,
specificity. None of those agents were assigned a structural role:

- No agent installs the denial/verdict scaffold (Gates 1, 2)
- No agent requires the falsification in fragment format (Gate 4)
- No agent plants an operative variable (Gate 5)
- No agent adds a CTA (Gate 6)
- Agent I checks for an opening "gap" but corrects it only to the degree
  the passage already contains a correctable element — it cannot install
  structural architecture that was never there

The content-pipeline control (Tier 1.0) had structural roles baked into the
agent assignments:
- Agent A: write the post (immersion principle)
- Agent B: find where finding was reported not shown — install fragment
  falsification (Gate 4)
- Agent C: place line breaks at verdicts + add CTA (Gates 2, 6)
- Agent D: compress for impatience (Gates 3, 5 tightened)

The interleaved pipeline replaced these structural roles with craft roles.
The craft improved. The structure disappeared.

---

## Gate-by-Gate Analysis

### Gate 1 — Denial
The opening shows the consequence of the wrong assumption rather than naming
and stripping the assumption. Immersive scene-setting replaced explicit denial.
No agent was assigned to install or protect the denial structure.

### Gate 2 — Verdict
The reframe ("the credential is not the persona") appears near the end, buried
in a paragraph, at roughly 120 words. No isolated ≤5-word verdict paragraph
exists anywhere in the output.

### Gate 3 — Filter words
"And here is what this means for how you write." — "this means" is on the
explicit filter list. One instance. Agent C removed filter words from the
draft it received; this phrase was introduced in a later pass.

### Gate 4 — Falsification
The compulsion falsification is narrated in prose paragraphs, not shown in
fragments. The structure is present — four variants, results stated — but the
form is summary, not demonstration. Agent B in exp-1000 protects content and
installs narrator identity; it does not require or install fragment format.

### Gate 5 — Operative variable
"The compulsion was always a passenger." (5 words) is the closest candidate.
Not falsifiable as stated — it names a conclusion, not a test. The testable
claim ("Mechanism vocabulary in either slot produced 10/10. Orientation
vocabulary produced 0/10.") exists but spans two sentences and is not isolated.

### Gate 6 — CTA
Absent. No agent in the pipeline was assigned to add one.

---

## What This Means for the Research Program

H1 failed, but the failure is informative. It isolates two independent axes:

**Axis 1 — Structural architecture:** denial, verdict, falsification format,
operative variable, CTA. These are the gates. They require explicit agent
assignment.

**Axis 2 — Craft quality:** immersion, voice, filter removal, showing,
texture, suspense, rhythm, specificity. These raise the quality of whatever
structure is already present.

The interleaved pipeline was a pure Axis 2 pipeline. The sequential
content-pipeline had Axis 1 agent roles that also improved Axis 2 incidentally.

**The correct model is not "craft layer then voice layer" (what H1 was designed
to replace) and not "interleaved craft+voice" (what H1 tested). It is
"structural scaffold first, then craft+voice refinement."**

The scaffold must be load-bearing before refinement begins. Craft applied to
an unscaffolded draft produces high-quality prose that clears no gates.

---

## Implications for exp-1000b

The ablation plan (exp-1000b: remove two middle agents) is no longer the right
next experiment. The pipeline architecture itself needs revision.

**Proposed redesign (exp-1000b):** Hybrid pipeline — structural agents first
(denial, verdict, falsification format, CTA), then interleaved craft+voice
agents after the scaffold is installed.

| Stage | Agent | Job |
|-------|-------|-----|
| Scaffold | S1 | Write the post + install denial/verdict structure |
| Scaffold | S2 | Show falsification in fragments + plant operative variable |
| Scaffold | S3 | Add CTA + place line breaks at verdicts |
| Craft+Voice | C1 | Voice identity + no content loss |
| Craft+Voice | C2 | Filter prohibition + narrative intrusion |
| Craft+Voice | C3 | Show don't tell + observational lens |
| Craft+Voice | C4 | Sentence variation + narrative distance |
| Gate | G1 | Language standards + opening/close gate |

This separates structure (load-bearing) from craft (quality of execution) while
preserving the interleaved author/voice pairing hypothesis within the craft stage.

---

## Cost

Total: $0.3302 (9 runs × 1 each, sonnet-4-6, temp=1)
