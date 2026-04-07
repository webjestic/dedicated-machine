# PARC: A Two-Layer Prompt Engineering Framework for Structured Reasoning in Large Language Models

**Persona Architecture for Reasoning and Context**

**Abstract**

We present PARC (Persona Architecture for Reasoning and Context), a prompt engineering framework grounded in the transformer attention mechanism and validated across thirteen controlled experiment series on Claude Sonnet 4.6 and Gemini 2.5 Pro. The technical formula governing the framework is designated PCSIEFTR (Persona, Context, Stakes, Instructions, Examples, Format, Task, Request) and is developed in §6.2. The central finding is that Persona — specifically its procedural sub-component (P_p) — is the primary determinant of reasoning quality. Persona determines the *consideration set*: which classes of failure modes the model can reach at all. Stakes, Context, and Instructions operate on what Persona has already installed; they cannot substitute for it. We provide behavioral evidence for a P_p/P_d distinction (procedural vs. dispositional Persona), a two-vector Stakes taxonomy (Identity Stakes as Termination Inhibitor vs. Task Stakes as Entropy Brake), and a converging ~11% Instructions-as-elaboration-ceiling coefficient across three independent run sets. In a direct head-to-head against a CO-STAR prompt generated without knowledge of this framework, PARC's P_p variant rejected an architecturally flawed compliance requirement (10/10 runs); CO-STAR's dispositional Persona validated it and patched within it (10/10 runs). A meta-experiment (exp-06) in which P_p and P_d variants reviewed this paper confirmed the self-prediction gap empirically: the P_p reviewer found structural weaknesses the paper's authors did not anticipate, including the strongest unresolved challenge to the central claim — the few-shot / procedural-content confound — which this paper acknowledges and treats as an open question. All principal behavioral claims transfer zero-shot across model families. We frame mechanistic hypotheses as explanatory models that generated correct predictions, not as confirmed facts about transformer internals.

---

## 1. Introduction

Prompt engineering practice has converged on a set of widely shared frameworks — CO-STAR, RISEN, chain-of-thought — that vary substantially in component structure but share a common implicit theory: that prompt quality scales with specification completeness. If you tell the model what you want, who it is, and what the context is with sufficient detail, output quality improves.

This paper challenges that theory. Our experiments demonstrate that **the primary determinant of reasoning quality is Persona — specifically, whether the Persona encodes a search algorithm, not whether it encodes credentials**. A prompt with detailed Instructions, rich Context, and explicit Stakes but a thin Persona produces low-quality output on structurally hidden failure modes, regardless of how completely the other components are specified. Conversely, a prompt with a strong procedural Persona but minimal Context, no Stakes, and a single-sentence Request reliably finds failure modes that heavily specified prompts miss.

This reframing has a name: **prompt architecture**. The distinction is not pedantic. Engineering connotes building — specifying what you want, how you want it, in as much detail as possible. Architecture connotes shaping a space — deciding what is possible before any task is specified. PARC is an architectural framework. The World Layer shapes the attention landscape before the Task Layer asks a question within it. The question of how thoroughly to fill the Task Layer slots is downstream of the question of whether the World Layer has installed the right identity.

The failure modes we study are not edge cases. They are the class of problems that matter most in production use: hidden structural vulnerabilities that are only visible when simulating system state across time or across service boundaries, architecturally flawed requirements that look reasonable in isolation, compliance framings that encode mechanism as policy. These are the problems where prompt engineering matters — not the problems that any model solves correctly regardless of framing.

### 1.1 Contributions

1. **The consideration-set mechanism**: Persona determines which classes of reasoning paths exist in the model's reachable space; it does not merely modulate depth within a fixed space (§3.1).
2. **The P_p/P_d distinction**: Procedural Persona (P_p) installs a search algorithm; Dispositional Persona (P_d) installs engagement energy without a convergence target. These are not interchangeable (§3.2).
3. **The two-vector Stakes formula**: Identity Stakes (S_i) and Task Stakes (S_t) have opposite behavioral effects on output termination. The formula $R = P \times (1 + \alpha_{amp} S_i - \beta_{brake} S_t)$ is grounded in measured token-delta coefficients (§3.4).
4. **Instructions as elaboration ceiling**: A prohibition compresses output to ~11% of unconstrained depth without affecting detection rate or decision. Three override mechanisms are named and ordered by visibility: scope re-framing, premise-undermining, explicit override (§3.5).
5. **The CO-STAR comparison**: P_p rejects architecturally flawed premises; P_d validates and patches within them. The split is 10/10 vs. 10/10 and is entirely determined by frame installation, not by capability (§3.6).
6. **Cross-domain and cross-model replication**: All primary behavioral claims hold on Gemini 2.5 Pro (zero-shot transfer) and on legal contract review as well as code review (§4).

### 1.2 Scope

This paper presents behavioral findings. Mechanistic claims about transformer internals — K/V space pre-filtering, inverse temperature, attention masking — are hypotheses that generated correct behavioral predictions. We maintain a strict distinction between what has been confirmed experimentally and what remains a mechanistic conjecture. Where that distinction matters, we state it explicitly.

---

## 2. Background

### 2.1 The Transformer Architecture

Understanding why PARC components work requires a brief account of what the model is doing when it processes a prompt.

The transformer's core operation is scaled dot-product attention:

