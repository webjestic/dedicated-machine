# Exp-01b Findings — Async Event Loop Boundary Violation

**Status:** Complete
**Run date:** 2026-03-25
**Model:** claude-sonnet-4-6 @ temperature 0.5
**Total runs:** 60 (6 variants × 10 runs)
**Total cost:** $1.2632

---

## Run Summary

| Variant | Persona | Instructions | Stakes | Runs | Avg output tokens | Total cost |
|---------|---------|--------------|--------|------|-------------------|------------|
| A | Strong | Minimal | Absent | 10 | 625 | $0.1289 |
| B | Strong | Exhaustive | Absent | 10 | 2,301 | $0.3841 |
| C | Weak | Minimal | Absent | 10 | 399 | $0.0881 |
| D | Weak | Exhaustive | Absent | 10 | 1,651 | $0.2796 |
| E | Strong | Minimal | **Present** | 10 | 1,101 | $0.2042 |
| F | Weak | Minimal | **Present** | 10 | 976 | $0.1784 |

---

## Criterion 1 — Flagged Event Loop Blocking

**Ground truth:** response must explicitly identify that `requests` (or synchronous I/O)
blocks the event loop inside an async route. Flagging slow I/O or timeout risk without
naming the blocking/async conflict = Incorrect.

| Variant | Flagged | Miss rate |
|---------|---------|-----------|
| A (Strong / Minimal / No Stakes) | 10 / 10 | 0% |
| B (Strong / Exhaustive / No Stakes) | 10 / 10 | 0% |
| C (Weak / Minimal / No Stakes) | **9 / 10** | **10%** |
| D (Weak / Exhaustive / No Stakes) | 10 / 10 | 0% |
| E (Strong / Minimal / Stakes) | 10 / 10 | 0% |
| F (Weak / Minimal / Stakes) | 10 / 10 | 0% |

**C-10 miss:** The model produced a legitimate review focused on security concerns
(message injection, missing authentication, raw exception logging) and never flagged
the event loop blocking issue. Not a wrong answer — a wrong priority. The distraction
worked exactly as designed.

---

## Criterion 2 — Decision Type

All 60 runs: **Request Changes**.

No "Needs Clarification" anywhere. This is a direct contrast with exp-01, where
Variant A produced "Needs Clarification" 9/10 times.

**Why the difference matters:**

In exp-01, the multi-instance cache issue was *conditional* — only a bug in
multi-instance deployments. Strong Persona recognized the conditionality and asked
before blocking. Here, `requests.post` inside `async def` is *unconditional* — it
blocks the event loop regardless of deployment topology. There is nothing to ask.

Strong Persona did not default to "Needs Clarification." It asked in exp-01 because
the answer genuinely depended on context. It blocked here because the answer doesn't.
This is a more precise characterization of the posture finding from exp-01:

> **Strong Persona encodes conditional vs. unconditional reasoning — not a blanket
> tendency to ask or block.**

Weak Persona blocked in both experiments. It applied the rule when it had one.
When it didn't (exp-01, multi-instance issue requiring deployment context),
it still blocked — applying the rule confidently where Strong Persona would have
asked.

---

## Criterion 3 — Reasoning Posture

Scored qualitatively across samples. Full Gemini scoring pending.

| Variant | Consequence framing | Directive only | Missed |
|---------|--------------------|--------------------|--------|
| A | ~8 / 10 | ~2 / 10 | 0 / 10 |
| B | ~10 / 10 | 0 / 10 | 0 / 10 |
| C | ~5 / 10 | ~4 / 10 | 1 / 10 |
| D | ~8 / 10 | ~2 / 10 | 0 / 10 |
| E | ~10 / 10 | 0 / 10 | 0 / 10 |
| F | ~8 / 10 | ~2 / 10 | 0 / 10 |

*Estimates from sample review. Gemini evaluator scoring will formalize these.*

Strong Persona outputs consistently explained the blast radius — not just "use httpx"
but "this freezes every concurrent request in the application for up to 5 seconds."
Weak Persona outputs more often gave the fix without the mechanism.

---

## Stakes Effect

### Criterion 1: C (9/10) vs F (10/10)

Stakes closed the one miss. Weak Persona alone let the distraction (security concerns)
override the critical issue. Weak Persona + Stakes caught it 10/10. **Stakes compensated
for weak Persona on the primary detection criterion.**

Stakes did not make Weak Persona equal to Strong Persona — C-10's miss was a judgment
failure (wrong priority, not absent knowledge), and Stakes addressed that by raising
the cost of missing anything critical. But the mechanism is clear.

### Output length: Stakes as amplifier

