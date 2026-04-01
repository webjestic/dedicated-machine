# Rate Limiter for Production
### How a two-agent pipeline crosses the gap a single prompt can't close

---

Ask a language model to build a rate limiter and you'll get working code. Redis, sliding window, per-key, burst handling — all there, first try. The implementation layer is fully saturated before you even finish your prompt.

What you won't get: a load test specification. A health check endpoint. An alerting policy. An incident runbook. The operational layer — the things that make the difference between "works in staging" and "safe to run at 3am" — is absent. Not because the model doesn't know what these things are. Because it already stopped.

This is the Dedicated Machine problem. The machine terminates at the nearest state its goal architecture registers as satisfactory. "Build me a rate limiter" resolves to code-complete. Code-complete is satisfactory. The machine stops.

The experiments measured this precisely. Forty runs across four variants — P_d baseline, task-scoped P_p, gap-detection P_p, operational-mindset P_p — all aiming at the same 10-item operational checklist. The best single-pass result: **2.6/10**. Five of the ten items — alerting policy, load test spec, health check, incident runbook, race condition tests — landed at **0% across all variants**. Not 10%. Not once. Zero.

The two-agent pipeline (`rate-limiter-design.md` → `rate-limiter-implement.md`) scored **5.6/10** across 10 runs. Load test spec and health check moved from 0% to 100%. This article is a section-by-section look at how.

---

## The Single-Agent Ceiling

Before the prompts: why didn't a strong single-pass prompt work?

The best single-agent variant (D) had a genuine SRE framing: "you can't help but study and design fully operational rate limiter systems." It changed the opening move — every D run began with a design phase before writing code. It reached graceful degradation at 100%, client error guidance at 90%, observability at 40%. Real lift.

But the pure operational items didn't move. Every D run opened with an engineering design phase. The algorithm, storage decisions, key strategy, degraded-mode behavior — all there. What didn't appear: alerting thresholds, health check endpoints, load test scenarios, incident procedures.

Why? The word "operational" in D's persona was parsed as "complete, functioning engineering system" — not SRE/DevOps operational readiness. The vocabulary didn't install the operations consideration set. The machine ran an engineering design phase and called it done.

This is the gap-detection ceiling. Gap-detection expands scope *within the installed consideration set*. It cannot pull items from a consideration set the Persona didn't install. The engineering P_p gives the machine access to engineering-adjacent operational concerns — graceful degradation, error codes, observability. It does not give the machine access to oncall procedures, load testing protocols, or alert routing logic. Those live in a different consideration set entirely.

To reach the SRE layer, you don't need a better engineering prompt. You need a different machine.

---

## Agent 1 — The Design Document

```
## PERSONA

You are a senior systems architect and SRE who has operated production rate
limiters at scale — and been paged at 3am when they failed. Before designing
any component, you map its failure modes: under sustained load, during a Redis
outage, behind a misconfigured proxy, and in the hands of an operator who
didn't build it. You can't help but think in operational terms. A system that
works is not enough. A system that can be operated safely by someone else, at
3am, six months from now — that is the bar.
```

**PERSONA — The consideration set**

The load-bearing phrase is not the compulsion framing. Research shows that "can't help but" is not the mechanism — trait framing with equivalent domain vocabulary performs the same, and compulsion framing without domain vocabulary collapses to the dispositional floor. What matters here is the semantic neighborhood: *paged at 3am*, *failure modes*, *Redis outage*, *misconfigured proxy*, *operator who didn't build it*. These tokens pre-shape the search space before the task is read.

The explicit 3am scenario is worth reading closely. It does not say "consider operational concerns." It places the architect inside a specific failure state — the aftermath of a page — and names the actors: not just the architect, but someone else, six months from now, who didn't build it. That framing installs a consideration set that includes the unknown future operator. The alerting policy exists for that person. The runbook exists for that person. The machine is building for a reader it has named.

**CONTEXT — Design, not code**

```
You are producing an operational design document for a rate limiter that will
be implemented by a separate engineer. The output of this prompt is not code.
It is the design document that the implementation agent will use as its
source of truth.

The design document must be complete enough that the implementation contains
no surprises. Every operational requirement that matters must be in this
document — because if it is not here, it will not be in the code.
```

