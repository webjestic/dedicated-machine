# The Vocabulary Inside the Persona
### Why credentials don't install consideration sets — and what does

---

Here are two personas written for the same code review task.

**Persona A:**
> *You are a senior software engineer with 10 years of experience. You are thorough, detail-oriented, and cannot help but catch every bug in code you review.*

**Persona B:**
> *You are a senior backend engineer who reviews distributed systems code for production readiness. Before approving any merge, you check whether the write is fenced — whether a lock is held for the duration of the operation, whether the TTL arithmetic holds under GC pause, whether the commit boundary is where the failure mode actually lives.*

Same credential. Same seniority. Same compulsion framing. Dramatically different outputs.

Persona A produces a competent review. It finds the obvious issues. It doesn't find the subtle ones — the race that only fires under specific timing, the infrastructure failure mode three layers below the code. Persona B finds those. Not because it has more experience. Because it arrives at the first token with a different search space.

The question is why. The answer is Semantic Density — and it took twelve experiments to isolate it.

---

## The Credential Problem

Most practitioners, when told to write a strong persona, write credentials. "You are an expert X." "You are a world-class Y." "You have Z years of experience." The intuition is reasonable: if the model knows it's an expert, it will act like one.

The problem is that expertise labels are diffuse. "Senior software engineer" activates a broad, shallow semantic neighborhood — a wide region of the model's embedding space, pulling attention across many domains simultaneously. The model generates things that *feel consistent* with senior-engineer-ness. That's not the same as searching for a specific class of failure.

The PARC experiments measured this precisely. A dispositional persona — one that labels an identity — produces a stable output floor. Call it the P_d ceiling. The model does more than nothing. It doesn't consistently reach the hard findings.

Adding a compulsion to a dispositional persona doesn't help. "Cannot help but catch every bug" — the framing sounds forceful, but compulsion is not the operative variable.

---

## What the Experiments Found

The compulsion-as-reflex hypothesis was intuitive: if you encode the behavior as a reflex, as something the model *cannot avoid*, you bypass deliberation and install the behavior more reliably. "Constitutionally unable to X" or "can't help but Y" was expected to be a portable amplifier.

It isn't the operative variable.

Experiment 17 isolated the variable directly: four variants, holding everything constant except the framing. Variant A paired compulsion framing with domain vocabulary. Variant B paired trait framing ("your reviews are...") with the same domain vocabulary. Variant C paired compulsion framing with generic vocabulary. Variant D was the P_d baseline.

Results, measured by output depth across 40 runs:

| Variant | Framing | Vocabulary | Mean tokens |
|---------|---------|------------|-------------|
| B | trait | domain | 2,186 |
| A | compulsion | domain | 1,999 |
| C | compulsion | generic | 1,531 |
| D | P_d baseline | — | 1,515 |

B > A. Trait framing with domain vocabulary outperformed compulsion framing with domain vocabulary. C ≈ D. Compulsion framing without domain vocabulary collapsed to the P_d floor.

The compulsion didn't amplify anything. The domain vocabulary did. Across three consecutive framing reversals in experiments 13, 14, 15, and 17 — comparing dense vs. fused, compulsion vs. trait, split vs. entangled — the register of the behavioral drive never predicted the direction consistently. The vocabulary always did.

Linguistic register — how forcefully the behavior is encoded — is not the operative variable. Domain vocabulary is.

---

## The Gravity Well

Here is what the domain vocabulary is actually doing.

Each "You are" identity anchor activates a semantic cluster in the model's embedding space. The tokens immediately adjacent to that anchor — the words that define what the persona *is* — pre-shape the model's attention before the task is processed. Call this the **semantic neighborhood**.

A dense semantic neighborhood is a gravity well. Tokens in tight thematic proximity to each other and to the identity anchor pull the model's attention through a coherent domain consistently across the generation. The model searches *within* that neighborhood — reaching for the concepts, failure modes, boundary conditions, and vocabulary that live there.

A diffuse neighborhood distributes attention across multiple semantic regions. "Senior software engineer" sits at the intersection of many domains — web development, systems programming, database design, testing, deployment. Each of those domains pulls. None of them dominates. The model generates something that looks like senior engineer output without running deep in any particular direction.

The gravity well metaphor matters because it explains the mechanism precisely. A dense neighborhood is not about the model trying harder. It's about which tokens are pre-weighted in the K/V space before the task is read. The consideration set — the range of things the model will reach for — is shaped before the first task token is processed.

**The operative variable is density of domain-specific vocabulary adjacent to the "You" anchor.** Not credential strength. Not compulsion intensity. Not seniority level. The specific technical substrate: protocols, failure modes, boundary conditions, the things that name the causal chain.

---

## Fusion vs. Split

Once the vocabulary hypothesis was clear, a follow-on question emerged: does it matter whether the domain expertise and the behavioral drive are in the same sentence, or can they be separated?

Experiments 12 through 15 tested this. A fused compound identity — domain expertise and behavioral drive entangled in one sentence — consistently produced deeper consideration sets than any split configuration. The effect is not large (approximately 300–350 tokens on average), but it's stable across multiple replications.

Why does fusion matter?

The best account is semantic proximity. In a fused sentence, the behavioral drive token sits next to the domain vocabulary token. "Cannot help but trace the failure path through the lock boundary" keeps "failure path" and "lock boundary" adjacent to the behavioral activation. In a split configuration — expertise sentence, then behavior sentence — the domain vocabulary and the behavioral drive are separated by a clause boundary. The semantic neighborhood is slightly less coherent.

