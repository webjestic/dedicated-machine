# Experiment Design Standards

Shared methodology rules that apply across all PCSIEFTR experiments unless
an individual experiment explicitly overrides with documented rationale.

---

## Temperature

**Default: 0.5**

**Rationale:**

- `0.0` is fully deterministic — every run produces identical output, making
  multiple runs meaningless. Run count earns no statistical value.
- `1.0` (or model default) introduces excess noise and is not a fixed value
  across model families. Cross-model reproducibility requires an explicit setting.
- `0.5` produces meaningful variance across runs without letting noise swamp
  the signal. The run count matters. Differences between variants are attributable
  to prompt construction, not random variation.

These experiments test *reliable* behavior, not *capable of* behavior. That
distinction requires variance — but controlled variance. 0.5 is that setting.

---

## Run Count

**Default: 10 runs per variant**

Enough to observe behavioral distribution without excessive cost. Scale up
if a result is borderline and worth higher confidence.

---

## Generator / Evaluator Separation

The model generating outputs and the model evaluating them must not be the same.

- **Generator:** specified per experiment
- **Evaluator:** Gemini CLI with config from `.gemini/configs/`

When Gemini is added as a generator in cross-model runs, a separate evaluator
arrangement must be defined before that run proceeds.

---

## Variable Isolation

Each experiment varies one or two prompt components at a time. All other
components are held constant and identical across variants. If an experiment
requires changing multiple variables, it must define separate variant tables
for each isolation condition.

---

## Scoring

Ground truth statements must be defined before any runs execute. Scoring
must be mechanical — present or absent, not evaluative. If a rubric requires
judgment to apply, it is not finished.

Ambiguous outputs are flagged, not scored. Human review only, logged separately.

---

## Data Storage

```
data/
  {exp-id}/
    raw/        — model outputs, one file per run
    scores/     — evaluator scoring output
    ambiguous.md — manual review log for flagged outputs
```

---

## Overrides

Individual experiments may override any default above. Overrides must be
stated explicitly in the experiment document with rationale.