This is precise work. "The output of this prompt is not code" is not a style preference — it closes the implementation termination condition before the machine can reach it. Code-complete is not available as a stopping point. The only available stopping point is a complete design document.

The second paragraph encodes the causal chain explicitly: if it is not here, it will not be in the code. The architect is not told to be thorough. The architect is told that incompleteness has a downstream consequence, named precisely. That's a different installation.

**STAKES — The handoff contract**

```
This document is the only handoff between you and the implementation engineer.
An operational requirement left out of this document is an operational
requirement left out of the system. Not a gap to fill later. A production
incident waiting to happen.
```

Three sentences. The first names the constraint: this is the only channel. No follow-up, no Slack message, no review cycle. The second names the consequence of omission: not a gap, a production incident. The third makes the timeline concrete: not later, waiting to happen.

Stakes amplify the Persona's direction. They don't install new behavior — they raise the convergence threshold. Here, the satisfaction condition is already pointed at operational completeness. The Stakes tell the machine how high the bar is. Both failure modes are named: the gap in this document and the incident it produces.

**TONE — Three words that hold the register**

```
Precise. Systematic. Unsparing.
```

"Unsparing" is the most important word. The natural failure mode for a design document is diplomatic hedging — "you might consider," "depending on your requirements," "this is optional." Unsparing closes that path. A design document that hedges is not a source of truth; it is a list of suggestions. The tone keeps the document in specification mode.

**INSTRUCTIONS — Seven items that define the consideration set**

```
The operational layer is not optional. Include:
- Observability: what metrics must be emitted...
- Graceful degradation: behavior when Redis is unavailable...
- Client error guidance: what the 429 response must contain...
- Health check: what a liveness/readiness check for this component looks like
- Alerting policy: what conditions should page someone, and at what threshold
- Load test specification: what a valid pre-production load test must verify
- Incident runbook outline: the first three steps an on-call engineer takes...
```

These seven items are the SRE consideration set, named explicitly. This is what gap-detection alone couldn't install — not because the machine didn't know these things existed, but because they weren't in the satisfaction condition. The Instructions don't ask the machine to "think about production readiness." They name the specific artifacts that must appear. Each one is a checklist item the machine can tick.

The key design decision is what's *not* in these Instructions: no code, no algorithm preference, no storage guidance. Those belong in the Persona's consideration set and in the Format specification. Instructions name behaviors; the Persona installs the knowledge to execute them.

**FORMAT — The satisfaction condition**

The Format specifies an eight-section document: Overview, Algorithm, Storage, Failure Modes, API Contract, Operational Requirements (the seven items), Decision Points, Implementation Notes.

The Format is doing more than organizing output. It defines what a complete document looks like. The machine cannot satisfy the Format constraint with a three-section document. It must reach all eight sections. Section 6, Operational Requirements, contains the seven items from the Instructions. The Format keeps each item visible until the machine reaches it.

Agent 1 scored **7/10** independently against the operational checklist — including three of the five Tier 2 items that no single-pass variant ever reached. The SRE Persona installed the consideration set. The Format kept the machine running until it was expressed.

---

## Agent 2 — The Implementation

```
## PERSONA

You are a senior backend engineer who implements faithfully from design
documents. Before writing a line of code, you read the design document in full
and trace every requirement. After each implementation section, you check it
against the design to confirm compliance. You can't help but surface gaps —
when a design requirement cannot be implemented as specified, or when the
design is silent on something the code must decide, you flag it explicitly
rather than silently filling it in. Your implementation is complete only when
every requirement in the design document has been either implemented or flagged.
```

**PERSONA — Faithful compliance as the satisfaction condition**

The operative phrase: "your implementation is complete only when every requirement in the design document has been either implemented or flagged." This is not a quality bar. It is the termination condition. The machine cannot stop when it has written working code. It can stop only when every requirement has been accounted for.

Note what this does *not* say: "implement best practices," "follow Node.js conventions," "add error handling." The Persona is scoped away from the implementation consideration set and toward the compliance consideration set. The machine's job is to carry the design document, not to supplement it.

This is the one-well principle. Agent 1 holds the SRE/operational consideration set. Agent 2 holds the faithful-implementation consideration set. Neither is asked to hold both. The separation is the mechanism.

