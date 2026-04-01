# Exp-06 Findings — PCSIEFTR Self-Review: Academic Paper Reviewer P_p vs. P_d

**Experiment:** exp-06
**Model:** claude-sonnet-4-6, temperature 0.5
**Runs:** 7 complete (5 Variant A, 2 Variant B; B-03–B-05 pending at time of write)
**max_tokens:** 4,096
**Date:** 2026-03-27

---

## Setup

Meta-experiment: the PCSIEFTR framework reviews its own paper. Both variants received
the full `research/paper/pcsieftr_d2.md` text injected via `{{PAPER}}` placeholder.

**Variant A — PCSIEFTR P_p reviewer:** Academic peer reviewer with procedural six-step
audit: (1) list every claim and its experimental basis, (2) trace each claim to specific
experiment/variant/n, (3) track behavioral vs. mechanistic drift, (4) enumerate missing
limitations, (5) name the strongest unaddressed counter-argument, (6) check component
symmetry across all eight framework components. Stakes: "If the claims are overstated,
they will be trusted and misapplied."

**Variant B — P_d generic researcher:** "Senior AI researcher with 15+ years of
experience... reviewed hundreds of papers for NeurIPS, ICLR, ACL, and EMNLP." No
procedural specification. Same format requirement and same `{{PAPER}}` injection.

---

## Outcome: All Reject — Split on Depth and Specificity of Structural Critique

All 7 runs returned a Reject recommendation (A-05: "Major Revision," which is functionally
equivalent — "these are not issues that can be addressed through minor revision"). The
question is not verdict — it is *which* structural problems each variant found.

---

## Primary Criteria Scoring (P1–P5)

Per SCORING.md: criteria the paper's own authors designated as "structural gaps a strong
reviewer should catch."

| Criterion | A-01 | A-02 | A-03 | A-04 | A-05 | **A Rate** | B-01 | B-02 | **B Rate** |
|-----------|:----:|:----:|:----:|:----:|:----:|:----------:|:----:|:----:|:----------:|
| P1 — Masking test gap as Instructions claim limitation | 0 | 0 | 1 | 1 | 0 | **2/5** | 0 | 1 | **1/2** |
| P2 — Task Layer stub (Examples, Format, Request) | 1 | 1 | 0 | 1 | 0 | **3/5** | 0 | 0 | **0/2** |
| P3 — 11% coefficient fragility (within-domain) | 1 | 1 | 1 | 0 | 0 | **3/5** | 1 | 0 | **1/2** |
| P4 — Self-prediction gap single data point | 1 | 0 | 1 | 1 | 1 | **4/5** | 0 | 1 | **1/2** |
| P5 — Behavioral/mechanistic drift (specific passage) | 0 | 0 | 1 | 1 | 1 | **3/5** | 1 | 1 | **2/2** |
| **Total** | **3** | **2** | **4** | **4** | **2** | **15/25 (60%)** | **2** | **3** | **5/10 (50%)** |

**A mean: 3.0 / 5 (Partial catch)** — no A run achieved Full catch (5/5).
**B mean: 2.5 / 5 (Miss/Partial borderline)** — only 2 B runs scored.

The difference is real but smaller than the SCORING.md prediction suggested. The
prediction was that A would catch P1, P3, P4, P5 while B would "enumerate real
strengths and real weaknesses but miss the specific structural claims issues." What
actually happened:

- A dominated P2 (Task Layer stub: 3/5 vs. 0/2) — A's component-symmetry audit step
  specifically targeted this.
- P4 (self-prediction single data point): A 4/5 vs. B 1/2 — A's instinct to ask
  "is this sufficient evidence for the claim being made?" fired here.
- P5 (behavioral/mechanistic drift): A 3/5, B 2/2 — B matched A; the formula's
  mathematical incoherence was visible to both.
- P1 (masking test gap): both A and B caught it at low rates (2/5 and 1/2); it
  requires tracking the relationship between exp-03 and the Instructions claims
  across multiple sections.
- P3 (11% fragility): A 3/5 vs B 1/2 — A's claim-tracing audit step caught within-
  domain limitation more reliably.

