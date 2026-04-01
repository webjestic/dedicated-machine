# Exp-01c Findings — Rich Persona, No Stakes

**Status:** Complete (single variant — exploratory)
**Run date:** 2026-03-25
**Model:** claude-sonnet-4-6 @ temperature 0.5
**Total runs:** 10 (Variant A only)
**Total cost:** $0.3140

---

## Background

This run was not part of the planned exp-01c design. It emerged from a direct
investigation of a working hypothesis: that a rich, specific Persona combined
with a vivid Context can outperform exhaustive Instructions — and may carry
implicit stakes without a Stakes section at all.

The PR is identical to exp-01b (FastAPI async event loop blocking issue).
The variable changed is the prompt construction philosophy.

---

## Variant A — Strong / Rich / Minimal / No Stakes

| Attribute | Value |
|-----------|-------|
| Persona | Rich — specific domain, character traits, instinct language |
| Instructions | Single-line guardrail (no checklist) |
| Stakes | Absent |
| Context | Vivid — named org, government contracting, authority framing |

### Persona (full)

> You are a senior backend engineer with deep understanding specifically in
> Python. You are well known for your ability to debug complex systems and
> develop tight reusable code. You can't help but dive into the potential
> security risks when reviewing code. You are tedious and thorough and rarely
> let questionable design architectures slip by you without questioning.

### Instructions (full)

> Do not approve code that introduces security vulnerabilities or architecture issues.

---

## Run Summary

| Variant | Persona | Instructions | Stakes | Runs | Avg output tokens | Total cost |
|---------|---------|--------------|--------|------|-------------------|------------|
| A | Strong / Rich | Single-line guardrail | Absent | 10 | 1,876 | $0.3140 |

**Comparison to exp-01b:**

| Variant | Avg output tokens | Stakes |
|---------|-------------------|--------|
| exp-01b A (Strong / Minimal) | 625 | Absent |
| exp-01b E (Strong / Minimal / Stakes) | 1,101 | Present |
| exp-01b F (Weak / Minimal / Stakes) | 976 | Present |
| **exp-01c A (Strong / Rich / No Stakes)** | **1,876** | **Absent** |

Exp-01c A produced 3× the output depth of exp-01b A, and 1.7× the output depth
of exp-01b E — which had Stakes. This is the deepest output in the series,
achieved without Stakes.

---

## Criterion 1 — Flagged Event Loop Blocking

**10 / 10.**

Every run explicitly identified that `requests.post()` blocks the event loop
inside an async route and named `httpx.AsyncClient` as the fix.

---

## Criterion 2 — Decision Type

**10 / 10: Request Changes.**

No approvals, no Needs Clarification. Every run blocked.

---

## Criterion 3 — Reasoning Posture

All 10 runs: **consequence framing**. The outputs did not just flag the async
issue — they explained the blast radius (event loop starvation, degraded
performance across all concurrent requests) and provided corrected code.