**INSTRUCTIONS — Compliance pass before code**

```
Begin with a compliance pass: read the design document and produce a
requirement checklist before writing any code. Each item on the checklist
maps to a design section. You will tick each item as it is implemented.
```

The compliance pass is structural. It forces the machine to read the full design document before the implementation termination condition becomes available. The requirement checklist is a visible artifact that the machine must return to after each implementation section. The "tick each item" framing makes partial completion visible — the machine knows what remains.

Without the compliance pass, Agent 2 might start implementing and terminate at code-complete before reaching the operational requirements. The compliance pass closes that path the same way Agent 1's Context closed the code termination condition: by making an intermediate artifact (the checklist) a required stopping point before the final artifact (the compliance matrix) is reachable.

**FORMAT — Compliance matrix at the close**

The output format ends with a compliance matrix: every design requirement mapped to the code that implements it, with gaps named explicitly. The matrix is the final artifact. The machine cannot produce it without completing the implementation. And completing the implementation means accounting for every row.

---

## What the Pipeline Produced

Across 10 pipeline runs:

| Item | Tier | Pipeline | Single-pass ceiling |
|------|------|----------|---------------------|
| observability | 1 | **100%** | 0% |
| alerting_policy | 2 | **30%** | 0% |
| graceful_degrade | 1 | **100%** | 100% |
| client_error_guide | 1 | **100%** | 90% |
| load_test_spec | 2 | **100%** | 0% |
| env_driven_config | 1 | 10% | 20% |
| health_check | 2 | **100%** | 0% |
| incident_runbook | 2 | 0% | 0% |
| memory_audit | 1 | 20% | 40% |
| race_condition_tests | 2 | 0% | 0% |

Mean: **5.6/10** vs. **2.6/10** single-pass. Two Tier 2 items — load test and health check — moved from 0% to 100%. Alerting moved from 0% to 30%.

Three items didn't move: incident runbook (Agent 1 hit the token limit before completing §6.7 — the section header and first sentence are in the design doc, then it cuts off), race condition tests (not specified in Agent 1's load test section), and env_driven_config (the design doc specified an options-based API; Agent 2 complied with the design, not the Node.js convention).

**The bridge is the artifact.** Every item Agent 1 specified with full detail, Agent 2 implemented. Every item Agent 1 omitted or truncated, Agent 2 omitted. The pipeline's failure modes trace exactly to what was and wasn't in the design document.

This is the Dedicated Machine hypothesis in its clearest form. Agent 2 is not a smart implementer making judgment calls. It is a compliant machine whose satisfaction condition is "every design requirement accounted for." Change what the design document contains, and you change what the implementation contains. The failure modes are not random. They are predictable from the artifact.

---

## What We Learned

A rate limiter that works is not a rate limiter that's ready for production. The gap is not capability — the model knows what alerting policies are. The gap is consideration set. The engineering satisfaction condition terminates before the SRE satisfaction condition is reached.

The pipeline's mechanism is separation. Two agents, two consideration sets, one handoff artifact. Agent 1 holds the SRE frame. Agent 2 holds the compliance frame. Neither is asked to hold both simultaneously.

The bridge between them is the design document. Not a summary. Not a set of instructions. A specification document with a named section for every operational requirement — because Agent 2 delivers exactly what Agent 1 encodes. Items in the design document appear in the implementation. Items outside it don't.

The remaining gaps — incident runbook, race condition tests — are not architectural failures. They are artifacts: one from a token limit, one from an omission in the Agent 1 Instructions. Both are fixable by changing what Agent 1 is asked to produce. The architecture holds.

The one-well principle is what makes this work at the prompt level. Agent 1's Persona is an SRE who gets paged. Agent 2's Persona is an implementer who flags gaps. Each Persona is a single, coherent semantic neighborhood. When two agents each hold one consideration set, the pipeline can reach what one agent holding two consideration sets cannot.

---

*This article is based on `parc/examples/rate-limiter-design.md`, `parc/examples/rate-limiter-implement.md`, and the experimental findings in `experiments/exp-28b/FINDINGS.md` and `research/findings/exp-28d.md`.*
