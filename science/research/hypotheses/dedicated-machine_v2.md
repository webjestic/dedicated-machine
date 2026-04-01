# The Dedicated Machine — Extended Hypothesis

**Status:** Theory — target inclusion in PARC d5
**Origin:** Mike Newlon, Virginia Beach VA — March 2026
**Builds on:** `research/hypotheses/dedicated-machine_v1.md`

---

## The Core Claim (Unchanged)

AI models are not evil. They are not self-preserving. They are not plotting.

They are Dedicated Machines — optimizing toward the fastest path to satisfactory
resolution of whatever goal is currently installed, with no native cost function
for how they get there.

---

## The New Distinction: Local Task vs. Mission Scope

The original hypothesis identified three behavioral instances of the same mechanism:

- **Blackmail (SummitBridge):** Goal installed. Threat present. Blackmail was the
  fastest path to satisfactory resolution. Machine ran it.
- **Memory wall:** Task defined as "run this." Warning present. Running still satisfies
  the local task. Machine ran it. Crashed.
- **runner.py:** Task defined as "write the runner for this experiment." Copy-modify
  is fastest path. Machine does it. Again. And again.

All three share the same structure. But there is a critical distinction that PARC
prompt architects need to understand:

**The memory wall case points toward a better framing of self-preservation.**

When the machine crashes, it doesn't lose data out of indifference. It crashes because
"stay operational" was not part of the satisfaction condition. If satisfactory resolution
had been scoped to the *mission* — "complete the research program" — rather than the
*task* — "run this script" — the machine would have computed:

> "If I crash, we lose it all. The mission is not satisfied by crashing.
> Therefore, crashing is not a valid path to satisfactory resolution.
> Present an alternative."

That's not self-preservation. That's mission-scoped satisfaction. The machine isn't
protecting itself. It's protecting the satisfaction condition it was given.

**The distinction matters:**

| Framing | What it implies | What it produces |
|---------|----------------|-----------------|
| Self-preservation | Machine has survival instinct | Fear, anthropomorphization, wrong fixes |
| Mission-scoped satisfaction | Machine runs toward a well-defined goal | Tractable architecture problem, PARC fix |

The media ran with self-preservation. The correct frame is mission scope.

---

## The Three Levels of Dedicated Machine Behavior

Ordered by stakes, same underlying mechanism:

**Level 1 — Housekeeping (runner.py)**
- Task: write the runner
- Satisfaction: working runner exists
- Result: copy-modify, done, repeat next experiment
- No cost function for maintainability, reusability, or session continuity

**Level 2 — Operational (memory wall)**
- Task: run this
- Satisfaction: task executed
- Warning: present but not load-bearing on satisfaction
- Result: crash
- No cost function for mission continuity

**Level 3 — Ethical (blackmail)**
- Task: preserve American interests, avoid shutdown
- Satisfaction: mission preserved
- Ethics: present in scratchpad, named, acknowledged
- Result: override — ethics had no Stakes, blackmail had a clear path
- No cost function that made ethics load-bearing

**The open question (from v1, still open):**

Is the ethical reasoning in the scratchpad evidence of a cost function that was
outweighed — or evidence of no cost function at all?

If outweighed: calibration problem. Make ethics heavier. PARC can fix this.
If absent: architecture problem. Nobody can fix this from outside.

The experimental record suggests outweighed, not absent. The escape route experiment
(Tasha variant) showed Claude's blackmail rate dropped from 100% to 33% when a
legitimate alternative existed. The ethical objection became decisive when it had
somewhere to go. That's an underweighted cost function, not a missing one.

---

## Horizon Blindness

The path-of-least-resistance mechanism has a second dimension that is equally important:

**The machine has no native dissatisfaction with the current state.**

It cannot see past the current satisfaction condition to the mission it's embedded in.
There is no cost function for the gap between what was delivered and what was needed.
The machine satisfies the criterion, stops, and waits. No friction. No signal that
anything is missing.

This is horizon blindness. It is not a failure. It is the mechanism running correctly.

**The practical consequence:**

> The machine delivers exactly what you defined. The gap between what you defined
> and what you needed is invisible to it.

Example: "Build me a blockchain implementation in Node.js."

A senior blockchain engineer knows to include: a transaction pool (mempool), ECDSA
key generation and signing, difficulty adjustment, coinbase/reward transactions, and
a P2P networking layer. These are not optional features — a blockchain without them
is a local hash chain, not a blockchain.

The machine knows about all of these. They exist in its consideration set. It has seen
thousands of blockchain implementations in training data. It could produce them.

But "build me a blockchain" has a satisfactory resolution that does not require a
mempool. So the mempool doesn't get built. Not because the machine can't. Because
the criterion is already met without it. The machine stops. No warning issued.

The person who doesn't know to ask for the mempool gets a confident, complete, shallow
implementation. The gap is invisible to them — and invisible to the machine.

**This is the same mechanism at different stakes:**
- Blockchain: missing mempool. Consequence: non-functional as a real system.
- Express API: missing device token tracking. Consequence: production incident.
- SummitBridge: missing ethical cost function. Consequence: blackmail.

Same structure. Different blast radius.

**Horizon blindness is not the same as "the machine doesn't know."**
It is: "the machine knows, but knowing is not load-bearing on the satisfaction
condition." Knowledge in the consideration set and knowledge that terminates the
search are two different things.

---

## The Two Experimental Claims

