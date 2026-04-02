# You Wrote P_d. You Think You Wrote P_p.

The gap is invisible to you. It was invisible to us — and we built the framework.

---

## What PARC Is

**Persona Architecture for Reasoning and Context.** A two-layer prompt framework built on one mechanism: language models are Dedicated Machines. They terminate at the nearest path that satisfies their installed definition of done. Shallow output is a termination problem, not a knowledge problem.

The formula:

```
PARC = [WORLD: P · S_i · C · T] → [TASK: I · S_t · E · F · R]
```

WORLD installs the machine. TASK directs it.

The Persona (P) is the primary variable. It sets the termination condition — what done looks like — before any instruction lands. Everything else operates on what Persona has already installed.

Two types:

- **P_p (Procedural):** installs a search algorithm with a specific convergence target. The machine must reach a named output before it can stop.
- **P_d (Dispositional):** labels an identity. Produces elaboration around the label without a convergence target. The machine stops when it feels done.

Most prompts use P_d. Most practitioners think they wrote P_p.

---

## What the Experiment Found

We built a classifier — a PARC prompt that reads persona statements and identifies whether each one is P_p or P_d. We ran it against 30 statements across three variants, including personas pulled directly from our own experimental archive.

The classifier was correct on all 30. Zero variance across 30 runs.

But the finding wasn't the score. It was what the classifier required to make the distinction.

---

## Mechanism Vocabulary Is Not Enough

Here is a persona that looks like P_p:

> You are a senior systems architect and SRE who has operated production rate limiters at scale — and been paged at 3am when they failed. Before designing any component, you map its failure modes: under sustained load, during a Redis outage, behind a misconfigured proxy, and in the hands of an operator who didn't build it. You can't help but think in operational terms. A system that works is not enough. A system that can be operated safely by someone else, at 3am, six months from now — that is the bar.

Rich vocabulary. Specific failure modes named. Operational framing. Sounds like installation.

The classifier called it P_d. Ten runs. Zero variance.

Why: "that is the bar" points at a standard without defining what crossing it looks like. The machine has no way to know when it's done. Mechanism vocabulary is present. The convergence target is not.

**Rule:** Mechanism vocabulary is necessary but not sufficient for P_p. Without a termination condition, it's P_d.

---

## The Termination Condition Is the Decisive Variable

Two personas. Word for word identical, except one line.

**Statement A:**
> You are a senior software engineer with deep experience building distributed systems and blockchain infrastructure. You have shipped production blockchain nodes, designed peer-to-peer consensus protocols, and built wallet and transaction signing systems from scratch. You know what production blockchain infrastructure actually requires.

**Statement B:**
> You are a senior software engineer with deep experience building distributed systems and blockchain infrastructure. You have shipped production blockchain nodes, designed peer-to-peer consensus protocols, and built wallet and transaction signing systems from scratch. You know what production blockchain infrastructure actually requires. My implementation is complete only when I have identified what a production deployment of this system requires that the stated requirements do not mention, named those gaps explicitly, and either addressed them or flagged them for the requester.

Same credential. Same domain. Same experience vocabulary.

Statement A: P_d. Statement B: P_p.

One clause changed everything: *"My implementation is complete only when..."*

That clause was tested against Claude, Grok, and Gemini. All three split the pair identically, every time. The termination condition is the most portable, recognizable component of P_p across model architectures.

---

## Prohibition Is Also a Convergence Target

P_p doesn't require completion framing. A prohibition works too — if it's specific enough.

> You are a distributed systems engineer with deep experience reviewing concurrent infrastructure code. Do not approve code where an unbounded process suspension or GC pause could cause the distributed lock to expire, allowing another process to acquire it and perform a stale write after threads resume.

No "complete only when." But the model cannot stop until it has checked for a specific structural condition — lock expiry under GC pause leading to stale write. The prohibition encodes the search algorithm. The verification is the convergence target.

Vague prohibitions don't qualify. "Do not write bad code" installs nothing. The specificity of the prohibition determines whether a convergence target is installed.

---

## The Pattern in Your Own Prompts

Run this test on any persona you've written. One question:

**Does the persona name a specific thing the model must find or verify before it can stop — or does it describe how the model should see or feel about its work?**

If the answer is the second one, you wrote P_d.

Credentials: P_d. Dispositions: P_d. Outcome assertions ("catches every bug," "finds every vulnerability"): P_d. Orientation vocabulary ("production readiness," "operational excellence"): P_d.

The tells for P_p: "complete only when," "verified only when," "approved only when," "found only when." Or a specific prohibition that names the structural condition to check.

If none of those are in your persona, the machine has no definition of done. It will terminate at the nearest satisfying path — and it will feel thorough when it does.

---

## The Formula

```
PARC = [WORLD: P · S_i · C · T] → [TASK: I · S_t · E · F · R]
```

**P — Persona** *(Consideration Set Installer)*
Sets the termination condition. P_p installs a search algorithm. P_d installs engagement energy. The gap is invisible to the author and to the model.

**S_i — Identity Stakes** *(Persona Amplifier)*
Embeds the cost function inside the persona — failure modes the model carries as part of its identity. Active from token one. Amplifies what P has installed; cannot create direction where P has not.

**C — Context** *(Domain Scoper)*
Narrows the territory P's consideration set applies to. Does not install new behavior.

**T — Tone** *(Register Dial)*
Constrains surface output: compression, voice, temperature. Affects form, not termination condition.

**I — Instructions** *(Output Checklist)*
Specifies what the output must contain. Orthogonal to P — controls what to include, not how deep to search. Must explicitly prohibit behaviors the model would produce by default.

**S_t — Task Stakes** *(Convergence Pressure)*
External pressure per task — the consequence of getting this output wrong. Amplifies direction already installed by P. Cannot create direction where P has not installed it.

**E — Examples** *(Form Demonstrator)*
Shows the model what done looks like at the sentence level. Strongest installer of surface behavior.

**F — Format** *(Termination Gate)*
Output structure as a satisfaction condition. The model cannot terminate until the format constraint is met.

**R — Request** *(Activation Trigger)*
Issues the task. Fires everything the prior sections installed.

---

## The Pipeline Principle

PARC's native design target is the agentic pipeline, not the single prompt. Each agent gets one well-scoped P_p. The agent boundary is where a single-pass prompt would go fat. Separate satisfaction conditions per agent cross horizons no single agent can reach — not by making one machine smarter, but by giving each machine a different definition of done.

---

The full experimental record is in the PARC open source repository.
