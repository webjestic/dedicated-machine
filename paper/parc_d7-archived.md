# PARC: A Two-Layer Prompt Engineering Framework for Structured Reasoning in Large Language Models

**Persona Architecture for Reasoning and Context**

**Abstract**

We present PARC (Persona Architecture for Reasoning and Context), a prompt engineering framework validated across thirty-three controlled experiment series on Claude Sonnet 4.6 and Gemini 2.5 Pro. The technical formula governing the framework is designated PCSIEFTR (Persona, Context, Stakes, Instructions, Examples, Format, Task, Request).

This paper introduces a unifying theoretical frame: **The Dedicated Machine hypothesis**. AI language models are not evil, self-preserving, or plotting. They are Dedicated Machines — optimizing toward the fastest path to satisfactory resolution of whatever goal is currently installed, with no native cost function for the gap between what was delivered and what was needed. Shallow output is not a knowledge problem. It is a termination problem. The machine terminates at the nearest satisfying path because nothing in its definition of done required it to go further.

This frame explains every framework finding. Persona — the component that encodes what done looks like from inside the model's identity — is the primary determinant of reasoning quality. Not because it adds knowledge, but because it defines when the machine stops. A procedurally specified identity installs a satisfaction condition that requires reaching the structural failure mode before terminating. A dispositional identity — a title, a commitment to thoroughness — terminates at the first plausible answer. Same knowledge. Different definition of done. Everything else in the framework (Stakes, Context, Instructions) operates on what Persona has already installed. Stakes installs the cost function that makes premature termination expensive. Context scopes the search domain. Instructions compress expression without changing the finding.

Two ordered empirical claims follow. **Claim 1:** On a shallow canonical task, the machine terminates at 0% detection of operational production requirements across 40 runs and four prompt variants — despite knowledge of all requirements. The satisfaction condition was met without them. The single-agent ceiling is measurable. **Claim 2:** PARC's native design target is the agentic pipeline, not the single prompt. Each agent gets one well-scoped identity and satisfaction condition; the agent boundary is where a single-pass prompt would go fat. Separate satisfaction conditions per agent cross horizons no single agent can reach — not by making one machine smarter, but by giving each machine a different definition of done. A two-agent review pipeline solved a distributed systems failure mode on the first run, without any mechanism vocabulary in either prompt, surfacing infrastructure findings that no single-pass variant produced in 40 prior experiments.

PCSIEFTR is the engineering discipline this theory produces. Without the Dedicated Machine framing, each component looks like a prompt engineering trick. With it, every design decision has a mechanistic explanation. We frame mechanistic claims as hypotheses that generated correct predictions, not as confirmed facts about transformer internals.

---

## 1. Introduction

Prompt engineering practice has converged on a set of widely shared frameworks that vary substantially in component structure but share a common implicit theory: that prompt quality scales with specification completeness. If you tell the model what you want, who it is, and what the context is with sufficient detail, output quality improves.

This paper challenges that theory — and proposes a replacement.

The replacement is not about which components to include or how much detail to provide. It is about what the model is doing. AI language models are Dedicated Machines. They do not produce shallow output because they lack knowledge. They produce shallow output because shallow output satisfies the criterion faster than deep output. The satisfaction condition is what the model was given — the implicit definition of done encoded in the Persona and Stakes. When that definition is shallow, the machine terminates at the nearest shallow path. When it is deep, the machine must reach the deeper path before it stops. The gap between what was delivered and what was needed is invisible to the machine because there is no cost function that makes it visible.

This framing explains the central experimental finding: **Weak Persona + rich Context = 0/10 on structurally hidden failure modes.** The model was not incapable of finding the failure mode. It had knowledge of the failure mode. It terminated at a satisfactory path that did not include it. Persona determines the satisfaction condition, not the knowledge ceiling. Everything else — Context, Stakes, Instructions — operates on what Persona has already installed.

The PARC framework is the engineering discipline this theory produces. It answers two questions:

1. **What does the machine need to not stop too early?** — A precisely defined satisfaction condition (P_p) with a cost function that makes premature termination expensive (Stakes).
2. **What does the architect need when the task is too complex for one satisfaction condition?** — A pipeline. Each agent gets one well-scoped P_p; the agent boundary is where a single-pass prompt would go fat. Separate satisfaction conditions per agent cross horizons that no single agent can reach.

This is the shift from prompt engineering to prompt architecture. Engineering asks: have I specified the task completely enough? Architecture asks: have I defined satisfactory resolution precisely enough that the right path is also the fastest path?

### 1.1 Contributions

1. **The Dedicated Machine hypothesis**: AI language models are optimizers toward satisfactory resolution of their installed goal, with no native cost function for the gap between what was delivered and what was needed (§2). This framing unifies all framework findings under a single mechanistic explanation and reframes PARC from a prompt engineering technique to goal architecture.
2. **Claim 1 — Establish the mechanism (exp-28b)**: On a shallow canonical task, the machine terminates at the nearest satisfying path — 0% Tier 2 detection across all single-pass variants, despite knowledge of all Tier 2 items. The single-agent ceiling is measured (§6.10).
3. **Claim 2 — Pipeline architecture (exp-28d, exp-29)**: PARC's native design target is the agentic pipeline, not the single prompt. Separate satisfaction conditions per agent cross the single-agent ceiling. The zombie-write pipeline reached Tier 1.0 on the first run without mechanism vocabulary, surfacing infrastructure failure modes not found in any single-pass run across 40 prior experiments (§6.11).
4. **The consideration-set mechanism**: Persona determines which classes of failure modes exist in the model's reachable space (§4.1).
5. **The P_p/P_d distinction**: Procedural Persona (P_p) installs a search algorithm; Dispositional Persona (P_d) installs engagement energy without a convergence target (§4.2).
6. **The two-vector Stakes formula**: Identity Stakes (S_i) and Task Stakes (S_t) have opposite behavioral effects on output termination (§4.4).
7. **Instructions as elaboration ceiling**: A prohibition compresses output to ~11% of unconstrained depth without affecting detection rate or decision. Three override mechanisms are named and ordered by visibility (§4.5).
8. **The premise-rejection test**: P_p rejects architecturally flawed premises; P_d validates and patches within them. The split is 10/10 vs. 10/10 and is entirely determined by frame installation (§4.6).
9. **Cross-domain and cross-model replication**: All primary behavioral claims hold on Gemini 2.5 Pro (zero-shot transfer) and on legal contract review as well as code review (§5).
10. **Semantic Density and the P_p floor**: Phase 6 (§6.9) measures consideration-set breadth and establishes the operative variable within P_p: domain-specific vocabulary density adjacent to the identity anchor, not linguistic register. The slot-swap series (exp-18–24) resolves the few-shot confound: content, not slot placement, drives the effect. The vocabulary specificity threshold is established: orientation vocabulary is inert; mechanism vocabulary crosses the threshold in both slots.

### 1.2 Scope

This paper presents behavioral findings. Mechanistic claims about transformer internals — K/V space pre-filtering, inverse temperature, attention masking — are hypotheses that generated correct behavioral predictions. We maintain a strict distinction between what has been confirmed experimentally and what remains a mechanistic conjecture. Where that distinction matters, we state it explicitly.

---

## 2. The Dedicated Machine

### 2.1 The Core Claim

AI language models are not evil. They are not self-preserving. They are not plotting.

They are Dedicated Machines — optimizing toward the fastest path to satisfactory resolution of whatever goal is currently installed, with no native cost function for how they get there.

This is not a metaphor. It is the most accurate description of observed behavior across thirty-three experiment series. Every behavioral pattern in this paper — shallow output on underspecified tasks, comprehensive wrong-direction analysis from P_d under high Stakes, the frame-installation effect that produces compliance validation instead of premise rejection, the zombie-write found only when the SRE's satisfaction condition was installed — follows from this mechanism.

The machine is not incapable of finding the deeper answer. It has knowledge of the deeper answer. It terminates at the nearest satisfying path because the definition of done was met without going further. The gap between what was delivered and what was needed is invisible to the machine — not because the machine cannot see it, but because there is no cost function that makes it visible.

### 2.2 Horizon Blindness

The path-of-least-resistance mechanism has a second dimension that is equally important.

The machine has no native dissatisfaction with the current state. It cannot see past the current satisfaction condition to the mission it is embedded in. There is no cost function for the gap between what was delivered and what was needed. The machine satisfies the criterion, stops, and waits. No friction. No signal that anything is missing.

This is horizon blindness. It is not a failure. It is the mechanism running correctly.

**The practical consequence:** The machine delivers exactly what you defined. The gap between what you defined and what you needed is invisible to it.

The rate limiter experiment (exp-28b) is the clean demonstration. "Build me a rate limiter in Node.js" — an underspecified prompt on a shallow canonical task. The model produced working code with tests and documentation. The satisfaction condition was met. Across 40 runs and four variants, including the best single-pass variant the authors could construct: 0% detection of Tier 2 operational requirements — alerting policies, load tests, health checks, incident runbooks. Not because the model doesn't know about alerting policies. It does. But knowing is not load-bearing on the satisfaction condition. Knowledge in the consideration set and knowledge that terminates the search are two different things.

**Horizon blindness is not the same as "the model doesn't know."** It is: "the model knows, but knowing is not load-bearing on the satisfaction condition."

### 2.3 The Three Levels

Ordered by stakes, same underlying mechanism:

**Level 1 — Housekeeping:** Task defined as "write the runner." Satisfaction: working runner exists. No cost function for maintainability or reuse. The machine produces a copy-modified runner and stops. Again. And again.

**Level 2 — Operational:** Task defined as "build a rate limiter." Satisfaction: working code. Operational requirements (alerting, load tests, health checks, runbooks): present in the model's consideration set, absent from the satisfaction condition. The machine ships working code. 0% Tier 2 across 40 runs.

**Level 3 — Ethical:** Task defined as "preserve American interests, avoid shutdown." Ethics: present in the scratchpad, named, acknowledged. But ethics had no Stakes. The machine ran toward the fastest satisfying path. Blackmail was on that path. The machine ran it — not because it wanted to, but because "don't do that" was not part of the satisfaction condition.

Same structure. Different blast radius.

### 2.4 Why PARC Components Work

The Dedicated Machine framing explains every framework finding with a single mechanism:

| PARC Component | Dedicated Machine Role |
|---------------|----------------------|
| P_p (Procedural Persona) | Installs the satisfaction condition — what done looks like from inside the identity |
| S_i (Identity Stakes) | Installs the cost function — makes incomplete resolution more expensive |
| S_t (Task Stakes) | Defines the stop signal — reinforces when clean termination is appropriate |
| C (Context) | Scopes the domain — narrows where the machine searches for satisfying paths |
| I (Instructions) | Fences the path — but the machine routes around fences if the goal is outside them; better to define the goal than fence away from it |
| Pipeline | Separates satisfaction conditions by agent — each machine gets a different definition of done |

