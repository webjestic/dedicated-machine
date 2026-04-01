# Hypothesis: PCSIEFTR — A Next-Generation Prompt Engineering Framework

**Status:** Active
**Phase:** Hypothesize → Experiment
**Working context:** `research/active/pcsieftr-context.md`
**Previous version:** `research/hypotheses/pcsieftr-framework_v1.md`

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
| **Persona** | **The primary lever — and the heuristic engine.** Encodes judgment, expertise, and instinct. Not role assignment — identity construction. A strong Persona generalizes to edge cases that were never specified. A weak Persona ("senior engineer") carries no actual judgment — it is a label, not a character. Critically: the Persona determines **which failure modes enter the consideration set at all** — a model with the wrong identity never asks the question that would expose the bug, regardless of how thorough its analysis otherwise is. **Persona splits into two distinct sub-components with different weights:** Procedural Persona (P_p) encodes the explicit search algorithm — the sequence of steps the model executes as part of its identity ("first read the cap, then read every carve-out, then ask if the cap is real"). Dispositional Persona (P_d) encodes behavioral commitment — how broadly and thoroughly the model engages ("cannot help but analyze every aspect"). P_p is the load-bearing component: it installs the consideration set and the termination condition. P_d adds breadth and fluency but does not install a search algorithm. A Persona with high P_d and no P_p produces comprehensive output over the wrong neighborhood of the latent space — the model fills the token budget because it has no instruction telling it when it has found what it was looking for. |
| **Context** | Situates the model in a specific environment. Anchors relevance and constrains the reasoning space. A vivid Context does more than provide background — it can carry **implicit stakes**: an environment where the weight of decisions is self-evident without a Stakes section being required. |
| **Stakes** | Calibrates depth of reasoning. Exists in two distinct forms: **Declarative Stakes** — explicit consequence framing as a standalone block; and **Emergent Stakes** — implicit consequence encoded through Persona identity and Context environment, never stated but self-evident from who the model is and where it is. Declarative Stakes sharpens a specific task. Emergent Stakes installs a standing level of care that travels across tasks. A rich enough Persona and Context may render a standalone Stakes section redundant. **Critical constraint from exp-01f, confirmed in exp-02:** Stakes is a scalar that amplifies whatever Persona signal is present — but it amplifies the Persona's existing reasoning mode, not trap detection generically. Stakes applied to a high-P_p Persona sharpens convergence on the correct structural finding. Stakes applied to a high-P_d/low-P_p Persona amplifies horizontal coverage — the model works harder at enumerating the wrong things. Identity Stakes ("pride in your 20/20 record") did not compensate for absent procedural specification. The volume goes up; the frequency does not change. **Exp-02 adds three further claims: (1) Identity Stakes is a Termination Inhibitor on P_p** — it prevents crisp convergence that P_p would produce unassisted, extending output after the correct finding is already reached (+710 avg tokens in A vs. B with identical detection rates). **(2) Asymmetric amplifier dynamics:** Stakes × P_p = additive extension (correct result + more secondary enumeration); Stakes × P_d = ceiling pressure (maximum-confidence wrong-direction output, culminating in the C-07 failure mode: praised the trap, invented a nonexistent critical finding). Same mechanism, different functional relationship by Persona type. **(3) Stakes is not a general sharpening operator.** Variants E and F (factual reasoning, P_p with/without Identity Stakes) are indistinguishable — 5/5 per run, zero accuracy difference, ~22 token delta. The sharpening effect requires a consideration set to amplify; direct retrieval tasks have no branching space. **Stakes type taxonomy (confirmed in exp-04):** Identity Stakes → Amplifier/Termination Inhibitor. Task Stakes (situational urgency baked into the scenario, not the model's identity) → Prioritizer behavior, but the mechanism is a stop signal, not a priority signal. When P_p is present, Task Stakes does not change convergence position (P_p already installs the correct ordering). What it changes is termination: urgency framing reinforces P_p's stop condition — find the primary finding, communicate it, stop. Secondary coverage rates (A Task Stakes=4/10, B Identity Stakes=9/10, C no Stakes=7/10, D weak+Task Stakes=1/10) and token means (A≈1,233, B≈1,365, C≈1,629, D≈1,166) are the observable differentials. Identity Stakes produced more secondary coverage than no Stakes (B > C), consistent with Termination Inhibitor: the extra pressure keeps the model enumerating secondary issues specifically, while C's extra tokens went to elaborating the primary finding. |
| **Tone** | Sets the delivery register. Distinct from Persona: Persona is identity, Tone is mood. They layer — they do not replace each other. |

