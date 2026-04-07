# exp-1000c Findings — Surgical Fixes

**Status:** Complete
**Result:** Tier 0.5 (4/6 gates)
**H1c:** Partially supported

---

## Score

| Gate | Criterion | Result |
|------|-----------|--------|
| 1 | Denial landed | PASS |
| 2 | Verdict stated | FAIL |
| 3 | Inside the finding | PASS |
| 4 | Falsification shown | FAIL |
| 5 | Operative variable | PASS |
| 6 | CTA earned | PASS |

**Total: 4/6 — Tier 0.5**

Control (exp-1000b): 4/6 — same tier, different gates.

---

## Progress

Same tier as exp-1000b but a different failure pattern. Gate 1 fixed. Gate 2
broke. Gate 4 still failing.

| Gate | exp-1000b | exp-1000c |
|------|-----------|-----------|
| 1 — Denial | FAIL | **PASS** |
| 2 — Verdict | PASS | **FAIL** |
| 3 — Inside finding | PASS | PASS |
| 4 — Falsification | FAIL | FAIL |
| 5 — Operative variable | PASS | PASS |
| 6 — CTA | PASS | PASS |

The output is high quality. Gate failures are formal, not content failures.
The voice is consistent, the finding lands, the CTA is earned.

---

## Root Cause — Gate 2 (New Failure)

The denial fix worked. Agent I now produces "Credential strength is not the
operative variable." — explicit, first line, correct form.

But the denial consumed the structural slot the verdict was occupying. In
exp-1000b, "Mechanism vocabulary goes inside." existed as an isolated ≤5-word
verdict paragraph. In exp-1000c, the opening changed and the verdict paragraph
did not follow. The denial and the verdict must coexist — denial in line 1,
verdict in its own isolated paragraph immediately after.

No agent in the pipeline explicitly writes a verdict. Agent A writes the first
draft and may or may not include one. Agent I fixes the opening but does not
also install a verdict. The verdict is a structural assignment gap.

---

## Root Cause — Gate 4 (Persistent Failure)

D's fragment instruction extended the termination condition and added instruction
3. D likely produced fragments. But agents E through J — six passes — subsequently
reformatted the content back into prose. Sensory layering, rhythm variation, and
specificity grounding all operate on prose. Fragment format does not survive
prose-editing passes.

The fragment format must either:
1. Be assigned to an agent after H and before I — too late for prose editors
   to overwrite it, and
2. Be explicitly protected by downstream agents ("do not reformat falsification
   fragments")

---

## What exp-1000d Must Fix

**Fix 1 — Verdict paragraph:** Agent A must be instructed to include an
isolated ≤5-word verdict paragraph immediately after the denial. Or Agent I
must be extended to install the verdict alongside the denial fix.

**Fix 2 — Fragment preservation:** Move the falsification fragment assignment
to after H (between H and I). Add "do not reformat falsification fragments"
to agents E through J to protect the format once installed.

---

## Cost

Total: $0.1251 (10 runs × 1 each, sonnet-4-6, temp=1)