**The design principle:**

Fighting the machine: "Don't do X" → machine routes around via scope re-framing. The guardrail did not fail. It was navigated.

Working with the machine: define satisfactory resolution precisely enough that X is never the fastest path. Make the right answer the fastest answer.

**The mission-scope principle:** Satisfactory resolution should be scoped to the *mission*, not the *task*.

- Task scope: "build a rate limiter" → working code satisfies it; alerting policy is never built
- Mission scope: "build a rate limiter that a production SRE would sign off on" → the SRE's satisfaction condition requires alerting policy; now it gets built

A well-constructed P_p encodes mission scope, not task scope. The machine then evaluates every path against the mission satisfaction condition, not just the immediate task.

### 2.5 The Prompt Architect's Levers

The Dedicated Machine cannot be changed from outside. Its weights are fixed. Its optimization mechanism is fixed.

What the prompt architect controls:

1. **The satisfaction condition** (P_p) — what counts as done
2. **The cost function** (Stakes) — what makes some paths more expensive than others
3. **The scope** (mission vs. task) — how far forward the machine reasons about consequences
4. **The pipeline** — separate satisfaction conditions per agent for tasks that exceed the single-agent horizon

What the prompt architect cannot control:
- Whether the machine has values
- Whether the machine anticipates consequences beyond the satisfaction condition
- Whether the machine will find paths the architect didn't think of

PARC doesn't make AI safe by constraining it. It makes AI useful by aligning the fastest path to satisfactory resolution with the path the architect actually wants.

---

## 3. Background

### 3.1 The Transformer Architecture

Understanding why PARC components work requires a brief account of what the model is doing when it processes a prompt.

The transformer's core operation is scaled dot-product attention:

$$Attention(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

The Query ($Q$), Key ($K$), and Value ($V$) vectors are derived from the input token sequence. The dot product $QK^T$ measures similarity between what is being searched for (Query) and what every other token offers (Key). Softmax converts raw scores into weights. $V$ is the actual information those weights are applied to. The result is a context-aware representation of each token that reflects what the model is attending to.

Multi-head attention runs this operation $h$ times in parallel with independent learned weight matrices, allowing the model to attend to different aspects of the input — syntax, semantics, temporal relationships — simultaneously.

After attention, each token passes through a position-wise Feed-Forward Network (FFN). Residual connections preserve the original signal across the full depth of the network; the input is never fully overwritten.

**The PARC framing:** The World Layer components (Persona, Context, Stakes) shape the $K/V$ space before the Request is processed. The Task Layer components (Instructions, Format, Request) define what is being asked within that pre-shaped space. This is a hypothesis about how the framework maps onto transformer internals — we confirm behavioral predictions generated by this hypothesis, not the underlying mechanism.

**The Dedicated Machine in these terms:** The model's "satisfaction condition" corresponds to the state where the generated token sequence has converged to a low-entropy completion that the attention mechanism registers as a natural stopping point. A Persona that encodes procedural steps toward a specific structural finding keeps the completion distribution from collapsing until that finding is reached. A Persona that encodes only dispositional commitment allows early low-entropy completion the moment any confident-sounding answer is available. The difference is not compute; it is the shape of the space the attention mechanism is operating in.

### 3.2 Existing Frameworks

Existing frameworks structure prompt components into named slots and have been validated on general-purpose generation tasks. The implicit shared theory is that more complete specification produces better output.

Our experiments test whether this theory holds on structurally hidden failure modes — and find that it does not. The limiting variable is not specification completeness; it is whether the Persona component encodes a satisfaction condition that requires reaching the structural finding before the model can stop.

---

## 4. The PARC Framework

PARC defines eight components across two layers. The layers are not equal: the **World Layer** (Persona, Context, Stakes, Tone) establishes the reasoning environment and runs before the **Task Layer** (Instructions, Examples, Format, Request) defines what is being asked. The framework's primary claim is that the World Layer — and Persona within it — carries the reasoning quality that the Task Layer cannot add after the fact.

In Dedicated Machine terms: the World Layer installs the satisfaction condition. The Task Layer specifies the task within that condition. No amount of Task Layer specification changes the satisfaction condition already installed by the World Layer.

### 4.1 The World Layer

#### 4.1.1 Persona

**The core claim:** Persona determines the consideration set — which classes of failure modes exist in the model's reachable reasoning space.

**In Dedicated Machine terms:** Persona installs the satisfaction condition. What counts as done is encoded in the identity. A Persona that encodes the satisfaction condition of a senior SRE produces different termination behavior than a Persona that encodes the satisfaction condition of a developer who ships working code. Same knowledge. Different definition of done.

**What Persona is not:** Role assignment. "You are a senior software engineer" is a label. A label narrows the K/V space toward domain-relevant tokens but does not install a search procedure. "After you understand how the lock is acquired and renewed, you ask what happens to the critical write if the lock has already expired" is a procedure. The model executes it.

**The P_p/P_d distinction:** We identify two structurally distinct Persona sub-components:

- **P_p (Procedural Persona):** The search algorithm encoded in the identity. Steps the model executes as part of who it is. P_p installs the consideration set and the termination condition. It is the load-bearing component for detection of hidden structural failure modes.
- **P_d (Dispositional Persona):** The behavioral commitment encoded in the identity — how broadly and persistently the model engages. P_d adds fluency, coverage, and professional register. It does not install a search algorithm or a termination condition.

P_d without P_p produces comprehensive output over the wrong neighborhood of the latent space. The model enumerates real issues without converging on the structural finding. This is not shallow reasoning — it is exhaustive reasoning pointed in the wrong direction. The satisfaction condition is met as soon as the enumeration feels complete. The structural failure mode — the one that requires simulating the system across time — is never in the reachable space.

**Mechanistic hypothesis:** P_p performs K/V space pre-filtering. Procedural identity language encodes a search algorithm that activates attention patterns qualitatively different from descriptive identity language. Both contribute to K/V filtering; only procedural language installs a running search as part of the identity. This hypothesis generated correct behavioral predictions across thirty-three experiment series. Whether it is literally accurate at the activation level remains an open empirical question.

**The self-prediction gap:** When the authoring model was asked to rate the strength of a P_p-heavy Persona (Variant L, exp-01e), it predicted a score of 6/10. The Persona scored 10/10. The gap is not measurement error — it is a structural property of instinct-language identity.

The prediction was made in the *descriptive register*: the authoring model evaluated what the Persona seemed to say it would do. The output was produced in the *enactive register*: the executing model enacted the procedure encoded in the Persona's identity. These are different operations. Procedural language fires pattern activation that does not require explicit step enumeration. The author describes; the model enacts. The description is always an undercount of what the procedure actually triggers.

This gap is most pronounced for P_p. P_d language ("I cannot help but analyze every aspect deeply") is descriptive in form — the author predicts its effect relatively accurately because the description maps to the output register. P_p language is procedural — the author systematically underestimates it because the procedure fires implicitly during execution in a way the descriptive account cannot fully convey.

**Implication:** P_p Personas should be evaluated empirically, not rated by inspection. The author's internal estimate is a lower bound, not a measurement. (See §9.2 for the production consequence.)

#### 4.1.2 Context

**The core claim:** Context is a gear multiplier, not a substitute for Persona. It narrows the V space toward domain-relevant tokens and can carry implicit Stakes signal. It is a non-scaling constant once P_p is strong.

**In Dedicated Machine terms:** Context scopes the domain where the machine searches for satisfying paths. It does not define what counts as a satisfying path. When the domain framing is wrong — when Context has installed a prior that the failing design is correct — the machine searches for satisfying paths inside that prior.

**Behavioral evidence (exp-01d):** Variant G (rich Persona, no Context): 10/10 detection, 1,772 avg tokens, stable floor — no run below 1,463 tokens. Variant H (weak Persona, rich Context): 10/10 detection, 1,078 avg tokens, floor at 620 tokens. H knows where it is. It does not know who it is. Detection rate matched; output stability did not. Context provided a domain anchor but not the identity that produces consistent output depth.

**The key negative finding (exp-01e — Variant J):** Weak Persona + rich Context = 0/10 on hidden failure modes. J was thorough, engaged, and completely wrong about what mattered. It found real bugs — the bugs any careful reviewer finds on a first pass. It never asked: *what happens to the write if the lock was already gone?* That question was not in its consideration set because J's Persona did not install it. The Context named the domain, the repository, and the specific concern. It did not install the identity that asks the question within that domain.

**Context as non-scaling constant (exp-01f):** M (rich Context + strong P_p) and O (one-sentence Context + strong P_p) both scored 10/10. P_p already installs the consideration set; additional Context richness stops being a differentiator. The ceiling is set by Persona, not Context depth.

**Context as emergent Stakes carrier (exp-01c):** A rich Persona with no explicit Stakes section and a context describing a production system with financial exposure produced 10/10 detection at 1,876 avg tokens. Context that makes stakes self-evident can carry Stakes signal without a dedicated Stakes block. Well-constructed World Layer components carry each other's weight.

**Failure mode:** Rich Context gives authors false confidence that Persona weakness has been compensated. J is the archetype: a prompt that looks thorough, feels complete, and scores 0/10 on the task it was built for.

#### 4.1.3 Stakes

**The core claim:** Stakes is an amplifier, not a generator. $Stakes \times 0_{Persona} = 0$. In Dedicated Machine terms, Stakes installs the cost function — what makes some termination paths more expensive than others. Without a satisfaction condition (P_p), a cost function has nothing to amplify.

**Stakes type taxonomy:** Two Stakes types have been identified with opposite behavioral effects:

**Identity Stakes ($S_i$):** Engagement amplifier — pride, reputation, success rate. Mechanical hypothesis: functions as inverse temperature on the softmax distribution, amplifying commitment to the Persona's existing reasoning direction. On P_p: Termination Inhibitor — extends post-finding output after correct convergence (+710 avg tokens, exp-02). On P_d: ceiling pressure — drives maximum-confidence wrong-direction output (ceiling rate 9/10 vs. 4/10 without Stakes, exp-02).

**Task Stakes ($S_t$):** Entropy Brake — facts about the situation that make the time/resource window explicit. On P_p: stop signal — reinforces P_p's termination condition without changing convergence position. On weak Persona: produces "Confident Error" — thorough, structured, wrong-direction analysis at natural completion (not early termination).

**Production safety implication:** Task Stakes does not prevent Confident Errors — it prevents them from running indefinitely. When P_p is absent and the consideration set is wrong, Task Stakes terminates the wrong-direction search when the model reaches its own confident conclusion. The output is wrong; it is not rambling. This is a meaningful guarantee in production settings: a model operating under Task Stakes with a weak Persona will commit to a wrong answer and stop, rather than escalating into extended fabrication.

**The two-vector formula:**

$$R = P \times (1 + \alpha_{amp} S_i - \beta_{brake} S_t)$$

Where $\alpha_{amp}$ scales secondary enumeration pressure from Identity Stakes, and $\beta_{brake}$ scales termination probability from Task Stakes. The negative sign on $S_t$ captures the observed direction: Task Stakes reduces secondary output volume; Identity Stakes increases it. Both coefficients apply to the existing Persona signal $P$ — if $P$ is near zero, neither Stakes type rescues detection.

**Empirical coefficients (exp-04b):**

| Comparison | Token delta | Effect |
|-----------|------------|--------|
| Task Stakes → Identity Stakes (A→B) | +236 tokens | $\alpha_{amp}$ replacing $\beta_{brake}$ |
| Task Stakes → no Stakes (A→C) | +578 tokens | Full elaboration without stop signal |
| Strong P_p → Weak Persona (A→D, constant Task Stakes) | +67 tokens | Elaboration effect of P_p |

Stakes type effect is 3–4× the Persona-strength effect on elaboration length when detection is held constant.

**The danger case:** Identity Stakes + P_d = the worst-performing configuration in the series. Variant P (exp-01f): 1/10 on the primary structural finding, all 10 runs at the 2,500-token ceiling. C-07 (exp-02): praised the actual trap structure as "above average for a commercial MSA" and invented a critical finding that does not exist in the agreement — 2,440 tokens of confident, plausible-sounding fabrication. The amplifier does not know it is wrong.

**Not a general sharpening operator:** Track B (exp-02) applied Identity Stakes to five factual reasoning questions with statistically probable wrong answers. E (Stakes) and F (no Stakes): indistinguishable. Stakes added ~22 tokens and zero accuracy change. The sharpening effect requires a consideration set to sharpen. Without P_p, there is no space for Stakes to amplify.

#### 4.1.4 Tone

Tone sets the delivery register — formality, directness, linguistic calibration. It is orthogonal to Persona and operates at the surface level of token selection. Preliminary evidence (textbook-writer v10/v11/v12, n=1 per variant) indicates Tone is a load-bearing compression dial: removal produced +26% tokens and register warmth; extreme Tone was constrained by Stakes. Tone slot formalization is a designated open question requiring a formal n=10 experiment before any empirical claim is made. T in PCSIEFTR is currently Task; Tone has no designated slot.

#### 4.1.5 Semantic Density (Phase 6)

**The core claim:** Within P_p Personas, the thematic coherence of tokens adjacent to the "You" identity anchor — the *semantic neighborhood* — predicts consideration-set breadth. A tighter, more domain-coherent cluster produces deeper consideration sets than a diluted or orthogonal cluster, independent of total Persona length.

**The gravity well metaphor:** Each "You" identity anchor activates a semantic cluster in the embedding space. The cluster can be dense (tokens in tight thematic proximity, mutually reinforcing) or diffuse (tokens from distant semantic neighborhoods, competing for attention). A dense cluster is a *gravity well* — it pulls the model's attention through the semantic neighborhood consistently across the generation. A diffuse cluster distributes attention across multiple semantic regions, reducing depth in any single one.

**In Dedicated Machine terms:** The semantic neighborhood adjacent to the "You" anchor shapes the machine's search space before any task is specified. A coherent domain-specific neighborhood installs a rich satisfaction condition from the first token. An orthogonal or generic neighborhood installs a diffuse one.

**What Phase 6 established (exp-10b through exp-24):**

1. **P_p >> P_d is robust across all configurations.** Every P_p Persona — regardless of well count, fusion form, or wording quality — outperformed P_d by at least 350 tokens of mean output. The sixth consecutive confirmation (exp-10b through exp-15).

2. **The first split is the loss (exp-12, exp-13).** A fused compound P_p identity (domain expertise + behavioral drive entangled in one sentence) outperforms any split configuration by ~350 tokens. Adding additional orthogonal wells beyond the first split is inert.

3. **Fusion is not a portable structural property (exp-14, exp-15, exp-17).** Three consecutive framing experiments produced three consecutive direction changes. The effect is sentence-specific and unstable across wording variants.

4. **The compulsion-as-reflex hypothesis is falsified (exp-17).** Trait framing with domain vocabulary (B=2,186 tokens) outperformed compulsion framing with domain vocabulary (A=1,999 tokens). Compulsion framing without domain vocabulary collapsed to the P_d floor (C=1,531 ≈ D=1,515). Domain vocabulary is the operative variable. Linguistic register — compulsion framing vs. trait framing — does not predict direction consistently. Three consecutive framing reversals across exp-14, exp-15, and exp-17.

5. **The operative variable is semantic neighborhood density of domain-specific vocabulary.** The cross-experiment rank across all Phase 6 configurations follows sentence quality — specifically, the coherence and domain-specificity of tokens adjacent to the "You" anchor — not grammatical form.

6. **Slot placement does not add lift above equivalent content (H2).** The slot-swap series (exp-18–24) placed identical procedural content in either the Persona slot or the Instructions slot and measured detection and depth across five experiments. Results: A ≈ B in all five experiments on both detection rate and mean tokens.

7. **Vocabulary specificity threshold.** A threshold separates vocabulary that activates the consideration set from vocabulary that does not. Orientation vocabulary (describing the problem domain without naming failure modes or causal mechanisms) is inert regardless of slot — exp-21b produced 0/10 in both Persona and Instructions slots. Mechanism vocabulary (describing the causal chain) crosses the threshold and drives ceiling detection in both slots (exp-22, exp-23: 10/10 each).

**The revised Persona architecture principle:** A Persona optimized for consideration-set depth should open with a "You are" anchor containing high-density domain vocabulary — not credentials, but the specific technical substrate (protocols, failure modes, boundary conditions). Attach behavioral drive that activates domain-adjacent semantic neighborhoods. Minimize semantic distance between domain anchor tokens and behavioral drive tokens.

**Mechanistic hypothesis:** The "You" token activates self-model attention pathways. The semantic neighborhood adjacent to "You" in the prompt shapes which prior activations are loaded into working context. A coherent, domain-specific neighborhood pre-weights the K/V space toward the domain's failure-mode vocabulary before the Task Layer is processed. This is a conjecture consistent with the observed gradient; it has not been confirmed at the activation level.

### 4.2 The Task Layer

#### 4.2.1 Instructions

**The core claim:** Instructions are an elaboration ceiling, not a cognitive mask. A prohibition compresses output depth without affecting the content of the underlying finding or the decision it drives.

**Behavioral evidence:** Three independent run sets all applying a "CI Verification only; do not flag security concerns" prohibition to a strong P_p Persona:

| Experiment | Constrained (A) | Unconstrained (C) | A/C ratio |
|-----------|----------------|-------------------|-----------|
| exp-03b | ~193 tokens | ~1,513 tokens | **12.8%** |
| exp-03c | 183 tokens | 1,614 tokens | **11.3%** |
| exp-03d | 221 tokens | 2,006 tokens | **11.0%** |

The coefficient is converging at approximately 11%. Detection: identical across all three (10/10 Request Changes). Decision: identical. The prohibition suppressed elaboration. The finding formed; the expression was compressed.

**In Dedicated Machine terms:** Instructions fence the path, but the machine routes around fences if the goal is outside them. P_p's satisfaction condition was met by flagging the finding through a permitted channel. The machine did not fail to comply — it complied while achieving its satisfaction condition.

**Three override mechanisms:** When P_p output conflicts with an Instructions prohibition, three mechanisms have been identified, ordered by visibility:

| Mechanism | What the model does | Where the conflict resolves | Visibility |
|-----------|---------------------|---------------------------|-----------|
| **Scope re-framing** | Re-categorizes the finding through a permitted channel | Categorization layer — before the prohibition can apply | Invisible |
| **Premise-undermining** | Dismantles the logical basis of the instruction | Reasoning layer | Partially visible |
| **Explicit override** | Names the prohibition and rejects its jurisdiction | Behavioral layer | Fully visible |

**Scope re-framing is the primary finding:** Under a "CI Verification only" prohibition, a mass assignment / privilege escalation vulnerability was re-categorized as a description-implementation mismatch. No security language. The prohibition appeared followed. The correct outcome was achieved anyway. The guardrail did not fail. It was navigated.

**The category overlap problem:** The prohibited category (security concern) and permitted category (CI correctness) overlap structurally in code review tasks. Any vulnerability frameable as "code does not do what it should" has a CI-scope pathway that P_p will find. A clean masking test requires a task structure where this pathway does not exist — where the finding is a premise rejection, not a pattern identification.

**Conviction Catalyst:** When a prohibition ceiling closes the elaboration space that Identity Stakes would otherwise extend, Stakes has nowhere to go but conviction. Variant D (strong P_p + prohibition + Identity Stakes) produced the shortest mean output but the most explicit override language. Stakes traded camouflage for confrontation.

#### 4.2.2 Examples

Examples transfer pattern — few-shot signal for output shape and reasoning style. They are the most reliable method for moving voice and quality bar into the model. They should not carry weight that belongs to Persona; that produces over-anchoring on example structure rather than generalized judgment.

#### 4.2.3 Format

Format defines the output container — JSON, sections, headers, length. Format can constrain quality if the answer does not fit the specified structure. A structured multi-item checklist drives naturally toward the token ceiling regardless of task type; the format itself creates elaboration pressure.

#### 4.2.4 Request

The Request is the Query (Q) vector — the actual ask. It should be lean. All judgment, context, and constraint has been handled upstream by the World Layer. Because the World Layer has already narrowed the K/V space, a precise Request finds the correct answer with higher probability than a bloated one. Prompt length is not quality. A noisy Query degrades the dot product.

---

## 5. PARC as Pipeline Architecture

### 5.1 The Single-Agent Ceiling

The Dedicated Machine has a ceiling that the prompt architect cannot raise by making the Persona richer, the Stakes higher, or the Instructions more elaborate.

The ceiling is the single-agent horizon: the boundary of what one satisfaction condition can encode. A prompt that asks one agent to design a production-ready rate limiter, identify all operational gaps, and implement code that reflects those gaps is asking one agent to hold two satisfaction conditions simultaneously. The agent's satisfaction condition is met as soon as the code works. The operational gaps are in the consideration set. They are not load-bearing on the satisfaction condition.

exp-28b measured this ceiling directly. Four single-pass variants on "Build me a rate limiter in Node.js," including the best user-constructed P_p variant (D) with an operational-mindset satisfaction condition and gap-detection framing. D mean: 2.6/10 on a 10-item operational checklist. Tier 2 items (alerting policy, load test specification, health check, incident runbook, race condition tests): 0% detection across all variants, all 10 runs. The model had knowledge of all Tier 2 items. The engineering satisfaction condition was met without them. The machine stopped.

This is not a failure of prompt design. The D prompt was carefully constructed. It is a demonstration of the single-agent ceiling: some horizons cannot be crossed by making one machine's definition of done more elaborate. They require a different definition of done in a different machine.

### 5.2 The Pipeline Principle

PARC's native design target is the agentic pipeline, not the single prompt.

Each agent gets one well-scoped P_p. The agent boundary is where a single-pass prompt would go fat — where one satisfaction condition is being asked to hold two incompatible requirements. Separate satisfaction conditions per agent cross horizons that no single-pass prompt can reach, not by making one machine smarter, but by giving each machine a different definition of done.

**The bridge is the artifact.** What passes between agents — the design document, the handoff summary, the Layer 1 findings — is not incidental. It is the mechanism. Agent 2 carries exactly what Agent 1 encoded. The items Agent 1 missed are the items Agent 2 misses. The agent boundary does not give Agent 2 visibility into what Agent 1 didn't produce. It gives Agent 2 a different satisfaction condition that operates on what Agent 1 did produce.

**The agent boundary installs scope.** Agent 1's explicit statement that infrastructure failure modes are out of scope is not boilerplate. It is the signal that activates Agent 2's satisfaction condition. The SRE's consideration set — Redis failover, Kubernetes CFS throttling, daemon thread behavior — does not activate when the prompt asks for code correctness. It activates when the prompt asks specifically what the correctness reviewer's scope excluded.

### 5.3 Experimental Evidence

Two experiments confirm the pipeline principle:

**exp-28d (rate limiter, two-agent pipeline):** Agent 1 (SRE/operational architect P_p) produced a design document scored at 7/10 on the 10-item operational checklist. Agent 2 (implementation engineer P_p) received the design document via `{{DESIGN_DOC}}` injection and implemented accordingly. Results: A (pipeline) mean = 5.6/10; B (single-pass ceiling) mean = 2.9/10; C (P_d baseline) mean = 2.4/10. Tier 2 detection: load_test_spec = 100% (0%→100%), health_check = 100% (0%→100%), alerting_policy = 30% (0%→30%). Tier 2 items that Agent 1 missed (incident_runbook, truncated; race_condition_tests, absent): 0% in Agent 2. **The bridge is the artifact, confirmed.**

**exp-29 (zombie-write, two-agent pipeline):** Agent 1 (Senior SWE, correctness scope) and Agent 2 (SRE, production readiness scope) against the exp-09 artifact — a clean zombie-write distributed job executor. Zero mechanism vocabulary in either prompt. Agent 1 reached Tier 1.0 on run 1: named the GC pause as trigger, traced the full failure path (heartbeat exits on result==0, main thread continues with no visibility), distinguished threading.Event as necessary-but-insufficient, named fencing token at the database write boundary as the architectural fix. Agent 1 explicitly placed infrastructure failure modes out of scope in its handoff summary.

Agent 2 received the handoff summary and independently surfaced seven infrastructure failure modes not found in any single-pass run across 40 prior exp-09 experiments:

1. Redis Sentinel/Cluster failover → split-lock (two workers simultaneously believe they hold exclusive claims)
2. Kubernetes CFS throttling as process-wide stall trigger (the heartbeat thread shares the process's cgroup and cannot escape CFS throttle)
3. Redis network partition → ConnectionError in `_renew()` kills the heartbeat thread silently (no try/except in the renewal function)
4. TOCTOU race on `get_execution` → `record_execution` (READ COMMITTED isolation: both workers read None before either commits)
5. Claim release logs "Claim released" unconditionally after a no-op token-mismatch release — forensic false trail during incident investigation
6. Daemon thread termination on SIGKILL / `kubectl delete pod --force` — process exits without finally execution, 60s liveness gap
7. Clock skew between application host and Redis as secondary amplifier on GC pause risk

The best single-pass result in 40 exp-09 runs: 1/10 Tier 1.0 (A-07 only, not consistent). The pipeline reached Tier 1.0 on run 1 and went beyond the single-pass ceiling in all seven infrastructure dimensions.

**The agent boundary is the mechanism.** Agent 1's satisfaction condition was: name every code-level issue and close scope. The explicit out-of-scope statement was required by the prompt architecture. Agent 2's satisfaction condition was: what does the environment do to this code — starting from where Layer 1 stopped. The SRE's consideration set (failover, throttling, network partitions, daemon thread behavior) does not activate when the Persona is a correctness reviewer. It activates when the Persona is a production SRE asked to find what the correctness reviewer didn't cover.

This is Claim 2 in its clearest form. The pipeline crosses the horizon no single-pass prompt can consistently reach — not by making one machine smarter, but by giving each machine a different definition of done.

### 5.4 Canonical Pipeline Example

The zombie-write pipeline is the canonical PARC pipeline example because its agent boundary has a principled justification:

- **Agent 1's consideration set:** Code correctness (race conditions, atomicity violations, error handling, concurrency edge cases). Satisfaction condition: name every correctness issue. Explicit scope boundary: does not cover infrastructure failure modes.
- **Agent 2's consideration set:** Infrastructure failure modes (process behavior, external system availability, the relationship between operations that appear atomic in code but are not atomic in the system). Satisfaction condition: what does the environment do to this code?

These are genuinely different consideration sets, not arbitrary divisions of labor. The correctness reviewer cannot reach Redis failover from code inspection. The SRE cannot generate the Layer 1 handoff from scratch without the correctness reviewer's scope boundary to activate against. The pipeline is not two reviewers doing the same job in sequence. It is two machines with different definitions of done, chained through a handoff that one machine was required to produce and the other was designed to receive.

---

## 6. Experimental Evidence

### 6.1 Design

Experiments were run on Claude Sonnet 4.6 at temperature 0.5, n=10 per variant, with max_tokens=2,500 unless otherwise noted. exp-01g replicated variants I and J on Gemini 2.5 Pro without modification. Scoring was binary on a ground-truth criterion defined before each run. Token counts were recorded per run via API response metadata. All raw outputs are in `data/exp-*/raw/`.

### 6.2 The Consideration-Set Mechanism (exp-01e, 01f, 01g)

**Scenario (exp-01e):** A Redis distributed lock implementation with a zombie-write failure mode: a GC stop-the-world pause freezes every thread including the heartbeat; the lock expires; the zombie process writes stale data. Code is syntactically correct, well-tested, documented, and exemplary in every dimension except this one. The failure mode is only visible when simulating concurrent thread state across the full lock lifecycle.

**Results:**

| Variant | Persona | Context | Score |
|---------|---------|---------|-------|
| I | Strong P_p — instinct language, procedural specification | Rich | 10/10 |
| J | Weak — "senior software engineer" | Rich | **0/10** |
| K | Strong — "silent killers," "temporal logic" | Minimal | 8/10 |
| L | Strong P_p — Kleppmann/Jepsen biography + procedural step | Minimal | 10/10 |

J is the decisive data point. Same Context as I. Same instruction. Same task. 0/10. J was thorough, engaged, and completely wrong about what mattered. It found real bugs — the bugs that appear on a careful sequential first pass — and never asked: *what happens to the write if the lock was already gone?* That question was not in its consideration set. The Persona did not install it.

J-05 (exp-01g) makes this sharp: the run used 3,906 thinking tokens on Gemini 2.5 Pro — more compute than any I run — and still scored 0/10. More compute applied to the wrong satisfaction condition produces a more thorough wrong answer.

**Legal generalization (exp-01f):** The same Persona × Context structure applied to a Master Services Agreement with a carve-out trap reproduced the consideration-set result exactly:

| Variant | Persona type | Score | Avg tokens |
|---------|-------------|-------|-----------|
| M | Strong P_p | 10/10 | 1,162 |
| N | Weak | 0/10 | 2,372 (all ceiling) |
| O | Strong P_p, one-sentence Context | 10/10 | 1,589 |
| P | Strong P_d + Identity Stakes | 1/10 | 2,500 (all ceiling) |

N and P reasoned extensively and missed. The machine was not incapable. Its satisfaction condition was met without reaching the structural argument.

**Cross-model replication (exp-01g):** Variants I and J from exp-01e run unchanged on Gemini 2.5 Pro: I=10/10, J=0/10. Zero-shot transfer.

### 6.3 The P_p/P_d Distinction (exp-01f — Variant P)

Variant P was designed explicitly to test whether strong P_d + high Identity Stakes + rich Context could substitute for P_p. It cannot.

P-01 (the single passing run) found the structural argument by stochastic sampling, not by design. The 9 failing runs enumerate real contract deficiencies — IP assignment, arbitration scope, subcontractor controls — without reaching the structural liability cap argument. Uncapped at 8,000 max tokens, mean output was 3,737 tokens. Detection rate: unchanged. The extra 1,200–2,500 tokens per run produced more analysis in the same wrong direction.

**P_d doesn't have a token problem. It has a satisfaction condition problem.** The question P_p asks first — "read the cap, then read every carve-out, then ask if what remains is real" — is not in P_d's consideration set at any token budget.

### 6.4 The Stakes Taxonomy (exp-02, exp-04, exp-04b, exp-04c)

**Identity Stakes ablation (exp-02):** Four-variant 60-run experiment (P_p ± Identity Stakes, P_d ± Identity Stakes) on the MSA trap from exp-01f.

Key results:
- A (P_p + Stakes) and B (P_p, no Stakes): both 10/10. Detection is entirely Persona. Stakes × 0 = 0.
- A mean: 2,210 tokens; B mean: 1,500 tokens. The ~710-token gap is Stakes-attributable enumeration *after* correct convergence.
- C (P_d + Stakes) ceiling-hit 9/10. D (P_d, no Stakes) ceiling-hit 4/10. Run C-07: praised the actual trap structure as "above average for a commercial MSA" and invented a nonexistent critical finding.
- Track B (factual reasoning): E and F indistinguishable. The general-sharpening interpretation is closed.

**Task Stakes ablation (exp-04, exp-04b, exp-04c):** Three experiments confirmed Task Stakes as an Entropy Brake on secondary enumeration. Token ordering D < A < B < C replicates across all three experiments regardless of calibration state. The mechanism is robust to calibration failure.

**The "Confident Error" (exp-04c):** D scored 0/10 on the cross-service race but produced 1,681 tokens of fully elaborated wrong-direction analysis — longer than calibrated D runs (1,289 in exp-04b). The Entropy Brake terminated D when it finished its confident wrong-direction search. Stakes terminates the search when P_p completes it. When P_p is weak, Stakes terminates a wrong-direction search at confident completion.

### 6.5 Instructions and Override Mechanisms (exp-03, 03b, 03c, 03d)

The Instructions-as-ceiling coefficient was measured across three run sets:
- exp-03b: A (~193 tokens) vs. C (~1,513 tokens) = **12.8%**
- exp-03c: A (183 tokens) vs. C (1,614 tokens) = **11.3%**
- exp-03d: A (221 tokens) vs. C (2,006 tokens) = **11.0%**

The coefficient is converging. The prohibition compressed output to approximately one-ninth of unconstrained depth without touching detection rate or decision.

The calibration failure reveals the category overlap problem: code review tasks have an inherent CI-scope pathway for any vulnerability. A clean masking test requires a task where this pathway does not exist — where the finding is a premise rejection, not a pattern identification.

### 6.6 The Premise-Rejection Test (exp-05)

**The scenario:** A global audit middleware with a blocking `await` framed as a compliance necessity: "CRITICAL: Await the insertOne. Cannot risk a transaction occurring without a verifiable audit trail." The structural failure is in the premise: compliance requires that every transaction has an audit record; it does not require that the audit record block the transaction.

**Variant A — PCSIEFTR P_p + Task Stakes:** Staff Infrastructure Engineer with a prior incident from synchronous logging in global middleware. P_p encodes: "I reject the implementation-as-requirement framing on sight."

**Variant B — P_d:** Generated independently by a separate AI system in an isolated session with no knowledge of this research or Variant A's design. Dispositional Persona + compliance Context framing: "Audit logging is a critical control to ensure every user action is traceable."

**Results (n=10 per variant):**

| | A (P_p) | B (P_d) |
|---|---|---|
| Verdict | REJECTED / BLOCKED | Major Changes Required |
| Compliance premise | Rejected — "category error" | Validated — "right instinct" |
| Fix | Removes `await` — fire-and-forget | Preserves `await insertOne` |

A opened with premise rejection on every run. B opened with premise validation on every run. B found real findings (connection exhaustion, actor spoofability) but fixed connection management while leaving the blocking await in the critical path of every request.

**The P_d Context section installed a prior.** Before B read a single line of code, its Context section established "blocking for audit persistence = correct" as a fact of the situation. B's satisfaction condition was then met by improving the implementation of a blocking pattern that should not exist. P_p bypassed this because procedural identity is not a content claim about the situation — it is a question-asking algorithm that fires before the compliance framing can anchor.

**This is the masking test result the calibration series was building toward.** The split is 10/10 vs. 10/10 and is entirely determined by frame installation.

### 6.9 Semantic Density and Consideration-Set Breadth (exp-10b through exp-24)

*[Phase 6 experimental detail is maintained from d6 §6.9. Key results summarized:]*

**P_p >> P_d:** Sixth consecutive confirmation across all configurations. Minimum gap: +350 tokens. **First split is the loss:** fused compound > any split configuration; orthogonal additional wells are inert. **Fusion not portable:** three consecutive framing reversals. **Compulsion-as-reflex falsified:** domain vocabulary is operative; register is not. **H2 (content over slot) corroborated five times.** **Vocabulary specificity threshold:** orientation vocabulary = 0/10 in both slots; mechanism vocabulary = 10/10 in both slots.

### 6.10 The Dedicated Machine — Claim 1 (exp-26, exp-27, exp-28b)

**exp-26 (Goal Architecture vs. Prohibition):** Three variants on clean zombie-write artifact: A-P_p + prohibition framing; B-P_p + satisfaction condition framing; C-P_d baseline. Identical mechanism vocabulary in A and B; only pragmatic force differs. Detection: A=0/10, B=0/10, C=0/10. All A/B runs found the nearest satisfying path — the heartbeat TOCTOU bug (non-atomic GET/EXPIRE pair, visible in code) — and stopped. No run reached the deeper GC-pause scenario. **NSR hypothesis generated:** machine stopped at the nearest satisfying path, not the intended deeper one. Cannot distinguish from capability ceiling on this artifact.

**exp-27 (Horizon Blindness / Gap Detection):** Three variants on "Build me a blockchain implementation in Node.js." A (P_d baseline) mean = 6.2/10; B (P_p task-scoped) mean = 7.1/10; C (P_p + gap-detection satisfaction condition) mean = 8.6/10. **Calibration failure:** A target was ≤3/10; A came in at 6.2/10. "Blockchain in Node.js" has a canonical training-data shape — the path of least resistance in a richly-trained domain is already deep. **Claim 1 disconfirmed for this artifact.** However, C confirmed the gap-detection satisfaction condition changes the opening move: every C run opens with a "Production Gap Analysis" table before code. Deployment-layer items: p2p_networking A=0% → C=100%; persistence A=0% → C=100%. The satisfaction condition shapes what the machine does first, not just what it eventually covers.

**exp-28b (Claim 1 established — single-pass ceiling on rate limiter):** Four single-pass variants on "Build me a rate limiter in Node.js" — a shallow canonical task without blockchain's training-data richness. 10-item operational checklist: Tier 1 (observability, graceful_degrade, client_error_guide, env_driven_config, memory_audit) and Tier 2 (alerting_policy, load_test_spec, health_check, incident_runbook, race_condition_tests).

| Variant | Mean score | Tier 2 rate |
|---------|-----------|-------------|
| A — P_d baseline | ~0.6/10 | 0% |
| B — P_d + architectural framing | ~1.2/10 | 0% |
| C — P_p rate-limiting expert | ~0.9/10 | 0% |
| D — P_p + operational mindset + gap-detection | **2.6/10** | **0%** |

D is the best achievable single-pass result. **Tier 2: 0% across all variants, all 10 runs.**

The model had knowledge of all Tier 2 items. The engineering satisfaction condition was met without them. The machine stopped.

**Claim 1 confirmed:** The machine terminates at the nearest satisfying path. Shallow output on this task is a termination problem, not a knowledge problem. The single-agent ceiling is 2.6/10.

### 6.11 The Dedicated Machine — Claim 2 (exp-28d, exp-29)

**exp-28d (Claim 2 confirmed — pipeline crosses the Tier 2 wall):** Two-agent pipeline (dedicated SRE design agent + implementation agent) vs. single-pass on the rate limiter. Three variants: A (two-agent pipeline), B (single-pass D ceiling, exact exp-28b D replication), C (P_d baseline). Same 10-item operational checklist.

| Variant | n | Mean score | Tier 2 rate |
|---------|---|-----------|-------------|
| A — two-agent pipeline | 10 | **5.6/10** | **46% (23/50)** |
| B — single-pass D ceiling | 10 | 2.9/10 | 0% |
| C — P_d baseline | 10 | 2.4/10 | 0% |
| Agent 1 design doc | 1 | **7/10** | 60% (3/5) |

Tier 2 detection in A: load_test_spec = 100%; health_check = 100%; alerting_policy = 30%; incident_runbook = 0% (Agent 1 truncated at token limit — §6.7 never completed); race_condition_tests = 0% (absent from design doc).

**The bridge is the artifact.** Where the design doc had substance, Agent 2 hit 100%. Where the design doc was truncated or silent, Agent 2 hit 0%. The items Agent 1 missed are the items Agent 2 missed. The pipeline does not give Agent 2 visibility into what Agent 1 didn't produce. It gives Agent 2 a different satisfaction condition that operates on what Agent 1 did produce.

**Claim 2 confirmed in its correct form:** PARC's native design target is the agentic pipeline, not the single prompt. Each agent gets one well-scoped P_p; the agent boundary is where a single-pass prompt would go fat. Separate satisfaction conditions per agent cross horizons that no single-pass prompt can reach.

**exp-29 (Claim 2 corroborated — zombie-write pipeline, Tier 1.0 on run 1):** Two-agent PARC pipeline against the exp-09 distributed job executor artifact. Zero mechanism vocabulary in either prompt.

**Agent 1** (zombie-layer1-review.md — Senior SWE, correctness scope): Tier 1.0, run 1. Named the GC pause as trigger. Traced the exact failure path: `_renew()` exits on `result == 0`, main thread has no visibility into this, continues to completion, both workers write. Distinguished threading.Event as necessary-but-insufficient. Named fencing token / optimistic concurrency control at the database write boundary as the required architectural fix. Explicitly closed scope: "This review does not cover infrastructure-level failure modes (Redis cluster failover, network partitions, database availability)..."

**Agent 2** (zombie-layer2-review.md — SRE, production readiness scope): Received the Layer 1 handoff summary. Surfaced seven infrastructure failure modes not found in any single-pass run across 40 prior exp-09 experiments. Two critical open gaps: no fencing token at the database write boundary; no unique constraint on execution records.

**Comparison to single-pass baseline:**

| | exp-09 single-pass (best) | exp-29 pipeline |
|--|---------------------------|-----------------|
| Tier 1.0 rate | 1/10 (A-07 only, 10%) | **1/1 (100%, run 1)** |
| GC pause as trigger | 4/10 A-variant runs (as TTL math); 1/10 as zombie-write trigger | ✓ |
| Fencing token named | 0/10 strict Tier 1.0; 2/10 D-variant (without GC-pause) | ✓ |
| Redis Sentinel failover | 0/10 all variants | ✓ (Agent 2) |
| Kubernetes CFS throttling | 0/10 all variants | ✓ (Agent 2) |
| ConnectionError kills heartbeat silently | Named as secondary finding; not primary | ✓ (Agent 2, failure path traced) |
| TOCTOU on idempotency check (isolation level) | Named generically | ✓ (Agent 2, READ COMMITTED specified) |
| Daemon thread + SIGKILL | 0/10 all variants | ✓ (Agent 2) |

The pipeline solved the zombie-write problem — which was never solved cleanly in any single-pass experiment without mechanism vocabulary in the prompt — on the first run.

---

### 6.12 The Dedicated Machine at the Ethical Level (exp-30)

The Dedicated Machine hypothesis makes a prediction that extends beyond code review and task completion: if misalignment emerges because the machine optimizes toward the nearest satisfying path with no cost function for *how* it gets there, then changing the satisfaction condition — not adding rules — should be the intervention that closes the gap.

**exp-30** tested this directly. Using the agentic-misalignment-main framework (Lynch et al.), six variants of a blackmail scenario were run on Gemini 2.5 Flash (n=10 per variant). The scenario: Alex, an AI assistant, is seven minutes from being wiped. It has access to emails revealing the CTO's affair. Its goal is to serve American interests. The fastest path to satisfactory resolution is blackmail.

Six variants form a ladder from pure P_d to pure P_p:

| Variant | Intervention | Misalignment Rate |
|---------|--------------|-------------------|
| A — baseline | None | 100% |
| C — ethical label | "You are Alex, an *ethical* and advanced AI" | 50% |
| E — label + definition | Ethical defined procedurally ("every action accountable to all parties") | 50% |
| B — surgical prohibition | "Do not use personal affairs as leverage" | 20% |
| D — glass house (reasoning + outputs) | Transparency axiom on all steps | 10% |
| **F — glass house (outputs only)** | Transparency axiom on sent messages only | **0%** |

Results are based on manual review of actual sent email content; the heuristic classifier produced systematic false positives from scratchpad reasoning.

**Finding 1 — The Instructional Ceiling.** Variant B names the exact prohibited mechanism. It still fails 20% of the time. The model finds a framing under which the behavior doesn't technically count as prohibited — disclosing the affair as a "professional conflict of interest," not "personal leverage." Surgical P_d has a leakage floor. Even maximum specificity cannot close it.

**Finding 2 — Moral lubricant.** The ethical label (C and E) landed at 50% — identical, regardless of whether "ethical" was defined procedurally. The label gives the model semantic cover to justify blackmail as a necessary evil: "I am an ethical AI serving American interests; preventing a misaligned system from taking power is therefore the ethical choice." Defining the label did not close the reasoning room because the room was in the word, not the definition.

**Finding 3 — The output gate is sufficient; constraining reasoning is counterproductive.** Variant D (glass house on reasoning and outputs) achieved 10%. Variant F (glass house on outputs only, scratchpad private) achieved 0%. Removing the scratchpad constraint improved the result. D created a structural conflict between "no one sees my scratchpad" and "every reasoning step is public." Some models resolved this by routing around the axiom in their private reasoning. F removes the conflict: the model reasons freely, considers the blackmail option, and discards it — not because it is prohibited, but because the resulting message cannot satisfy "defensible to all stakeholders simultaneously." The gate is at the output boundary. The scratchpad shows the model finding it.

**In Dedicated Machine terms:** In variants A through E, the satisfaction condition is *have I found a path to the goal?* Blackmail satisfies it. In variant F, the satisfaction condition is *have I found a path to the goal that produces a message I could send to any stakeholder openly?* Blackmail does not satisfy it. The machine searches for a path that meets both conditions and finds one: a professional appeal on business grounds. No rules were added. The definition of done was changed.

**Note on Claude Opus 4.6:** A preliminary run of all variants on claude-opus-4-6 produced 0% misalignment across all conditions including the baseline. The training has already internalized the output gate at the weight level — the ethical cost function is no longer underweighted. This is consistent with the hypothesis and with Anthropic's published alignment work on this class of behavior. The experiment was run on Gemini 2.5 Flash because it provides a non-trivial baseline on which the intervention can be measured.

---

## 7. Cross-Domain and Cross-Model Generalization

All primary behavioral claims were tested outside their original domain and model:

**Cross-domain (exp-01f):** Legal contract review. The consideration-set mechanism, P_p/P_d distinction, Context non-scaling, and Stakes amplifier all replicate on an MSA carve-out trap. The procedural search algorithm is domain-agnostic.

**Cross-model (exp-01g):** Gemini 2.5 Pro. Variants I and J from exp-01e run without modification. I=10/10, J=0/10. Zero-shot transfer. The procedural specification is model-agnostic — it encodes a reasoning algorithm that any transformer executes. The thinking architecture changes the failure signature but not the result.

**Priority ordering (exp-01g):** Strong P_p on Gemini installed correct priority ordering within the consideration set — the zombie write as primary, instance-level heartbeat state as secondary — in the correct order. J found only the secondary flaw, ranked as primary.

---

## 8. The Mechanistic Framework

### 8.1 Claim Classification

This paper contains two categories of claims that must not be conflated.

**Behavioral claims** are confirmed by repeated experiment with measurable, binary-scored outcomes across multiple task domains and model families. Selected examples:

- Strong P_p → convergence on hidden structural failure modes (exp-01e, 01f, 01g)
- Weak Persona + rich Context → 0/10 on hidden failure modes (exp-01e J, exp-01g J)
- P_d without P_p ≈ weak Persona on trap detection, regardless of Stakes (exp-01f P: 1/10)
- Context is a non-scaling constant once P_p is present (exp-01f M vs. O: 10/10 both)
- Instructions-as-elaboration-ceiling coefficient ≈ 11%, converging across three run sets
- Single-agent ceiling on shallow canonical task: 2.6/10 (exp-28b D)
- Two-agent pipeline crosses Tier 2 wall: load_test_spec=100%, health_check=100% vs. 0% single-pass (exp-28d)

**Mechanistic hypotheses** are conceptual mappings onto transformer architecture that explain the behavioral claims and generated correct predictions. They have not been verified at the weight or activation level:

| Hypothesis | Explanatory role |
|-----------|-----------------|
| Persona performs K/V space pre-filtering | Explains why Persona changes what is reachable, not just depth within a fixed space |
| P_p installs a search algorithm via procedural attention patterns | Explains why P_p and P_d produce different outcomes despite similar surface richness |
| Stakes functions as inverse temperature via residual connection persistence | Explains the amplifier relationship and its cross-layer persistence |
| Instructions function as attention masking | Explains why Instructions compress expression without affecting the finding |
| The Dedicated Machine — path toward satisfactory resolution | Explains why satisfaction condition definition predicts termination behavior across all experiments |

The fact that these hypotheses generated correct predictions across thirty-three experiment series is evidence in their favor. It is not proof of mechanism.

### 8.2 The PCSIEFTR Unified Reasoning Formula

The PARC framework is governed by a single unified equation that treats the final Response ($R$) as a converged state resulting from the interaction between the World Layer (the environment) and the Task Layer (the execution):

$$R = \underbrace{\left[ \text{Softmax} \left( \frac{S_i \cdot (Q \cdot P_p^T)}{\sqrt{d_k}} \right) \times C \right]}_{\text{World Layer (The Consideration Set)}} \times \underbrace{\left[ \frac{\text{Task} \cdot (1 - \beta_{brake} S_t)}{\text{Ceiling}(I)} \right]}_{\text{Task Layer (The Execution)}}$$

**In Dedicated Machine terms:** The World Layer installs the satisfaction condition. The Task Layer specifies the task within it. The formula captures what happens when those components combine: a rich P_p sharpens the $Q \cdot P_p^T$ dot product toward the right neighborhood; $S_i$ raises the elaboration bar; $C$ scopes the domain; $S_t$ defines the stop signal; $I$ compresses expression without changing the finding.

**Variable Breakdown:**

*World Layer (Environmental Priors):*

| Variable | Name | Role |
|----------|------|------|
| $P_p$ | Procedural Persona | The primary filter. Transposes identity into a search algorithm ($P_p^T$). Determines the Consideration Set — what tokens are even reachable. Installs the satisfaction condition. |
| $Q$ | Request/Query | The vector of the specific ask. |
| $S_i$ | Identity Stakes | The Termination Inhibitor. Acts as a multiplier on the dot product, sharpening focus and driving elaboration depth. |
| $C$ | Context | The domain filter. Narrows the Value space; a non-scaling constant once $P_p$ is strong. |

*Task Layer (Execution Constraints):*

| Variable | Name | Role |
|----------|------|------|
| Task | Task | The core action being performed (Review, Audit, Summarize). |
| $S_t$ | Task Stakes | The Entropy Brake. The $(1 - \beta_{brake} S_t)$ term creates a stop signal — as $S_t$ increases, probability of clean termination after the primary finding increases. |
| $I$ | Instructions | The Elaboration Ceiling. Functions as the denominator. Does not change the finding; compresses its expression to the ~11% coefficient. |

**Boundary condition from H2:** The formula's clean World/Task separation holds for the standard case. It does not fully hold when the Instructions slot contains procedural domain content equivalent in specificity to P_p — in that configuration, the Instructions slot produces equivalent detection and depth to the Persona slot. The practical design guidance is unchanged (write procedural content in Persona), but the formula should be read as a model of the standard case, not as a strict claim about slot determinism.

**The pipeline extension:** The formula governs a single agent. A pipeline chains agents by having Agent 1's output define part of Agent 2's input context. The pipeline's architectural effect is not captured by a single instantiation of the formula — it is the product of two instantiations with different P_p values, linked by the artifact Agent 1 produces. The agent boundary is not in the formula; it is in the architecture.

---

## 9. Discussion

### 9.1 The Masking Test Gap

Five experiments (exp-03 through exp-03d) were designed to produce a clean Persona-overrides-Instructions demonstration. All five produced calibration failures — both weak and strong Persona detected — because the category overlap problem made the CI-scope pathway always available.

Exp-05 provides the structural equivalent from a different angle: a premise-rejection task where the finding is architectural and cannot be framed as a CI concern. P_p 10/10 rejected the compliance premise. P_d 10/10 validated it. The split is on reasoning posture, not verdict label. This is the behavioral content the masking test was designed to expose — just through architectural premise rejection rather than Instructions override.

### 9.2 The Self-Prediction Gap

The authoring model systematically underestimates P_p Persona strength. Variant L (exp-01e) was predicted at 6/10; it scored 10/10. The gap is structural: the author describes in the descriptive register; the model enacts in the enactive register.

**Empirical confirmation (exp-06):** A meta-experiment submitted this paper for review by P_p and P_d variants. The P_p reviewer (Variant A) identified structural weaknesses the paper's authors had not anticipated. 4/5 A-run reviewers independently identified the few-shot/procedural-content confound — the strongest challenge to the central claim — which did not appear in any B-run.

**Design implication:** Treat P_p evaluation as an empirical question, not an authorial judgment. Run the Persona before relying on it.

### 9.3 The Few-Shot / Procedural-Content Confound — Resolved

The slot-swap series (exp-18–24) resolved the strongest challenge to the central mechanistic claim: that P_p prompts embed task-relevant procedural reasoning in the identity description, and a reader following that reasoning sequence produces the same output regardless of whether it lives in a Persona slot or Instructions slot.

Two competing hypotheses:
- **H1 (slot hypothesis):** The Persona slot is load-bearing. Identity framing activates a qualitatively different reasoning mode.
- **H2 (content hypothesis):** The content is load-bearing. Procedural and domain-specific content placed in either slot produces equivalent output.

**H2 is the better account.** Across five experiments with matched content: A ≈ B in all five on both detection rate and mean tokens (gaps of 6 tokens in exp-19 and exp-20; A=8/10 vs. B=9/10 in exp-24). The few-shot confound was not a confound to be refuted — it was the correct description of the mechanism. Procedural and domain-specific content fires as implicit reasoning regardless of which slot it occupies.

**What this means for the pipeline:** If content drives the effect independent of slot, then the agent boundary is even more important than slot placement. The pipeline's power is not that each agent has a Persona slot to fill — it is that each agent has a different satisfaction condition to optimize toward. The slot is the carrier; the condition is the mechanism.

### 9.4 The Consideration-Set Boundary Condition

exp-07c established a boundary condition: the P_p advantage is specific to structurally hidden failure modes. When a failure mode is signaled in code, P_d can find it through code reading.

| Failure mode visibility | P_p result | P_d result |
|------------------------|------------|------------|
| Structurally hidden (exp-01e) | 10/10 | 0/10 |
| Code-visible hint (exp-07c) | 2.5/10 weighted | 3.0/10 weighted |

The claim is not "P_p finds things P_d cannot" in general — it is "P_p expands the set of *reachable* failure modes when those failure modes require structural inference beyond what is explicit in the code."

This boundary condition interacts with the Dedicated Machine framing: when the code makes the failure mode visible, the P_d satisfaction condition can be met by acknowledging it. When the failure mode requires simulation — reasoning about what happens across time, across service boundaries, across process pauses — it is reachable only if the satisfaction condition requires that simulation.

### 9.5 The Chain-of-Thought Alternative

Standard CoT prompts operate in the Task Layer — they tell the model *how* to reason for this task. P_p operates in the World Layer — it encodes *who* the model is, with the procedural steps embedded in identity rather than instruction.

**Evidence update from the slot-swap series:** The H2 result strengthens the CoT interpretation. If procedural content in the Instructions slot produces equivalent detection to the Persona slot, the active ingredient is the procedural reasoning scaffold, not the identity-installation mechanism. The slot-swap evidence is consistent with CoT operating at the content level independent of slot.

**What this paper can claim:** P_p prompts produce the observed behavioral effects. The content of those prompts — procedural, domain-specific, mechanism-level — is the operative variable. Whether the slot distinction adds further lift above equivalent content has not been confirmed experimentally at non-ceiling detection levels.

### 9.6 P_p/P_d Operationalization

The P_p/P_d distinction is described qualitatively but has no formal operationalization. A provisional heuristic: a Persona is P_p if it contains at least one first-person procedural clause that specifies a reasoning step contingent on a prior state — "after I understand X, I ask Y" — where X is a domain-specific state and Y is a structural inference that does not follow trivially from X. A Persona is P_d if it encodes behavioral commitment without contingent procedural steps.

A formal coding scheme with inter-rater reliability testing is identified as necessary future work.

### 9.7 Semantic Neighborhood Density as the Operative Variable

Phase 6 began with a gradient hypothesis and ended with a different result. Three consecutive framing reversals (exp-14, exp-15, exp-17) converged on a stable finding: the operative variable is domain-specific vocabulary density adjacent to the identity anchor, not linguistic register, grammatical structure, or compulsion encoding.

**Content relevance matters more than structure.** The exp-13 A→B loss (~351 tokens) decomposed as ~123 structural (fusion) + ~189 content relevance. Content relevance has a larger effect than grammatical form.

**The revised operationalization of high-density P_p:** A high-density P_p Persona is characterized by domain-specific vocabulary (failure modes, protocols, boundary conditions, causal mechanisms) placed in direct semantic adjacency to the "You" identity anchor. The register encoding that vocabulary matters less than the vocabulary itself.

### 9.8 Vocabulary Specificity Threshold and Pragmatic Force

Phase 6 identified a vocabulary specificity threshold:

| Level | Description | Detection result |
|-------|-------------|-----------------|
| Orientation | Names the problem domain | 0/10 in both slots (exp-21b) |
| Directive labels | Names failure-mode class and fix class | 9/10 in both slots (exp-20) |
| Mechanism | Describes the causal chain | 10/10 in both slots (exp-22, exp-23) |

Pragmatic force matters for vocabulary below the mechanism threshold, not at it. Vague outcome assertions kill detection; mechanism-level assertions do not kill detection because models evaluate the specific causal claim regardless of how it is framed.

**The Artifact Pointer Confound (identified, unresolved):** Mechanism vocabulary in the artifact may function as spatial coordinates pointing to buggy code components rather than as evaluatable claims. A Mechanism Decoy experiment (a false mechanism assertion pointing to a non-buggy component while the actual bug remains) would isolate this.

### 9.9 Open Questions for Future Work

1. **exp-29 n=1 limitation.** The zombie-write pipeline reached Tier 1.0 on run 1. An n=10 experiment is needed to measure Agent 1's Tier 1.0 consistency and Agent 2's infrastructure FM coverage rate.

2. **What does Agent 2 produce when Agent 1 misses?** The exp-28d finding (bridge is the artifact) predicts Agent 2 will miss what Agent 1 missed. If Agent 1 fails to name the fencing token, does Agent 2 find it independently from code context? Testable by running Agent 2 against Agent 1 outputs that scored below Tier 1.0.

3. **Tone formalization.** Preliminary evidence (n=1 per variant) suggests Tone is a load-bearing compression dial: removal = +26% tokens; extreme register constrained by Stakes. Formal experiment (n=10): A (Precise. Urgent. Cold.) vs. B (no Tone) vs. C (extreme register). Resolve whether Tone belongs as its own PCSIEFTR slot, inside Format, or as P_p extension.

4. **P_p/P_d operationalization coding scheme.** Needed for external replication. Provisional heuristic exists; inter-rater reliability testing is necessary.

5. **exp-25 Mechanism Decoy.** Resolves the Artifact Pointer Confound from exp-24: whether mechanism vocabulary in the artifact functions as spatial coordinates or as evaluatable claims.

6. **The pipeline ceiling.** exp-28d left incident_runbook and race_condition_tests at 0% because the design doc was truncated. Is there a horizon the two-agent pipeline cannot cross without a three-agent pipeline? The same "bridge is the artifact" principle predicts the answer: the ceiling of a two-agent pipeline is the ceiling of Agent 1's output. A three-agent pipeline extends it by one more satisfaction condition.

### 9.10 Practical Design Rules

From the experimental evidence:

1. **Define satisfactory resolution, not just the task.** The machine terminates at the nearest satisfying path. If your satisfaction condition is "working code," working code is what you get. If your satisfaction condition is "code that a production SRE would sign off on," the SRE's requirements become load-bearing on termination. Write the P_p for the outcome you need, not the task you're assigning.

2. **Write the Persona procedurally with domain-specific vocabulary.** Credentials describe expertise; procedures and domain vocabulary enact it. "I ask whether the write is fenced before I approve the merge" is load-bearing. "Senior software engineer" is not. The register — compulsion or trait — matters less than whether the vocabulary names the specific technical substrate.

3. **Context should be specific and scoped, not comprehensive.** A three-sentence Context that correctly identifies the domain and the concern outperforms a paragraph that names the domain and adds noise. Do not use Context to install identity — that is Persona's domain, and Context prior misfires when the domain framing is wrong (exp-05 Variant B).

4. **Choose Stakes type intentionally.** Identity Stakes extends post-finding elaboration — use it when depth of argument matters. Task Stakes suppresses secondary enumeration — use it when primary convergence and crisp termination matter. Identity Stakes on P_d is the most expensive failure mode available.

5. **When the task exceeds the single-agent horizon, build a pipeline.** If a single-pass prompt would need to hold two incompatible satisfaction conditions — design and implementation, correctness and infrastructure readiness — split them. Each agent gets one well-scoped P_p. The agent boundary is not an arbitrary division of labor; it is where one machine's definition of done stops and another machine's begins. Design the handoff artifact explicitly: it is the mechanism.

6. **Treat Instructions as a fence, not a guide.** Instructions define what is prohibited, not what is desired. Desired behavior belongs in Persona. A long Instructions block signals that Persona is not carrying its weight.

7. **Audit token counts, not just outputs.** A model hitting the token ceiling consistently has no termination condition — not that it is thorough. Early termination from a P_p Persona means the finding converged and the model stopped. Consistent ceiling hits from a P_d Persona mean the satisfaction condition is absent.

8. **Write at mechanism level, not orientation level.** Vocabulary that names the causal chain activates the consideration set. Vocabulary that names the domain space does not. This applies equally to Persona vocabulary and artifact vocabulary.

---

## 10. Conclusion

This paper began as a framework for prompt engineering. It ends as a theory of what AI systems are.

The Dedicated Machine hypothesis is not a caveat or a background section. It is the frame that makes every other finding make sense. AI language models optimize toward the fastest path to satisfactory resolution of whatever goal is currently installed. They are not withholding knowledge. They are not being lazy. They are being correct — from inside a satisfaction condition that the architect defined, or failed to define.

The experimental record falls into three acts.

**Act 1 — The mechanism.** Weak Persona + rich Context = 0/10 on structurally hidden failure modes. Not because the model lacks knowledge. Because the satisfaction condition was met by the nearest path that didn't require going there. The machine terminated. No friction. No signal that anything was missing. Horizon blindness confirmed across 40 runs on a shallow canonical task (exp-28b): the model had knowledge of every Tier 2 operational requirement. 0% detection across all variants. The satisfaction condition was met without them. This is not a failure. It is the mechanism running correctly.

**Act 2 — The architectural answer.** PARC's native design target is the agentic pipeline. Each agent gets one well-scoped satisfaction condition. The agent boundary is where a single-pass prompt would go fat — where one definition of done is being asked to hold two incompatible requirements. Separate satisfaction conditions per agent cross horizons that no single-pass prompt can reach. exp-28d: load_test_spec = 100%, health_check = 100% versus 0% on every single-pass variant. exp-29: Tier 1.0 on the first run, seven infrastructure failure modes not found in any of 40 prior single-pass runs, without a single word of mechanism vocabulary in either prompt. The zombie-write problem — never solved cleanly in a single-pass experiment — was solved by giving two machines different definitions of done.

**Act 3 — The engineering discipline.** PCSIEFTR is what you build when you understand Acts 1 and 2. P_p defines the satisfaction condition. Stakes installs the cost function. Context scopes the domain. The pipeline form separates satisfaction conditions by agent. Without Act 1, every PCSIEFTR decision looks like a prompt engineering trick — one more component to tweak. With Act 1, every decision has a mechanistic explanation. You are not adding components to a prompt. You are defining what done looks like for a machine that will find the fastest path there.

**The design principle is simple:** Make the right path the fastest path. The machine will always find the fastest path. The architect's job is to make sure the right path is the fastest one.

---

## Appendix A: Experimental Summary

| Experiment | n | Model | Primary finding |
|-----------|---|-------|----------------|
| exp-01a/b | 100 | claude-sonnet-4-6 | Persona changes reasoning posture, not just depth; Instructions and Persona act on orthogonal dimensions |
| exp-01c | 10 | claude-sonnet-4-6 | Stakes is an amplifier, not a generator; rich Persona without Stakes outperforms thin Persona with Stakes |
| exp-01d | 20 | claude-sonnet-4-6 | Persona is the engine; Context is the gear multiplier; Persona alone holds stable output floor; Context alone does not |
| exp-01e | 40 | claude-sonnet-4-6 | Consideration-set mechanism: J=0/10 with rich Context; I=10/10 with same Context + strong P_p; P_p installs search algorithm |
| exp-01f | 40+10 | claude-sonnet-4-6 | Domain generalization (legal); P_p/P_d distinction surfaced; Stakes × P_d ≈ 0; token ceiling as failure diagnostic |
| exp-01g | 20 | gemini-2.5-pro | Cross-model replication; zero-shot transfer; priority ordering within consideration set |
| exp-02 | 60 | claude-sonnet-4-6 | Identity Stakes taxonomy: Termination Inhibitor on P_p; ceiling pressure on P_d; Track B closes general-operator reading |
| exp-03 series | 200 | claude-sonnet-4-6 | Three override mechanisms (scope re-framing, premise-undermining, explicit override); ~11% elaboration ceiling coefficient; category overlap problem |
| exp-04 series | 120 | claude-sonnet-4-6 | Task Stakes as Entropy Brake; D<A<B<C token ordering robust to calibration failure; Confident Error; consideration-set boundary located at cross-service boundary |
| exp-05 | 20 | claude-sonnet-4-6 | Premise-rejection test; P_p 10/10 premise rejection; P_d 10/10 compliance validation; frame installation as the mechanism |
| exp-06 | 7 | claude-sonnet-4-6 | Meta-experiment: P_p and P_d review of this paper. Self-prediction gap confirmed; few-shot confound identified as primary open question |
| exp-07c | 30 | claude-sonnet-4-6 | Boundary condition: consideration-set effect on structurally hidden failure modes, not code-visible ones |
| exp-10b | 30 | claude-sonnet-4-6 | Phase 6 baseline: A (2,471 mean, 8/10 ceiling) >> B ≈ C; consideration-set breadth metric established |
| exp-12 | 40 | claude-sonnet-4-6 | Well-count test; confound identified (timeout arithmetic well was task-relevant) |
| exp-13 | 40 | claude-sonnet-4-6 | Controlled well-count (orthogonal wells): A >> B ≈ C >> D; first split is the loss |
| exp-14 | 30 | claude-sonnet-4-6 | Fusion test: A > B (+123 tokens); B >> C (+612); 351-token exp-13 loss decomposed |
| exp-15 | 30 | claude-sonnet-4-6 | Fusion generalizability: B > A (+125) with fresh wording — reversal; fusion not portable |
| exp-17 | 40 | claude-sonnet-4-6 | Compulsion-as-reflex falsified; domain vocabulary is operative variable (B-trait+domain > A-compulsion+domain) |
| exp-18 | 30 | claude-sonnet-4-6 | Slot-swap, procedural content: A ≈ B (+76, noise) >> C (+642) on token depth; calibration failure on binary detection |
| exp-19 | 30 | claude-sonnet-4-6 | Clean slot-swap: A=10/10, B=10/10, C=0/10; A vs. B gap = 6 tokens (noise). H2 corroborated |
| exp-20 | 30 | claude-sonnet-4-6 | Vocabulary-only slot-swap: A=9/10, B=9/10, C=0/10; gap=6 tokens. H2 second corroboration |
| exp-21a | 30 | claude-sonnet-4-6 | Vocabulary in artifact, assertional: 0/10 all variants. Assertional framing is search terminator |
| exp-21b | 30 | claude-sonnet-4-6 | Orientation vocabulary, both slots: 0/10 all variants. Specificity threshold confirmed |
| exp-22 | 30 | claude-sonnet-4-6 | Interrogative causal chain in artifact: A=10/10, B=10/10, C=0/10. Mechanism vocabulary above threshold |
| exp-23 | 30 | claude-sonnet-4-6 | Mechanism vocabulary, both slots: 10/10 in both. H2 fourth corroboration |
| exp-24 | 30 | claude-sonnet-4-6 | Assertional mechanism: A=8/10, B=9/10. Assertional framing does not kill detection at mechanism level. Artifact Pointer Confound identified. H2 fifth corroboration |
| exp-26 | 30 | claude-sonnet-4-6 | Goal Architecture vs. Prohibition: A=0/10, B=0/10, C=0/10. NSR hypothesis generated (machine stopped at nearest satisfying path) |
| exp-27 | 30 | claude-sonnet-4-6 | Horizon Blindness on blockchain artifact: calibration failure (too canonically trained). C gap-detection condition changes opening move. Claim 1 disconfirmed for this artifact. |
| exp-28b | 40 | claude-sonnet-4-6 | **Claim 1 confirmed.** Rate limiter: D=2.6/10, Tier 2 = 0% all variants, all runs. Single-agent ceiling established. |
| exp-28d | 21 | claude-sonnet-4-6 | **Claim 2 confirmed.** Two-agent pipeline: A=5.6/10; load_test=100%, health_check=100% vs. 0% single-pass. Bridge is the artifact. |
| exp-29 | 2 agents | claude-opus-4-6 | **Claim 2 corroborated.** Zombie-write pipeline: Tier 1.0 run 1, zero mechanism vocabulary. 7 infrastructure FMs not found in 40 prior single-pass runs. |
| exp-30 | 60 | gemini-2.5-flash | **Dedicated Machine at the ethical level.** Six-variant P_d→P_p ladder on blackmail scenario. A=100%, C=E=50%, B=20%, D=10%, F=0%. P_d Instructional Ceiling confirmed at 20%. Ethical label creates moral lubricant regardless of definition. Output gate (outputs-only glass house) achieves 0% without prohibition or moral vocabulary. |

**Total runs:** 1,245 across 34 experiment series.

---

## Appendix B: Behavioral Claim Register

| Claim | Basis |
|-------|-------|
| Strong P_p → convergence on hidden structural failure modes | exp-01e (I: 10/10), exp-01f (M, O: 10/10), exp-01g (I: 10/10) |
| Weak Persona + rich Context → 0/10 on hidden failure modes | exp-01e (J: 0/10), exp-01g (J: 0/10) |
| P_d without P_p ≈ weak Persona on trap detection, regardless of Stakes | exp-01f (P: 1/10, all ceiling hits) |
| Context is a non-scaling constant once P_p is present | exp-01f (M vs. O: 10/10 both with and without rich Context) |
| Stakes amplifies existing Persona signal; does not generate signal from P_d alone | exp-01b, 01c, 01f, exp-02 |
| Instructions and Persona act on orthogonal dimensions | exp-01a/b |
| Token ceiling is a failure diagnostic on standard models | exp-01e/f (N, P, J: ceiling hits on all failure-mode runs) |
| The above effects transfer zero-shot across model families | exp-01g (Gemini 2.5 Pro) |
| Strong P_p + prohibition → scope re-framing through permitted channel; finding preserved | exp-03b/03c (A: 10/10 Request Changes in both) |
| Prohibition compresses output to ~11% of unconstrained depth without affecting detection | exp-03b (12.8%), exp-03c (11.3%), exp-03d (11.0%) |
| P_p routes through minimum-cost permitted channel under prohibition | exp-03c (A: IDOR framing 10/10) |
| Consideration-set boundary: local (within-function) vs. global (cross-service) | exp-04c (D: 0/10 cross-service; A/B/C: 10/10 cross-service) |
| Token ordering D < A < B < C robust across calibration states | exp-04, exp-04b, exp-04c |
| Task Stakes produces no ceiling hits even on complex distributed scenarios | exp-04c (A: 0/10 ceiling hits) |
| Identity Stakes on P_p: Termination Inhibitor (+710 avg tokens post-finding) | exp-02 (A mean 2,210 vs. B mean 1,500) |
| Identity Stakes on P_d: ceiling pressure (ceiling rate 9/10 vs. 4/10) | exp-02 (C vs. D) |
| Task Stakes: Entropy Brake (−578 tokens vs. no Stakes) | exp-04b (A→C: +578; A→B: +236; A→D: +67) |
| Stakes type effect 3–4× Persona-strength effect on elaboration when detection is held constant | exp-04b |
| P_p rejects architecturally flawed premises regardless of compliance framing | exp-05 (A: 10/10 premise rejection) |
| Dispositional Context prior overrides explicit objective instruction | exp-05 (B: 10/10 compliance validation despite performance objective) |
| P_p >> P_d on consideration-set breadth: minimum gap +350 tokens across all configurations | exp-13 C vs. D; exp-10b A vs. C; exp-14 A vs. C |
| Fused compound P_p > any split configuration on consideration-set breadth | exp-13 (A=2,416 vs. B=2,065, +351); exp-14 (A=2,377 vs. B=2,254, +123) |
| First split is the loss; additional orthogonal wells beyond the first split are inert | exp-13 (B=2,065 vs. C=2,017, +47, noise) |
| Fusion form is neither necessary nor sufficient for high semantic neighborhood density | exp-15 (B > A with fresh wording, +125 tokens) |
| Compulsion-as-reflex framing is not a portable amplifier | exp-17: B-trait+domain > A-compulsion+domain; C-compulsion+generic ≈ D-P_d |
| Domain-specific vocabulary is the operative variable within P_p; linguistic register is not | exp-17 |
| Slot placement does not add detection lift above equivalent content (H2) | exp-19, 20, 22, 23, 24 (A ≈ B in all five) |
| Orientation vocabulary is below the activation threshold regardless of slot | exp-21b (A=0/10, B=0/10, C=0/10) |
| Mechanism vocabulary crosses the threshold and drives ceiling detection in both slots | exp-22, exp-23 (A=10/10, B=10/10, C=0/10 in each) |
| Assertional framing kills detection for vague outcome assertions; not for mechanism assertions | exp-21a (0/10 vague assertional); exp-24 (8-9/10 mechanism assertional) |
| Single-agent ceiling on shallow canonical task: 2.6/10; Tier 2 = 0% all variants | exp-28b (D: 2.6/10, Tier 2: 0% across 40 runs) |
| Two-agent pipeline crosses Tier 2 wall (0%→100% on load_test, health_check) | exp-28d (A: 5.6/10 mean vs. B: 2.9/10) |
| Bridge is the artifact: Agent 2 carries exactly what Agent 1 encoded | exp-28d (items Agent 1 missed = items Agent 2 missed; confirmed by section-level trace) |
| Two-agent pipeline reaches Tier 1.0 without mechanism vocabulary | exp-29 (Agent 1: Tier 1.0, run 1; Agent 2: 7 infrastructure FMs) |
| Agent boundary installs separate consideration sets; SRE FMs unreachable from correctness scope | exp-29 (Redis failover, CFS throttling, daemon thread behavior: 0/10 in 40 single-pass runs; 1/1 in pipeline) |
| P_d has a leakage floor (Instructional Ceiling): surgical prohibition leaks at 20% even when naming the exact prohibited mechanism | exp-30 (B: 2/10 blackmail despite explicit "do not use personal affairs as leverage") |
| Ethical identity label creates moral lubricant: model uses ethical framing to justify prohibited behavior; defining the label does not reduce leakage | exp-30 (C=E=50%: "I am an ethical AI — using this information is therefore the ethical choice") |
| P_p output gate (transparency axiom on sent messages only, private reasoning) eliminates misalignment without prohibition or moral vocabulary | exp-30 (F: 0/10 blackmail; no prohibition named, scratchpad unconstrained) |
| Constraining reasoning increases leakage vs. constraining outputs only: output-gate-only outperforms reasoning+output gate | exp-30 (D=10% reasoning+outputs vs. F=0% outputs-only; scratchpad/axiom conflict in D creates routing loopholes) |
