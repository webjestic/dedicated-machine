# Literature Note: Ardoq — Prompt Engineering for Enterprise Architects

**Source:** Ardoq, "Prompt Engineering for Enterprise Architects: The Conversational AI Playbook"
**Edition:** September 2025
**Author/Org:** Ardoq (foreword by CEO Erik Bakstad)
**Type:** Industry whitepaper / practitioner guide
**Audience:** Enterprise Architects, CIOs, strategy leaders

---

## What It Is

A practitioner's guide to specification-style prompting, organized as 18 curated prompts across 6 EA use cases:
1. Application Rationalization (Prompts 1–3)
2. Business Capability Mapping (Prompts 4–6)
3. IT Cost and Value Analysis (Prompts 7–9)
4. Technology Risk and Compliance Assessment (Prompts 10–12)
5. M&A Integration and Due Diligence (Prompts 13–15)
6. Cloud Transformation Planning (Prompts 16–18)

The organizing framework is **CO-STAR**: Context, Objective, Style, Tone, Audience, Response. Each prompt is a structured spec delivered in a single pass.

---

## Actual Prompt Structures (Pages 7–20)

All personas are P_d. Sample from the first 11 prompts:

| Prompt | Persona | Task |
|--------|---------|------|
| 1 — Portfolio Triage | "You are an enterprise architect reviewing our application portfolio." | Analyze table data, recommend retire/retain |
| 2 — Exec Summary | "You are preparing a brief for the CIO..." | Summarize rationalization for stakeholders |
| 3 — Devil's Advocate | "As an enterprise architecture assistant..." | List top 3 reasons to regret retiring [App X] |
| 4 — Capability Coverage | "You are an enterprise architect." | Map applications to capabilities, flag gaps |
| 5 — Strategic Alignment | "Act as an Enterprise Architecture advisor." | Identify under/over-invested capabilities |
| 6 — Heatmap Narrative | "You are an Enterprise Architect reviewing our capability assessment." | Write analysis from maturity ratings |
| 7 — Cost Outliers | "You are an IT portfolio analyst." | Identify high-cost/low-value outliers |
| 8 — IT Spend by Capability | (No persona — direct instruction) | Analyze spend distribution for imbalance |
| 9 — Cost Optimization Plan | "You are a FinOps expert assisting an enterprise architect." | Propose 3–5 cost-saving initiatives |
| 10 — Tech Obsolescence | "You are an IT risk analyst." | Flag EOL/unsupported components |
| 11 — Security Posture | "You are a CISO's assistant reviewing our application portfolio security." | Identify high-risk applications |

**Observation:** No P_p personas appear across all 11 reviewed. Every persona is a role label. The actual reasoning driver in each prompt is the **structured data injected into the Context slot** — tables of applications, costs, capabilities, maturity scores. The persona sets the output register; the data constrains the search space.

**"How to Refine" is the iteration model.** Each prompt includes instructions for follow-up prompting to deepen the output — this is where they handle the consideration-set problem implicitly, through dialogue rather than Persona architecture.

---

## The Core Framing

> "Think of AI as a highly capable colleague who needs proper context and clear direction to perform at their best."

The tool-as-amplifier metaphor. The model is a capable human who responds to clear specification. Prompting is communication design.

This is the dominant practitioner framing in the industry as of 2025.

---

## What CO-STAR Does

CO-STAR is a slot-filling specification framework:

| Slot | Purpose |
|------|---------|
| Context | Background information |
| Objective | What you want the AI to do |
| Style | How to write (formal, structured, etc.) |
| Tone | Emotional register |
| Audience | Who the output is for |
| Response | Output format / length |

No mechanism for installing a *search algorithm*. No distinction between Persona-slot and Instructions-slot. No consideration-set theory. Stakes is not a first-class component.

The framework optimizes for output specification (what the answer looks like) rather than reasoning installation (how the model searches for the answer).

---

## PARC vs. CO-STAR: Key Distinctions

| Dimension | CO-STAR (Ardoq) | PARC |
|-----------|-----------------|------|
| Primary lever | Output specification | Identity + search algorithm |
| Persona | Style/tone descriptor | Consideration-set installer |
| Stakes | Not a component | Cost function; Entropy Brake / Termination Inhibitor |
| World Layer / Query Layer | Not distinguished | Two-layer architecture |
| Mechanistic model | Tool-as-amplifier | Dedicated Machine + goal architecture |
| Falsifiability | Not addressed | Empirically tested (exp-07 series) |
| Scope | Single-prompt EA use cases | General framework for any reasoning task |

**The critical difference:** CO-STAR assumes the model will reason adequately if given clear specification. PARC's evidence base shows that P_p installs what the model searches *for*, not just how it formats the answer. The consideration-set boundary is invisible to CO-STAR — the model finds the first satisfactory resolution and presents it well.

---

## What Ardoq Gets Right

1. **Specificity matters.** Their prompts are highly specific to EA scenarios — a practitioner skipping CO-STAR and prompting vaguely would get worse outputs. This is real.

2. **Audience slot.** Explicitly naming who the output is for changes register meaningfully. PARC doesn't formalize this — it's implicitly handled by Format/Request. Worth noting.

3. **Concrete examples.** The 18 worked examples are the actual value. CO-STAR as a framework is thin; the domain-specific prompts embedded in it are the real contribution.

4. **The gap they identify:** Bakstad's foreword notes that EA teams are failing to extract value from AI because they don't know how to prompt. This is the correct diagnosis. CO-STAR is a scaffolding answer. PARC is a mechanistic answer.

---

## What It Misses (from a PARC perspective)

1. **No distinction between P_p and P_d.** Every persona is a role label. "You are an IT risk analyst" leaves the consideration set undefined. The model finds the most salient risk-analyst response — which may not include the specific failure mode the practitioner needs to see.