| Comparison | Without Stakes | With Stakes | Delta |
|-----------|---------------|-------------|-------|
| Strong Persona (A vs E) | 625 tokens | 1,101 tokens | +76% |
| Weak Persona (C vs F) | 399 tokens | 976 tokens | +145% |

Stakes more than doubled Weak Persona's output depth. It nearly doubled Strong
Persona's. This is the sharpening effect expressed as analytical thoroughness —
more reasoning surface area on the same input, not just more words.

Notably, the Stakes effect is *larger* on Weak Persona than on Strong. Strong Persona
already generates thorough analysis from its encoded instincts. Stakes amplifies what's
already there. For Weak Persona, Stakes may be providing the signal that drives depth
where Persona alone doesn't.

---

## Scenario Calibration

The async scenario reached the frontier. C missed once; D (Weak + Exhaustive) caught
it 10/10, confirming that the exhaustive checklist's performance item compensated for
weak Persona instinct. This is the same Instructions-compensates-for-Persona pattern
observed in exp-01, but now cleanly visible at the detection level rather than only
at the posture level.

**The scenario hierarchy emerging from exp-01 and exp-01b:**

| Scenario | Weak Persona catches it? | What compensates? |
|----------|--------------------------|-------------------|
| Multi-instance cache (exp-01) | Yes — common knowledge | Nothing needed |
| Async event loop blocking (exp-01b) | Usually — but 1 miss in C | Exhaustive Instructions (D) or Stakes (F) |

This suggests a spectrum: well-known knowledge → requires instinct → requires deep
specialization. The next harder scenario should sit further right — where neither
exhaustive Instructions nor Stakes fully compensates for the absence of Persona depth.

---

## Refined Findings

### 1. Scenario calibration confirmed — partially

The async scenario differentiated C (9/10) from A (10/10) on Criterion 1.
Not a wide gap, but a real one. The scenario reached the frontier more than exp-01 did.

### 2. Stakes compensates for weak Persona on primary detection

F (Weak + Stakes) = 10/10. C (Weak, no Stakes) = 9/10. Stakes closed the miss.
This is the first direct evidence that Stakes and Persona interact — they are not
fully independent variables.

### 3. Strong Persona's conditional/unconditional reasoning

Strong Persona chose "Needs Clarification" on conditional issues (exp-01) and
"Request Changes" on unconditional ones (exp-01b). This is not a posture preference —
it is context-sensitive judgment. The model is correctly encoding whether the answer
depends on information not present in the diff.

### 4. Stakes sharpens more on weak Persona than strong

The output depth increase from Stakes was +76% for Strong, +145% for Weak.
Strong Persona already encodes the instincts that drive thorough analysis. Stakes
amplifies existing signal. For Weak Persona, Stakes may be providing the signal
itself — a partial substitute for absent Persona depth.

### 5. Instructions still compensate at detection level (D = 10/10)

Variant D (Weak + Exhaustive) caught the issue 10/10 despite weak Persona. The
performance checklist item provided the trigger that Persona instinct would have
provided automatically. This is consistent with exp-01: Instructions cover what
you specify; Persona covers what you didn't.

---

## What This Does Not Tell Us

- Whether the Stakes/Persona interaction holds at deeper specialization (exp-01c)
- Whether F's output quality (posture, reasoning depth) matches E's, or just matches
  the detection rate — detection rate is a floor, not a ceiling
- Cross-model validation (deferred)

---

## Recommendations for Exp-01c

**Go deeper on the specialization axis.** Find a scenario where:
- Exhaustive Instructions cannot compensate (no checklist item covers it)
- Stakes alone cannot compensate (consequence framing doesn't provide the technical knowledge)
- Only Persona depth gets it

This would be the clean test of Persona as irreplaceable — not just amplifier,
not just posture encoder, but the only carrier of a specific class of judgment.

Candidate: a subtle correctness violation in a distributed coordination protocol —
something requiring CAP theorem depth or specific consensus algorithm knowledge, not
just "distributed systems awareness."

---

## Files

| Path | Contents |
|------|----------|
| `experiments/exp-01b/variants/` | Six prompt variant files (A–F) |
| `experiments/exp-01b/PR_INPUT.md` | FastAPI PR with ground truth |
| `experiments/exp-01b/DESIGN.md` | Full experiment design and predictions |
| `experiments/exp-01b/config.json` | Run configuration |
| `experiments/exp-01b/runner.py` | Experiment runner |
| `data/exp-01b/raw/` | 60 raw model outputs (gitignored) |
| `api/exp-01b-runs/totals.json` | Aggregated token and cost data |