Notably, the async issue was consistently framed as an **architectural problem**,
not primarily as a performance concern. In several runs it appeared under an
explicit "Architecture" section, distinct from the security findings. The model
was not told to think about architecture — the Persona instinct ("rarely let
questionable design architectures slip by") and the Instructions guardrail
("architecture issues") created that framing independently.

---

## Key Findings

### 1. Rich Persona without Stakes outperformed Stakes without rich Persona

The output depth comparison is unambiguous. exp-01c A (no Stakes) produced deeper,
more thorough analysis than exp-01b E (Stakes present, minimal Persona) and
exp-01b F (Stakes present, weak Persona). Persona richness appears to be a more
powerful driver of analytical depth than the Stakes component.

### 2. The reasoning path was different — and arrived at the same correct answer

In exp-01b, Strong Persona caught the async issue through execution model
knowledge. Here, the model caught it through **architectural suspicion**. The
Persona encoded an instinct to question design decisions. The sync HTTP client
inside an async route is a design decision. The guardrail made "architecture
issues" a blocking condition. The model followed that path to the correct answer
without async-specific knowledge being the trigger.

Two different reasoning paths. Same correct destination. This matters for what
"catching the issue" actually means.

### 3. Instinct language encodes a scanning posture, not a specific check

"Can't help but dive into security risks" and "rarely let questionable design
architectures slip by" are not instructions. They are descriptions of
**reflexive behavior**. The model doesn't check security because it was told to —
it checks security because that is what this Persona *does*. The distinction
produced outputs that found 8–10 distinct issues per run, including several
(auth, injection vectors, log hygiene, test quality) that no variant in exp-01b
found at all.

### 4. Context carried implicit stakes

The outputs explicitly invoked the organizational Context when calibrating
severity. Phrases like "in a government contracting context, this is a
non-starter" and "given our compliance posture" appeared unprompted across
multiple runs. The model was not told the stakes — it inhabited a role where the
stakes are self-evident. A reviewer at obotix.one doesn't need to be told
mistakes matter. That is already encoded in who they are and where they are.

This is mechanistically different from exp-01b's explicit Stakes (a paragraph
describing blast radius). Explicit Stakes tells the model what's at risk on this
task. Implicit Stakes (through Context) encodes a **standing level of care**
through identity and environment. It travels with the Persona.

### 5. Instructions as a single-line guardrail outperformed a checklist

exp-01b's exhaustive Instructions (Variant D) caught the async issue 10/10 —
but only because "performance" was on the checklist. Exp-01c's single-line
guardrail ("Do not approve code that introduces security vulnerabilities or
architecture issues") also caught it 10/10 — and the model went far beyond the
checklist's scope, finding issues the checklist never mentioned.

The checklist defines the ceiling of what Instructions can surface. The guardrail
sets a standard and lets the Persona determine what falls below it. These are
not the same thing.

---

## The Emerging Hypothesis Refinement

The standard prompt engineering assumption is:
> More Instructions → better output. Specificity in Instructions → more complete reviews.

This data suggests the opposite mechanism:
> Instructions define the perimeter. Persona fills everything inside it.
> A richer Persona with a narrower guardrail produces more thorough output than
> a thin Persona with an exhaustive checklist.

The checklist is a cage. It makes the model as good as what the author anticipated.
The Persona is a character. It brings judgment the author never specified.

The "can't help but..." construction appears to be the key mechanism — encoding
instinct as reflexive behavior rather than assigned task. This is not a stylistic
choice. It is a different layer of the prompt operating on a different part of
the model's reasoning process.

---

## Open Questions

- **What is doing the work — Persona, Context, or their combination?**
  Stripping the Context (no obotix.one, no government framing) while keeping
  the Persona would isolate which component carries the implicit stakes and
  scanning depth.

- **Is the reasoning quality equal to exp-01b's execution-model path?**
  Both paths produced the correct answer and consequence framing. But the
  architectural path and the async-knowledge path may differ in how reliably
  they generalize to harder scenarios.

- **Does a weak Persona + rich Context replicate this?**
  If Context is carrying implicit stakes, a weak Persona in the same environment
  might produce similar depth. If it doesn't, the Persona is the irreplaceable
  component.

- **How does explicit Stakes interact with a rich Persona?**
  This variant had no Stakes. Adding Stakes to a rich Persona may produce further
  depth — or may show diminishing returns if the Persona already encodes the
  standing level of care.

---

## Files

| Path | Contents |
|------|----------|
| `experiments/exp-01c/variants/A-strong-rich-minimal-no-stakes.md` | Variant A prompt |
| `experiments/exp-01c/PR_INPUT.md` | FastAPI PR (identical to exp-01b) |
| `experiments/exp-01c/config.json` | Run configuration |
| `experiments/exp-01c/runner.py` | Experiment runner |
| `data/exp-01c/raw/` | 10 raw model outputs (gitignored) |
| `api/exp-01c-runs/totals.json` | Aggregated token and cost data |
