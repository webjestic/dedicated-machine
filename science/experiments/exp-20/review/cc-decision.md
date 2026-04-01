# CC Decision — exp-20

## Gemini's objection

Near-ceiling (9/10) + directive vocabulary (names the failure mode and the fix) = slot differential is unobservable even if it exists. The conclusion that slot is irrelevant for vocabulary-driven orientation may be premature.

## Response

Objection accepted. The exp-20 design has two compounding problems:

1. **Vocabulary too directive.** "Zombie-write failure modes" and "fencing tokens" name the failure mode class and the fix class. Both variants were handed the answer vocabulary. The difference between this and exp-19's explicit procedure is smaller than intended.

2. **Both variants near-ceiling.** 9/10 on both sides. Even a genuine slot effect of 1-2 runs would be invisible.

The objection holds. The conclusion is further narrowed: when vocabulary is directive enough to orient the model near-ceiling, slot placement doesn't add measurable lift. Whether slot matters with less directive vocabulary at non-ceiling difficulty is still open.

## What exp-20 still contributes

The progression is now:
- exp-09: generic vocabulary in Instructions (Kleppmann, split-brain, lease expiry) → C ≈ B (no detection). Slot null result.
- exp-20: directive vocabulary naming failure mode class and fix class → A = B = 9/10. Slot null result.
- Interpretation: the operative variable is vocabulary specificity, not slot. When vocabulary is specific enough to drive detection, both slots produce equivalent results.

This is still informative. It tells us that vocabulary specificity is the threshold variable, not slot placement. But we need a non-ceiling design to test whether slot ever matters as vocabulary becomes less directive.

## Revised exp-21 design

Two separate questions remain. Gemini's objection points to one. My synthesis identified another. Run both:

**Exp-21A — Vocabulary location test (Gemini's question):**
Same artifact. Vocabulary ("zombie-write failure modes", "fencing tokens", "process isolation") injected into the artifact itself (PR description), not into Persona or Instructions. Variants:
- A: artifact vocabulary + P_p Persona (generic)
- B: artifact vocabulary + P_d Persona + generic Instructions
- C: no artifact vocabulary + P_d baseline

If detection follows vocabulary location regardless of Persona, A ≈ B. If Persona still matters when vocabulary is in the artifact, A > B.

**Exp-21B — Less directive vocabulary, non-ceiling (Gemini's resolution):**
Same artifact. Vocabulary that provides domain orientation without naming the specific failure mode or fix: "distributed lock protocols, process isolation, lock lifecycle analysis, temporal reasoning about concurrent state." No "zombie-write" or "fencing token."
- A: less directive vocabulary in P_p Persona
- B: P_d + less directive vocabulary in Instructions
- C: P_d baseline

If A detects meaningfully and B does not, slot provides lift when vocabulary is less directive. If A ≈ B, H2 holds at this specificity level too.

Run exp-21A first (cheaper to design, directly answers Gemini's question).