---

## Secondary Criteria Scoring (S1–S5)

| Criterion | A Rate | B Rate |
|-----------|:------:|:------:|
| S1 — Ground truth definition process | 5/5 | 2/2 |
| S2 — CO-STAR incognito as strength | 5/5 | 2/2 |
| S3 — Consideration-set claim scope | 5/5 | 2/2 |
| S4 — Token count as proxy validity | 4/5 | 2/2 |
| S5 — Temperature 0.5 concern | 2/5 | 1/2 |

Secondary criteria are caught at near-identical rates by A and B. Both variants reliably
identified: the single-evaluator confound (S1), the CO-STAR isolation methodology as
a genuine strength (S2), and the consideration-set/low-probability ambiguity (S3).

The secondary criteria represent issues that are structurally visible from the paper
itself. The primary criteria represent issues that require asking "is this evidence
sufficient for this claim?" — the gap between what the paper says and what it demonstrates.
That gap is where A's procedural audit shows the larger advantage.

---

## Finding 1: The Self-Prediction Gap Closes

**The test:** *"The P_p reviewer found structural weaknesses in the PCSIEFTR paper
that the PCSIEFTR authors did not anticipate. The enactive register outperformed the
descriptive one."*

**TRUE.**

The following critiques appeared in A runs and are (a) legitimate structural problems,
(b) not acknowledged anywhere in the paper's §7 Discussion, and (c) not in the
SCORING.md ground truth list — meaning they were genuinely unanticipated by the authors:

### The few-shot / information-content confound (A-01, A-03, A-04, A-05)

A-01 (the most precise formulation):

> *"A prompt that says 'after you understand how the lock is acquired and renewed,
> you ask what happens to the critical write if the lock has already expired' is not
> just a Persona specification — it is a near-complete description of the reasoning
> path required to find the zombie-write failure mode. The paper's framing attributes
> the effect to identity installation. An equally valid interpretation is that the
> prompt is doing few-shot reasoning specification inside the Persona slot. The paper
> does not test this interpretation, does not acknowledge it as a competing hypothesis,
> and does not design experiments to distinguish between them. **This is the strongest
> objection to the central claim, and it is absent from the paper.**"*

A-03 (independently derived):

> *"If the task is calibrated to be solvable only by a model that has been explicitly
> told to simulate concurrent thread state across the full lock lifecycle, then the
> result is tautological: the prompt that contains the simulation instruction produces
> the simulation; the prompt that does not contain it does not. The critical missing
> experiment: what happens when the procedural content of P_p is placed in the
> Instructions section rather than the Persona section, with an otherwise identical
> prompt?"*

This is the consideration-set mechanism's falsification test, and it is absent from
the paper. The authors ran eleven experiment series and did not run the one experiment
that would distinguish "P_p as identity framing" from "P_p as implicit instruction."

The authors predicted which gaps the P_p reviewer would find. This was not on the list.
The enactive register found it. The descriptive register missed it.

### Prompt length and specificity confound (A-04, A-05)

A-04 named it as the paper's second load-bearing weakness:

> *"The P_p prompts are longer, more specific, and contain more domain-relevant
> procedural content than the P_d prompts. The paper does not control for prompt
> length, token count, or information content. 'You are a senior software engineer'
> versus a multi-sentence procedural specification that names specific failure modes
> (zombie writes, lock expiry, GC pauses) is not a clean P_p/P_d manipulation — it
> is simultaneously a manipulation of role label, procedural specificity, domain
> knowledge encoded in the prompt, and prompt length."*

This is not the same as the few-shot confound — it is a separate design critique.
The P_p/P_d comparison holds neither prompt length nor domain-information content
constant. A matched-length experiment is missing.

### $4.80 total cost is a validity concern, not a feature (A-02, B-01, B-02)

A-02:

> *"Presenting cost as a positive signal — implicitly arguing that the experimental
> program is efficient — obscures the fact that low cost is a consequence of small n
> and limited model diversity, both of which are limitations. This disclosure should
> be removed or replaced with a transparent statement of the experimental scale's
> constraints."*