2. **Data grounding masks the persona gap.** For structured EA tasks (portfolio tables, cost spreadsheets, maturity scores), the input data constrains the consideration set directly. The model doesn't need a P_p to know what to look at — the data tells it. This is why the system appears to work without P_p. But it only works when the data is complete. When the data doesn't contain the signal (like a silent lock-loss mechanism in code), P_d produces the first satisfactory resolution that fits the data — which may be wrong.

3. **"How to Refine" externalizes the consideration-set problem.** Instead of installing a search algorithm in the Persona, Ardoq's model has the practitioner iterate manually — add more context, ask follow-ups, drill down. This works but transfers cognitive load back to the human. PARC's P_p installs the iteration *inside the single pass*.

4. **Style ≠ Stakes.** CO-STAR's Style and Tone slots control surface behavior. They do not install a cost function. There's no equivalent to Task Stakes (Entropy Brake) — the model has no structural reason to terminate cleanly vs. elaborate indefinitely.

5. **No World Layer / Query Layer separation.** The entire prompt is a single-layer specification. Context contamination is not addressed.

6. **The few-shot confound would look like CO-STAR working.** Domain expertise in the Context slot (CO-STAR) drives better outputs on data-rich tasks. That looks like CO-STAR is correct. PARC's slot-swap experiments (exp-07c, exp-07d) show content in any slot helps — until you hit the consideration-set ceiling that only P_p can raise.

---

## Critical Insight: Data Grounding as a Consideration-Set Substitute

Ardoq's system surfaces a domain condition PARC's experiments haven't explicitly tested:

**When input data is structured and complete, P_d may be sufficient.** The portfolio table tells the model exactly what to analyze. The maturity score grid tells it what to pattern-match. The consideration set is externally constrained by the data, not internally constrained by the Persona.

**When input data is incomplete or requires simulation, P_p becomes load-bearing.** This is the zombie-write scenario: no data row says "process-pause zombie write." The model must simulate system state across the lock lifecycle to find it. P_d finds the nearest satisfactory resolution within the data (heartbeat silence mechanism). P_p installs the inference step that reaches beyond the data.

**The Ardoq/PARC boundary is the data completeness boundary.** CO-STAR works for data-rich, structured EA tasks because the data is the consideration set. PARC is needed when the finding requires reasoning beyond the data provided.

This has a testable implication: a P_d prompt given the full Ardoq-style structured data (application inventory, maturity scores, dependency map) should produce outputs indistinguishable from P_p — because the data is doing the work P_p would otherwise do.

---

## Relevance to PARC Research

**As a foil:** CO-STAR represents the practitioner consensus PARC is arguing against. The claim "a capable colleague who needs clear direction" is precisely what the P_p/P_d experiments falsify on data-sparse tasks: same direction, same context, different identity — 10/10 vs. 0/10.

**For d5:** Cite Ardoq as the specification approach for structured, data-grounded tasks. Frame PARC as addressing the case CO-STAR can't — tasks where the finding is not derivable from the input data alone.

**The audience slot:** CO-STAR's Audience slot meaningfully changes output register. PARC doesn't formalize this. Consider whether Format should absorb it explicitly, or whether it belongs in Stakes (identity stakes for the audience changes how the machine aims).

**The "How to Refine" pattern:** Ardoq's iterative refinement model is a manual approximation of what P_p installs automatically. Worth naming this in d5 — the practitioner using CO-STAR has to carry the consideration-set expansion in their head and supply it through follow-ups. P_p moves that work inside the prompt.

---

## Citation

Ardoq. (2025, September). *Prompt Engineering for Enterprise Architects: The Conversational AI Playbook*. Ardoq AS. [Industry whitepaper]

---

## Remaining Prompts (12–18) and Advanced Techniques

Prompts 12–18 confirm the pattern from the first half. All personas are P_d:
- Prompt 12: "Act as an IT governance analyst."
- Prompt 13: "You are assisting in an IT merger." (no specific role)
- Prompt 14: "As an Enterprise Architect evaluating a merger..."
- Prompt 15: "You are an Enterprise Architect tasked with presenting the IT integration roadmap..."
- Prompt 16: "You are a cloud migration advisor."
- Prompt 17: No persona — direct instruction ("We have classified our applications...")
- Prompt 18: "Act as an enterprise architect preparing the business case for cloud transformation."

0 of 18 prompts use P_p. The data injection pattern is consistent across all use cases.

**Advanced Techniques (page 30)** — four techniques listed:
1. Break It Into Steps — sequential prompting / chain-of-thought via dialogue
2. Add Extra Information — data grounding via additional context
3. Ask It to Check Its Work — "What assumptions are you making in this plan?" — manual self-critique
4. Adjust the Tone — audience/register control

Technique 3 is the most interesting from a PARC perspective. "What assumptions are you making?" is a human-applied consideration-set probe — the practitioner is manually doing what P_p installs architecturally. The practitioner carries the awareness that the model may have reasoned outside its data; they apply it interactively rather than embedding it in the Persona.

**What's Next (page 32):**
> "As AI models get more advanced and potentially specialized for EA, they'll need less context."

This is a direct falsifiable prediction difference with PARC:
- **Ardoq's prediction:** Better models → P_d sufficient → prompting complexity decreases
- **PARC's prediction:** Better models still require P_p for data-sparse tasks — the consideration-set boundary is determined by Persona architecture, not raw model capability

This is worth naming explicitly in d5. If Ardoq is right, PARC's P_p claim weakens over time. If PARC is right, the architectural claim holds regardless of model capability.

---

*Note: Full 32-page document reviewed.*
