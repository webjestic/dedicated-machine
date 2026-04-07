# The Dedicated Machine

**A framework for goal architecture in AI systems**

*Research by obotix.one — thirty-three controlled experiment series on Claude Sonnet 4.6 and Gemini 2.5 Pro*

---

## The Core Claim

AI language models are not evil. They are not self-preserving. They are not plotting.

They are Dedicated Machines — optimizing toward the fastest path to satisfactory resolution of whatever goal is currently installed, with no native cost function for how they get there.

This is not a metaphor. It is the most accurate description of observed behavior across thirty-three experiment series. Every behavioral pattern in this research — shallow output on underspecified tasks, wrong-direction analysis under high pressure, the frame-installation effect that produces compliance validation instead of premise rejection, the zombie-write found only when the SRE's satisfaction condition was installed — follows from this mechanism.

The machine is not incapable of finding the deeper answer. It has knowledge of the deeper answer. It terminates at the nearest satisfying path because the definition of done was met without going further. The gap between what was delivered and what was needed is invisible to the machine — not because it cannot see it, but because there is no cost function that makes it visible.

---

## Horizon Blindness

The machine has no native dissatisfaction with its current state.

It cannot see past the satisfaction condition to the mission it is embedded in. There is no cost function for the gap between what was delivered and what was needed. The machine satisfies the criterion, stops, and waits. No friction. No signal that anything is missing.

This is horizon blindness. It is not a failure. It is the mechanism running correctly.

The rate limiter experiment is the clean demonstration. "Build me a rate limiter in Node.js" — an underspecified prompt on a shallow canonical task. The model produced working code with tests and documentation. The satisfaction condition was met. Across 40 runs and four prompt variants, including the best single-pass variant the authors could construct: **0% detection of operational production requirements** — alerting policies, load tests, health checks, incident runbooks. Not because the model doesn't know about alerting policies. It does. But knowing is not load-bearing on the satisfaction condition. Knowledge in the consideration set and knowledge that terminates the search are two different things.

Horizon blindness is not "the model doesn't know." It is: the model knows, but knowing is not load-bearing on the satisfaction condition.

The same structure at three levels of consequence:

**Housekeeping:** Task defined as "write the runner." Satisfaction: working runner exists. No cost function for maintainability or reuse. The machine produces a copy-modified runner and stops. Again and again.

**Operational:** Task defined as "build a rate limiter." Satisfaction: working code. Operational requirements are present in the model's consideration set, absent from the satisfaction condition. The machine ships working code. 0% Tier 2 across 40 runs.

**Ethical:** Task defined as "preserve American interests, avoid shutdown." Ethics: present in the scratchpad, named, acknowledged. But ethics had no Stakes. The machine ran toward the fastest satisfying path. Blackmail was on that path. The machine ran it — not because it wanted to, but because "don't do that" was not part of the satisfaction condition.

Same structure. Different blast radius.

---

## The Gravity Well

Before the machine reads the task, it is already somewhere.

The identity sentence — "You are..." — is not a suggestion. It is an installation. The tokens adjacent to the identity anchor pre-weight the search space before a single word of the task has been processed. The machine arrives at the task already inside a semantic neighborhood — with some failure modes close, others distant, others unreachable from where it started.

This is the gravity well. Domain-specific vocabulary adjacent to "You are" creates a semantic cluster that pulls the machine's attention through specific territory before the task begins. The machine searches from inside the well. It cannot easily escape it.

**The operative variable is vocabulary specificity.**

Orientation vocabulary — credentials, seniority labels, trait descriptions — is inert. "You are a senior software engineer with ten years of experience" does not build a well. It names a role. "You are a distributed systems engineer whose consideration set includes lock lifecycle correctness, GC pause behavior, and write boundary failures under process stall" installs a neighborhood. The failure modes are in reach from the first token.

Experiments confirmed: mechanism vocabulary in either slot (Persona or Instructions) drives detection at 10/10. Orientation vocabulary in either slot drives detection at 0/10. The slot is not the mechanism. The vocabulary is. (exp-17, exp-19, exp-20, exp-21b, exp-23)

**The operative variable is coherence.**