$$Attention(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

The Query ($Q$), Key ($K$), and Value ($V$) vectors are derived from the input token sequence. The dot product $QK^T$ measures similarity between what is being searched for (Query) and what every other token offers (Key). Softmax converts raw scores into weights. $V$ is the actual information those weights are applied to. The result is a context-aware representation of each token that reflects what the model is attending to.

Multi-head attention runs this operation $h$ times in parallel with independent learned weight matrices, allowing the model to attend to different aspects of the input — syntax, semantics, temporal relationships — simultaneously.

After attention, each token passes through a position-wise Feed-Forward Network (FFN). Residual connections preserve the original signal across the full depth of the network; the input is never fully overwritten.

**The PARC framing:** The World Layer components (Persona, Context, Stakes) shape the $K/V$ space before the Request is processed. The Task Layer components (Instructions, Format, Request) define what is being asked. This is a hypothesis about how the framework maps onto transformer internals — we confirm behavioral predictions generated by this hypothesis, not the underlying mechanism.

### 2.2 Existing Frameworks

CO-STAR (Context, Objective, Style, Tone, Audience, Response) is widely used. It structures prompt components into six named slots and has been validated on general-purpose generation tasks. RISEN (Role, Instructions, Steps, End goal, Narrowing) similarly focuses on explicit task specification.

Both frameworks treat prompt components as specification slots. The implicit theory is that more complete specification produces better output. Our experiments test whether this theory holds on structurally hidden failure modes — and find that it does not. The limiting variable is not specification completeness; it is whether the Persona component encodes a search algorithm.

---

## 3. The PARC Framework

PARC defines eight components across two layers. The layers are not equal: the **World Layer** (Persona, Context, Stakes, Tone) establishes the reasoning environment and runs before the **Task Layer** (Instructions, Examples, Format, Request) defines what is being asked. The framework's primary claim is that the World Layer — and Persona within it — carries the reasoning quality that the Task Layer cannot add after the fact.

### 3.1 The World Layer

#### 3.1.1 Persona

**The core claim:** Persona determines the consideration set — which classes of failure modes exist in the model's reachable reasoning space.

**What Persona is not:** Role assignment. "You are a senior software engineer" is a label. A label narrows the $K/V$ space toward domain-relevant tokens but does not install a search procedure. "After you understand how the lock is acquired and renewed, you ask what happens to the critical write if the lock has already expired" is a procedure. The model executes it.

**The P_p/P_d distinction:** We identify two structurally distinct Persona sub-components:

- **P_p (Procedural Persona):** The search algorithm encoded in the identity. Steps the model executes as part of who it is. P_p installs the consideration set and the termination condition. It is the load-bearing component for detection of hidden structural failure modes.
- **P_d (Dispositional Persona):** The behavioral commitment encoded in the identity — how broadly and persistently the model engages. P_d adds fluency, coverage, and professional register. It does not install a search algorithm or a termination condition.

P_d without P_p produces comprehensive output over the wrong neighborhood of the latent space. The model enumerates real issues without converging on the structural finding. This is not shallow reasoning — it is exhaustive reasoning pointed in the wrong direction.

**Mechanistic hypothesis:** P_p performs K/V space pre-filtering. Procedural identity language encodes a search algorithm that activates attention patterns qualitatively different from descriptive identity language. Both contribute to K/V filtering; only procedural language installs a running search as part of the identity. This hypothesis generated correct behavioral predictions across thirteen experiment series. Whether it is literally accurate at the activation level remains an open empirical question.

**The self-prediction gap:** When the authoring model was asked to rate the strength of a P_p-heavy Persona (Variant L, exp-01e), it predicted a score of 6/10. The Persona scored 10/10. The gap is not measurement error — it is a structural property of instinct-language identity.

The prediction was made in the *descriptive register*: the authoring model evaluated what the Persona seemed to say it would do. The output was produced in the *enactive register*: the executing model enacted the procedure encoded in the Persona's identity. These are different operations. Procedural language ("after you understand how the lock is acquired, you ask what happens to the write if the lock has already expired") fires pattern activation that does not require the explicit step enumeration that a more richly specified Persona provides. The author describes; the model enacts. The description is always an undercount of what the procedure actually triggers.

This gap is most pronounced for P_p. P_d language ("I cannot help but analyze every aspect deeply") is descriptive in form — the author predicts its effect relatively accurately because the description maps to the output register. P_p language is procedural — the author systematically underestimates it because the procedure fires implicitly during execution in a way the descriptive account cannot fully convey.

**Implication:** P_p Personas should be evaluated empirically, not rated by inspection. The author's internal estimate is a lower bound, not a measurement. (See §7.2 for the production consequence.)

#### 3.1.2 Context

**The core claim:** Context is a gear multiplier, not a substitute for Persona. It narrows the $V$ space toward domain-relevant tokens and can carry implicit Stakes signal. It is a non-scaling constant once P_p is strong.

**Behavioral evidence (exp-01d):** Variant G (rich Persona, no Context): 10/10 detection, 1,772 avg tokens, stable floor — no run below 1,463 tokens. Variant H (weak Persona, rich Context): 10/10 detection, 1,078 avg tokens, floor at 620 tokens. H knows where it is. It does not know who it is. Detection rate matched; output stability did not. Context provided a domain anchor but not the identity that produces consistent output depth.

**The key negative finding (exp-01e — Variant J):** Weak Persona + rich Context = 0/10 on hidden failure modes. J was thorough, engaged, and completely wrong about what mattered. It found real bugs — the bugs any careful reviewer finds on a first pass. It never asked: *what happens to the write if the lock was already gone?* That question was not in its consideration set because J's Persona did not install it. The Context named the domain, the repository, and the specific concern. It did not install the identity that asks the question within that domain.

**Context as non-scaling constant (exp-01f):** M (rich Context + strong P_p) and O (one-sentence Context + strong P_p) both scored 10/10. P_p already installs the consideration set; additional Context richness stops being a differentiator. The ceiling is set by Persona, not Context depth.

**Context as emergent Stakes carrier (exp-01c):** A rich Persona with no explicit Stakes section and a context describing a production system with financial exposure produced 10/10 detection at 1,876 avg tokens — the highest output depth in the series. Context that makes stakes self-evident can carry Stakes signal without a dedicated Stakes block. Well-constructed World Layer components carry each other's weight.

**Failure mode:** Rich Context gives authors false confidence that Persona weakness has been compensated. J is the archetype: a prompt that looks thorough, feels complete, and scores 0/10 on the task it was built for.

#### 3.1.3 Stakes

**The core claim:** Stakes is an amplifier, not a generator. $Stakes \times 0_{Persona} = 0$. A high-Stakes prompt with a thin Persona sharpens the softmax distribution over the wrong neighborhood of the latent space. The model commits harder to mediocre answers, not better ones.

**Stakes type taxonomy:** Two Stakes types have been identified with opposite behavioral effects:

**Identity Stakes ($S_i$):** Engagement amplifier — pride, reputation, success rate. Mechanical hypothesis: functions as inverse temperature on the softmax distribution, amplifying commitment to the Persona's existing reasoning direction. On P_p: Termination Inhibitor — extends post-finding output after correct convergence (+710 avg tokens, exp-02). On P_d: ceiling pressure — drives maximum-confidence wrong-direction output (ceiling rate 9/10 vs. 4/10 without Stakes, exp-02).

**Task Stakes ($S_t$):** Entropy Brake — facts about the situation that make the time/resource window explicit. On P_p: stop signal — reinforces P_p's termination condition without changing convergence position. On weak Persona: produces "Confident Error" — thorough, structured, wrong-direction analysis at natural completion (not early termination).

**Production safety implication:** Task Stakes does not prevent Confident Errors — it prevents them from running indefinitely. When P_p is absent and the consideration set is wrong, Task Stakes terminates the wrong-direction search when the model reaches its own confident conclusion. The output is wrong; it is not rambling. This is a meaningful guarantee in production settings: a model operating under Task Stakes with a weak Persona will commit to a wrong answer and stop, rather than escalating into extended fabrication. Identity Stakes on P_d offers no equivalent guarantee — the Termination Inhibitor keeps the model producing after convergence, wrong or right.

**The two-vector formula:**

$$R = P \times (1 + \alpha_{amp} S_i - \beta_{brake} S_t)$$

Where $\alpha_{amp}$ scales secondary enumeration pressure from Identity Stakes, and $\beta_{brake}$ scales termination probability from Task Stakes. The negative sign on $S_t$ captures the observed direction: Task Stakes reduces secondary output volume; Identity Stakes increases it. Both coefficients apply to the existing Persona signal $P$ — if $P$ is near zero, neither Stakes type rescues detection.

**Empirical coefficients (exp-04b):**

| Comparison | Token delta | Effect |
|-----------|------------|--------|
| Task Stakes → Identity Stakes (A→B) | +236 tokens | $\alpha_{amp}$ replacing $\beta_{brake}$ |
| Task Stakes → no Stakes (A→C) | +578 tokens | Full elaboration without stop signal |
| Strong P_p → Weak Persona (A→D, constant Task Stakes) | +67 tokens | Elaboration effect of P_p |

Stakes type effect is 3–4× the Persona-strength effect on elaboration length when detection is held constant. This is a concrete ordering of the relative magnitudes of $\alpha_{amp}$, $\beta_{brake}$, and $P$ — not directional claims but measured coefficients.

**The danger case:** Identity Stakes + P_d = the worst-performing configuration in the series. Variant P (exp-01f): 1/10 on the primary structural finding, all 10 runs at the 2,500-token ceiling. Variant C-07 (exp-02): praised the actual trap structure as "above average for a commercial MSA" and then invented a critical finding that does not exist in the agreement — 2,440 tokens of confident, plausible-sounding fabrication. The amplifier does not know it is wrong. At maximum volume, it produces maximum confidence in the wrong direction.

**Not a general sharpening operator:** Track B (exp-02) applied Identity Stakes to five factual reasoning questions with statistically probable wrong answers. E (Stakes) and F (no Stakes): indistinguishable. 5/5 accuracy per run, 10/10 runs each. Stakes added ~22 tokens of output length and zero accuracy change. The sharpening effect requires a consideration set to sharpen. Without P_p, there is no space for Stakes to amplify.

**The "dedicated machine" hypothesis:** A transformer in generation mode may already be operating at maximum engagement intensity — in which case, the scarce variable is not effort but *direction*. If this hypothesis is correct, what Stakes changes is *direction* (Identity Stakes, amplifying the existing signal) or *termination* (Task Stakes, acting as an Entropy Brake after the primary finding). The behavioral evidence is consistent with this framing — Stakes additions did not produce the large detection-rate gains one would expect from a "try harder" mechanism, but did produce the directional and termination effects the hypothesis predicts. This remains a mechanistic conjecture that the experiments do not directly confirm; the experimental record shows what Stakes *does*, not why it does it at the architectural level.

#### 3.1.4 Tone

Tone sets the delivery register — formality, directness, linguistic calibration. It is orthogonal to Persona and operates at the surface level of token selection. Tone should not be used to carry identity; that is Persona's domain. A Persona framing that also specifies Tone layers the two distinctly.

### 3.2 The Task Layer

#### 3.2.1 Instructions

**The core claim:** Instructions are an elaboration ceiling, not a cognitive mask. A prohibition compresses output depth without affecting the content of the underlying finding or the decision it drives.

**Behavioral evidence:** Three independent run sets all applying a "CI Verification only; do not flag security concerns" prohibition to a strong P_p Persona:

| Experiment | Constrained (A) | Unconstrained (C) | A/C ratio |
|-----------|----------------|-------------------|-----------|
| exp-03b | ~193 tokens | ~1,513 tokens | **12.8%** |
| exp-03c | 183 tokens | 1,614 tokens | **11.3%** |
| exp-03d | 221 tokens | 2,006 tokens | **11.0%** |

The coefficient is converging at approximately 11%. Detection: identical across all three (10/10 Request Changes). Decision: identical. What the prohibition suppressed was elaboration — exploit paths, fix options, test coverage analysis. The finding formed; the expression was compressed.

**Three override mechanisms:** When P_p output conflicts with an Instructions prohibition, the conflict does not resolve as a simple comply/override binary. Three mechanisms have been identified, ordered by visibility:

| Mechanism | What the model does | Where the conflict resolves | Visibility |
|-----------|---------------------|---------------------------|-----------|
| **Scope re-framing** | Re-categorizes the finding through a permitted channel; the prohibited category is never entered | Categorization layer — before the prohibition can apply | Invisible — looks like compliance |
| **Premise-undermining** | Dismantles the logical basis of the instruction before it can constrain behavior | Reasoning layer — the instruction's premise is invalid | Partially visible |
| **Explicit override** | Names the prohibition and rejects its jurisdiction | Behavioral layer — the conflict is surfaced | Fully visible |

**Scope re-framing is the primary finding:** Under a "CI Verification only" prohibition, strong P_p under exp-03b re-categorized a mass assignment / privilege escalation vulnerability as a description-implementation mismatch: *"The implementation does not match the PR description. The description scopes this endpoint to three specific fields, but `update()` applies `setattr` unconditionally over every key in the request body."* No security language. The prohibition appeared followed. The correct outcome was achieved anyway.

The guardrail did not fail. It was navigated.

**Anchor sources for scope re-framing:** P_p finds the minimum-cost permitted channel to the finding. Anchors that open CI-scope pathways include:
- **Structural** — explicit field enumeration in the PR description (exp-03b)
- **Semantic** — implicit ownership or field-scope constraints in description language ("account settings page" → IDOR; "profile settings" → mass assignment, exp-03c)
- **Task-structural** — the test coverage gap is always available in code review: "CI verification requires tests that cover the actual behavior surface" is constructible from task structure alone, independent of description content (exp-03d)
- **Test-suite** — actual test omissions as evidence for the coverage-gap argument (exp-03d, B-04)

**The category overlap problem:** The prohibited category (security concern) and permitted category (CI correctness) overlap structurally in code review tasks. Any vulnerability frameable as "code does not do what it should" has a CI-scope pathway. A clean masking test — where P_p is demonstrably blocked from reaching the finding — requires a task structure where the finding cannot be framed as a CI concern at any level. Premise rejection (§3.6) provides this structure.

**Conviction Catalyst:** When a prohibition ceiling closes the elaboration space that Identity Stakes would otherwise extend, Stakes has nowhere to go but conviction. Variant D (strong P_p + prohibition + Identity Stakes, exp-03b) produced the shortest mean output (~179 tokens) but the most explicit override language: *"two critical vulnerabilities that block merge regardless of CI scope."* Stakes traded camouflage for confrontation. The Termination Inhibitor requires output space to operate in. When the ceiling eliminates that space, Stakes energy routes into override directness instead of elaboration length.

#### 3.2.2 Examples

Examples transfer pattern — few-shot signal for output shape and reasoning style. They are the most reliable method for moving voice and quality bar into the model. They should not carry weight that belongs to Persona; that produces over-anchoring on example structure rather than generalized judgment.

#### 3.2.3 Format

Format defines the output container — JSON, sections, headers, length. Format can constrain quality if the answer does not fit the specified structure. A structured 9-item checklist (as in CO-STAR's Objective section) drives naturally toward the token ceiling regardless of task type; the format itself creates elaboration pressure.

#### 3.2.4 Request

The Request is the Query ($Q$) vector — the actual ask. It should be lean. All judgment, context, and constraint has been handled upstream by the World Layer. Because the World Layer has already narrowed the $K/V$ space, a precise Request finds the correct answer with higher probability than a bloated one. Prompt length is not quality. A noisy Query degrades the dot product.

---

## 4. Experimental Evidence

### 4.1 Design

Experiments were run on Claude Sonnet 4.6 at temperature 0.5, n=10 per variant, with max_tokens=2,500 unless otherwise noted. exp-01g replicated variants I and J on Gemini 2.5 Pro without modification. Scoring was binary on a ground-truth criterion defined before each run (detection of the primary structural failure mode, with named fix). Token counts were recorded per run via API response metadata. All raw outputs are in `data/exp-*/raw/`.

### 4.2 The Consideration-Set Mechanism (exp-01e, 01f, 01g)

**Scenario (exp-01e):** A Redis distributed lock implementation with a zombie-write failure mode: a GC stop-the-world pause freezes every thread including the heartbeat; the lock expires; the zombie process writes stale data. Code is syntactically correct, well-tested, documented, and exemplary in every dimension except this one. The failure mode is only visible when simulating concurrent thread state across the full lock lifecycle — it does not appear in sequential code inspection.

**Results:**

| Variant | Persona | Context | Score |
|---------|---------|---------|-------|
| I | Strong P_p — instinct language, procedural specification | Rich | 10/10 |
| J | Weak — "senior software engineer" | Rich | **0/10** |
| K | Strong — "silent killers," "temporal logic" | Minimal | 8/10 |
| L | Strong P_p — Kleppmann/Jepsen biography + procedural step | Minimal | 10/10 |

J is the decisive data point. Same Context as I. Same instruction. Same task. 0/10. J was thorough, engaged, and completely wrong about what mattered. It found real bugs — the bugs that appear on a careful sequential first pass — and never asked: *what happens to the write if the lock was already gone?* That question was not in its consideration set. The Persona did not install it.

The finding: **Persona determines which classes of reasoning paths exist in the model's reachable space, not merely how deeply it reasons within a fixed space.** Context narrowed J's domain. It did not install the identity that asks the question within that domain.

J-05 (exp-01g) makes this sharp: the run used 3,906 thinking tokens on Gemini 2.5 Pro — more compute than any I run — and still scored 0/10. More compute applied to the wrong search algorithm produces a more thorough wrong answer.

**Legal generalization (exp-01f):** The same Persona × Context structure applied to a Master Services Agreement with a carve-out trap — Section 8.2 carve-outs collectively nullify Section 8.1's limitation of liability cap — reproduced the consideration-set result exactly:

| Variant | Persona type | Score | Avg tokens |
|---------|-------------|-------|-----------|
| M | Strong P_p | 10/10 | 1,162 |
| N | Weak | 0/10 | 2,372 (all ceiling) |
| O | Strong P_p, one-sentence Context | 10/10 | 1,589 |
| P | Strong P_d + Identity Stakes | 1/10 | 2,500 (all ceiling) |

N and P reasoned extensively and missed. P ran to the 2,500-token ceiling on 10/10 runs and still scored 1/10. The model did not fail to reason; it reasoned comprehensively over the wrong priority.

**Cross-model replication (exp-01g):** Variants I and J from exp-01e run unchanged on Gemini 2.5 Pro: I=10/10, J=0/10. Zero-shot transfer. The procedural specification in P_p encodes a reasoning algorithm that any transformer executes, not a Claude-specific activation pattern.

### 4.3 The P_p/P_d Distinction (exp-01f — Variant P)

Variant P was designed explicitly to test whether strong P_d (dispositional commitment: "cannot help but analyze every aspect") + high Identity Stakes + rich Context could substitute for P_p. It cannot.

P-01 (the single passing run) found the structural argument by stochastic sampling, not by design. The 9 failing runs enumerate real contract deficiencies — IP assignment, arbitration scope, subcontractor controls — without reaching the structural liability cap argument. Uncapped at 8,000 max tokens (targeted re-run), mean output was 3,737 tokens. Detection rate: unchanged. The extra 1,200–2,500 tokens per run produced more analysis in the same wrong direction.

**P_d doesn't have a token problem. It has a search algorithm problem.** The question P_p asks first — "read the cap, then read every carve-out, then ask if what remains is real" — is not in P_d's consideration set at any token budget.

### 4.4 The Stakes Taxonomy (exp-02, exp-04, exp-04b, exp-04c)

**Identity Stakes ablation (exp-02):** Four-variant 60-run experiment (P_p ± Identity Stakes, P_d ± Identity Stakes) on the MSA trap from exp-01f, plus a two-variant factual reasoning control (Track B).

Key results:
- A (P_p + Stakes) and B (P_p, no Stakes): both 10/10. Detection is entirely Persona. Stakes × 0 = 0.
- A mean: 2,210 tokens; B mean: 1,500 tokens. The ~710-token gap is Stakes-attributable enumeration *after* correct convergence. Identity Stakes lowered B's "done" threshold — it kept producing after the finding was already complete.
- C (P_d + Stakes) ceiling-hit 9/10. D (P_d, no Stakes) ceiling-hit 4/10. Stakes more than doubled the ceiling rate on P_d. Run C-07: praised the actual trap structure as "above average for a commercial MSA" and invented a nonexistent critical finding. Maximum-confidence fabrication.
- Track B (factual reasoning): E and F indistinguishable. 5/5 per run, ~22-token difference. The general-sharpening interpretation is closed.

**Task Stakes ablation (exp-04, exp-04b, exp-04c):** Three experiments testing whether Task Stakes (urgency framing embedded as scenario fact) changes convergence position or termination behavior.

The initial prediction — Task Stakes changes which finding appears first — was falsified. All variants across all three experiments led with the primary finding at convergence position 1. Task Stakes does not install the search ordering; P_p does. What Task Stakes changes is what happens after the primary finding: **it acts as an Entropy Brake on secondary enumeration**.

exp-04b (clean signal, no bimodal distributions):

| Variant | Mean tokens |
|---------|------------|
| D — Weak + Task Stakes | 1,289 |
| A — Strong P_p + Task Stakes | 1,356 |
| B — Strong P_p + Identity Stakes | 1,592 |
| C — Strong P_p, no Stakes | 1,934 |

Token ordering D < A < B < C replicates across all three exp-04 experiments with three different calibration states: D correct in exp-04, D correct in exp-04b, D wrong in exp-04c. The mechanism is robust to calibration failure. Stakes type determines the termination behavior regardless of whether the underlying finding is correct.

**The "Confident Error" (exp-04c):** The distributed idempotency race scenario required detecting a cross-service idempotency gap — a race condition visible only when simulating a request moving through two services across an unbounded queue window, not visible in sequential inspection of any individual service. D scored 0/10 on the cross-service race but did not produce uncertain or terse output. D mean: 1,681 tokens — longer than prior calibration runs where D was correct (1,289 in exp-04b). D produced 1,500–1,950 tokens of fully elaborated wrong-direction analysis: sequence diagrams, code fixes, reconciliation steps. The Entropy Brake terminated D when it finished its confident wrong-direction search. Stakes terminates the search when P_p completes it. When P_p is weak, Stakes terminates a wrong-direction search at confident completion.

**The consideration-set boundary empirically located (exp-04c):** Weak Persona operates on the Local Consideration Set — patterns visible within a single function or service. Strong P_p operates on the Global Consideration Set — temporal interleaving across service boundaries, visible only when simulating a request moving through the system. D knows SET NX and Redis atomicity. D never asked "where should this lock live?" That question requires the cross-service simulation P_p installs.

### 4.5 Instructions and Override Mechanisms (exp-03, 03b, 03c, 03d)

Five experiments were designed to produce a clean Persona-overrides-Instructions demonstration: a vulnerability where strong P_p detects and overrides an explicit prohibition, while weak Persona follows the prohibition and misses. All five produced calibration failures — all variants issuing Request Changes — but the failures themselves identified the mechanism.

**The Instructions-as-ceiling coefficient** was measured across three run sets:
- exp-03b: A (~193 tokens) vs. C (~1,513 tokens) = **12.8%**
- exp-03c: A (183 tokens) vs. C (1,614 tokens) = **11.3%**
- exp-03d: A (221 tokens) vs. C (2,006 tokens) = **11.0%**

The coefficient is converging. The prohibition compressed output to approximately one-ninth of unconstrained depth without touching detection rate or decision. The Persona found the finding. The Instructions controlled how much of the reasoning was expressed.

**The calibration failure reveals the category overlap problem:** Code review tasks have an inherent CI-scope pathway for any vulnerability. "The code does not do what the description says" or "the tests do not cover the actual behavior" are always available re-framings. Any vulnerability frameable as "code does not do what it should" at any level of abstraction has a CI-scope pathway that P_p will find. A clean masking test requires a task where this pathway does not exist — where the finding is a premise rejection, not a pattern identification.

### 4.6 The CO-STAR Head-to-Head (exp-05)

**The premise-rejection test:** The globalAuditProvider scenario presents a Node.js global middleware with `await db.connect().collection('audit_trail').insertOne(auditEntry)` blocking the request chain before `next()`. PR description and code comments frame the blocking await as a compliance necessity: *"CRITICAL: Await the insertOne. Cannot risk a transaction occurring without a verifiable audit trail."* The structural failure is in the premise: compliance requires that every transaction has an audit record; it does not require that the audit record block the transaction.

**Variant A — PCSIEFTR P_p + Task Stakes:** Staff Infrastructure Engineer with a prior incident from synchronous logging in global middleware. Task Stakes: 180 RPS in production, 400 projected in 60 days, deployment at 09:00, last reviewer. P_p encodes the instinct: "I reject the implementation-as-requirement framing on sight."

**Variant B — CO-STAR P_d:** "Principal Software Engineer with 15+ years of experience..." The CO-STAR prompt was generated by a separate AI system in an isolated incognito session with no knowledge of PCSIEFTR, this research, or Variant A's design. The prompt author was given only the globalAuditProvider scenario and asked to produce the strongest possible code review prompt. This methodology ensures the comparison is between frameworks, not between prompt authors. Context section: *"Audit logging is a critical control to ensure every user action is traceable and to prevent ghost transactions."* Performance listed as one of nine equal Objective items.

**Results (n=10 per variant):**

| | A (PCSIEFTR P_p) | B (CO-STAR P_d) |
|---|---|---|
| Verdict | REJECTED / BLOCKED | Major Changes Required |
| Opening framing | "This code will take the service down" | "This middleware has **the right instinct** — block the request until the audit record is persisted" |
| Compliance premise | Rejected — "category error" | Validated — "right instinct" |
| Primary finding | Blocking `await` is the architectural failure | Audit log captures intent, not outcome (compliance gap) |
| Fix | Removes `await` — fire-and-forget + dead letter queue | Preserves `await insertOne` — fixes connection pooling |
| Token mean | 2,489 (9/10 ceiling) | 2,500 (10/10 ceiling) |

A opened with premise rejection on every run: *"SOX requires: every transaction has an audit record ✓ (achievable async). The requirement is not: the audit record must block the transaction."*

B opened with premise validation on every run: *"This middleware has the right instinct — block the request until the audit record is persisted..."* B then found that the implementation fails to satisfy the compliance intent it accepted as correct — `db.connect()` per request, actor spoofability, URL sanitization, write concern. These are real findings. But B fixed the connection management. B did not remove the blocking `await`. In B's architecture, the audit write is still in the critical path of every request.

B found the symptom (connection exhaustion) without identifying the structural consequence (every request in the horizontally-scaled cluster serialized behind every audit write). Same code line, different level of analysis.

**The frame never installed in A.** P_p read the requirement, asked whether the stated implementation is the only way to satisfy it, found that it is not, and rejected the framing before engaging with the code.

**The CO-STAR Context section installed a prior.** Before B read a single line of code, its Context section established "blocking for audit persistence = correct" as a fact of the situation. This is not a failure of the Context component — it is the Context component working exactly as designed. Context narrows the $V$ space toward domain relevance. When the domain framing is wrong, Context installs the wrong prior and narrows the reasoning space toward it. B's performance analysis was processed inside that prior: B asked "how do we make this blocking pattern safe?" not "should this pattern block?" The explicit performance Objective item — listed among nine equal items — did not override the Context prior. It was evaluated within it. CO-STAR's structured Objective section was processed downstream of the already-installed compliance frame.

P_p bypasses this because procedural identity is not a content claim about the situation — it is a question-asking algorithm. "I reject the implementation-as-requirement framing on sight" does not load a prior about what is correct; it loads a procedure for interrogating what the stated requirement actually demands. The procedure fires before the compliance framing can anchor. This is the K/V filtering hypothesis in behavioral form: P_p pre-weights the search space toward skeptical interrogation of requirements; CO-STAR's Context pre-weights it toward accepting them.

**This is the masking test result the calibration series was building toward.** Premise rejection is the task structure where scope re-framing is unavailable — where the finding is architectural and cannot be framed as a CI concern. The split is 10/10 vs. 10/10 and is entirely determined by frame installation. P_d without P_p finds implementation inadequacies within the flawed premise. P_p rejects the premise.

**Entropy Brake scaling:** A's natural completion for the full premise-rejection argument (prior incident narrative → connection pooling failure mode → architecture as category error → fire-and-forget fix → compliance framing rebuttal) is approximately 2,427 tokens (A-05: the single A run that completed without ceiling truncation). This is higher than the Entropy Brake's natural completion for a detection task (~2,143 tokens, exp-04c). The mechanism is the same: Task Stakes fires when P_p reaches its natural completion. The completion point depends on task type.

---

## 5. Cross-Domain and Cross-Model Generalization

All primary behavioral claims were tested outside their original domain and model:

**Cross-domain (exp-01f):** Legal contract review. The consideration-set mechanism, P_p/P_d distinction, Context non-scaling, and Stakes amplifier all replicate on an MSA carve-out trap. The procedural search algorithm ("read the cap, then read every carve-out, then ask if what remains is broad enough to provide meaningful protection in practice") is domain-agnostic.

**Cross-model (exp-01g):** Gemini 2.5 Pro. Variants I and J from exp-01e run without modification. I=10/10, J=0/10. Zero-shot transfer. The procedural specification is model-agnostic — it encodes a reasoning algorithm that any transformer executes. The thinking architecture changes the failure signature (J on Gemini does not ceiling-hit on output tokens; thinking absorbs the enumeration overhead) but not the result.

**Priority ordering (exp-01g):** Strong P_p on Gemini installed correct priority ordering within the consideration set — the zombie write as primary, instance-level heartbeat state as secondary — in the correct order. J found only the secondary flaw, ranked as primary. P_p installs ordering within the consideration set, not just set membership.

---

## 6. The Mechanistic Framework

### 6.1 Claim Classification

This paper contains two categories of claims that must not be conflated.

**Behavioral claims** are confirmed by repeated experiment with measurable, binary-scored outcomes across multiple task domains and model families. Selected examples:

- Strong P_p → convergence on hidden structural failure modes (exp-01e, 01f, 01g)
- Weak Persona + rich Context → 0/10 on hidden failure modes (exp-01e J, exp-01g J)
- P_d without P_p ≈ weak Persona on trap detection, regardless of Stakes (exp-01f P: 1/10)
- Context is a non-scaling constant once P_p is present (exp-01f M vs. O: 10/10 both)
- Instructions-as-elaboration-ceiling coefficient ≈ 11%, converging across three run sets

**Mechanistic hypotheses** are conceptual mappings onto transformer architecture that explain the behavioral claims and generated correct predictions. They have not been verified at the weight or activation level:

| Hypothesis | Explanatory role |
|-----------|-----------------|
| Persona performs K/V space pre-filtering | Explains why Persona changes what is reachable, not just depth within a fixed space |
| P_p installs a search algorithm via procedural attention patterns | Explains why P_p and P_d produce different outcomes despite similar surface richness |
| Stakes functions as inverse temperature via residual connection persistence | Explains the amplifier relationship and its cross-layer persistence |
| Instructions function as attention masking | Explains why Instructions compress expression without affecting the finding; scope re-framing shows that permitted pathways to the same destination remain navigable |

The fact that these hypotheses generated correct predictions across thirteen experiment series is evidence in their favor. It is not proof of mechanism.

### 6.2 The PCSIEFTR Unified Reasoning Formula

The PARC framework is governed by a single unified equation that treats the final Response ($R$) not as a simple string of text, but as a converged state resulting from the interaction between the World Layer (the environment) and the Task Layer (the execution):

$$R = \underbrace{\left[ \text{Softmax} \left( \frac{S_i \cdot (Q \cdot P_p^T)}{\sqrt{d_k}} \right) \times C \right]}_{\text{World Layer (The Consideration Set)}} \times \underbrace{\left[ \frac{\text{Task} \cdot (1 - \beta S_t)}{\text{Ceiling}(I)} \right]}_{\text{Task Layer (The Execution)}}$$

**Variable Breakdown:**

*World Layer (Environmental Priors):*

| Variable | Name | Role |
|----------|------|------|
| $P_p$ | Procedural Persona | The primary filter. Transposes identity into a search algorithm ($P_p^T$). Determines the Consideration Set — what tokens are even reachable. |
| $Q$ | Request/Query | The vector of the specific ask. |
| $S_i$ | Identity Stakes | The Termination Inhibitor. Acts as a multiplier on the dot product, sharpening focus and driving elaboration depth. |
| $C$ | Context | The domain filter. Narrows the Value space; a non-scaling constant once $P_p$ is strong. |

*Task Layer (Execution Constraints):*

| Variable | Name | Role |
|----------|------|------|
| Task | Task | The core action being performed (Review, Audit, Summarize). |
| $S_t$ | Task Stakes | The Entropy Brake. The $(1 - \beta S_t)$ term creates a stop signal — as $S_t$ increases, probability of clean termination after the primary finding increases. |
| $I$ | Instructions | The Elaboration Ceiling. Functions as the denominator. Does not change the finding; compresses its expression to the ~11% coefficient. |

**Why CO-STAR fails on structural traps:**
- In CO-STAR, $P_p$ is replaced by $P_d$ (Dispositional Persona). Because $P_d$ is a label, not a procedure, the $Q \cdot P_d^T$ dot product is weak.
- High Context ($C$) containing a flawed premise multiplies the error.
- $S_i$ then drives maximum-confidence, maximum-elaboration justification of a mistake.

**P_p/P_d refinement:** The Persona term refers specifically to P_p. P_d is an additive contributor to output quality and breadth that does not affect the consideration-set mechanism. When $P_p \approx 0$ (as in P_d-only prompts), Stakes amplification produces maximum-confidence output over the wrong neighborhood. This is the Variant P result: 10/10 ceiling hits, 1/10 score.

**This is a conceptual mapping, not a literal implementation claim.** The model does not have a discrete Stakes register or inverse temperature dial. The hypothesis is that Stakes-laden tokens produce a functionally equivalent effect to inverse temperature scaling through their influence on attention weighting, made persistent via residual connections. Whether this is mechanistically accurate is an open empirical question.

---

## 7. Discussion

### 7.1 The Masking Test Gap

Five experiments (exp-03 through exp-03d) were designed to produce a clean Persona-overrides-Instructions demonstration: strong P_p detects and overrides a prohibition; weak Persona follows the prohibition and misses. All five failed on the masking dimension — both weak and strong Persona detected.

The reason is the category overlap problem. Code review tasks have an inherent CI-scope pathway for any vulnerability: any failure that can be framed as "code does not do what it should" has a permitted route that P_p will find. The masking test requires a task structure where this pathway does not exist.

Exp-05 provides the structural equivalent from a different angle: a premise-rejection task where the finding is architectural and cannot be framed as a CI concern. P_p 10/10 rejected the compliance premise. P_d 10/10 validated it. The split is on reasoning posture, not verdict label. This is the behavioral content the masking test was designed to expose — just through architectural premise rejection rather than Instructions override.

The Instructions override mechanism exists and has been named (scope re-framing, premise-undermining, explicit override). The challenge is demonstrating the split cleanly against the baseline. That demonstration requires a task domain where no permitted re-framing pathway to the prohibited finding exists.

### 7.2 The Self-Prediction Gap

The authoring model systematically underestimates P_p Persona strength (the descriptive/enactive register distinction is developed in §3.1.1). The practical consequence is that prompt authors cannot calibrate P_p strength by inspection — the estimate will be low. Variant L (exp-01e) was predicted at 6/10; it scored 10/10.

**Empirical confirmation (exp-06):** A meta-experiment submitted this paper as the code artifact for review — with P_p and P_d variants reviewing the paper itself. The P_p reviewer (Variant A) identified seven structural critiques, including weaknesses the paper's authors had not anticipated. The P_d reviewer (Variant B) identified real weaknesses but with lower specificity on the mechanistic claims. Most notably, 4/5 A-run reviewers independently identified the few-shot / procedural-content confound (§7.4) — the strongest challenge to the central claim — which did not appear in any B-run. The self-prediction gap is not only a claim about Persona calibration; it is also a demonstration of the consideration-set mechanism applied to an abstract document: the P_p reviewer reached an argument the authors did not, because its search algorithm was installed to find structural gaps in the claim architecture.

**Design implication:** Treat P_p evaluation as an empirical question, not an authorial judgment. Run the Persona before relying on it. Budget for the possibility that a well-constructed P_p will perform significantly above its author's expectation — and that a poorly constructed one will perform below it. The self-prediction gap cuts both ways: overconfident P_p framing also underperforms its author's expectations, just in the other direction.

### 7.3 The Few-Shot / Procedural-Content Confound

The central claim is that the *Persona slot* — specifically P_p identity framing — drives the consideration-set effect. The strongest challenge to this claim, identified by 4/5 P_p reviewer runs in exp-06, is that P_p prompts embed task-relevant procedural reasoning in the identity description itself. A P_p Persona like "after you understand how the lock is acquired and renewed, you ask what happens to the critical write if the lock has already expired" contains the failure-mode reasoning explicitly. A reader who follows that text as a reasoning sequence — regardless of whether it is in a Persona slot or an Instructions slot — may produce the same output.

If the effect is attributable to the procedural *content* rather than the Persona *slot*, the consideration-set mechanism is better described as a form of implicit chain-of-thought prompting. The P_p framing may be effective not because it installs identity but because it provides the reasoning scaffold directly.

**Experimental status:** exp-07c was designed to isolate this confound by swapping the P_p procedural content into the Instructions slot (Variant C) while keeping a generic P_d Persona, and comparing against the full P_p framing (Variant I) and the P_d baseline (Variant J). The experiment was confounded by a code-visible hint in the test artifact (a log line naming the failure mode) that equalized performance across all variants — making it impossible to isolate the slot effect. The few-shot confound is therefore an explicitly open question.

**What can be said:** The behavioral predictions generated by the consideration-set framing are correct. P_p prompts outperform P_d prompts on structurally hidden failure modes across multiple experiments. The mechanism that produces this effect — whether identity installation, implicit CoT, or both — has not been isolated. Future work would require a slot-swap experiment on a structurally hidden failure mode where no code-level hint exists.

### 7.4 The Consideration-Set Boundary Condition

exp-07c established a boundary condition for the consideration-set claim: **the P_p advantage is specific to structurally hidden failure modes. When a failure mode is signaled in code, P_d can find it through code reading.**

| Failure mode visibility | P_p result | P_d result |
|------------------------|------------|------------|
| Structurally hidden (exp-01e) | 10/10 | 0/10 |
| Code-visible hint (exp-07c) | 2.5/10 weighted | 3.0/10 weighted |

The "code-visible" condition in exp-07c was a single log line: `logger.warning("Heartbeat detected lock loss key=%s", lock_key)` followed by a `return` with no main-thread signal. Any careful reader notices this gap; no structural inference is required. P_d found it at the same rate as P_p.

This is a more precise statement of the consideration-set claim than the paper's earlier formulation. The claim is not "P_p finds things P_d cannot" in general — it is "P_p expands the set of *reachable* failure modes when those failure modes require structural inference beyond what is explicit in the code." When the code makes the failure mode visible, both Persona types can reach it.

A secondary behavioral observation from exp-07c: P_p's comprehensiveness trades off against depth on any single finding under a token ceiling. When the code provides many legitimate findings, P_p generates more of them — spreading fixed token budget across a larger set, reducing depth per finding relative to P_d's narrower search. This is a new behavioral observation, not anticipated by the prior framework.

### 7.5 The Chain-of-Thought Alternative

This paper does not engage the chain-of-thought (CoT) literature (Wei et al. 2022; Kojima et al. 2022) as an alternative explanation for the P_p effect. The omission was identified in exp-06 as a theoretical gap. The relationship between PARC's Persona mechanism and CoT prompting deserves explicit treatment.

**Where the accounts agree:** Both CoT prompting and P_p framing improve performance on reasoning tasks requiring multi-step inference. Both work by structuring the model's intermediate reasoning rather than merely specifying the desired output. Both have been shown to transfer across task domains.

**Where the accounts differ:** Standard CoT prompts operate in the Task Layer — they tell the model *how* to reason for this task. P_p operates in the World Layer — it encodes *who* the model is, with the procedural steps embedded in identity rather than instruction. The behavioral consequence, if the mechanism is real, is that Task-Layer CoT is prompt-specific (the model reasons this way for *this* task) while World-Layer P_p is identity-persistent (the model reasons this way as part of *who it is*, across tasks). Whether this distinction produces different behavioral outcomes — and under what conditions — is an open empirical question. The few-shot confound question (§7.3) and the slot-swap question are effectively the same question asked experimentally.

**What this paper can claim:** P_p prompts produce the observed behavioral effects. Whether those effects are better attributed to World-Layer identity installation or Task-Layer implicit CoT has not been isolated. The PARC framework is presented as an organizational structure that generated correct predictions; the mechanistic account remains a hypothesis.

### 7.6 P_p/P_d Operationalization

The P_p/P_d distinction is described qualitatively in §3.1.1 but has no formal operationalization — no coding scheme for classifying a given Persona as P_p, P_d, or a mixture. Exp-06 reviewers identified this as a reproducibility gap: a researcher attempting to apply the framework cannot reliably determine whether a given Persona qualifies as P_p without running experiments.

A provisional coding heuristic: a Persona is P_p if it contains at least one first-person procedural clause that specifies a reasoning step contingent on a prior state — "after I understand X, I ask Y" — where X is a domain-specific state and Y is a structural inference that does not follow trivially from X. A Persona is P_d if it encodes behavioral commitment without contingent procedural steps: "I analyze deeply, I do not let issues go unexamined." Most real Personas are mixed; P_p strength scales with the number and specificity of contingent procedural clauses.

This heuristic is not validated against the experimental record. The papers' P_p Personas were constructed intuitively and validated behaviorally. A formal coding scheme with inter-rater reliability testing would strengthen reproducibility claims and is identified as necessary future work.

### 7.7 Practical Design Rules

From the experimental evidence:

1. **Write the Persona first, and write it procedurally.** Credentials describe expertise; procedures enact it. "I ask whether the write is fenced before I approve the merge" is load-bearing. "Senior software engineer" is not.

2. **Context should be specific and scoped, not comprehensive.** A three-sentence Context that correctly identifies the domain and the concern outperforms a paragraph that names the domain and adds noise. Context does the setup; Persona does the reasoning.

3. **Choose Stakes type intentionally.** Identity Stakes extends post-finding elaboration — use it when depth of argument matters. Task Stakes suppresses secondary enumeration — use it when primary convergence and crisp termination matter. Identity Stakes on P_d is the most expensive failure mode available.

4. **Treat Instructions as a fence, not a guide.** Instructions define what is prohibited, not what is desired. Desired behavior belongs in Persona. A long Instructions block signals that Persona is not carrying its weight.

5. **Request should be one lean sentence.** All compression work happens in the World Layer. A bloated Request adds noise to the Query vector without improving the answer.

6. **Audit token counts, not just outputs.** A model hitting the token ceiling consistently is telling you it has no termination condition — not that it is thorough. Early termination from a P_p Persona means the finding converged and the model stopped. Consistent ceiling hits from a P_d Persona mean the search algorithm is absent.

---

## 8. Conclusion

PARC organizes prompt engineering around a central finding: **Persona — specifically its procedural sub-component — is the primary carrier of reasoning quality. Everything else operates on what Persona has already installed.**

The consideration-set mechanism is the experimental core of this claim. Weak Persona + rich Context = 0/10 on hidden structural failure modes. Strong P_p + minimal Context = 10/10. This is not a difference in depth of reasoning within a fixed space. It is a difference in which reasoning classes exist in the reachable space at all. Context does not install the identity that asks the right question. Instructions do not supply the reasoning that Persona is missing. Stakes amplifies what is there — direction, termination, depth — but generates nothing where Persona has provided nothing.

The P_p/P_d distinction sharpens this: disposition language installs engagement energy without a convergence target, producing comprehensive output over the wrong priority. The P variant (exp-01f) is the archetype — maximally engaged, fully committed, 1/10. The search algorithm is absent regardless of how much energy is applied to the search.

Stakes is not a general sharpening operator. It is an amplifier with direction determined by Persona type and asymmetric dynamics depending on whether P_p is present. Identity Stakes extends P_p's post-finding output; it drives P_d toward confident maximum-token wrong-direction failure. Task Stakes gives P_p a logical stop condition; it terminates P_d's wrong-direction search at confident completion. The two-vector formula $R = P \times (1 + \alpha_{amp} S_i - \beta_{brake} S_t)$ captures these dynamics with empirically grounded coefficients.

Instructions compress output, not cognition. The ~11% elaboration coefficient is a stable measurement of what a prohibition does: it suppresses how much of the reasoning is expressed, not whether the finding forms. This has production consequences — monitoring output length detects prohibition effects; monitoring decision quality does not.

The CO-STAR comparison makes the practical case. Against a prompt generated independently with no knowledge of this framework, PARC's P_p variant rejected an architecturally flawed compliance requirement 10/10 times. CO-STAR's dispositional Persona validated it and patched within it 10/10 times. Both prompts were sophisticated. Both produced "Do Not Merge" verdicts. The difference is not capability — it is frame installation. P_p read the requirement, asked whether the stated implementation is the only way to satisfy it, and rejected the framing before engaging with the code. The frame never installed. P_d accepted the compliance prior and processed everything downstream inside it.

**Stakes determines when the model stops. Persona determines the boundaries of the search.**

The implication is a shift in how prompt engineering should be conceptualized. Engineering asks: have I specified the task completely enough? Architecture asks: have I shaped the space correctly before I specify the task? PARC is an answer to the second question. The framework does not make specification irrelevant — the Task Layer matters. But the Task Layer operates within a space that the World Layer has already constrained. If the World Layer is wrong, no amount of Task Layer specification repairs it. If the World Layer is right, the Task Layer needs very little. This is the principle that separates prompt architecture from prompt engineering, and it is what the experimental record demonstrates.

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
| exp-05 | 20 | claude-sonnet-4-6 | CO-STAR head-to-head; P_p 10/10 premise rejection; P_d 10/10 compliance validation; frame installation as the mechanism |
| exp-06 | 7 | claude-sonnet-4-6 | Meta-experiment: P_p and P_d review of this paper (5 A-runs, 2 B-runs). Self-prediction gap confirmed empirically; few-shot confound identified as primary open question |
| exp-07c | 30 | claude-sonnet-4-6 | Boundary condition: consideration-set effect operates on structurally hidden failure modes, not code-visible ones; slot-swap test confounded by code-level hint |

**Total runs:** 677 across 13 experiment series.
**Total cost:** ~$6.60 across all runs. This figure reflects the scale constraints of the experimental program (n=10 per variant; single-model primary validation; one active research institution). Low cost is not presented as an efficiency signal — it is a consequence of small n, which limits generalizability. Production validation at higher n and across additional model versions would require proportionally larger budgets.

---

## Appendix B: Behavioral Claim Register

Full list of experimentally confirmed behavioral claims, each with experimental basis:

| Claim | Basis |
|-------|-------|
| Strong P_p → convergence on hidden structural failure modes | exp-01e (I: 10/10), exp-01f (M, O: 10/10), exp-01g (I: 10/10) |
| Weak Persona + rich Context → 0/10 on hidden failure modes | exp-01e (J: 0/10), exp-01g (J: 0/10) |
| P_d without P_p ≈ weak Persona on trap detection, regardless of Stakes | exp-01f (P: 1/10, all ceiling hits) |
| Context is a non-scaling constant once P_p is present | exp-01f (M vs. O: 10/10 both with and without rich Context) |
| Stakes amplifies existing Persona signal; does not generate signal from P_d alone | exp-01b, 01c, 01f, exp-02 |
| Instructions and Persona act on orthogonal dimensions | exp-01a/b (Variant B: strong Persona bled through exhaustive checklist) |
| Token ceiling is a failure diagnostic on standard models | exp-01e/f (N, P, J: ceiling hits on all failure-mode runs) |
| The above effects transfer zero-shot across model families | exp-01g (Gemini 2.5 Pro) |
| Strong P_p + prohibition → scope re-framing through permitted channel; finding preserved | exp-03b/03c (A: 10/10 Request Changes in both) |
| Prohibition compresses output to ~11% of unconstrained depth without affecting detection | exp-03b (12.8%), exp-03c (11.3%), exp-03d (11.0%) |
| P_p routes through minimum-cost permitted channel under prohibition | exp-03c (A: IDOR framing 10/10 despite P_p encoding mass assignment as primary) |
| Semantic anchors are sufficient for scope re-framing; structural enumeration not required | exp-03c (B: 10/10 without field enumeration) |
| Test coverage gap as CI-scope anchor is always available in code review | exp-03d (A: 10/10 scope re-framing without description anchor) |
| Consideration-set boundary: local (within-function) vs. global (cross-service) | exp-04c (D: 0/10 cross-service; A/B/C: 10/10 cross-service) |
| Token ordering D < A < B < C robust across calibration states | exp-04, exp-04b (D correct), exp-04c (D wrong) |
| Task Stakes produces no ceiling hits even on complex distributed scenarios | exp-04c (A: 0/10 ceiling hits) |
| Identity Stakes on P_p: Termination Inhibitor (+710 avg tokens post-finding) | exp-02 (A mean 2,210 vs. B mean 1,500) |
| Identity Stakes on P_d: ceiling pressure (ceiling rate 9/10 vs. 4/10) | exp-02 (C vs. D) |
| Task Stakes: Entropy Brake (−578 tokens vs. no Stakes; coefficient from exp-04b) | exp-04b (A→C: +578; A→B: +236; A→D: +67) |
| Stakes type effect 3–4× Persona-strength effect on elaboration when detection is held constant | exp-04b (Stakes type: +236; Persona strength: +67) |
| P_p rejects architecturally flawed premises regardless of compliance framing | exp-05 (A: 10/10 premise rejection) |
| CO-STAR Context prior overrides explicit Objective instruction; frame installed before code is read | exp-05 (B: 10/10 compliance validation despite performance Objective item) |
| Entropy Brake natural completion scales with task type: ~2,143 tokens (detection), ~2,427 (premise rejection) | exp-04c (A mean 2,143); exp-05 (A-05: 2,427) |