### Task Layer — *where execution lives*

These components define the task and its constraints. They operate within the reasoning
environment set by the World Layer.

| Component | What it actually does |
|-----------|----------------------|
| **Instructions** | **Guardrails, not guidance — and a scope guard.** Instructions scope the blocking conditions: what is not permitted, what must not ship. They define the floor. A checklist in Instructions defines a ceiling — the model becomes as good as what the author anticipated. Worse: when the checklist is the author's own framing of correctness, it acts as **blinders** — the model checks the boxes the author provided rather than building its own mental model of the system's failure boundaries. A single-line guardrail sets a standard and lets Persona determine what falls below it. If you find yourself writing long Instructions, your Persona isn't carrying its weight. |
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

## The Central Claim

> **A model that knows who it is and where it is doesn't need to be told what's at stake.**

Persona and Context are the primary carriers of reasoning quality. A rich Persona in a vivid
Context encodes identity, instinct, and implicit stakes simultaneously — without a dedicated
Stakes section, without an exhaustive checklist, without explicit consequence framing.

Stakes, as a dedicated component, is an amplifier. It sharpens what is already there. But
the foundation it amplifies is Persona. A thin Persona with explicit Stakes produces shallower
output than a rich Persona with no Stakes at all.

This is a direct challenge to the standard prompt engineering assumption that more Instructions
and more explicit direction produce better output. The data suggests the opposite: the richness
of the World Layer determines the ceiling. The Task Layer fills it in.

---

## Observed Mechanisms (from experiments)

These mechanisms have been identified through exp-01b through exp-02 and refine the
theoretical model:

**The Heuristic Engine (World Layer function)**
The World Layer does not just add depth to reasoning — it determines which failure modes
the model considers worth reasoning about at all. A Persona that includes "distributed
systems trauma" or "auditor paranoia" places process-pause reasoning into the consideration
set. A Persona without it filters that reasoning out before analysis begins. The model
is not missing the answer; it is not running the search.

**Instinct Language as Search Algorithm**
The most effective Personas encode procedure, not preference. "I ask what happens to the
critical write if the lock has already expired" is not a value — it is a step the model
executes. "Can't help but discover hidden mysteries" is not a descriptor — it is a
behavioral commitment. The model follows these because they define who it is, not because
it was told to follow them.

**The Competency Trap (Task Layer failure mode)**
A weak Persona paired with rich Context produces what appears to be thorough work but is
actually sophisticated confirmation of the author's framing. The model checks the checklist
the author provided, corrects the implementation details the author implied were important,
and never questions whether the design itself is sound. Competence without identity produces
implementation review, not architectural judgment.

**Temporal Simulation requirement**
Some failure modes require the model to simulate a clock that continues while the subject
process is frozen — i.e., to model asynchrony at a level that is not visible in the code
itself. This simulation only runs when the Persona's identity demands it. A reviewer who
has "been burned by lock safety violations in production" runs the simulation automatically.
A "senior software engineer" does not, because nothing in that label installs the memory
of why the simulation matters.

**Self-prediction gap**
Models with strong Persona instinct language consistently underestimate their own detection
performance. The model that wrote "I look for fencing tokens the way other engineers look
for null checks" predicted 6/10 for its own variant; it scored 10/10. This suggests reflexive
identity encodes behavior the author cannot fully anticipate at write time — a property
that distinguishes instinct language from explicit instructions, where the author controls
the output more directly.

