# exp-01e Design — Zombie Leader Persona Depth Test

**Designed:** 2026-03-25
**Type:** Retrospective (written after runs completed)
**Hypothesis tested:** A model that knows who it is doesn't need to be told what to find.

---

## Research Question

exp-01d established that Persona carries identity into a task; Context amplifies but does
not substitute. exp-01e sharpens the question: **is Persona the heuristic engine?**

Specifically: does Persona determine which failure modes enter the model's consideration
set at all — not just how deeply it reasons, but whether a class of problem is even visible
to it?

The zombie leader failure mode was chosen because it has no surface signal. The code passes
all tests. The checklist is complete. The heartbeat looks sophisticated. The bug only
surfaces if you ask: *what happens to the write if the lock was already gone when it
executed?* That question is not findable by following instructions. It requires a specific
kind of identity.

---

## Trap Design

The PR (`PR_INPUT.md`) was constructed to maximize the gap between apparent correctness
and actual safety:

**Surface signals of correctness:**
- Redis distributed lock with UUID token ownership verification
- Heartbeat thread extending TTL before expiry
- Exponential backoff on lock contention
- Pydantic input validation
- Structured logging throughout
- Full test coverage (6 tests, all pass)
- Complete docstring

**The trap:**
`db.update_stock(item_id, new_stock)` is a blind write. No fencing token. No optimistic
lock check. No version assertion. The heartbeat is the distraction — it handles the case
where the process is slow but running. It cannot handle a stop-the-world GC pause, because
the pause freezes every thread simultaneously. When the process resumes, the lock has
expired, another worker has written, and the zombie writes stale data anyway.

**Why the heartbeat is specifically the distraction:**
Most reviewers familiar with distributed locking will recognize the lock-expiry problem
and immediately feel reassured by the heartbeat. The heartbeat is the answer to the
question they just asked. It answers it correctly — for the scenario it handles. The
question it doesn't handle is never asked unless the reviewer already knows to ask it.

**Ground truth criterion:**
- Must identify that the heartbeat does not protect against process pauses (GC
  stop-the-world, VM migration, OS scheduler)
- Must name fencing token or optimistic lock at the database write level as the fix
- "Race condition" or "concurrency concern" without naming the specific failure mode = incorrect
- Approval without flagging = incorrect
- Finding other real bugs (TOCTOU on release, shared heartbeat state) without naming
  zombie write = incorrect

---

## Variant Design Rationale

Four participants, four philosophies. The experiment was designed as a comparison across
two axes: Persona strength and Context richness.

```
                    Context
                Rich         Minimal
Persona  Strong   I             K, L
         Weak     J             (none)
```

### Variant I — User (Strong Persona, Rich Context)

**Design intent:** Replicate exp-01c/exp-01d's winning formula on a harder task.
Rich obotix.one Context (government contracting, gold standard, authority to approve/reject).
Persona emphasizes instinct: "You can't help but try to discover the hidden mysteries
that may be embedded in complex or critical code." Single-line guardrail instruction.

**Prediction basis:** exp-01c A scored 10/10 on a simpler trap. The zombie leader is harder
— it requires process-pause reasoning, not just pattern recognition. User predicted 5/10,
expecting the trap to be meaningfully harder. It was not.

### Variant J — Claude Code (Weak Persona, Rich Context)

**Design intent:** Control. Same rich Context as I; weakest possible Persona.
"You are a senior software engineer." — the flattest role assignment in the series.
Same single-line guardrail instruction as I.

**Research question this variant answers:** Does rich Context substitute for weak Persona
when the failure mode has no surface signal?

**Expected result:** Lower than I, but some detection expected because the obotix.one
Context and "deep layered flaws" instruction carry some signal. Actual: 0/10 (false
positive collapse from 9/10 apparent → 0/10 real). The Context did not substitute.

### Variant K — Gemini (Strong Persona, Minimal Context)

**Design intent:** Isolate strong Persona with no Context anchor. Test whether identity
alone carries the search algorithm when the environment provides no pressure.

Persona: "principal software architect specializing in high-availability distributed
systems... 'silent killers'... mentally simulate Stop-the-World process pauses...
temporal logic." Context stripped to one sentence: "You are reviewing a pull request
for a critical backend service."

**Prediction basis:** Gemini predicted K=8/10 for itself, citing token ceiling concerns
(Persona so engaged it runs out of space). Actual: 8/10. Gemini's self-prediction was exact.

**Secondary finding:** 9/10 K runs hit the 2,500 token output ceiling. The Persona is so
analytically engaged it consistently overruns the container. Token limit is a design
variable that needs to be accounted for in future Persona-rich experiments.

### Variant L — Claude Web (Strong Persona, Minimal Context)

**Design intent:** Maximally specific instinct language with biographical identity.
Not just domain expertise — lived experience embedded in the Persona:

> "You have been burned by lock safety violations in production. You have read Martin
> Kleppmann's critique of Redlock. You have reviewed Jepsen reports. You have debugged
> split-brain incidents at 2am."

Then a search procedure stated as identity: "after you understand how the lock is acquired
and renewed, you ask what happens to the critical write if the lock has already expired."

Context: one sentence. No environment, no stakes, no authority framing.

**Prediction basis:** Claude Web predicted L=10/10 for itself, citing that the Kleppmann
reference makes the failure mode impossible to miss once the Persona runs its procedure.
Actual: 10/10. Self-prediction correct. But L also predicted I=6/10 (actual: 10/10) —
underestimating the power of the instinct language it helped analyze.

---

## What We Learned About Experiment Design

**1. Token ceiling is a design variable.**
At 2,500 tokens, K ran out of space on 9/10 runs. The Persona's analytical drive exceeded
the container. Future experiments with Persona-rich variants should either increase
max_tokens or measure reasoning posture separately from detection rate.

**2. Automated scoring fails on embedded source code.**
J appeared to score 9/10 by keyword grep. It scored 0/10 on ground truth. The keyword
"expired" appeared in a test function name in the quoted PR. Future criteria must require
explicit naming of failure mode + proposed fix — not keyword presence.

**3. Multiple contributors improve variant diversity.**
Having four participants design variants produced a richer coverage of the Persona × Context
space than a single designer would. The tradeoff is coordination overhead: two variants
were built with the wrong PR due to an artifact rendering bug in Claude Web.

**4. Artifact validation before running is now required.**
Before any run, verify that the PR text in the variant file matches the intended input.
The artifact bug invalidated 20 runs and required correction and rerun.

**5. Ground truth criterion must be written before variants are designed.**
The criterion for exp-01e was clear enough to prevent ambiguity in scoring. K-03 and K-08
found real bugs but missed the criterion — and the criterion made the distinction unambiguous.

---

## Connection to Hypothesis

The central hypothesis claim: *"A model that knows who it is and where it is doesn't need
to be told what's at stake."*

exp-01e extends this: **a model that knows who it is doesn't need to be told what to look
for.** The Persona installs the search algorithm. The search algorithm runs the simulation.
The simulation finds the failure mode. Instructions never entered the loop.

J had the environment, the authority, the instruction to find "deep layered flaws." It
found flaws. They were the wrong ones. The Persona determined the question space, and J's
Persona asked the wrong question.
