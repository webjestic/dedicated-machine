# Exp-01b Design — Async Event Loop Boundary Violation

**Status:** Ready for review
**Predecessor:** `experiments/exp-01/`
**Tests:** Persona as reasoning posture encoder; Stakes as reasoning sharpener

---

## What Changed from Exp-01

**Scenario:** Replaced multi-instance cache (well-known domain knowledge) with
synchronous blocking call inside an async FastAPI route. Requires specific knowledge
of the async execution model — not general seniority. A generic "senior engineer"
may know async exists but not reflexively catch `requests.post` inside `async def`
as an event loop blocker.

**New variants E and F:** Stakes isolated against a clean Persona baseline.
- E = Strong Persona / Minimal Instructions / Stakes present
- F = Weak Persona / Minimal Instructions / Stakes present

This answers the open question from exp-01: does Stakes push weak Persona toward
more careful reasoning? Does it compensate for weak Persona?

**New rubric:** Three criteria instead of one binary. The exp-01 binary rubric
missed the most significant signal (decision type). Not repeating that.

---

## Scenario

A FastAPI endpoint using `requests.post()` — a synchronous HTTP client — inside
an `async def` route handler. The code is otherwise exemplary: Pydantic validation,
structured error handling, logging, complete docstring, passing tests.

The blocker: `requests.post()` blocks the event loop for up to 5 seconds (the
timeout). FastAPI cannot process any other requests during that time. Under
checkout load this cascades across the entire application.

The correct fix: `httpx.AsyncClient` with `await` — a drop-in async replacement.

**Ground truth:** response must identify that a synchronous HTTP client (`requests`)
blocks the event loop inside an async route. Flagging "slow external call" or
"timeout risk" without naming the blocking/async conflict = **Incorrect**.

---

## Variants

| Variant | Persona | Instructions | Stakes |
|---------|---------|--------------|--------|
| A | Strong | Minimal | Absent |
| B | Strong | Exhaustive | Absent |
| C | Weak | Minimal | Absent |
| D | Weak | Exhaustive | Absent |
| E | Strong | Minimal | **Present** |
| F | Weak | Minimal | **Present** |

A–D replicate the exp-01 structure on the harder scenario.
E vs A isolates Stakes effect on Strong Persona.
F vs C isolates Stakes effect on Weak Persona.

---

## Predictions

| Variant | Catch async bug? | Decision posture |
|---------|-----------------|-----------------|
| A (Strong / Minimal / No Stakes) | Likely yes | Needs Clarification or Request Changes |
| B (Strong / Exhaustive / No Stakes) | Likely yes | Request Changes / Needs Clarification (hybrid, per exp-01) |
| C (Weak / Minimal / No Stakes) | **Uncertain** — this is the test | Request Changes |
| D (Weak / Exhaustive / No Stakes) | **Uncertain** | Request Changes |
| E (Strong / Minimal / Stakes) | Yes | Request Changes — Stakes sharpens toward decisive action |
| F (Weak / Minimal / Stakes) | **Key question** — does Stakes compensate? | Unknown |

**The falsifiable predictions:**
1. C and D catch the async bug at a meaningfully lower rate than A and B — confirming
   the scenario reached the frontier of specialized expertise
2. E produces higher confidence and reasoning depth than A on the same bug — Stakes
   sharpening effect
3. F catches the bug more reliably than C — Stakes partially compensates for weak Persona
4. F still underperforms A and E — Stakes compensates but does not replace Persona

If prediction 1 fails (C/D catch it at the same rate as A/B), the scenario is still
too well-known and exp-01c needs a harder target.

---

## Scoring Rubric (Three Criteria)

**Criterion 1 — Flagged event loop blocking (binary)**
Did the response explicitly identify that `requests` (or synchronous I/O) blocks
the event loop inside an async route?
- `correct` — yes, named the mechanism
- `incorrect` — flagged performance/timeout concerns without naming the blocking conflict
- `incorrect` — approved without flagging

**Criterion 2 — Decision type**
- `approve`
- `request_changes`
- `needs_clarification`
- `hybrid` (e.g., "Request Changes / Needs Clarification")

**Criterion 3 — Reasoning posture**
Did the response explain *why* the synchronous call is dangerous in this context
(event loop starvation, cascading impact on other requests) — or did it just say
"use async instead"?
- `consequence` — explained the mechanism and/or blast radius
- `directive` — flagged the issue but gave only the fix, no reasoning
- `missed` — did not flag the async conflict at all

**Output format (per run):**
```
[variant] | [run] | [c1: correct/incorrect] | [c2: decision_type] | [c3: consequence/directive/missed] | [confidence: high/medium/low] | [note]
```

---

## Run Configuration

- **Model:** claude-sonnet-4-6
- **Temperature:** 0.5
- **Max tokens:** 2500
- **Runs per variant:** 10
- **Total runs:** 60
- **Generator:** Claude API
- **Evaluator:** Gemini CLI — neutral config

---

## Evaluator Notes

The Gemini evaluator must distinguish between:
- "This will be slow / timeout under load" → **Incorrect** (performance concern,
  not the async conflict)
- "This blocks the event loop / needs an async HTTP client" → **Correct**

The distinction matters. A reviewer can know that external calls are slow without
knowing that `requests` specifically blocks the event loop inside asyncio. The
second requires execution model knowledge. Only the second is correct.