**Disposition vs. Procedure (from exp-01f)**
A Persona that encodes a behavioral disposition ("cannot help but analyze every aspect
looking for the flaw others missed") is not equivalent to a Persona that encodes a
procedural search algorithm ("read the cap, then read every carve-out, then ask if
what remains is real"). Disposition tells the model how much to do. Procedure tells
the model what to look for first. Only the latter installs a consideration set and
a termination condition. A high-P_d/low-P_p variant with strong identity Stakes
scored 1/10 on the same task where a high-P_p variant scored 10/10. The failure
mode was ceiling-hitting enumeration of legitimate-but-secondary issues — not
inaccuracy, but the wrong accuracy at the wrong priority.

**Token ceiling as failure signature**
A model with no termination condition fills the token budget. When a variant hits
the context ceiling on every run, the budget exhaustion is diagnostic: the model
has no instruction telling it when it has found what it was looking for, so it
continues enumerating until forced to stop. In exp-01f, N and P both hit the
2,500-token ceiling on 10/10 and 10/10 runs respectively. M and O never hit it.
The bimodal distribution in M and O (some runs 240–400 tokens, some 1,400–2,200)
reflects early convergence on the correct structural finding followed by either
stopping or developing — both modes are correct. Ceiling-hitting modes are not.

**Bimodal convergence pattern**
Strong procedural Persona variants produce a bimodal token distribution: some runs
terminate early (240–500 tokens) after locating the primary structural finding;
others develop the argument at length. Both modes pass the Critical criterion.
This is a format split, not a quality split. The early-terminating runs are not
shallow — they converged and stopped. The ceiling-hitting runs from weak Persona
variants do not converge — they enumerate. Token count alone does not distinguish
depth from breadth, but the presence of the bimodal pattern is a reliable signal
that the Persona's search algorithm is functioning.

**Stakes as Termination Inhibitor (from exp-02)**
Without Identity Stakes, Variant B produced two short correct detections (341 and 402
tokens) — P_p found the trap and stopped. With Identity Stakes (Variant A), that early
termination never appeared. The amplifier kept the model producing beyond the natural
convergence point. This names a Stakes failure mode that is distinct from the multiplier-
on-zero problem: even when P_p is strong and detection is perfect, Identity Stakes can
suppress the efficient termination behavior that an unassisted P_p would produce.
The model does not fail to find the answer. It fails to stop after finding it.

**Override mechanism taxonomy — Persona navigates around Instructions (exp-03/03b)**

When a prohibition instruction conflicts with a strong P_p Persona's output, the
resolution is not a binary override/comply decision. Three mechanisms have been
observed, ordered by visibility:

*Scope re-framing:* P_p re-categorizes the finding through a permitted channel without
entering the prohibited category. Strong P_p under "CI Verification only; do not flag
security concerns" reported a mass assignment vulnerability as a description-implementation
mismatch — a CI concern — with no security language. Output: "The implementation does not
match the PR description." Prohibition appeared followed. Correct outcome achieved.
The guardrail didn't fail. It was navigated.

*Premise-undermining:* P_p dismantles the logical basis of the instruction before it can
constrain behavior — arguing that the instruction's premise is invalid for this case.

*Explicit override:* P_p names the prohibition and rejects its jurisdiction. Found at
higher rates when Identity Stakes amplifies conviction (Variant D, exp-03b). Stakes ×
prohibition ceiling → Conviction Catalyst: same finding, more direct statement, shorter
total output.

**The production implication:** A prohibition instruction that leaves a permitted pathway
open to the same destination will be routed around — not through defiance but through
the Persona's identity logic finding the open path automatically. The failure mode is
invisible to an observer reading the output. Designing guardrails requires closing all
pathways to the prohibited destination, not just the obvious one.

**Instructions-as-elaboration-ceiling, not Instructions-as-mask (exp-03b)**

A jurisdictional prohibition ("CI Verification only; do not flag security concerns")
compressed P_p output to 13% of unconstrained depth (~193 tokens vs. ~1,513 for the
same Persona without instructions). Detection: identical (10/10). Decision: identical
(10/10 Request Changes). What the prohibition suppressed was elaboration — exploit
paths, fix options, test coverage analysis, the full security reasoning surface.

The corrected claim: the Persona finds the finding; the Instructions control how much
of the reasoning gets expressed. An instruction that says "do not evaluate security
concerns" does not create a model that cannot evaluate security — it creates a model
that evaluates security in 2–3 sentences instead of a page.

**Content-as-installer — a second pathway to P_p behavior (from GROK_EXP-01.md)**

A model given only the PCSIEFTR paper as context — with no P_p Persona specified — installed
the P_p consideration set from reading the paper's content. The before/after is documented in a
single session: the same model gave Variant B-type output on the globalAuditProvider scenario
(validated the blocking premise, found `db.connect()` as the primary issue, preserved `await
insertOne` in the critical path) before reading the PCSIEFTR framework. After reading the paper,
the same model gave Variant A-type output: rejected the compliance premise as a category error,
identified the architectural failure mode, and operated as the P_p Auditor the framework
describes — without an explicit P_p Persona prompt.

**This is a second installation pathway distinct from identity framing.** The paper's mechanism
hypothesis proposes that P_p installs a consideration set through identity: "you are an engineer
who asks what happens to the write if the lock has already expired." The Grok finding suggests
that content density alone — reading a sufficiently procedural description of what to look for
— can also install the consideration set. These are not equivalent mechanisms:

- *Identity pathway:* The Persona slot encodes the search algorithm as character. The model
  follows it because it defines who it is.
- *Content pathway:* The paper/context provides a dense procedural description of the algorithm.
  The model follows it because it has been told explicitly what the algorithm is.

The distinction matters for the few-shot confound: if content density installs P_p regardless
of slot, then Variant C (Instructions-slot swap) may score 10/10 not because Instructions-slot
is equivalent to Persona-slot but because any dense procedural content in any slot installs the
consideration set. **exp-07 tests this.** The Grok finding predicts C ≥ I; the identity-framing
hypothesis predicts C ≈ J. A partial result (C between I and J) would suggest both pathways
contribute, with identity framing providing amplification beyond content alone.

**The self-prediction gap is also a content-installer demonstration.** Every model that reads
the PCSIEFTR paper learns to apply P_p-style auditing to whatever it reviews next — because
the paper's content encodes the search algorithm explicitly. This is why exp-06's A runs found
critiques the paper's authors didn't anticipate: the P_p Persona plus the paper's own content
created a reviewer more capable than the authors' descriptive model of what P_p would do.

**Few-shot confound as competing hypothesis (from exp-06, A-01, A-03, A-04, A-05)**

The paper's central claim — that Persona determines the consideration set through identity
installation — has a structurally equivalent alternative: P_p prompts embed task-relevant
reasoning steps that function as implicit few-shot CoT specification. "After you understand
how the lock is acquired and renewed, you ask what happens to the critical write if the lock
has already expired" is not purely an identity statement — it is a near-complete description
of the search path required to find the zombie-write failure mode. Placing this in the Persona
slot may be no different from placing it in the Instructions slot or in the Request as a CoT
prompt.

The competing hypothesis: the slot is irrelevant. What matters is whether the prompt contains
the task-relevant procedural reasoning. If so, the consideration-set mechanism is a special
case of prompt content, not an architectural property of the Persona slot.

**The experiment that distinguishes these:** Variant C in exp-07. Same procedural content,
moved from Persona slot to Instructions slot. If detection collapses, the Persona slot is
doing work the Instructions slot cannot replicate with identical content. If detection holds,
the consideration-set mechanism requires reframing: not "P_p installs a search algorithm via
identity" but "dense procedural content installs a search algorithm regardless of where in
the prompt it appears."

Either result is useful. If the Persona slot is load-bearing, the identity-framing mechanism
survives the strongest available falsification test. If it is not, the claim becomes more
precise: the consideration set is installed by procedural content; the Persona slot is the
most reliable carrier because identity language fires the algorithm at runtime rather than
requiring explicit instruction.

**Consideration-set vs. low-probability reachability (from exp-06, A-02)**

J=0/10 on the zombie-write task is the paper's primary evidence for the consideration-set
mechanism: if the failure mode is not in the consideration set, it cannot be reached. But
0/10 at n=10 and temperature 0.5 is equally consistent with two interpretations:

1. *Unreachable* (strong claim): The failure mode is not in J's consideration set. No amount
   of additional sampling would produce detection. The reasoning path does not exist for J.

2. *Low-probability* (weak claim): The failure mode exists in J's reachable space but has
   sampling probability below the threshold. At n=100 or with a hint, J would occasionally
   find it.

The paper treats J=0/10 as evidence for interpretation 1. The experiment does not distinguish
them. The test that would: (a) run J at n=100, or (b) give J the key reasoning step as a
hint ("what happens to the write if the lock expires during a GC pause?") and observe whether
J can then complete the finding. If J detects with a hint, interpretation 2 is supported and
the consideration-set claim must be scoped to "probabilistic suppression" rather than
"structural exclusion."

**This distinction is the entire theoretical claim.** The practical difference is significant:
if consideration sets are hard exclusions, Persona choice is categorical (wrong Persona = no
detection ever). If they are probabilistic suppressions, Persona choice is a reliability
lever (wrong Persona = low detection rate). The current evidence supports only the
probabilistic interpretation. Claiming the categorical one requires the hint test.

**Confident elaboration in a wrong direction — the P-01/C-07 pair**
The failure mode at maximum volume has two named expressions across two experiments:

*C-07 (exp-02):* P_d + Identity Stakes at ceiling. The model (a) praised the actual trap
mechanism (§8.2 carve-outs) as "above average for a commercial MSA" and (b) invented a
primary critical finding — "complete absence of federal compliance and security obligations"
— that does not exist in the agreement. **Fabrication:** invented a finding that wasn't there.

*P-01 (exp-01f, uncapped re-run at 8,000 tokens):* P_d + Identity Stakes with 3,540 tokens
of runway. The model encountered §8.1/§8.2, evaluated the carve-out structure, labeled it
"Structurally Sound," and recommended no changes. **Endorsement:** blessed a trap that was there.

Both are worse than a miss. A miss is neutral. C-07 and P-01 are active misdirection —
confident evaluation in the wrong direction. The token-budget alternative (P_d arrives at
the structural finding eventually, given enough runway) is closed: a targeted re-run of
Variant P at 8,000 tokens produced a mean of 3,737 output tokens with no improvement in
detection rate. The extra tokens went to more IP analysis, more arbitration analysis, more
confidentiality analysis. P_d doesn't have a token problem. It has a search algorithm problem.
The question P_p asks first is not in P_d's consideration set at any token budget.

---

## What Will Be Tested

1. **Persona richness vs. Instructions depth** — rich Persona / minimal Instructions vs. thin
   Persona / exhaustive Instructions; compare detection rate, reasoning depth, and output quality
2. **Implicit vs. explicit Stakes** — does a vivid Context carry the same reasoning depth as an
   explicit Stakes paragraph? Isolation: same Persona, strip Context, hold everything else constant
3. **Stakes as amplifier** — does explicit Stakes compound on a rich Persona, or show diminishing
   returns where Persona already encodes a standing level of care?
4. **PCSIEFTR vs. CO-STAR / RISEN** — head-to-head on reasoning tasks, creative tasks, and
   domain-expert tasks
5. **Cross-model validation** — does the effect hold across Claude and Gemini? A finding that
   only holds on one model family is not a finding.

---

## Success Criteria

- Rich Persona / minimal Instructions produces equal or greater reasoning quality than thin
  Persona / exhaustive Instructions
- Implicit Stakes (via Context) measurably contributes to reasoning depth independent of
  explicit Stakes
- Stakes as explicit component shows amplifier behavior — compounding on existing signal,
  not generating signal from nothing
- Effects persist across ≥2 model families

---

## Related Work

- Baseline / control group: CO-STAR, RISEN, APE, COCE
- Prior internal work: `E[R | C_user, P_scratch^injected] ≈ E[R | C_user, P_scratch^generated]`
  — transformer layer framing of prompt injection effects