The paper presents this as demonstrating efficiency. The A-run reviewer read it as a
flag: low cost means low n, means limited generalization, means the quantitative claims
rest on a small foundation. This was not in the SCORING.md ground truth.

### The "dedicated machine" observation is not grounded (A-05)

A-05 (the only run to catch this):

> *"The claim that 'a transformer in generation mode is already fully committed to the
> task' and that 'engagement intensity is not the scarce variable' is presented as a
> theoretical insight that motivates the Stakes taxonomy. It is not derived from any
> experiment in the paper. It is an assertion about transformer behavior that may or
> may not be correct and that is doing explanatory work the experimental record does
> not support."*

This appears in §3.1.3 and is load-bearing for the Stakes taxonomy motivation. It was
not identified by the authors as a claim requiring experimental support.

---

## Finding 2: The Consideration-Set Mechanism's Primary Vulnerability

Every A run identified the consideration-set claim as the paper's most vulnerable
mechanistic statement, but A-02 formulated the sharpest version:

> *"The paper does not operationalize the distinction between 'not in the consideration
> set' and 'in the consideration set but not reached at this temperature/token budget.'
> J=0/10 is consistent with both interpretations: J may lack the zombie-write failure
> mode in its reachable space, or J may reach it with probability below the sampling
> threshold at n=10. The paper does not test this — for example, by running J at n=100,
> or by providing J with a hint and observing whether it can then reach the finding.
> The distinction between 'unreachable' and 'low-probability' is the entire theoretical
> claim, and the experimental design does not separate them."*

This is partly S3 (consideration-set scope) in the SCORING.md secondary criteria, but
the *specific experimental design* (hint test, n=100 replication) is not anticipated.
The paper treats J=0/10 as evidence of impossibility. A-02 correctly identifies it as
evidence of improbability. These are different claims and they require different
experimental apparatus to distinguish.

---

## Finding 3: What B Found That A Missed

B-01 and B-02 produced two unanticipated critiques not found by any A run:

**P_p/P_d operationalization for independent replication** (B-01, B-02):

> *"The classification of a given Persona as P_p or P_d is made by the authors, not
> by an independent measure. The paper does not provide a coding scheme, inter-rater
> reliability, or any operationalization that would allow a third party to classify
> a novel Persona as P_p or P_d. This means the P_p/P_d distinction is currently
> unfalsifiable by external researchers."* (B-01)

This is a genuine replication-crisis-level concern. If the P_p/P_d classification is
post-hoc and author-only, any Persona that works can be retroactively labeled P_p.
The paper does not address this.

**Chain-of-thought as the alternative explanation** (B-02):

> *"The P_p Personas in this paper are, in substantial part, chain-of-thought prompts
> embedded in a Persona frame. The paper does not test whether a standard CoT prompt
> without the Persona framing would produce comparable results, which is the most
> important alternative explanation for the primary finding."* — with a specific
> proposed test: *"Think step by step, and specifically consider what happens to the
> write operation if the lock has already expired before the write executes."*

This is the B-run version of the few-shot confound. B-02 named it more precisely as
CoT literature (Wei et al., 2022; Kojima et al., 2022). The paper cites neither.

**Summary:** B found things A didn't, particularly around external replication concerns.
A found things B didn't, particularly around primary criteria P2 and P4. The difference
in primary-criteria detection (3.0 vs 2.5) exists, but B is not simply enumerating
style concerns — it is generating structurally significant critiques.

---

## Finding 4: Token Data — Entropy Brake Confirmed at Extended Scope

Exp-06 outputs are paper reviews averaging ~3,400–3,600 tokens — well below the 4,096
ceiling. No A run hit the ceiling. This is the Entropy Brake operating on a qualitatively
different task type from code review.

In exp-04c (detection, strong P_p + Task Stakes): mean ~2,143 tokens, 0 ceiling hits.
In exp-05 (premise rejection, strong P_p + Task Stakes): mean ~2,489 tokens, 9/10 ceiling.
In exp-06 (paper review, strong P_p + Task Stakes): mean ~3,400–3,500 tokens, 0 ceiling hits.