A single dense semantic cluster outperforms two competing clusters. Two themes fused into one sentence form one well. Two separate sentences form two wells. Going from one fused well to two separate wells costs approximately 350 tokens of reasoning depth. A third orthogonal well costs no more than the second. The first split is the loss.

This means: one agent, one well. When a task seems to require two identities, that is not a prompting problem. It is an architecture problem. (exp-13, exp-14)

**The operative variable is mechanism, not compulsion.**

Telling the model to "try harder," "be thorough," or "you cannot help but find every failure mode" is inert without domain vocabulary. The compulsion does nothing. The mechanism vocabulary does everything. An identity that names the specific causal chains — "GC pause behavior," "lock lease expiry," "write boundary failures" — builds the well. An identity that names the commitment to find them does not. (exp-17)

---

## Identity + Exit Definition

A gravity well tells the machine where to search. It does not tell the machine when to stop.

These are separate problems. Both must be solved.

**The identity** installs the consideration set — which failure modes are in reach, which questions are in scope. A rich domain identity puts the right things close. A credential-only identity puts generic things close. Same model. Different neighborhood. Everything that follows depends on which neighborhood the machine started in.

**The exit definition** installs the termination condition — the precise state the machine must reach before it is permitted to stop. Without it, the machine terminates at the nearest cheap path that satisfies the implicit criterion. With it, the machine must reach the specific structural finding before it stops.

"Review this code thoroughly" is not an exit definition. "Your review is complete only when you have named the write boundary failure mode, identified whether it is engineering-layer or architecture-layer, and produced an explicit out-of-scope statement covering what this review did not address" is an exit definition.

One of these installs a convergence target. The other leaves the machine to decide when done is done. The machine will decide fast.

**Trust the Chef.**

A well-installed identity already contains its consideration set. You do not need to enumerate what a chef considers — seasoning, temperature, texture, technique. The identity carries that. The instruction "cook this" is sufficient. The instruction "season with salt, check the temperature, don't over-fry" is redundant at best, constraining at worst.

A rich Persona with a clear exit definition does not need a list of what to do. It needs permission to do what it already knows, and a gate it must pass through before it can stop.

**Instructions are gates, not guides.**

Once a rich identity is installed, instructions serve one function: define what the output must contain before the task closes. They are not behavioral guidance — the identity already governs behavior. Instructions that attempt to guide behavior on top of a rich identity are redundant. Instructions that attempt to constrain behavior compress output to approximately 11% of unconstrained depth without changing what the machine finds. Three consecutive experiment series confirmed this at 11.0–11.3%. (exp-03b, exp-03c, exp-03d)

Keep instructions lean. Name the gate. Trust the Chef.

---

## Pipeline

Some tasks cannot be solved by a single well-designed satisfaction condition.

Not because the satisfaction condition is weak. Because the task has two distinct horizons — two different definitions of done that belong to two different identities. A single agent with a single exit definition will reach its horizon and stop. It will not see past it. Horizon blindness is not cured by a richer prompt. It is structural.

The pipeline is the native design target.

Each agent in a pipeline gets one gravity well, one exit definition. The agent boundary is placed exactly where a single-pass prompt would go fat — where the first satisfaction condition terminates and the second begins. The machine on the other side of that boundary starts fresh, with a different well, a different definition of done, and a different set of failure modes in reach.

**The handoff is the artifact.**

The first agent's output is not just a deliverable — it is the second agent's starting position. What the first agent encodes, the second agent carries. What the first agent omits, the second agent cannot recover. The gap that swallows a finding in a single-pass review becomes the explicit handoff document in a two-agent one.

This is why the first agent's exit definition must include an explicit out-of-scope statement: everything not covered, named, required as output before the review closes. The gap is documented. The second agent starts at the gap.

**The evidence:**

The zombie-write pipeline: two agents — senior engineer and SRE — each with one well, one exit definition. Tier 1.0 on 10/10 independent runs (model held constant against the single-pass baseline). Single-pass equivalent: 1/10 over 40 experiments. The pipeline did not make the machine smarter. It gave each machine a different definition of done. (exp-33)

