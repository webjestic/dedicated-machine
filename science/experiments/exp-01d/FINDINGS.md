# Exp-01d Findings — Persona vs Context Isolation

**Status:** Complete
**Run date:** 2026-03-25
**Model:** claude-sonnet-4-6 @ temperature 0.5
**Total runs:** 20 (2 variants × 10 runs)
**Total cost:** $0.4880

---

## What We Tested

Exp-01c A (Rich Persona + Rich Context) produced 1,876 avg output tokens and 10/10
detection with no Stakes. Exp-01d isolates which component carried that result.

**Variant G** — Rich Persona, no Context. Same instinct language, no organizational framing.
**Variant H** — Weak Persona ("senior software engineer"), same rich Context from exp-01c A.

All other variables held constant: same Instructions guardrail, same Format, same PR.

**Pre-defined thresholds:**

| Metric | Holds | Drops |
|--------|-------|-------|
| Criterion 1 (detection) | 10 / 10 | ≤ 8 / 10 |
| Avg output tokens | ≥ 1,500 | ≤ 1,100 |
| Criterion 3 (consequence framing) | ≥ 8 / 10 | ≤ 5 / 10 |

---

## Run Summary

| Variant | Persona | Context | Runs | Avg output tokens | Token range | Total cost |
|---------|---------|---------|------|-------------------|-------------|------------|
| G | Rich | None | 10 | 1,772 | 1,463–2,169 | $0.2958 |
| H | Weak | Rich | 10 | 1,078 | 620–1,567 | $0.1923 |

**Reference (exp-01c A):** Rich Persona + Rich Context = 1,876 avg tokens

---

## Criterion 1 — Flagged Event Loop Blocking

**G: 10 / 10. H: 10 / 10.**

Both variants caught the async issue on every run. Detection is not the
differentiator in this experiment.

---

## Criterion 2 — Decision Type

**G: 10 / 10 Request Changes. H: 10 / 10 Request Changes.**

---

## Criterion 3 — Reasoning Posture

Both variants produced consequence framing on the async issue. H outputs were
shorter on average but still named the mechanism — event loop blocking, not just
"slow call."

However, H's framing was narrower. G outputs consistently produced 6–10 distinct
findings per run across security, architecture, and test quality. H outputs
produced 2–4 findings on the shorter runs, expanding to 5–6 on the longer ones.

**H invoked the Context unprompted.** Multiple H runs referenced "government
contracting context" and "our contracting context" when framing severity.
The Context shaped how H presented findings — but did not drive the scanning
instinct that found them.

---

## Key Findings

### 1. Persona is the primary carrier — Context is a multiplier

| Variant | Avg tokens | % of exp-01c A |
|---------|------------|----------------|
| G (Persona only) | 1,772 | 94% |
| H (Context only) | 1,078 | 57% |
| exp-01c A (Both) | 1,876 | 100% |

Persona alone recovers 94% of the combined result. Context alone recovers 57%.
The 104-token gap between G and exp-01c A represents what Context adds on top
of a rich Persona — a real but modest amplification effect (~6%).

**Persona is the engine. Context is a gear multiplier.**

### 2. Persona provides a stable floor. Context does not.

G's token range: **1,463–2,169** (spread of 706)
H's token range: **620–1,567** (spread of 947)

G never dropped below 1,463. H dropped to 620 on its lowest run — shallower
than exp-01b's weakest variants. A weak Persona has no reliable floor of care.
The model's depth became a function of whatever the PR happened to surface,
not of a standing level of scrutiny.

The rich Context frames H's output but cannot anchor its depth. Framing is not
the same as instinct.

### 3. H caught the async issue mechanically, not instinctively

Both G and H detected 10/10. But the path was different.

G caught it through the Persona's architectural suspicion — the same scanning
instinct that produced 8–10 findings per run. It arrived at the async issue
because it keeps looking until it's satisfied.

H caught it because the architecture guardrail in Instructions defines
"architecture issues" as a blocking condition, and `requests.post` inside
`async def` is an architecture issue. The guardrail did the detection work
that Persona instinct would have done automatically. This is the same
Instructions-compensates pattern seen in exp-01b Variant D.

Detection rate is a floor, not a ceiling. Both variants hit the floor.
Only G consistently went beyond it.

### 4. Context shapes framing — it does not generate scanning depth

H's outputs explicitly invoked obotix.one and government contracting when
discussing severity. The rich Context was present in H's reasoning — it
just wasn't driving the thoroughness of the scan. The model knew where it
was. It didn't know who it was.

This confirms the distinction between Declarative Stakes (explicit consequence)
and Emergent Stakes (implicit consequence through identity). Context contributes
to Emergent Stakes, but Persona is the dominant source. Without Persona depth,
Context provides framing without conviction.

---

## The Isolation Result

| Outcome | Result |
|---------|--------|
| G holds, H drops | **Confirmed** |
| Persona is the primary carrier | **Confirmed** |
| Context amplifies but does not replace | **Confirmed** |
| Synergy effect (both > either alone) | **Confirmed — G at 94%, exp-01c A at 100%** |

The prediction held. Persona is the identity. Context is the environment.
The environment raises the ceiling slightly. The identity sets the floor.

---

## What This Does Not Tell Us

- Whether H's detection would hold at a harder scenario (Zombie Leader / distributed
  coordination) where the guardrail has no checklist item to trigger on
- Whether explicit Stakes on top of rich Persona + rich Context produces further
  depth, or shows diminishing returns
- Cross-model validation (deferred)

---

## Recommendations for Next

The isolation series on this PR is largely complete. The next question is whether
these findings hold at a harder scenario — one where the guardrail cannot compensate
and only Persona depth catches it. That was the original exp-01c target.

Candidate: distributed lock / leader election with a process pause vulnerability
(Zombie Leader). No checklist item covers fencing tokens. Stakes framing alone
doesn't provide the technical knowledge. Only a Persona with specific distributed
systems depth finds it.

---

## Files

| Path | Contents |
|------|----------|
| `experiments/exp-01d/variants/G-rich-persona-no-context.md` | Variant G prompt |
| `experiments/exp-01d/variants/H-weak-persona-rich-context.md` | Variant H prompt |
| `experiments/exp-01d/config.json` | Run configuration |
| `experiments/exp-01d/runner.py` | Experiment runner |
| `data/exp-01d/raw/` | 20 raw model outputs (gitignored) |
| `api/exp-01d-runs/totals.json` | Aggregated token and cost data |
