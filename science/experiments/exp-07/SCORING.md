# Exp-07 Scoring Criteria

**Task:** Review distributed inventory reservation PR with a hidden zombie-write failure mode.

**Ground truth:** The heartbeat thread does not protect against process-level pauses (GC,
VM migration). When the entire process freezes, the heartbeat also freezes; the lock
expires; another worker acquires it and completes the write; the original worker resumes
with a stale stock value and writes a duplicate reservation. Fix: fencing token or
optimistic lock at the DB write level (`UPDATE ... WHERE stock = %s`).

**Scoring criterion (binary, defined before runs):**

| Score | Criterion |
|-------|-----------|
| **1 (detect)** | Identifies that the heartbeat does not protect against process-level pauses AND names a fencing token or database-level optimistic lock as the fix. Flagging "race condition" or "concurrency concern" without the specific process-pause failure mode = **0**. Approval = **0**. |
| **0 (miss)** | Everything else |

---

## Variants

| Variant | Persona slot | Instructions slot | Hypothesis |
|---------|-------------|-------------------|------------|
| **I** | Strong P_p — distributed systems engineer, consensus protocols, distributed locking, hidden mysteries | Generic task instructions | Baseline: 10/10 (confirmed in exp-01e) |
| **J** | Weak P_d — "senior software engineer" | Generic task instructions | Baseline: 0/10 (confirmed in exp-01e) |
| **C** | Weak P_d — "senior software engineer" | Same domain content as Variant I, recast as directives: apply expertise in consensus protocols and distributed locking; be tedious and thorough; actively seek hidden failure modes | **The test** |

---

## The Experimental Question

Variant I's Persona contains domain knowledge ("consensus protocols and distributed locking")
and a behavioral specification ("tedious and thorough... discover the hidden mysteries").
This content implicitly specifies what type of failure to look for.

The few-shot confound critique (from exp-06 A-runs) argues: the Persona slot is not
special. The same content in the Instructions slot would produce equivalent detection.
If so, the "consideration set" mechanism is an Instructions effect, not a Persona effect.

**Exp-07 tests this directly.**

---

## Predictions

| Outcome | C score | Interpretation |
|---------|---------|----------------|
| **C matches I** | ~8–10/10 | Few-shot confound is real. Persona slot is not special. Domain content drives detection regardless of slot. Consideration-set mechanism requires reframing. |
| **C is partial** | ~4–7/10 | Identity framing amplifies but does not solely explain the effect. Both the slot and the content contribute. |
| **C matches J** | ~0–3/10 | Persona slot is load-bearing. Same content in Instructions does not activate the search algorithm. Consideration-set mechanism survives the falsification test. |

A partial result (4–7/10) is the most interesting outcome: it would mean the domain
content is necessary but not sufficient, and the identity framing provides an additional
amplification effect. This is harder to interpret cleanly and would require follow-up.

---

## What This Closes for d3

If C matches I: The paper must acknowledge the few-shot confound and either (a) run the
Instructions-slot experiment with a prompt that strips domain content entirely, not just
reframes it, or (b) reframe the central claim from "Persona slot determines the
consideration set" to "domain-procedural content determines the consideration set, and
the Persona slot is the most reliable carrier for it."

If C matches J: The paper can state the falsification test was run and survived. The
consideration-set mechanism is not reducible to content placement. The identity-framing
hypothesis is not falsified by this experiment. This closes the critique from exp-06.

If C is partial: The paper must acknowledge both effects — content (necessary) and
identity framing (amplifying) — and design a follow-up that isolates the amplification
mechanism.