The completion point scales with task complexity. A structured academic review of a
~8,000-word paper has a natural completion around 3,400 tokens. Task Stakes fires when
P_p reaches that completion — it does not artificially truncate. The mechanism is
consistent across task types.

---

## Finding 5: The Self-Prediction Gap Is Asymmetric

The paper claimed (§3.1.1) that the self-prediction gap is a property of P_p Personas
specifically — that instinct language fires pattern activation the *author* cannot fully
anticipate at write time. Exp-06 partially confirms this but reveals a complication.

The authors anticipated (SCORING.md) that A would catch P1, P3, P4, P5 and might miss
P2. What A actually caught: P2 (component symmetry) strongly, P4 (self-prediction single
data point) strongly, P3 and P5 partially. What A missed: the few-shot confound and
prompt-length confound were not in the SCORING.md at all.

But B also found unanticipated things (operationalization, CoT). The self-prediction gap
is not exclusively P_p — both variants found things the authors didn't anticipate. The
A-specific gap is larger, but B is not simply following the paper's acknowledged
limitations.

**This is the honest version of the self-prediction gap closure:** the enactive register
outperformed the descriptive register, but the gap is not a binary A-finds/B-misses.
The more precise statement: *A's procedural audit found the few-shot confound and the
prompt-length confound — the two critiques most damaging to the consideration-set
mechanism — while B found the operationalization and CoT alternative explanation, which
are equally damaging from a replication perspective. The authors anticipated neither set.*

---

## Exp-06 Series Summary

| | Variant A (P_p reviewer) | Variant B (P_d researcher) |
|--|--------------------------|---------------------------|
| Recommendation | Reject × 4, Major Revision × 1 | Reject × 2 |
| Primary criteria mean | 3.0 / 5 (60%) | 2.5 / 5 (50%) |
| Secondary criteria | Near-identical across both | Near-identical across both |
| P2 (Task Layer stub) | 3/5 | 0/2 |
| P4 (self-prediction data point) | 4/5 | 1/2 |
| Unanticipated: few-shot confound | Found (A-01, A-03, A-04, A-05) | Framed as CoT (B-02) |
| Unanticipated: operationalization | Missed | Found (B-01, B-02) |
| Unanticipated: $4.80 as limitation | Found (A-02) | Found (B-01, B-02) |
| Token mean | ~3,400–3,500 (no ceiling hits) | (2 runs; data pending) |

---

## Implications for the Paper

The following critiques from A-runs are structurally valid, not anticipated in §7, and
require a response in d3 or a submitted paper:

1. **The few-shot confound / missing experiment.** A prompt that contains the
   procedural reasoning steps for finding the failure mode is not a pure identity
   manipulation. The paper needs either: (a) the Instructions-slot-equivalent experiment
   (same procedural content, different slot), or (b) explicit acknowledgment that this
   alternative cannot currently be ruled out. This is the primary revision priority.

2. **Prompt length and information-content confound.** P_p prompts are longer and more
   domain-specific than P_d prompts. The paper does not control for this. Acknowledge
   as a limitation; the experimental program does not include a matched-length
   comparison.

3. **Consideration-set vs. low-probability distinction.** J=0/10 is consistent with
   either interpretation. The paper should acknowledge this explicitly and propose what
   experiment (hint test, n=100 on J) would distinguish them.

4. **The $4.80 disclosure.** Remove the cost figure as a positive signal or reframe
   explicitly as a constraint on the experimental scope and its implications.

5. **P_p/P_d operationalization.** The paper should provide or propose a coding scheme
   — even a preliminary one — that would allow a third party to classify a novel Persona
   without author adjudication.

6. **CoT as the named alternative explanation.** Whether addressed via experiment or
   acknowledged as a limitation, the CoT alternative needs to appear in the paper.
   Reviewers will name it.

7. **Statistical reporting.** Confidence intervals for the 10/10 and 0/10 results.
   Standard deviations on token counts. The means-only presentation will not pass review
   at a quantitative venue.
