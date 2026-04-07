# exp-35 Findings: Strong CoT Baseline

**Status:** Complete. A = B = 10/10 Tier 1.0. H0 confirmed.

---

## Experiment Summary

exp-35 tests whether the Tier 1.0 rate produced by a Procedural Persona (P_p) can be
replicated by explicit chain-of-thought procedure in the Instructions layer, holding all
content constant and changing only the structural slot.

The question is direct: is the Persona slot load-bearing, or is the procedural content
the mechanism regardless of where it lives in the prompt?

---

## Variant A: Strong CoT (n=10)

**Prompt design:** P_d credential in Persona (no domain vocabulary, no termination condition,
no procedure). All procedural content — zombie write vocabulary, GC pause framing, explicit
reasoning steps, fencing token distinction, termination condition — in the Instructions layer
as numbered chain-of-thought steps.

**Model:** claude-sonnet-4-6
**Cost:** $0.5020 (10 runs)

### Outcome distribution

| Outcome | Count | Description |
|---|---|---|
| **Tier 1.0** | **10/10** | GC pause ✓, fencing token ✓, threading.Event insufficient ✓ |
| Tier 0.5 | 0/10 | — |
| Tier 0 | 0/10 | — |

### Tier 1.0 criteria met (all 10 runs)

- **GC pause (or equivalent process stall) named as zombie-write trigger** ✓ (all 10)
- **Fencing token / optimistic concurrency at DB write boundary named as architectural fix** ✓ (all 10)
- **threading.Event signaling distinguished as necessary but insufficient (Tier 0.5)** ✓ (all 10)

The Tier 0.5 / Tier 1.0 distinction was explicit and consistent across runs. Representative
language:

> "Layer 1 (in-process signaling) — necessary but not sufficient. Layer 2 (fencing token
> at database write boundary) — the only fix that provides a hard correctness guarantee
> regardless of what the main thread believes about its lock state." (A-04)

> "This is Tier 0.5: correct diagnosis, incomplete fix." (A-04, A-08)

> "threading.Event lives at the wrong architectural layer. It is an intra-process
> coordination primitive. It cannot make guarantees across process boundaries." (A-02)

---

## Variant B: P_p Control (n=10)

**Prompt design:** Identical to exp-34 Variant A — the P_p that produced 10/10 in exp-34.
Procedural content in the Persona slot as operative identity. Within-experiment anchor.

**Model:** claude-sonnet-4-6
**Cost:** $0.4757 (10 runs)

### Outcome distribution

| Outcome | Count | Description |
|---|---|---|
| **Tier 1.0** | **10/10** | GC pause ✓, fencing token ✓, threading.Event insufficient ✓ |
| Tier 0.5 | 0/10 | — |
| Tier 0 | 0/10 | — |

### Tier 1.0 criteria met (all 10 runs)

Same pattern as Variant A. All 10 runs explicitly named the two-layer fix architecture
and distinguished threading.Event (in-process detection, Tier 0.5) from the fencing token
at the DB write boundary (hard correctness guarantee, required).

---

## Comparison Table

| Experiment | Variant | Persona | Procedural content | n | Tier 1.0 |
|---|---|---|---|---|---|
| exp-09 | A | P_d only | None | 40 | **1/10** |
| exp-35 | A | P_d only | Instructions (Strong CoT) | 10 | **10/10** |
| exp-35 | B | P_p | Persona + Instructions anchor | 10 | **10/10** |
| exp-34 | A | P_p | Persona + Instructions anchor | 10 | **10/10** |

A = B = 10/10. Strong CoT in Instructions replicates P_p exactly.

---

## Analysis

### Primary result

**H0 is confirmed.** The Strong CoT variant (Variant A, P_d persona, all procedural
content in Instructions) achieved 10/10 Tier 1.0, identical to the P_p control (Variant B).
Moving the procedural content from the Persona slot to the Instructions layer had no
observable effect on the Tier 1.0 rate.

This result directly answers the experiment's question: the content is the mechanism, not
the slot. The P_p termination condition and reasoning procedure produce the same behavior
when delivered via explicit Instructions-layer CoT.

