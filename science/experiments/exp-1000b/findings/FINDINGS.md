# exp-1000b Findings — Scaffold + Interleaved Pipeline

**Status:** Complete
**Result:** Tier 0.5 (4/6 gates)
**H1b:** Partially supported

---

## Score

| Gate | Criterion | Result |
|------|-----------|--------|
| 1 | Denial landed | FAIL |
| 2 | Verdict stated | PASS |
| 3 | Inside the finding | PASS |
| 4 | Falsification shown | FAIL |
| 5 | Operative variable | PASS |
| 6 | CTA earned | PASS |

**Total: 4/6 — Tier 0.5**

Control (content-pipeline A→B→C→D): Tier 1.0 (6/6)
Previous (exp-1000, pure interleaved): Tier 0 (0/6)

---

## Progress

exp-1000b more than doubled the gate score — 0/6 to 4/6. The scaffold hypothesis
is partially supported: installing structural agents before craft refinement
produced measurable improvement. Gates 2, 3, 5, and 6 now clear.

Gates 1 and 4 fail for the same underlying reason.

---

## Root Cause — Gates 1 and 4

**Gate 1 (Denial):** The opening is immersive scene-setting that implies the
wrong assumption through contrast — two engineers, same label, different output.
The reader infers the failure of the credential assumption. But the gate requires
the assumption to be named and stripped explicitly in the first line. Immersion
and denial are not the same move. The pipeline produces the first; the gate
requires the second.

**Gate 4 (Falsification):** The falsification exists and is correctly positioned.
The moves are present:
- Strip the domain vocabulary, keep the compulsion → baseline
- Strip the compulsion, keep the domain vocabulary → outputs hold

But they are combined into sentences rather than broken into fragments. The gate
requires one move per line with no connecting tissue. The pipeline produces
compressed prose where two moves share a sentence. Close in content. Wrong in form.

Both failures are **formal failures, not content failures.** The information is
present. The structure required by the gate is not.

---

## Gate-by-Gate Analysis

### Gate 1 — Denial
The output opens: "Two engineers. Same model. Same ten-year label. One gets a
competent review. The other gets the race condition that only fires under 50ms
contention windows."

Strong opening. Creates immediate tension. Shows the gap. Does not name and
strip the assumption. The gate requires: "The 'You are' sentence isn't guidance."
— explicit, direct, the wrong thing named. This opening shows the consequence
of the wrong assumption instead of naming the assumption itself.

Agent I (opening+CTA) saw a gap-creating opening and left it. Correct by its
own termination condition. The gate requires a different type of gap.

### Gate 2 — Verdict
"Mechanism vocabulary goes inside." — 4 words, isolated paragraph, white space
before and after. Clean pass.

### Gate 3 — Inside the finding
No filter language. First person throughout. Experiential. The reader is inside
the experiment, not watching someone describe it. Clean pass.

### Gate 4 — Falsification
"Strip the domain vocabulary, keep the compulsion — output collapses to baseline.
Strip the compulsion, keep the domain vocabulary — the outputs hold."

Two moves in two sentences. The gate requires:
```
Strip the domain vocabulary. Keep the compulsion.
Baseline.

Strip the compulsion. Keep the domain vocabulary.
Outputs hold.
```

The information is identical. The form is not. No agent was explicitly assigned
to produce fragment format. Agent D (filter intrusion) handles filter words and
narrative intrusion but not falsification fragment structure.

### Gate 5 — Operative variable
"write the technical substrate, not the credential" — 7 words. Falsifiable.
States exactly what to change and test. Clean pass.

### Gate 6 — CTA
"If you want to know what the fusion sentence actually looks like — and why the
grammar matters as much as the vocabulary — it's in the repository."

Names the unanswered question. Points to the repository. Does not explain what's
there. Clean pass. Agent I performed correctly.

---

## What This Means for the Research Program

The two remaining failures are structural assignment problems, not craft problems.

**Gate 1** requires an agent whose explicit job is to write a denial — name the
wrong assumption, strip it — in the first line. Agent I rewrites the first line
if it doesn't create a gap, but "gap" as defined by Agent I is broader than
"denial." An immersive scene-setting opening creates a gap. A denial creates a
different kind of gap. The termination condition needs to be more specific.

**Gate 4** requires an agent whose explicit job is to take the falsification
and reformat it into fragments — one move per line, no connecting tissue. No
agent in the current pipeline has this assignment.

**Proposed fixes for exp-1000c:**

1. Sharpen Agent I's opening instruction: the first line must name and strip a
   wrong assumption — not just create a gap. A gap is necessary but not
   sufficient. The specific form is: "The [X] is not [Y]." or equivalent denial.

2. Add falsification fragment assignment. Either:
   - Add an agent between H and I specifically for falsification format, or
   - Assign it to an existing agent (Agent D, filter intrusion, is a candidate —
     it already handles precision editing and could be extended to include
     fragment format for the falsification)

---

## Cost

Total: $0.1131 (10 runs × 1 each, sonnet-4-6, temp=1)