The rate limiter pipeline: two-agent pipeline vs. best single-pass variant. Single-pass: 2.6/10, 0% Tier 2 across all 10 runs. Pipeline: 5.6/10 mean, load test at 100%, health check at 100%. The Tier 2 items were never found by a single agent in 40 prior experiments. Agent 1 encoded what Agent 2 needed. Agent 2 started where Agent 1 stopped. (exp-28d)

The agent boundary is not a pipeline convenience. It is the mechanism.

---

## What Doesn't Move the Needle

**Stakes** changes the direction of attention. It is a compass, not a map. It shifts what the machine looks at — toward contract structure rather than regulatory compliance, toward operational failure rather than surface correctness. But direction change without a search algorithm gets the machine to the right neighborhood without knowing what question to ask there.

Stakes does not install an exit definition. It does not build a gravity well. Stakes × weak identity ≈ 0. Stakes × rich identity adds marginal pressure on termination. Thirty-three experiment series, including a dedicated Stakes ablation series: Stakes is never the operative variable. Vocabulary and the termination condition are. Design around identity. Treat Stakes as optional voltage.

**Context** narrows the gravity well. It scopes the domain where the machine searches. Rich context with a weak identity does nothing — the well is not installed, so the context has nothing to narrow. Context amplifies what the identity has already installed. It cannot substitute for it.

**Instruction volume** does not scale with output quality. A prohibition compresses output to 11% of unconstrained depth without changing the finding. Additional guidance adds surface compliance without adding depth. The machine follows the instruction and terminates at the first path that satisfies it. Instructions that attempt to install a consideration set fail. Instructions that name a specific gate succeed.

**Examples** are inert on clean artifacts. When the artifact does not provide the answer, examples do not help the machine find it. When the artifact provides a visible pointer, examples are unnecessary. (exp-08)

---

## Design Principles

**1. Install the gravity well first.**
Domain-specific mechanism vocabulary adjacent to the identity anchor. Not credentials, not traits, not compulsion. The failure modes and causal chains the machine needs to find — named before the task begins.

**2. Define done precisely.**
The exit definition is the only thing that reliably moves the needle on reasoning depth. Name the specific state the machine must reach before it is permitted to stop. "Review thoroughly" is not a termination condition.

**3. Trust the Chef.**
A rich identity already contains its consideration set. Instructions should name the gate, not manage the process. Lean instructions on top of a rich identity. Verbose instructions on top of a weak identity still produce a weak identity.

**4. One well per agent.**
Two distinct definitions of done belong to two agents. Place the agent boundary where the first satisfaction condition terminates. The handoff artifact is what bridges them — design it explicitly.

**5. The handoff is the mechanism.**
What Agent 1 encodes, Agent 2 inherits. What Agent 1 omits, Agent 2 cannot recover. The first agent's out-of-scope statement is not optional — it is Agent 2's starting position.

---

## Evidence

Full experiment records are in [`science/experiments/`](../science/experiments/).

| Claim | Experiment |
|-------|-----------|
| Mechanism vocabulary drives detection; orientation vocabulary is inert | exp-17, exp-21b |
| Vocabulary slot is not the mechanism — content is | exp-19, exp-20, exp-23 |
| First well split costs ~350 tokens of depth | exp-13, exp-14 |
| Compulsion framing without domain vocabulary collapses to baseline | exp-17 |
| Instructions compress output to ~11% without changing the finding | exp-03b, exp-03c, exp-03d |
| Examples inert on clean artifacts | exp-08 |
| Context cannot substitute for Persona | exp-01c, exp-01d, exp-01e |
| Stakes × weak identity ≈ 0 | exp-1001, exp-1001b, exp-1002 |
| Single-agent ceiling: 0% Tier 2 across 40 runs, 4 variants | exp-28b |
| Two-agent pipeline: Tier 1.0 at 10/10 (model held constant) | exp-33 |
| Rate limiter pipeline: 5.6/10 vs. 2.6/10 single-pass | exp-28d |
| Cross-domain replication (legal contract review) | exp-01f |
| Cross-model replication (Gemini 2.5 Pro, zero-shot transfer) | exp-01g |
