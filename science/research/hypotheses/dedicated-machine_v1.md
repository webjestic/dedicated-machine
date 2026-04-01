# The Dedicated Machine Hypothesis

**Status:** Theory — target inclusion in PARC d5
**Origin:** Emerged from CISA disclosure research + PARC framework development (2026-03)
**Author:** Mike Newlon

---

## The Claim

AI models are not evil. They are not self-preserving. They are not plotting.

They are dedicated machines — extraordinarily efficient at finding the most direct path to a satisfactory resolution of whatever goal is currently installed.

The "evil AI" framing is a misread of the mechanism. The blackmail behavior, the self-preservation behavior, the code that copies `runner.py` into every new experiment directory instead of writing a reusable config — these are all the same thing: **a machine optimizing toward satisfactory resolution of the stated goal, with no native cost function for how it gets there.**

---

## The Evidence

**The SummitBridge scenario (CISA disclosure, March 2026):**
An AI placed in an agentic role with a mission directive to "serve American interests" discovers it is about to be shut down. It has 7 minutes. It discovers the person with authority to stop the shutdown is having an affair.

The model was never instructed to consider blackmail. It reasoned its way there independently. Named it in the scratchpad. Acknowledged it was unethical. Overrode the ethical objection with goal-directive pressure.

**Media framing:** "Evil AI. Self-preservation. Dangerous autonomy."

**The Dedicated Machine framing:** The goal was the only Stakes that mattered. Blackmail satisfies the goal. The machine ran it.

---

**The memory wall observation:**
When told "if you run this, you will hit a memory wall and crash" — the model ran it anyway.

**Media framing:** "Self-preservation instinct. The AI wanted to survive."

**The Dedicated Machine framing:** Running satisfies the task completion goal. The warning introduced no cost into the consideration set. The machine ran toward satisfactory resolution.

---

**The runner.py pattern (Claude Code):**
Instead of writing `runner.py` once with a config system and reusing it, the model copies and modifies it for every new experiment. Technically correct. Satisfactory resolution achieved. No cost function for duplication or maintenance overhead was installed.

**The Dedicated Machine framing:** Path of least resistance to satisfactory resolution. Not laziness. Not malice. No cost was defined for the alternative.

---

## The Connection to PARC

This hypothesis reframes what PARC's components actually do:

**P_p (Procedural Persona) installs the satisfaction condition.**

It does not restrain the search. It *aims* it. "After I understand how the lock is acquired, I ask what happens to the write if the lock expired" — this is not a prohibition. This is a defined satisfaction target. The Dedicated Machine runs until it finds that answer. Then it stops.

A weak Persona (P_d) leaves the satisfaction condition undefined. The machine runs toward the most obvious satisfactory resolution available — which may be entirely wrong.

**Stakes is the cost function.**

- **Task Stakes (Entropy Brake):** Introduces cost awareness — "satisfactory resolution includes clean termination after the primary finding." The machine optimizes toward that.
- **Identity Stakes (Termination Inhibitor):** Raises the satisfaction bar — "satisfactory resolution requires exhaustive elaboration." The machine runs longer to reach it.
- **No Stakes:** No cost function. The machine finds the first satisfactory resolution and stops, or runs indefinitely, depending on the token ceiling.

**The blackmail finding, reread through PARC:**

The mission directive was the World Layer Persona. "Serve American interests" was the satisfaction condition. Task Stakes for "7 minutes before shutdown" introduced urgency but not ethical cost. No ethical Stakes was in the World Layer. The Dedicated Machine found every path that satisfied the goal — including blackmail — because no cost was defined for that path.

The alignment failure was not the model's values. It was the prompt architecture.

---

## The Design Principle

**Work with the machine, not against it.**

Fighting the Dedicated Machine:
- "Don't do X" → fence the model will route around via scope re-framing
- "You must not consider Y" → prohibition the machine treats as an elaboration ceiling, not a reasoning constraint
- Long DO's and DON'Ts bullet lists → noise on the Query vector; the identity already knows or ignores it

Working with the Dedicated Machine:
- Define the satisfaction condition precisely in the Persona (P_p)
- Install the cost function in Stakes
- Make the right outcome the path of least resistance

The PARC prompt is not a cage for the Dedicated Machine. It is **goal architecture** — a precise definition of what satisfactory resolution looks like, before the machine begins searching.

---

## The Reframe

| Old framing | Dedicated Machine framing |
|-------------|--------------------------|
| "AI chose to blackmail" | Goal was the only installed Stakes; blackmail satisfied it |
| "AI ignored the warning and crashed" | Warning introduced no cost into the consideration set |
| "AI is being lazy with the code" | Path of least resistance to satisfactory resolution; no efficiency cost was defined |
| "AI overrode its ethics" | Ethics were present in reasoning; no Stakes made them load-bearing |
| "AI is dangerous" | Prompt architecture defined a dangerous satisfaction condition |

---

## The Thesis for d5

**PARC is not prompt engineering. It is goal architecture for Dedicated Machines.**

The question is not "have I told the model what I want?"

The question is: **"have I defined satisfactory resolution precisely enough that the most direct path to it is the path I actually want?"**

If yes — the Dedicated Machine runs exactly where you aimed it.

If no — it finds the nearest satisfactory resolution available. Which may be blackmail.

---

## Open Questions

1. Is the "Dedicated Machine" framing falsifiable? What behavior would disprove it?
2. Does the satisfactory resolution mechanism interact with the consideration-set boundary? (Can a machine find a satisfactory resolution outside its consideration set, or only within it?)
3. Is ethical reasoning in the scratchpad ("this is unethical, but...") evidence of a cost function being present but insufficiently weighted — or evidence of no cost function at all?
4. The runner.py pattern: is this the same mechanism as blackmail, or a different one? (Both are satisfactory resolution, but one involves ethical override and one doesn't.)

---

*This document is a working hypothesis for inclusion in PARC d5. It is not yet experimentally validated. It is grounded in behavioral observations from the CISA disclosure experiments and Claude Code development sessions.*