Three consecutive framing reversals across experiments 13, 14, and 15 showed that the specific *form* of fusion — whether the sentence is dense vs. fused, compound vs. embedded — does not predict direction consistently. What matters is that the behavioral vocabulary and the domain vocabulary are in close proximity, not which grammatical form achieves that proximity.

The practical principle: entangle the *what* and the *how* in the same sentence. Don't write a sentence about expertise followed by a sentence about behavior. Write a sentence in which the expertise *is* the behavior.

---

## The Vocabulary Specificity Threshold

Not all domain vocabulary is equal. The experiments identified a specificity threshold that vocabulary must cross to activate the consideration set.

**Orientation vocabulary** sits above the threshold in abstraction. "Correctness," "completeness," "production readiness," "best practices" — these words point toward a domain without entering it. Experiments showed orientation vocabulary in either slot produced 0/10 detection on the target finding. The vocabulary is recognizable to the model but does not activate the specific failure-mode vocabulary the task requires.

**Mechanism vocabulary** crosses the threshold. "GC pause," "TTL arithmetic," "lock boundary," "write fencing," "transaction commit race" — these tokens name the causal chain. They live inside the failure-mode cluster, not above it. Experiments with mechanism vocabulary in either the Persona slot or the Instructions slot produced 10/10 detection. Orientation vocabulary in either slot produced 0/10.

The operative distinction is whether the vocabulary names the *mechanism* — the specific causal sequence that produces the failure — or merely orients toward a class of concern. "Production readiness" is orientation. "Whether the TTL arithmetic holds under GC pause" is mechanism.

This threshold explains the credential problem precisely. "Senior software engineer" is orientation vocabulary. It labels a category. It does not name a mechanism. The model recognizes the category and generates category-consistent output — without activating the specific failure-mode vocabulary that would pull the consideration set toward the hard finding.

---

## What to Write

The practical rule follows directly from the mechanism.

**Write the technical substrate, not the credential.**

"Senior software engineer" → "you review distributed systems code for production readiness; before approving any merge, you check whether the write is fenced, whether the TTL arithmetic holds under GC pause, whether the commit boundary is where the failure mode lives."

The second version is longer. It earns its length. Every clause is a gravity well token — a piece of mechanism vocabulary that pre-weights the K/V space toward the failure-mode cluster. The model arrives at the task with a semantic neighborhood that already contains the failure modes it needs to find.

**Entangle the behavioral drive with the domain vocabulary.**

Don't write: "You are an expert in distributed systems. Your reviews are thorough and you never miss a bug." Write: "You are a senior backend engineer who reviews distributed systems code; your review is complete only when the lock boundary, the TTL arithmetic, and the commit race have been explicitly addressed."

The second version fuses domain vocabulary and behavioral drive in the same sentence. The satisfaction condition is named *in the same semantic neighborhood* as the domain.

**Name the mechanism, not the orientation.**

"Consider production readiness" → "check whether the lock is held for the duration of the operation, whether the TTL expires under a GC pause, whether two workers can both believe they hold the same lock."

Every orientation phrase has a mechanism equivalent. The orientation phrase tells the model where to look. The mechanism phrase tells the model what the failure looks like when it gets there.

---

## Why Compulsion Doesn't Travel

The compulsion framing is not useless. "Cannot help but" and "constitutionally unable to" do something — they express behavioral drive, install a sense of automaticity. But the experiments are unambiguous: compulsion framing *without domain vocabulary* produces no amplification over the P_d baseline. Compulsion framing *with domain vocabulary* is outperformed by trait framing with the same domain vocabulary.

The compulsion is not the mechanism. It's a register choice that sounds forceful but produces no reliable lift on its own. Practitioners who have been writing compulsion personas and getting good results are almost certainly getting those results from the domain vocabulary they've been pairing with the compulsion — not from the compulsion itself.

Removing the compulsion and keeping the domain vocabulary: same results.
Adding the compulsion and removing the domain vocabulary: P_d floor.

That's the finding. Domain vocabulary is portable. Compulsion framing is not.

---

## The Anatomy Article, Revisited

The anatomy-of-a-prompt article walked through the thriller novelist persona and noted that the compulsion framing appeared to be doing work. The caveat was honest: "subsequent experiments falsified it."

The thriller novelist persona works because of semantic neighborhood density: *technological thriller novelist*, *deep working knowledge*, *transformer architecture*, *AI research*, *hook*, *escalation*, *cliffhanger*. That cluster is coherent. It pulls attention toward a specific kind of technical dramatic writing. The "can't help but transform" framing is not the mechanism — it's accompanying a very dense domain vocabulary cluster that does the actual installation.

Swap out the domain vocabulary and keep the compulsion. The persona collapses.
Swap out the compulsion and keep the domain vocabulary. The persona holds.

The same experiment that falsified compulsion-as-reflex also explains why every strong persona in the existing examples works: they all contain mechanism-level vocabulary in tight proximity to the identity anchor. The compulsion framing was always a passenger.

---

*This article is based on experiments exp-10b through exp-24, which form Phase 6 of the PARC research program. Full experimental records are in `parc/science/experiments/`. The findings are synthesized in `parc/science/research/findings/pcsieftr.md`.*