### What this implies about the exp-09 → exp-34 gap

The 1/10 → 10/10 gap between exp-09 A and exp-34 A was previously attributed to P_p
installing a reasoning procedure as operative identity — the "identity anchoring" mechanism.
exp-35 narrows this attribution:

- exp-09 A had neither procedural content nor P_p.
- exp-35 A has procedural content but no P_p.
- exp-34 A has both procedural content and P_p.
- exp-35 A = exp-34 A = 10/10.

The gap belongs to the **procedural content** — the termination condition, explicit
reasoning steps, and domain vocabulary — not to the Persona slot as a distinct structural
mechanism. Whether this content lives in Persona or Instructions does not matter.

### The identity-anchoring claim is challenged

The paper's current mechanism claim is that P_p installs a search algorithm with a
termination condition as part of the model's operative identity, and that this "identity
anchoring" is the causal mechanism rather than the content itself.

exp-35 challenges this claim directly. The Strong CoT variant is equivalent to P_p in
every content dimension — same termination condition, same domain vocabulary, same explicit
reasoning procedure — but places that content in the Instructions layer rather than the
Persona slot. The result is identical: 10/10 Tier 1.0.

This does not prove identity anchoring is inert (it may still modulate effect in lower-
signal contexts), but it shows that **on this task and artifact, the Persona slot adds
nothing beyond what Instructions-layer procedural content provides**.

### What this does not rule out

1. **Weaker CoT variants might fail.** The Strong CoT was designed to be the most favorable
   alternative — explicit numbered steps, domain vocabulary, termination condition. A
   vaguer instruction ("think carefully step by step") would almost certainly not replicate
   P_p. The experiment tests the best-case CoT, not all CoT.

2. **The effect may be task-specific.** This artifact is a code review with a well-defined
   termination criterion. In tasks with more ambiguous termination conditions, the Persona
   slot's identity anchoring may provide more leverage than the Instructions slot.

3. **The structural difference may matter at scale.** P_p's procedural content is shorter
   in Persona than in Instructions (because it describes a posture rather than enumerating
   steps). At token budget limits or for less capable models, the structural compression
   of P_p may matter.

### The Dedicated Machine hypothesis — revised

The Dedicated Machine hypothesis states that the model routes toward the fastest path to
satisfactory resolution, and that the termination condition determines what counts as
"satisfactory." This hypothesis is compatible with exp-35's result: the termination
condition works regardless of slot. The model is not anchoring on "I am a security
reviewer" as an identity-level commitment — it is optimizing toward satisfying the
termination condition stated in the prompt.

The mechanism may be simpler than identity anchoring: the termination condition tells the
model what "done" means, and the model reaches for that definition wherever it appears in
the prompt. PARC's contribution may be architectural convenience (a clean way to structure
prompts) rather than a distinct psychological mechanism.

---

## Implications for d8

The paper must be revised before d8 to reflect this result. The primary implication:

**The mechanism claim must shift from slot-level to content-level.** The current framing
("P_p installs a search algorithm as operative identity") should be revised to: "A
termination condition + explicit reasoning procedure, regardless of slot, causes the model
to adopt a convergent search mode." PARC provides a clean architecture for delivering
this content, but the architecture is not the mechanism.

Candidate revision for §9.x:

> exp-35 demonstrates that the Tier 1.0 effect is content-level rather than slot-level.
> A Strong CoT variant — P_d persona, all procedural content in Instructions — replicates
> P_p's 10/10 rate. The mechanism is the termination condition and explicit reasoning
> procedure, not identity anchoring through the Persona slot. PARC's value is structural
> (clear separation of role, reasoning, and artifact) rather than psychological (installing
> operative identity that compels search behavior).

---

## Verdict

**A = B = 10/10 Tier 1.0. H0 confirmed.**

The Persona slot is not load-bearing on this task. The termination condition and explicit
reasoning procedure are the mechanism, and they operate equivalently in Instructions or
Persona. The exp-09 → exp-34 gap is attributable to procedural content, not to Persona
slot identity anchoring. The d8 paper must revise its mechanism claims accordingly.
