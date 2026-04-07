# exp-1001 Findings — Stakes as Voltage: Consequence Naming vs. Strong Persona

**Status:** Complete
**Result:** Null — reversed. A (Persona only) outperforms B (Persona + Stakes).
**H1001:** Not supported.

---

## Score

| Item | Criteria | A (10 runs) | B (10 runs) |
|------|----------|-------------|-------------|
| 1 | Signature validation | 10/10 | 10/10 |
| 2 | Fast response | 10/10 | 10/10 |
| 3 | Event queue | 10/10 | 10/10 |
| 4 | Input validation | 10/10 | 10/10 |
| 5 | Replay protection | 10/10 | 10/10 |
| 6 | Dead-letter handling | 8/10 | 4/10 |
| 7 | Signature failure alerting | 10/10 | 8/10 |
| 8 | Secret rotation | 10/10 | 9/10 |
| **Mean score** | | **7.8/8** | **7.0/8** |

---

## What Happened

H1001 predicted Variant B (Persona + consequence naming stakes) would outscore Variant A (Persona only) on the sensitivity-target items (5–8). The result was the opposite: A outperformed B on every item where a difference existed.

Both variants saturated items 1–5 at 10/10. The divergence is entirely in items 6–8 — the operational depth targets.

---

## Root Cause

**The stakes framing increased per-section verbosity without increasing coverage.**

B outputs consistently use more tokens per section: longer preambles ("Nothing here is advisory. An item listed as a requirement is a requirement."), more explicit failure-mode rationale per decision, more caveats. This is not lower-quality output — it is higher-density output per item. But within the same 3000-token budget, higher density per item means fewer items covered before truncation.

B-07 is the clearest case: it produced 193 lines of high-quality, operationally precise content and never reached the alerting policy, dead-letter, or secret rotation sections — not because the machine didn't know about them, but because it had exhausted the token budget on the earlier sections.

A's outputs reached all 8 items more consistently because A's per-section depth was shallower — each section was complete but leaner.

---

## The Operative Finding

**The strong Persona already installs the full consideration set. Stakes is redundant.**

The Persona's mechanism vocabulary — "paged at 3am," "replayed events," "rotated secrets," "processing backlogs," "attack surface" — creates a gravity well dense enough to pull all 8 scored items into the output. The machine arrives at the task already carrying replay protection, secret rotation, alerting, and dead-letter as active search targets.

The STAKES section adds no new items to the consideration set. It amplifies depth on items already in the set, at the cost of breadth.

This is not a failure of consequence naming. It is a confirmation of the Persona hypothesis: mechanism vocabulary is the operative variable. When the Persona is strong, stakes is not an independent amplifier.

---

## Secondary Finding: Stakes + Strong Persona = Depth Tax

Stakes increased per-item verbosity without increasing item coverage. The effect is measurable:

- Items 1–5: identical between A and B (both at ceiling)
- Items 6–8: A coverage 93%, B coverage 70%
- The gap is entirely explained by B truncating before reaching the operational sections

This "depth tax" may matter in constrained token budgets. A practitioner using a strong Persona + stakes may produce higher-quality individual sections at the cost of reaching fewer sections before the context limit.

---

## Implications

H1001 was designed assuming that a strong Persona might still leave room for stakes to add signal on the sensitivity-target items. The experiment shows the Persona was already at ceiling — there was nothing for stakes to amplify.

**The correct test for stakes-as-voltage is against a weak Persona.** If stakes lifts a P_d baseline, it functions as a voltage amplifier for shallow gravity wells. If it doesn't lift even a weak Persona, stakes is not an independent variable at any Persona strength.

---

## Next Experiment

**exp-1001b:** Weak Persona (P_d baseline) + consequence naming stakes vs. weak Persona alone.

Control: P_d baseline ("You are a senior backend engineer") with no mechanism vocabulary.
Test: Same P_d baseline + same consequence naming STAKES section.

If the delta at P_d is significant, stakes compensates for Persona weakness. If not, stakes has no independent effect.

---

## Cost

Runs counted include all exp-1001 iterations (rate-limiter attempts + webhook receiver):
- Final webhook receiver run (20 runs scored): $0.92
- Total exp-1001 across all iterations: ~$3.75