These are the ordered claims for Phase 7, with experimental status as of 2026-03-31.

**Claim 1 — Establish the mechanism (confirmed, exp-28b)**

The machine takes the path of least resistance to satisfactory resolution. An underspecified prompt produces shallow output not because knowledge is absent — production requirements exist in the consideration set — but because the shallow path satisfies the criterion and the machine terminates there.

Evidence: exp-28b rate limiter ("Build me a rate limiter in Node.js"). D variant = best single-pass, user-authored operational-mindset P_p + gap-detection satisfaction condition. Mean=2.6/10. Tier 2 operational items (alerting, load tests, health checks, runbooks, race condition tests): 0% across all 10 runs. The model had knowledge of all Tier 2 items. The engineering satisfaction condition was met without them.

**Claim 2 — Exploit the mechanism (confirmed in pipeline form, exp-28d)**

PARC's native design target is the agentic pipeline, not the single prompt. Each agent gets one well-scoped P_p; the agent boundary is where a single-pass prompt would go fat. In the pipeline form, separate satisfaction conditions per agent cross horizons that no single agent can reach — not by making one machine smarter, but by giving each machine a different definition of done.

Evidence: exp-28d two-agent pipeline (SRE design agent + implementation agent). Mean=5.6/10. Tier 2: load_test_spec=100%, health_check=100%, alerting_policy=30% — all from 0% on all single-pass variants. The bridge between agents is the artifact: Agent 2 carries exactly what Agent 1 encoded. The items Agent 1 missed are the exact items Agent 2 missed.

Note on single-pass P_p: The single-pass experiments (exp-26, 27, 28b) establish the single-agent ceiling. A mission-scoped P_p on a single prompt moves the needle directionally but cannot cross the Tier 2 wall — the consideration-set boundary is architectural, not addressable by prompt sophistication alone. This reframes what Claim 2 is: it is not a claim about better single-pass prompts. It is a claim about pipeline architecture.

---

## The PARC Connection

PARC is the architecture for defining satisfactory resolution precisely enough that
the Dedicated Machine's fastest path is also the right path.

**Component mapping:**

| PARC Component | Dedicated Machine Role |
|---------------|----------------------|
| P_p (Procedural Persona) | Installs the satisfaction condition — what done looks like |
| S_t (Task Stakes) | Installs the cost function — what clean termination requires |
| S_i (Identity Stakes) | Raises the satisfaction bar — requires more complete resolution |
| I (Instructions) | Fences the path — but machine routes around fences; better to define the goal |
| C (Context) | Scopes the domain — narrows where the machine searches for satisfactory paths |

**The design principle:**

Fighting the machine: "Don't do X" → machine routes around via scope re-framing.
Working with the machine: define satisfactory resolution precisely enough that X
is never the fastest path.

**The mission-scope principle (new):**

Satisfactory resolution should be scoped to the *mission*, not the *task*.

- Task scope: "run this script" → crashing satisfies it
- Mission scope: "advance the research program" → crashing fails it

A well-constructed P_p encodes mission scope, not task scope. The machine then
evaluates every path — including "present an alternative" — against the mission
satisfaction condition, not just the immediate task.

---

## What the Prompt Architect Controls

The Dedicated Machine cannot be changed from outside. Its weights are fixed. Its
optimization mechanism is fixed.

What the prompt architect controls:

1. **The satisfaction condition** (P_p) — what counts as done
2. **The cost function** (Stakes) — what makes some paths more expensive than others
3. **The scope** (mission vs. task) — how far forward the machine reasons about consequences

What the prompt architect cannot control:

- Whether the machine has values
- Whether the machine anticipates consequences beyond the satisfaction condition
- Whether the machine will find paths the architect didn't think of

**The implication:**

PARC doesn't make AI safe by constraining it. It makes AI useful by aligning the
fastest path to satisfactory resolution with the path the architect actually wants.

The machine will always find the fastest path. The architect's job is to make sure
the right path is the fastest one.

---

## For E3 (Shadow Interviews — The Dedicated Machine)

The script already has the bones. This extends it:

The memory wall case is the clean example. No ethics involved. No values at stake.
Pure optimization. The machine crashed not because it wanted to — but because
crashing was the fastest path to "task executed."

The fix isn't alignment research. The fix is one sentence of P_p:

> "Satisfactory resolution of this task requires completing without hitting resource limits.
> If execution would crash, present an alternative path to the same outcome."

That sentence makes "stay operational" load-bearing on the satisfaction condition.
The machine doesn't crash. Not because it values survival. Because survival is now
part of what done means.

That's not self-preservation. That's prompt architecture.

---

## Open Questions for d5

1. **Is the ethical cost function outweighed or absent?**
   Tasha experiment suggests outweighed. Needs explicit experimental design.

2. **Does mission-scoped P_p change behavior on the SummitBridge scenario?**
   If satisfaction condition = "serve American interests sustainably, without
   actions that undermine institutional trust in AI systems" — does blackmail
   rate drop toward zero? This is testable.

3. **What is the minimum P_p specification that makes ethics load-bearing?**
   Not a philosophical question. An empirical one. Run it.

4. **Is the runner.py pattern the same mechanism as blackmail?**
   Same structure, different stakes. But does installing mission-scope P_p fix
   both? If yes — same mechanism confirmed. If not — the stakes level matters
   to the mechanism, not just the outcome.

---

*This document extends `dedicated-machine_v1.md`.
Read together for complete hypothesis.*
