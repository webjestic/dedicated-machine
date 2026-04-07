# Dedicated Machine

The model isn't failing. It's finished.

Shallow output isn't a knowledge problem. It's a termination problem. The machine terminates at the nearest satisfying path because nothing in its definition of done required it to go further. The gap between what was delivered and what was needed is invisible to it — not because it can't see it, but because there's no cost function that makes it visible.

Thirty-three controlled experiment series on Claude Sonnet 4.6 and Gemini 2.5 Pro. The primary finding: **Persona is the primary determinant of reasoning quality — not because it adds knowledge, but because it defines when the machine stops.**

---

## Articles

Practitioner-facing case studies. Real problems, what the research found, why it matters.

- [The Zombie Leader](articles/zombie-leader.md) — the code review passes; the bug ships anyway; and why a two-agent pipeline catches what a single pass never will
- [Rate Limiter for Prod](articles/rate-limiter-for-prod.md) — 40 runs, four prompt variants, 0% on operational requirements; what the single-agent ceiling actually looks like
- [Anatomy of a Prompt](articles/anatomy-of-a-prompt.md) — the PCSIEFTR formula, section by section, with what each component actually does
- [Semantic Density](articles/semantic-density.md) — why one compound identity outperforms two separate ones, and what that means for how you write a Persona
- [PARC Reference](articles/parc-reference.md) — compact framework reference; the classifier and the formula on one page

---

## Examples

Working prompts, not descriptions of prompts.

- [Zombie-write Layer 1](examples/zombie-layer1-review.md) — senior engineer review agent (consideration-set layer)
- [Zombie-write Layer 2](examples/zombie-layer2-review.md) — SRE infrastructure agent (handoff layer)
- [Rate limiter design](examples/rate-limiter-design.md) — SRE/operational architect agent
- [Rate limiter implementation](examples/rate-limiter-implement.md) — implementation engineer agent
- [iSPARK](examples/ispark.md) — P_p/P_d classifier; audit any Persona in under a minute

---

## Framework

[The Dedicated Machine](paper/DM_d1.md)

---

## Where to Start

Five minutes: [The Zombie Leader](articles/zombie-leader.md).

Audit your current prompts: [iSPARK](examples/ispark.md) — classifies any Persona as procedural or dispositional in one run.

The framework: [paper/DM_d1.md](paper/DM_d1.md).

---

## The Core Finding

A model with a weak Persona and rich Context scores 0/10 on structurally hidden failure modes — not because it lacks knowledge, but because the satisfaction condition was met without finding them.

A model with a procedurally specified Persona scores 10/10 on the same task. Same model. Same context. Different definition of done.

That gap is not a prompt engineering trick. It's architecture.
