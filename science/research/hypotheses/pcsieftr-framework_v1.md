# Hypothesis: PCSIEFTR — A Next-Generation Prompt Engineering Framework

**Status:** Active
**Phase:** Hypothesize
**Working context:** `research/active/pcsieftr-context.md`

---

## The Problem with Existing Frameworks

Standard prompt engineering frameworks (CO-STAR, RISEN, APE, COCE, etc.) treat prompt
construction as a **task-specification problem**. They optimize one layer: what to do,
how to format it, what role to assign. They largely ignore the layer that handles everything
you didn't write instructions for.

This is not a minor gap. It means existing frameworks break down predictably at:
- Edge cases not covered by the instructions
- Tasks requiring judgment under ambiguity
- Scenarios where accuracy and fluency conflict

**PCSIEFTR proposes that prompt components are not equal weight — they split into two
distinct layers with fundamentally different functions.**

---

## The Two-Layer Model

### World Layer — *where judgment lives*

These components encode the reasoning environment. They activate the model's capacity to
handle situations that were never written into the instructions.

| Component | What it actually does |
|-----------|----------------------|
| **Persona** | Encodes judgment and expertise. Not role assignment — reasoning calibration. A strong Persona generalizes to edge cases that were never specified. A weak Persona ("expert writer") gives you nothing because it carries no actual judgment. |
| **Context** | Anchors relevance. Situates the model in a specific knowledge domain. Too much context dilutes attention; the right context constrains the reasoning space. |
| **Stakes** | Calibrates quality of reasoning. Encoding consequence shifts the model's reasoning posture — it attends to edge cases, hedges where appropriate, and prioritizes accuracy over fluency when the two conflict. **This is the central hypothesis.** |
| **Tone** | Sets the delivery register. Distinct from Persona: Persona is identity, Tone is mood. They layer — they do not replace each other. |

### Task Layer — *where execution lives*

These components define the task and its constraints. They are important but secondary —
they operate within the reasoning environment set by the World Layer.

| Component | What it actually does |
|-----------|----------------------|
| **Instructions** | **Guardrails, not guidance.** This is a deliberate redefinition. Instructions in this framework do not carry voice, quality standards, or edge case handling — Persona does that. Instructions scope constraints specific to the task: what is permitted, what is off-limits, what the epistemic or ethical boundaries are. If you find yourself writing long Instructions, your Persona isn't carrying its weight. |
| **Examples** | Transfers pattern. The most reliable way to move voice and quality bar into the model. Risk: over-anchoring — the model may not generalize beyond the example's shape. |
| **Format** | Defines the container. Output structure. Can constrain quality if the container doesn't fit the answer. |
| **Request** | Routes the task. The actual ask. One sentence. Everything else is handled upstream. |

---

## The Key Redefinition

**Instructions ≠ a list of DOs and DON'Ts.**

Traditional prompt engineering treats Instructions as the primary carrier of task direction.
PCSIEFTR strips Instructions to guardrails and moves the judgment load to Persona.

> If you were briefing a Senior Architect, you would not write: "review this file, check that
> the database is normalized, make sure you write comments." That's distrust encoded as text.
> You give them the problem. Their expertise fills the rest.

The same applies to a model with a well-constructed Persona. Heavy Instructions are what you
write when your Persona isn't strong enough.

**Instructions cover what you thought of. Persona covers what you didn't.**

---

## The Stakes Hypothesis (Central Claim)

Explicitly encoding **what is at risk** in a prompt shifts the model's internal attention
weighting in a way that improves reasoning quality — not just output polish.

This is distinct from being "more specific." Stakes activate a different reasoning posture.

Working theory: Stakes-laden context may shift attention in middle-to-late transformer layers
in a way that parallels the effect of high-stakes fine-tuning data in RLHF. This is
speculative and is one of the things the experiment is designed to probe.

---

## What Will Be Tested

1. **Stakes vs. No-Stakes** — identical prompts with and without the Stakes component; compare output quality, reasoning depth, and error rate across tasks
2. **PCSIEFTR vs. CO-STAR / RISEN** — head-to-head on reasoning tasks, creative tasks, and domain-expert tasks
3. **Stakes isolation (ablation)** — which component(s) drive the quality delta; Stakes must be shown as an independent contributor, not noise from prompt length
4. **Cross-model validation** — does the effect hold across Claude and Gemini? A finding that only holds on one model family is not a finding.

---

## Success Criteria

- Measurable quality delta on reasoning tasks with Stakes present vs. absent
- Delta persists across ≥2 model families
- Ablation shows Stakes as a significant independent contributor

---

## Related Work

- Baseline / control group: CO-STAR, RISEN, APE, COCE
- Prior internal work: `E[R | C_user, P_scratch^injected] ≈ E[R | C_user, P_scratch^generated]` — transformer layer framing of prompt injection effects
