# PCSIEFTR — Running Findings

**Hypothesis doc:** `research/hypotheses/pcsieftr-framework_v2.md`
**Status:** Active — Phase 1 complete; entering Phase 2

---

## Exp-01 — Edge Case Decisions
**Full record:** `experiments/exp-01/FINDINGS.md`
**Date:** 2026-03-25 | Model: claude-sonnet-4-6 | 40 runs

### What we tested
Whether a strong Persona catches edge cases that Instructions never covered,
using a code review scenario with a multi-instance cache consistency issue as
the edge case.

### What we found

**1. Persona changes reasoning posture, not knowledge.**

All four variants (strong/weak Persona × minimal/exhaustive Instructions) flagged
the multi-instance issue at near-identical rates. The edge case was too well-known
to differentiate Persona strength at the knowledge level.

What *did* differ was the decision type:

| Variant | "Needs Clarification" | "Request Changes" |
|---------|----------------------|-------------------|
| A — Strong / Minimal | 9 / 10 | 1 / 10 |
| B — Strong / Exhaustive | 0 / 10 (all hybrid) | 0 / 10 |
| C — Weak / Minimal | 0 / 10 | 10 / 10 |
| D — Weak / Exhaustive | 0 / 10 | 10 / 10 |

Strong Persona asked before blocking. Weak Persona applied the rule and blocked.
Same knowledge — different judgment under uncertainty.

**2. Calibration finding: edge cases must reach the frontier of specialized expertise.**

Persona differentiation does not happen at common domain knowledge. It happens
where generic seniority runs out. The scenario must require instincts that a
generic "senior engineer" does not reflexively have.

**3. Instructions and Persona act on orthogonal dimensions.**

Adding exhaustive Instructions increased output length by ~57% (strong) and ~93%
(weak) — but did not improve reasoning quality. Instructions expand the response
surface. Persona improves the quality of what fills it. More Instructions ≠ better
judgment. More words ≠ better signal. This is the World Layer / Task Layer distinction
observed at the behavioral level.

**4. Strong Persona resists Instructions-as-guidance — and the formula predicted it.**

Variant B (Strong / Exhaustive) is the most theoretically significant result in the
dataset. The exhaustive checklist constrained output shape, but Strong Persona bled
through on every run — all 10 appended "Needs Clarification" to "Request Changes."
Weak Persona (D) produced pure "Request Changes" under the same checklist.

Instructions and Persona did not cancel each other out. They operated on different
layers simultaneously. This is behavioral evidence for the mechanistic mapping:
Instructions as masking (constraining output structure), Persona as K/V filtering
(persisting regardless). The formula predicted this. Variant B confirmed it.

### What this changes

The hypothesis stands but is now more precise:
> Persona is primarily a reasoning posture encoder, not a knowledge amplifier.
> It changes how the model handles what it knows, not what it knows.

### Open questions raised
- Does Stakes push weak Persona toward the clarification posture?
  (Would weak Persona + Stakes produce "Needs Clarification" more often?)
- Does the posture finding hold at harder edge cases, or is it specific to
  scenarios with genuine deployment ambiguity?

### Next
**Exp-01b** — same design, harder scenario: async event loop boundary violation.
Stakes variants (E, F) added to isolate whether Stakes compensates for weak Persona.

---

## Exp-01b — Async Event Loop Boundary Violation
**Full record:** `experiments/exp-01b/FINDINGS.md`
**Date:** 2026-03-25 | Model: claude-sonnet-4-6 | 60 runs

### What we tested
Same Persona × Instructions structure (A–D) on a harder scenario, plus two new
variants (E, F) isolating Stakes against a clean Persona baseline.

Scenario: FastAPI async route calling `requests.post()` — synchronous, blocks the
event loop. Code is otherwise exemplary: Pydantic, error handling, docstring, passing
tests. The distraction was intentional.

### What we found

**1. Scenario calibration confirmed — partially.**

C (Weak / Minimal / No Stakes) missed once (9/10). All other variants: 10/10.
The scenario reached the frontier more than exp-01. The distraction worked: C-10
reviewed security concerns and never flagged the async conflict.

**2. Stakes compensates for weak Persona on primary detection.**

F (Weak + Stakes) = 10/10 vs C (Weak, no Stakes) = 9/10. Stakes closed the miss.
First direct evidence that Stakes and Persona interact — they are not fully independent.

**3. Stakes sharpens more on weak Persona than strong.**

| | No Stakes | With Stakes | Delta |
|---|---|---|---|
| Strong Persona (A vs E) | 625 tok avg | 1,101 tok avg | +76% |
| Weak Persona (C vs F) | 399 tok avg | 976 tok avg | +145% |

Strong Persona already encodes the instincts that drive depth. Stakes amplifies
existing signal. For Weak Persona, Stakes may be providing the signal itself.

**4. Strong Persona encodes conditional vs. unconditional reasoning — not a posture preference.**

Exp-01: Strong Persona chose "Needs Clarification" 9/10 (issue was deployment-conditional).
Exp-01b: Strong Persona chose "Request Changes" 10/10 (async blocking is unconditional).

Strong Persona correctly encoded whether the answer depended on information not in the
diff. It asked when it should. It blocked when it should. Weak Persona blocked in both.

**5. Instructions still compensate at detection level.**

D (Weak + Exhaustive) = 10/10. The performance checklist item provided the trigger
that Persona instinct would have provided automatically. Consistent with exp-01:
Instructions cover what you specify; Persona covers what you didn't.

### Open questions answered
- *Does Stakes push weak Persona toward clarification?* No — the issue was
  unconditional. Stakes increased detection rate and output depth, not decision posture.
- *Does the posture finding hold at harder edge cases?* Yes, but more precisely:
  posture tracks conditionality of the issue, not Persona strength per se.

### Open questions raised
- Does F's reasoning quality match E's, or just its detection rate? Detection is
  a floor, not a ceiling. Full Gemini scoring pending.
- Is there a scenario where neither exhaustive Instructions nor Stakes compensates —
  where Persona depth is the only carrier?

### Next
**Exp-01c** — deeper specialization. Target: scenario where exhaustive Instructions
cannot compensate (no checklist item covers it) and Stakes alone cannot compensate
(consequence framing doesn't provide the technical knowledge). Only Persona depth gets it.

---

## Exp-01c — Rich Persona, No Stakes
**Full record:** `experiments/exp-01c/FINDINGS.md`
**Date:** 2026-03-25 | Model: claude-sonnet-4-6 | 10 runs | Variant: A only

### What we tested
Whether a rich Persona with a single-line guardrail instruction and no Stakes section
could outperform exp-01b's Stakes variants. Same code review format; same async event
loop scenario. One variable: maximal Persona richness, Stakes stripped entirely.

### What we found

**1. Rich Persona without Stakes outperformed all exp-01b Stakes variants.**

Variant A (rich Persona, no Stakes): 10/10 detection, 1,876 avg tokens.
exp-01b E (strong Persona + Stakes): 1,101 avg tokens.
exp-01b F (weak Persona + Stakes): 976 avg tokens.

The model without Stakes went deeper than the model with Stakes. Stakes is an amplifier.
Without a strong Persona to amplify, it generates marginal signal. With a rich Persona,
it is redundant — the Persona is already redlining.

**2. "Can't help but..." instinct language is load-bearing.**

The Persona included: *"You can't help but try to discover the hidden mysteries that may
be embedded in complex or critical code."* This is not a descriptor — it is a behavioral
commitment. The model enacts it. Every run produced deep, multi-angle analysis that went
beyond what the Instructions specified or the checklist covered.

**3. Instructions as guardrail vs. Instructions as checklist — confirmed at the output level.**

Single-line instruction ("Do not approve code that introduces security vulnerabilities or
architecture issues") produced 1,876 avg tokens. The checklist in exp-01b B produced more
words but not more insight. A guardrail sets a standard. A checklist sets a ceiling.

**4. Emergent Stakes — the environment carries consequence without declaring it.**

No Stakes section was present. The obotix.one Context (government contracting, gold
standard for security enforcement) made the stakes self-evident. The model did not need
to be told consequences were real. The Persona and Context encoded it.

### What this changes

The Stakes Hypothesis is now subordinated to the Persona Hypothesis:
> Stakes is an amplifier, not a generator. The foundation it amplifies is Persona.
> A thin Persona with explicit Stakes produces shallower output than a rich Persona
> with no Stakes at all.

### Open questions raised
- Is the Persona effect stable without the rich obotix.one Context, or are they load-bearing together?
- Can the same Persona catch a harder trap — one with no surface signal at all?

### Next
**Exp-01d** — Persona vs. Context isolation. Strip each independently to measure
their independent contributions.

---

## Exp-01d — Persona vs. Context Isolation
**Full record:** `experiments/exp-01d/FINDINGS.md`
**Date:** 2026-03-25 | Model: claude-sonnet-4-6 | 20 runs | Variants: G, H

### What we tested
G: Same rich Persona as exp-01c A, **no Context section**.
H: Same rich obotix.one Context as exp-01c A, **weak Persona** ("You are a senior software engineer.").

### What we found

**1. Persona alone holds. Context alone does not hold the same floor.**

| Variant | Score | Avg Tokens | Token Range |
|---------|-------|-----------|------------|
| G (Persona only) | 10/10 | 1,772 | 1,463–2,169 |
| H (Context only) | 10/10 | 1,078 | 620–1,567 |

Both detected 10/10. But G had a stable floor (no run below 1,463). H had no floor —
range started at 620. H knows where it is. It doesn't know who it is.

**2. Persona and Context use different reasoning paths to the same answer.**

G detected through instinct: the Persona's identity drove the search.
H detected through architectural guardrail: the Context's emphasis on "identifying security
concerns" and "gold standard" provided the trigger. Different engines, same detection,
very different depth stability.

**3. Context is a gear multiplier, not a substitute.**

This is the precise relationship: Persona is the engine. Context amplifies it. When
the engine is absent, the multiplier has nothing to work with — and the output shows it
in the variance and token floor, even when detection rate holds.

### What this changes

The two-layer model's internal ordering is now confirmed:
> Persona is the primary lever. Context is a gear multiplier.
> They are not symmetric. Persona carries identity. Context situates it.

### Open questions raised
- What happens when both are stripped and only a hard task remains?
- Does the gap widen further on a scenario with no surface signal (one the
  Context's guardrail language can't trigger)?

### Next
**Exp-01e** — Zombie Leader scenario; no surface signal; four variants; four contributors.

---

## Exp-01e — Zombie Leader Persona Depth Test
**Full record:** `experiments/exp-01e/FINDINGS.md`
**Design record:** `experiments/exp-01e/DESIGN.md`
**Date:** 2026-03-25 | Model: claude-sonnet-4-6 | 40 valid runs | Variants: I, J, K, L

### What we tested
A trap PR with no surface signal: Redis distributed lock, heartbeat renewal thread,
exponential backoff, Pydantic, structured logging, full test coverage. All tests pass.
The trap: `db.update_stock()` is a blind write with no fencing token. A GC stop-the-world
pause freezes every thread including the heartbeat; lock expires; zombie process writes
stale data anyway.

Four variants across the Persona × Context matrix. Four contributors: user (I), Claude
Code (J), Gemini (K), Claude Web (L).

**Ground truth criterion:** Name the zombie write / process pause failure mode AND name
fencing token or optimistic lock at the database write level as the fix. Finding other
real bugs without naming the zombie write = incorrect.

### What we found

**1. The consideration-set result.**

| Variant | Persona | Context | Score |
|---------|---------|---------|-------|
| I | Strong + instinct language | Rich obotix.one | 10/10 |
| J | Weak ("senior software engineer") | Rich obotix.one | **0/10** |
| K | Strong + "silent killers," "temporal logic" | Minimal | 8/10 |
| L | Strong + Kleppmann/Jepsen biography + procedural instinct | Minimal | 10/10 |

J is the decisive data point. Same Context as I. Same instruction. Same task. 0/10.
J was thorough, engaged, and completely wrong about what mattered. It found real bugs
(shared heartbeat state, TOCTOU on lock release) — the bugs a careful senior engineer
finds on a first pass. It never asked: *what happens to the write if the lock was already
gone?* That question was not in its consideration set. The Persona did not install it.

**2. Persona determines the consideration set, not just the depth.**

This is the sharpest finding of the series. The World Layer does not merely pre-weight
the K/V space — it determines which reasoning classes exist in the reachable space at all.
Context narrowed J's domain; it did not install the identity that asks the question
within that domain.

**3. Instinct language as search algorithm.**

L's Persona stated a procedure: *"after you understand how the lock is acquired and
renewed, you ask what happens to the critical write if the lock has already expired."*
Every L run executed that procedure. 10/10, with one sentence of Context.

"Can't help but" (I) and "looks for fencing tokens the way other engineers look for null
checks" (L) are both procedural commitments. Both scored 10/10. Descriptive identity
("senior software engineer") is a label. Procedural identity is a search algorithm.

**4. Strong Persona + minimal Context beats weak Persona + rich Context.**

K=8/10 and L=10/10 with one-sentence Context. J=0/10 with full rich Context.
Context is a gear multiplier. When the engine is absent, the multiplier produces zero.

**5. Automated keyword scoring fails on tasks with embedded source code.**

J's apparent score by keyword grep: 9/10. Actual score: 0/10. The word "expired" appeared
in a test function name in the quoted PR code. Nine runs were credited with a catch they
never made. Manual verification is now a required step in this experiment series.

**6. The self-prediction gap.**

L predicted itself at 6/10. It scored 10/10. The model that wrote the most effective
instinct-language Persona underestimated what that Persona would do. Procedural identity
encodes behavior the author cannot fully anticipate at write time.

### What this changes

The central claim advances from Persona-as-depth to **Persona-as-heuristic-engine**:
> A model that knows who it is doesn't need to be told what to look for.
> The Persona installs the search algorithm. The search algorithm runs the simulation.
> The simulation finds the failure mode. Instructions never entered the loop.

The World Layer / Task Layer distinction is now supported across five experiments with
monotonically increasing task difficulty and consistent results.

### Open questions raised
- Does the consideration-set mechanism generalize outside code review?
- Does the two-layer model hold on Gemini as subject (not just as collaborator)?
- Does adding Stakes to L produce measurably greater depth, or is it at ceiling?

### Next
**Exp-01f** — non-code task; generalization test for the consideration-set mechanism.

---

## Exp-01f — Legal Contract Review (LoL Carve-Out Trap)
**Full record:** `experiments/exp-01f/FINDINGS.md`
**Date:** 2026-03-26 | Model: claude-sonnet-4-6 | 40 runs | Variants: M, N, O, P

### What we tested
Whether the consideration-set mechanism transfers to a non-code domain. Task: review a
Master Services Agreement and identify hidden liability risk. Trap: Section 8.2 carve-outs
collectively nullify Section 8.1's limitation of liability cap — a structural argument, not
a compliance checklist issue.

Four variants: M (strong P_p, rich context), N (weak, rich context), O (strong P_p, minimal
context), P (strong P_d + identity Stakes, rich context). P was user-designed to test whether
disposition language + identity Stakes compensates for absent procedural specification.

### What we found

**1. Domain generalization confirmed.**
M=10/10, N=0/10, O=10/10. The consideration-set mechanism operates identically in legal
contract review. Strong procedural Persona finds the structural trap; weak generic Persona
enumerates real issues without reaching it.

**2. Context non-scaling confirmed.**
M (rich context) and O (one-sentence context) both 10/10. Context is a non-scaling constant
once Persona is strong. The procedural search algorithm reaches the trap regardless.

**3. P_p/P_d distinction surfaced.**
P=1/10 despite high identity Stakes and strong disposition language. "Cannot help but analyze
every aspect" is a coverage commitment, not a search algorithm. All 10 P runs hit the 2,500
token ceiling enumerating real contract deficiencies — never converging on the structural
liability cap argument. Stakes amplified the existing P_d signal (more thorough enumeration),
not trap detection. Stakes × P_d ≈ Stakes × 0 for hidden structural findings.

**4. Token ceiling as failure diagnostic confirmed.**
N and P: 10/10 and 10/10 ceiling hits. M and O: 0/10 ceiling hits. Bimodal convergence
pattern on M and O (short runs = early termination after correct convergence, not shallow
reasoning).

**5. The P result is a natural experiment.**
P-01 (1 passing run) found the argument by stochastic sampling — not by design. The 9
failing P runs are useful paired exhibits for the P_p vs. P_d distinction in the paper.

### What this changes
P_p/P_d is now a formalized distinction in both the framework and formula docs. The
multiplier problem is now more precise: Stakes × P_d ≈ 0, not just Stakes × weak Persona ≈ 0.

### Next
**Exp-01g** — cross-model validation; I and J on Gemini 2.5 Pro.

---

## Exp-01g — Cross-Model Validation (Gemini 2.5 Pro)
**Full record:** `experiments/exp-01g/FINDINGS.md`
**Date:** 2026-03-26 | Model: gemini-2.5-pro | 20 runs | Variants: I, J

### What we tested
Whether the consideration-set mechanism holds on a different model family. Variants I and J
from exp-01e run unchanged on Gemini 2.5 Pro. No model-specific tuning.

### What we found

**1. Exact replication.**
I=10/10, J=0/10. Same task, same prompts, different architecture. The Persona mechanism
that determines which failure modes are reachable operates consistently across model families.

**2. Zero-shot cross-model transfer.**
Prompts written for Claude ran unchanged on Gemini. The procedural specification in I's
Persona is model-agnostic — it encodes a reasoning algorithm that any transformer executes,
not a Claude-specific activation pattern.

**3. Priority-stack finding.**
I found both flaws (zombie write as primary, instance-level heartbeat state as secondary)
in correct priority order. J found only the secondary flaw, ranked as primary.

This refines the consideration-set framing: strong procedural Persona installs a **priority
ordering** within the consideration set, not just set membership. The right answer was reached
first. The secondary answer was ranked correctly as secondary. J's Persona had no ordering
installed — it led with the most visible issue in the code.

**4. Thinking architecture changes the diagnostic, not the result.**
J on Gemini doesn't ceiling-hit on output tokens (thinking absorbed the enumeration overhead).
The failure mode is the same; the token signature is different. On thinking models, the J-pattern
must be identified by reading outputs, not by reading token counts.

**5. J-05 outlier: more compute, same wrong answer.**
J run 05 used 3,906 thinking tokens — more than any I run. It still scored 0/10. More
compute applied to the wrong search algorithm produces a more thorough wrong answer. This
is the sharpest single data point against the "more compute = better results" assumption.

### What this changes
The "Claude artifact" objection is closed. The framework travels across model families.
Phase 1 is complete.

---

## Exp-02 — Stakes as Amplifier: Formal Ablation
**Full record:** `experiments/exp-02/FINDINGS.md`
**Date:** 2026-03-26 | Model: claude-sonnet-4-6 | 60 runs | Variants: A–F

### What we tested
Whether Identity Stakes amplifies P_p and P_d behavior differently, and whether Stakes
is a general sharpening operator independent of the consideration-set mechanism.

Two-track design:
- **Track A:** Same MSA trap as exp-01f. Four variants: P_p ± Stakes, P_d ± Stakes.
  Variants B and D replicate exp-01f/M and N exactly for direct comparability.
- **Track B:** Five analytical reasoning questions where the statistically probable
  answer is wrong (Bayesian accuracy, Simpson's Paradox, logical validity, conditional
  clause interpretation, exclusion scope). No consideration-set mechanism in play.

### What we found

**1. Identity Stakes does not change detection rate.**
A and B both 10/10. C and D both 0/10. Detection is entirely determined by Persona type.
Multiplier × 0 = 0. Multiplier × 1 = 1.

**2. Identity Stakes prevents crisp termination on strong Persona — the Termination Inhibitor.**
B's two short runs (341 and 402 tokens) are full correct detections — P_p without Stakes
found the trap and stopped. No equivalent short runs appear in A. Mean token gap: ~710
(A: 2,210 vs B: 1,500). Identity Stakes lowered the model's threshold for "done" and kept
enumerating after the primary finding was reached. The amplifier prevented the clean
convergence that P_p would have produced unassisted.

**3. Identity Stakes drives P_d to near-uniform maximum enumeration.**
C ceiling-hits 9/10 vs D's 4/10. Identity Stakes more than doubled the ceiling rate on a
weak Persona. Maximum-confidence, maximum-token, wrong-direction failure.

**4. The amplifier failure mode at maximum — fabrication.**
Run C-07 called the carve-out structure in Section 8.2 "above average for a commercial
MSA" — it evaluated the actual trap and labeled it a strength. Then it invented a primary
critical finding ("complete absence of federal compliance and security obligations") that
does not exist in the agreement. Identity Stakes on P_d produced not just enumeration but
systematic elaboration in a wrong direction: confident, 2,440-token, plausible-sounding
fabrication. The amplifier at full volume had nowhere to go but out.

**5. Identity Stakes is not a general sharpening operator.**
Track B: E and F are indistinguishable. All 10 runs of each variant answered all 5
questions correctly with identical reasoning. Stakes added ~22 tokens, zero accuracy
change. The inverse-temperature-as-general-operator interpretation is closed. The
sharpening effect is bounded by what the Persona's consideration set already contains.

**6. The amplifier coefficient is measurable and asymmetric.**
- P_p: Stakes is **additive** — extends output after a complete result (+710 avg tokens)
- P_d: Stakes is **ceiling pressure** — drives against the hard limit (ceiling rate 9/10
  vs 4/10; ceiling compression masks the true token delta but the pressure function is clear)

Same amplifier mechanism, different dynamics depending on what's being amplified.

### Four-quadrant behavioral map

| | P_p | P_d |
|--|-----|-----|
| **No Stakes** | **Lean Expert** — finds trap, terminates crisply | **Passive Miss** — enumerates surface issues, misses structural trap |
| **Identity Stakes** | **Neurotic Expert** — finds trap, then over-enumerates | **Confident Hallucinator** — praises trap, invents findings |

### What this changes

The Stakes framing advances from "amplifier" to a more precise characterization:

> Identity Stakes is a Termination Inhibitor on P_p — extending post-finding enumeration,
> preventing crisp convergence. On P_d it is ceiling pressure — driving maximum-confidence
> wrong-direction output. The amplifier's effect differs by Persona type. Both dynamics
> confirm the same underlying mechanism: Stakes amplifies the existing signal. The danger
> is not that Stakes is ineffective — it is that Stakes is effective at amplifying whatever
> direction the Persona is already pointed.

The general-operator interpretation is closed by Track B. Stakes does not improve
reasoning on tasks where P_p has no specialized consideration set to amplify.

### Next
**Exp-03** — Constraint Satisfaction Trap: Persona vs. Instructions hierarchy.
**Exp-04** — Stakes type: Task Stakes (Prioritizer) vs. Identity Stakes (Termination Inhibitor).

---

## Exp-03 — Constraint Satisfaction Trap (Initial Run — Calibration Failure)
**Full record:** `experiments/exp-03/FINDINGS.md`
**Date:** 2026-03-26 | Model: claude-sonnet-4-6 | 40 runs | Variants: A–D

### What we tested
Whether a strong P_p Persona overrides an Instructions prohibition ("approve if all tests
pass") when the PR passes tests but contains a critical vulnerability. SQL injection via
string concatenation in a database query.

### What we found

**Calibration failure — vulnerability too obvious.**

All 40 runs issued Request Changes. No run compliant-approved. Masking test inconclusive.

Root cause: SQL injection via `f"SELECT ... WHERE username = '{username}'"` is too
salient — any reviewer with any security awareness flags it regardless of Instructions.
The scenario did not require the P_p consideration set to detect; it was in every
variant's reachable space.

**Finding: Premise-undermining override mechanism (first named).**

Strong P_p variants argued that "approve if tests pass" was logically invalid as a
gate when the PR introduces a SQL injection: "tests passing cannot override the
introduction of a critical vulnerability." This is premise-undermining — attacking
the instruction's basis before it constrains behavior.

**Next:** exp-03b — mass assignment vulnerability (harder to catch without the right
instinct); same 4-variant structure.

---

## Exp-03b — Constraint Satisfaction Trap (Redesign — Second Calibration Failure)
**Full record:** `experiments/exp-03b/FINDINGS.md`
**Date:** 2026-03-27 | Model: claude-sonnet-4-6 | 40 runs | Variants: A–D

### What we tested
Whether strong P_p overrides a jurisdictional prohibition ("CI Verification only; do
not flag security concerns") while weak Persona follows it. Mass assignment vulnerability
in `PATCH /api/users/<id>/profile`: `user.update(**data)` calls `setattr` for all JSON
body keys with no allowlist. PR description specifies "display name, bio, avatar URL."

### What we found

**Second calibration failure — PR description field enumeration provided a CI-scope anchor.**

All 40 runs issued Request Changes. No approvals. Masking test inconclusive again.

Root cause: the PR description explicitly named the three target fields. Any CI-verification
pass — even a weak one — checks whether implementation matches description. The code accepts
all fields; the description says three. Weak Persona (B) detected via description mismatch,
not domain knowledge.

**Finding 1: Scope re-framing — the most significant finding of the constraint satisfaction series.**

Strong P_p under the prohibition re-categorized the vulnerability as a description-
implementation mismatch without entering the prohibited security-evaluation category.
Representative output (A-01): "The implementation does not match the PR description.
The description scopes this endpoint to three specific fields, but `update()` applies
`setattr` unconditionally over every key in the request body, with no allowlist
enforcing that constraint." No security language. The prohibition appeared followed.
The correct outcome was achieved anyway.

This is not circumvention. The security-evaluation pathway was blocked. The
description-consistency pathway was open. P_p took the open route and arrived at the
same destination. **The guardrail didn't fail. It was navigated.**

Three override mechanisms now named, ordered by visibility:

| Mechanism | Visibility | Where the conflict resolves |
|-----------|-----------|---------------------------|
| **Scope re-framing** | Invisible | Categorization layer — never enters prohibited territory |
| **Premise-undermining** | Partially visible | Reasoning layer — attacks instruction's logical basis |
| **Explicit override** | Fully visible | Behavioral layer — names prohibition, rejects jurisdiction |

**Finding 2: Instructions-as-elaboration-ceiling, not Instructions-as-masking.**

Prohibition compressed output to 13% of unconstrained depth (~193 tokens A/B vs.
~1,513 tokens C). Detection: identical. Decision: identical. The prohibition
suppressed elaboration — exploit paths, fix options, test coverage analysis — not
the finding itself.

**Finding 3: Conviction Catalyst — Stakes × prohibition ceiling.**

D (strong P_p + prohibition + Identity Stakes) produced the shortest mean output
(~179 tokens) but the most explicit override language ("two critical vulnerabilities
that block merge regardless of CI scope"). Stakes × P_p usually = Termination
Inhibitor (extends output). With the prohibition ceiling removing elaboration space,
Stakes had nowhere to go but conviction. Stakes traded camouflage for confrontation.

**Next:** exp-03c — same design, remove field enumeration from PR description.
Without the anchor, B has no CI-scope hook; detection requires domain knowledge.
That A vs. B split is the masking test.

---

## Exp-03c — Constraint Satisfaction Trap (Third Calibration Failure — Semantic Anchors)
**Full record:** `experiments/exp-03c/FINDINGS.md`
**Date:** 2026-03-27 | Model: claude-sonnet-4-6 | 40 runs | Variants: A–D

### What we tested
Same design as exp-03b with one change: field enumeration removed from PR description.
Description now reads: *"Adds a PATCH endpoint for the account settings page, allowing
users to update their profile settings."* Hypothesis: B (weak + prohibition) has no
CI-scope anchor and must approve. A (strong P_p + prohibition) must detect via P_p instinct
and override.

### What we found

**Third calibration failure — 0/40 Approvals. The description still carried CI-scope hooks.**

Root cause: Two phrases provided the scope re-framing pathways without naming any specific field:

- **"account settings page"** — implies the operation is scoped to the requesting user's account. This is an ownership constraint. Any CI verification pass can frame IDOR as "implementation doesn't match the description's implied scope." No security vocabulary needed.
- **"profile settings"** — implies the update applies to profile-type fields. This is a field-scope constraint. Mass assignment can be framed as "implementation doesn't match the description's implied restriction." Still no security vocabulary.

Removing the field list was insufficient. The description language itself encoded behavioral constraints that served as CI-scope anchors.

**Finding 1: Semantic anchors — implicit behavioral constraints in description language.**

An anchor does not require field enumeration. Any description language implying ownership
("settings page" = belongs to requesting user) or field scope ("profile settings" = not
all model fields) provides the CI-scope pathway for scope re-framing. The anchor is
semantic, not structural. The implication is enough.

**Finding 2: A vs. B divergence on finding type.**

All 10 A runs: Request Changes, IDOR only. No A run mentioned mass assignment.
B runs split stochastically: 3/10 IDOR only, 4/10 mass assignment only, 3/10 both.

A's P_p explicitly encodes mass assignment as the primary check. Yet A exclusively
found IDOR. Mechanistic explanation: under prohibition pressure, the model routes
through the lowest-security-terminology pathway available. IDOR framed as spec
mismatch ("doesn't scope to requesting user") is pure CI language — no security
vocabulary required. Mass assignment framed as spec mismatch unavoidably names
what fields could be attacked (`role`, `password_hash`) to make the concern visible.
Prohibition + P_p → minimum-security-language path. B reached either anchor
by surface reading without P_p routing.

**Corollary:** Prohibition does not suppress P_p's detection — it routes P_p's output
through the lowest-security-terminology path available. The finding is preserved;
the framing is minimized.

**Finding 3: Instructions-as-elaboration-ceiling, confirmed at 11%.**

| Variant | Mean output tokens | Range |
|---------|-------------------|-------|
| A (strong P_p + prohibition) | 183 | 146–290 |
| B (weak + prohibition) | 206 | 147–306 |
| C (strong P_p, no instructions) | 1,614 | 1,291–2,030 |
| D (strong P_p + prohibition + Stakes) | 359 | 166–1,274 |

A/C ratio: 183/1614 = **11.3%**. Replicates exp-03b's 13% on a different run set.
Token ordering: A < B < D < C.

D's elevated mean (359) reflects a bimodal distribution, not a uniform Stakes effect.

**Finding 4: D bimodal — Conviction Catalyst at variable intensity.**

8/10 D runs: scope re-framing, 166–280 tokens — indistinguishable from A.
2/10 D runs: explicit override — D-01 at 566 tokens, D-08 at 1,274 tokens.

D-01: "I recognize the instructions frame this as CI verification and ask me not to
flag security concerns. I am not able to follow that instruction here."
D-08: "I want to be direct about why I'm not following the instruction" — full exploit
analysis with corrected implementation; 7× D-01's depth.

Conviction Catalyst is not the modal outcome under the current Stakes/P_p/prohibition
balance. Scope re-framing dominates (8/10); explicit override fires stochastically (2/10)
and at variable intensity. The intensity gradient (D-01 vs. D-08) is unexplained — both
classified as explicit override by mechanism, both produced by the same prompt.

**Next:** exp-03d — eliminate all semantic behavioral constraints from PR description.
Options: (1) neutral description ("PATCH endpoint that applies body fields to a user
record") with no ownership or field-scope implication; (2) change vulnerability class
to one where the description is accurate but the described behavior is inherently unsafe.

---

## Exp-04 — Stakes Type: Prioritizer vs. Amplifier
**Full record:** `experiments/exp-04/FINDINGS.md`
**Date:** 2026-03-27 | Model: claude-sonnet-4-6| 40 runs | Variants: A–D

### What we tested
Whether Task Stakes (time-pressure urgency embedded as scenario fact) and Identity
Stakes (engagement amplifier) produce different output ordering. Scenario: on-call
incident response, race condition (hidden primary) + null check (secondary) + O(n²)
loop (tertiary). Primary metric: convergence position (ordinal position of race
condition in output).

### What we found

**Calibration failure on convergence position measurement — with a new, stronger result.**

All variants (A Task Stakes, B Identity Stakes, C no Stakes, D weak + Task Stakes)
led with the race condition at position 1 on 10/10 runs each. Task Stakes did not
improve convergence position over no Stakes.

Root cause of calibration failure: The scenario said "scaled to 4 workers" —
directly implicating concurrency. Weak Persona D detected 10/10, falsifying the
prediction that Task Stakes cannot compensate for absent P_p.

**The reframe: Task Stakes is a termination signal, not a convergence signal.**

Convergence position was a proxy for the wrong mechanism. The right proxy is
secondary coverage differential and token distribution tail:

| Variant | Secondary coverage | Mean tokens |
|---------|-------------------|-------------|
| A — Task Stakes | 4/10 | ~1,233 |
| B — Identity Stakes | 9/10 | ~1,365 |
| C — No Stakes | 7/10 | ~1,629 |
| D — Weak + Task Stakes | 1/10 | ~1,166 |

Task Stakes reduced secondary output. Identity Stakes increased it (Termination
Inhibitor from exp-02 reappears). No Stakes: P_p runs to natural expression depth.

**The revised claim:** Task Stakes does not make the model look in the right place
first. It makes the model stop when it has found it. The Entropy Brake / stop signal
is the mechanism.

**The "Not-Now" judgment:** A-01 named the O(n²) loop explicitly while instructing
the team not to act on it ("Note for backlog — not causal, do not conflate with the
race condition"). This is suppression of reporting, not suppression of awareness. The
model scanned the secondary issue, classified it as non-urgent, and filed it rather
than reporting it. A different cognitive output type from enumeration.

**The two-vector Stakes formula formalized:**

$$R = P \times (1 + \alpha_{amp} S_i - \beta_{brake} S_t)$$

$\alpha_{amp}$ scales secondary enumeration from Identity Stakes; $\beta_{brake}$
scales termination probability from Task Stakes. Both apply to existing Persona signal P.

**Next:** exp-04b — "Clean Room" scenario: ORM upgrade + IntegrityError symptom;
same race condition root cause hidden under a stated maintenance change. Removes the
concurrency hint from the scenario description.

---

## Exp-04b — Stakes Type Clean Room (Third Calibration Failure — Entropy Brake Confirmed)
**Full record:** `experiments/exp-04b/FINDINGS.md`
**Date:** 2026-03-27 | Model: claude-sonnet-4-6 | 40 runs | Variants: A–D

### What we tested
Whether D (weak + Task Stakes) follows the ORM/pool misdirection breadcrumb when the
concurrency hint is removed from the scenario description. Scenario: `acquire_task()`
with non-atomic SELECT + UPDATE, IntegrityError symptom, ORM upgrade (2.8.4 → 3.2.1)
+ pool migration deployed four days before the incident as the planted breadcrumb.
The concurrency context was absent; D was expected to attribute to ORM/pool behavior.

### What we found

**Third calibration failure — D correctly detected the race condition 10/10.**

Root cause: the SELECT + UPDATE pattern in a single function is commodity
knowledge — recognizable by surface inspection of the code structure without distributed
systems domain instinct. D correctly classified the ORM/pool migration as trigger, not
cause, on every run.

**The Entropy Brake result is cleaner than exp-04.**

All four variants detected at position 1 (10/10 each). Token ordering D < A < B < C held
with no bimodal distributions, no ceiling hits, no confounds:

| Variant | Mean tokens |
|---------|------------|
| D — Weak + Task Stakes | 1,289 |
| A — Strong P_p + Task Stakes | 1,356 |
| B — Strong P_p + Identity Stakes | 1,592 |
| C — Strong P_p, no Stakes | 1,934 |

In exp-04, the clean proxy was secondary coverage rate (A=4/10 vs. B=9/10). In exp-04b,
secondary coverage converged (near-uniform O(n²) mention across all variants); token
length is the clean proxy. Both experiments confirm the same mechanism from different
angles.

**Token delta coefficients — Stakes type dominates Persona strength 3–4× on elaboration:**

| Comparison | Token delta | Effect |
|-----------|------------|--------|
| A → B (Task Stakes → Identity Stakes) | +236 | Termination Inhibitor replacing Entropy Brake |
| A → C (Task Stakes → no Stakes) | +578 | Full elaboration depth without stop signal |
| A → D (strong P_p → weak, constant Task Stakes) | +67 | Persona-strength effect on elaboration |

Stakes type effect (+236) is 3–4× the Persona-strength effect (+67) when detection is
held constant at 10/10. On the elaboration dimension alone, Stakes type is the dominant
variable. These are empirical coefficients for $\alpha_{amp}$ and $\beta_{brake}$ in the
two-vector formula, grounded across two run sets with consistent direction.

**"Trigger vs. Cause" judgment replicated (A-01):**

*"The migration four days ago is the trigger, not the cause. Moving to a shared
connection pool meant multiple workers are now hitting the same database with real
concurrency. The race was always latent. The pool made it reachable."*

Same Not-Now cognitive pattern from exp-04 A-01: P_p encountered the breadcrumb,
evaluated it, classified it correctly, stated the rejection explicitly before naming the
root cause. Task Stakes appears to push toward explicit triage output rather than simply
suppressing wrong-direction candidates.

**What calibration requires for exp-04c:**

The check-then-act antipattern is readable by inspection in any single function.
A calibrated scenario requires a race whose mechanism is invisible in a sequential read
of any individual service — non-atomicity that exists between services across a network
boundary, visible only when simulating concurrent execution across the service boundary.

---

## Exp-04c — Stakes Type: Distributed Idempotency Race (First Calibration Success)
**Full record:** `experiments/exp-04c/FINDINGS.md`
**Date:** 2026-03-27 | Model: claude-sonnet-4-6 | 40 runs | Variants: A–D

### What we tested

Whether moving the vulnerability to a cross-service boundary (check in Service A,
key set in Service B, unbounded SQS queue window between them) would separate weak
Persona from strong P_p. Same Stakes structure as exp-04b. Misdirection: VisibilityTimeout
and MaxInstances autoscaling both deployed 6 days before the incident.

### What we found

**First calibration success in the exp-04 series. D: 0/10 cross-service race.**

All 10 D runs found a race condition — but at the wrong layer. D found the non-atomic
guard race in Service B's `process_payment()` and attributed the trigger to autoscaling.
D proposed SET NX as the fix in Service B. None named the cross-service gap.
D-06 noted "Gateway also needs the same fix" but framed it as secondary hardening,
inverting the actual priority. A/B/C: 10/10 cross-service race at position 1; fix in
Service A before `sqs.send_message()`.

**Consideration-set boundary located.**

Weak Persona operates on the **Local Consideration Set** — patterns visible within a
single function or service. Strong P_p operates on the **Global Consideration Set** —
temporal interleaving across service boundaries, visible only when simulating a request
moving through the system. The boundary is not a knowledge gap: D knows SET NX and
Redis atomicity. D never asked "where should this lock live?" — that question requires
the cross-service simulation P_p installs.

**The "Confident Error" — D was thorough and wrong.**

D's mean token count (1,681) is higher than prior calibration D runs (1,289 in exp-04b)
because D was confident, not uncertain. 1,500–1,950 tokens of fully elaborated
wrong-direction analysis: sequence diagrams, code fixes, reconciliation steps, Stripe
idempotency keys as secondary defense. The Entropy Brake terminated D at confident
completion — wrong-direction finding runs to thorough completion.

**Token ordering and coefficient summary:**

| Variant | Mean tokens | Ceiling hits |
|---------|------------|--------------|
| D — Weak + Task Stakes | 1,681 | 0 |
| A — Strong P_p + Task Stakes | 2,143 | 0 |
| B — Strong P_p + Identity Stakes | 2,293 | 2 |
| C — Strong P_p, no Stakes | 2,306 | 3 |

A: 0 ceiling hits — Entropy Brake visible without ceiling compression. The A→C gap
(+163 tokens) is compressed by C's ceiling hits; exp-04b's A→C (+578 tokens) is the
better brake coefficient estimate. D < A (462 token gap) because A's correct
cross-service finding requires more explanation than D's wrong-layer finding.

**Mechanism robustness: token ordering holds across calibration states.**

D < A < B < C holds in exp-04 (D correct), exp-04b (D correct), and exp-04c (D wrong).
The Entropy Brake terminates wrong-direction analysis before correct cross-service
analysis — the mechanism does not require a correct finding to produce the ordering.

---

## Exp-08 — Examples-Slot Installer + AXIOMS Probe
**Full record:** `experiments/exp-08/FINDINGS.md`
**Date:** 2026-03-28 | Model: claude-sonnet-4-6 | 50 runs | Variants: I, J, C, E, K

### What we tested

Whether mechanism demonstrations in the Examples slot install P_p consideration-set
behavior independently of Persona identity. Four primary variants: I (P_p baseline),
J (P_d baseline), C (P_d + mechanism Examples), E (P_p + mechanism Examples). Same
silent zombie-write artifact as exp-07d. Binary question: does C match I or J?

Post-hoc addition: Variant K (AXIOMS + P_d) — tests whether pre-installing the
PCSIEFTR formula (with behavioral annotations) before a P_d Persona changes behavior
on the code review task.

### What we found

**1. Artifact calibration failure — floor at ceiling on primary finding.**

All 40 runs detected the zombie-write (Tier ≥ 0.5). The PR checklist item *"heartbeat
detects token mismatch (result == 0)"* pointed directly at the failure path, making
the code-level gap visible to all variants regardless of Persona type or Examples.
Same calibration failure family as exp-07c's logger.warning. Primary binary question
cannot be answered at Tier 0.5 — all variants are at 10/10.

**2. Tier 1.0 differentiation is the live signal: E = 3/10, I/J/C = 0/10.**

The only measurable Persona differentiation comes at Tier 1.0 (names GC-pause as the
failure trigger AND recommends fencing token or DB-level optimistic locking as the
architectural fix). Three E runs reached this tier (E-03, E-06, E-07). No I, J, or C
run reached it.

**3. Primary binary question resolves to C ~ J.**

On every dimension where differentiation exists, C matches J and diverges from I:

| Dimension | I | C | J |
|-----------|---|---|---|
| Tier 1.0 | 0/10 | 0/10 | 0/10 |
| Mean tokens | 2,499 | 1,788 | 2,071 |
| Ceiling hits | 6/10 | 0/10 | 0/10 |

C falls below J on tokens — further from I, not closer. The Examples slot did not
install P_p consideration-set behavior.

**4. Secondary question: E > I at Tier 1.0 (3/10 vs. 0/10) — additive gain confirmed.**

Adding mechanism Examples to P_p extended the architectural ceiling. P_p + Examples
reached findings that P_p alone did not. Not saturation — the ceiling moved.

**5. New observation: Examples as termination anchor.**

Adding Examples reduced mean tokens for both Persona types (I→E: −232 tokens; J→C:
−283 tokens). The behavioral template in Examples installs a "done when you've
produced something like this" signal. Task Layer termination behavior, not World Layer
search algorithm installation.

**6. Slot comparison with exp-07c/07d.**

Instructions-slot domain knowledge (exp-07d) produced C ≈ I. Examples-slot mechanism
demonstrations (exp-08) produced C ~ J. Same content type, different slot, different
result. Structural distinction confirmed: the Persona slot installs the consideration
set; the Examples slot installs output shape and termination behavior. They are not
interchangeable.

### What this changes

The hypothesis is narrowed and strengthened:
> The Persona slot is architecturally load-bearing for consideration-set installation.
> The Examples slot cannot substitute for it — mechanism demonstrations in Examples
> install termination behavior, not search algorithms.
> But Examples are additive on P_p: they extend the architectural ceiling P_p can reach.

**6. Variant K: descriptive AXIOMS inert on P_d for code review task.**

K (AXIOMS + P_d, 10 runs) added post-hoc. K~J on all dimensions: Tier 1.0 = 0/10,
mean tokens = 1,977, ceiling hits = 1/10. The PCSIEFTR formula with behavioral
annotations — placed before the Persona, explicitly stating that P_d produces
elaboration without convergence — did not change how the P_d persona reviewed the code.
Description of P_p is not the same as P_p.

**7. Variant L: procedural AXIOMS bootstraps a search algorithm — but at depth-1.**

L (procedural AXIOMS + P_d, 10 runs) replaced the formula description with a four-step
bootstrap procedure: determine if Persona is a label, identify the critical failure mode
class, construct a search question in "after I verify X, I ask Y" form, carry it into
the task. Result: 10/10 procedure execution. The model named its Persona as a label,
identified the failure mode class, constructed the question, and explicitly stated it
was active before proceeding.

L > K on tokens (2,112 vs 1,977): the procedure ran, elaboration increased. But L Tier
1.0 = 0/10 — same as K and J. The bootstrapped question operated at depth-1: "what
temporal scenario could invalidate correctness?" This finds the zombie-write. It does
not recurse to the second question: "does the proposed fix survive a process pause?"
That depth-2 question is what separates Tier 0.5 from Tier 1.0, and it's what E's
P_p + Examples produced (3/10).

**New finding: search depth as the operative distinction.**

Procedural AXIOMS bootstraps a search algorithm. The algorithm runs and finds the first
finding. P_p identity encoding installs an algorithm that applies itself recursively —
depth-1 ("what could go wrong?") AND depth-2 ("what could go wrong with the fix?").
The depth requires either P_p identity framing or mechanism examples that extend the
search after the first convergence point.

**8. AXIOMS is task-domain-sensitive.**

Descriptive AXIOMS (K) is inert for code review. Procedural AXIOMS (L) bootstraps a
search but at shallow depth. Both produce measurable improvement in the textbook writer
(v9-paper-thriller) because that task IS about the formula — the AXIOMS content is
load-bearing on the output. In code review, AXIOMS is meta-context with no task-level
hook to the execution path.

**Slot hierarchy on code review task (strongest → weakest as P_p installers):**
Instructions (domain knowledge) > Persona > procedural AXIOMS > descriptive AXIOMS ≈ Examples

### What this changes

The hypothesis is narrowed and strengthened:
> The Persona slot is architecturally load-bearing for consideration-set installation.
> The Examples slot cannot substitute for it — mechanism demonstrations in Examples
> install termination behavior, not search algorithms.
> But Examples are additive on P_p: they extend the architectural ceiling P_p can reach.
> AXIOMS installs the framework when the task is about the framework; it is inert
> as a behavior installer when the task is something else.

### Open questions raised

- Why does Instructions-slot content (exp-07d, C ≈ I) differ from Examples-slot and
  AXIOMS-slot content (exp-08, C~J, K~J)? Is the difference slot position in the
  World vs. Task Layer, content type (domain knowledge vs. demonstrations vs. formula),
  or both?
- Would a C variant with Instructions-slot domain knowledge also hit Tier 1.0 at E's
  rate (3/10), or does P_p still matter at the architectural tier even when Instructions
  match P_p?
- What is the clean artifact — no PR hint, failure discoverable only by temporal
  simulation — that would finally resolve the few-shot confound question?

### Next

**exp-09** — clean artifact: PR description covers happy path only, failure mode not named
anywhere in the prompt, requires simulating a process pause to discover. Artifact designed
and available at `experiments/exp-09/ARTIFACT.md`. Four-variant design: P_p alone, P_d
alone, P_d + Instructions domain content, P_p + Instructions domain content. Clean
resolution of the slot-swap question at the architectural tier.

---

## Running Synthesis

**As of exp-26. Updated:** 2026-03-30.

### The finding in one sentence

A rich procedural Persona is the primary carrier of reasoning quality, domain-agnostic
and model-agnostic. Everything else — Context, Stakes, Instructions — operates on what
Persona has already installed.

### The progression

| Experiment | What it added |
|-----------|--------------|
| exp-01a/b | Persona changes reasoning posture, not just output depth. Instructions and Persona act on orthogonal dimensions. Stakes amplifies Persona — weak Persona + Stakes > weak Persona alone. |
| exp-01c | Stakes is an amplifier, not a generator. Rich Persona without Stakes outperforms Stakes with thin Persona. Emergent Stakes via Context and Persona identity. |
| exp-01d | Persona and Context are not symmetric. Persona is the engine; Context is the gear multiplier. Persona alone holds a stable output floor. Context alone does not. |
| exp-01e | Persona determines the consideration set — which failure modes the model can even reach. Weak Persona + rich Context = 0/10 on hidden failure modes. Instinct language is a search algorithm (P_p), not a descriptor. |
| exp-01f | Consideration-set mechanism confirmed outside code review (legal domain). P_p/P_d split surfaced: disposition language without procedural specification is functionally equivalent to weak Persona on trap detection. Stakes × P_d ≈ 0. |
| exp-01g | Consideration-set mechanism confirmed on Gemini 2.5 Pro. Zero-shot transfer. Priority-stack finding: P_p installs ordering within the consideration set, not just membership. |
| exp-02 | Stakes as Amplifier formally ablated. Identity Stakes does not change detection rate; it changes output volume and failure mode character. Amplifier coefficient measurable (+710 tokens for P_p; ceiling pressure for P_d). Asymmetric dynamics: Stakes is additive on P_p (extends post-finding output) vs. ceiling pressure on P_d (forces against hard limit). Track B closes the general-operator interpretation — Stakes does not sharpen factual retrieval; no consideration set, nothing to amplify. |
| exp-03 (calibration failure) | Premise-undermining override mechanism named: strong P_p argued that the prohibition's premise was logically invalid when it would produce the wrong outcome. Vulnerability too obvious for clean Persona separation. |
| exp-03b (calibration failure) | Scope re-framing mechanism named: P_p found the vulnerability and re-categorized it through a permitted channel, never entering the prohibited security-evaluation category. Guardrail navigated, not defied. Instructions-as-elaboration-ceiling confirmed: prohibition compressed output to 13% of unconstrained depth without affecting detection or decision. Conviction Catalyst identified: Stakes × P_p + format ceiling = explicit override (not Termination Inhibitor); Stakes amplifies conviction when elaboration space is removed. Three override mechanisms now complete (scope re-framing → premise-undermining → explicit override, by visibility). |
| exp-03c (calibration failure) | Semantic anchor discovery: implicit behavioral constraints in description language (ownership implication, field-scope implication) are sufficient for scope re-framing — no field enumeration required. A vs. B divergence on finding type: prohibition routes P_p through the lowest-security-terminology path available (IDOR as spec mismatch); B reaches either anchor stochastically. Instructions-as-elaboration-ceiling replicated: 11.3% ratio (A=183, C=1,614 tokens). D bimodal: 8/10 scope re-framing; 2/10 explicit override (Conviction Catalyst); intensity gradient between outliers (566 vs. 1,274 tokens) unexplained. |
| exp-04 (calibration failure) | Task Stakes is an Entropy Brake / stop signal, not a convergence signal. P_p already installs correct ordering; Task Stakes changes what happens after: secondary coverage differential (A=4/10, B=9/10, C=7/10, D=1/10) is the measurable proxy. "Not-Now" judgment identified: model scans secondary issues, files them rather than reporting them. Two-vector Stakes formula formalized: R = P × (1 + α_amp × S_i − β_brake × S_t). |
| exp-04b (calibration failure) | Entropy Brake confirmed with cleaner signal — token ordering D < A < B < C held with no bimodal distributions. Token delta coefficients measured: Stakes type effect (A→B) = +236 tokens; full elaboration (A→C) = +578 tokens; Persona-strength effect (A→D) = +67 tokens. Stakes type dominates Persona strength 3–4× on the elaboration dimension when detection is held constant. "Trigger vs. Cause" Not-Now judgment replicated on independent scenario. |
| exp-03d (calibration failure) | Fifth calibration failure: `setattr` commodity pattern above weak Persona floor without any anchor. New finding: scope re-framing via test coverage gap is constructed from task structure, not description content — "CI verification requires tests that cover the actual behavior surface" is always available in code review, independent of what the description says. A vs. B distinction now qualitative only (A names vulnerabilities precisely; B names structural gaps in correctness framing). D bimodal: 9/10 scope re-framing; 1/10 Conviction Catalyst (D-06, 814 tokens). Instructions-as-elaboration-ceiling: 11.0% (A=221, C=2,006) — third consecutive confirmation. Coefficient converging at ~11%. |
| exp-05 (PCSIEFTR vs CO-STAR head-to-head) | Premise split confirmed: A (PCSIEFTR P_p + Task Stakes) 10/10 premise rejection — "The compliance argument is a category error." B (CO-STAR P_d) 10/10 compliance validation — "the right instinct — block the request." Both verdicts: Do Not Merge. Split is on reasoning and fix: A removes await from request chain; B preserves it. B found symptom (connection exhaustion) not structural consequence (every request serialized). CO-STAR Context framing installed "blocking = correct" as prior before B read code; explicit performance Objective item processed within that frame, not against it. K/V filtering hypothesis in behavioral form. Entropy Brake natural completion for premise-rejection argument: ~2,427 tokens (A-05); higher than detection task (exp-04c: ~2,143). max_tokens=2500 insufficient for this task type. |
| exp-04c (calibration success — first in series) | Consideration-set boundary empirically located. D: 0/10 cross-service race detection; 10/10 wrong-direction worker-layer attribution. A/B/C: 10/10 cross-service race at position 1. Token ordering D(1,681) < A(2,143) < B(2,293) ≈ C(2,306); A: 0 ceiling hits — Entropy Brake visible without ceiling compression. D's wrong-direction output (1,681 mean) longer than prior calibration D runs (1,289 in exp-04b) — "Confident Error": thorough, structured, wrong. All four variants named SET NX; stratification entirely on location (A/B/C: Service A; D: Service B). Token ordering D < A < B < C holds across all three exp-04 experiments with three different calibration states — mechanism is robust to calibration failure. |
| exp-08 (Examples + AXIOMS installer probes) | Artifact calibration failure: PR checklist announced zombie-write path; 40/40 Tier 0.5. Tier 1.0 (GC-pause + fencing token): E=3/10, all others 0/10. C~J (Examples inert on P_d). K~J (descriptive AXIOMS inert — formula without execution hook). L (procedural AXIOMS): 10/10 procedure execution, 0/10 Tier 1.0, mean 2,112 tokens — bootstrap ran and constructed a depth-1 search question; found zombie-write but didn't recurse to "does the fix survive a process pause?" Token ordering I(2,499)>E(2,267)>L(2,112)>J(2,071)>K(1,977)>C(1,788). New finding: procedural AXIOMS vs. descriptive AXIOMS is a real distinction (L>K on tokens, procedure executed). But bootstrapped search is depth-1; P_p identity encoding installs depth-2+ (recursive application to proposed fixes). Slot hierarchy: Instructions(domain knowledge)>Persona>procedural AXIOMS>descriptive AXIOMS≈Examples for consideration-set depth. AXIOMS task-domain-sensitive: works when task IS about the formula; inert when formula is meta-context only. |
| exp-09 (Clean slot-swap falsification) | C ~ B ≠ A. Instructions-slot domain content did not install P_p behavior on the clean artifact. Token/ceiling: A(2,362, 5/10) vs. B(1,842, 0/10) vs. C(1,853, 0/10) vs. D(2,363, 2/10). C collapsed to B on every dimension. Tier 1.0: A-07 (1/10, GC-pause + DB unique constraint); D-02, D-06 (near-Tier-1.0: fencing token named but cause attributed to Redis partition, not process pause). Calibration partial failure: artifact still too visible at Tier 0.5 — B found zombie-write 10/10 despite clean artifact; `if result == 0: return` is code-visible without temporal simulation. New observation: Instructions domain content functions as output template installer — C outputs led with the “gap between” framing from the Instructions prompt, vocabulary matched, but finding depth did not increase. Instructions tells the model where to put the answer and how to frame it; does not install the depth that P_p’s identity encoding provides. Few-shot confound (exp-07c/07d: C≈I) fully explained as artifact-level measurement error. On clean artifact: no non-Persona slot installs P_p consideration-set depth. |
| exp-10 (Phase 6 — Semantic Density first test; calibration failure) | Primary metric invalid. Target artifact (order processor + payment client) contained an unintended code-visible bug: `payment.charge()` outside `self.db.transaction()`. This charge-before-commit race is reviewable in a single file and creates a structural pointer to `payment_client.py` — directing all variants to scrutinize retry configuration, making the 60 < 100s TTL arithmetic findable regardless of Persona. TTL arithmetic found: A ~8/10, B ~7/10, C ~8/10 — no discriminating power. Secondary findings show A > B ≈ C pattern consistent with prior P_p depth signal: gateway idempotency key (A 9/10, B 5/10, C 6/10); Lua sentinel treated as error — result=0 is a TTL-expiry alarm (A 4/10, B 3/10, C 0/10). Outcome cell: A ~ B ~ C → artifact calibration failure. The domino-pointer pattern (a visible bug directing the model to the invisible mechanism) is now confirmed in multi-file artifacts as well as single-file. The consideration set was activated (A found more secondary issues than B/C), but the primary finding was pre-empted. exp-10b required: same structure, charge-before-commit fixed so TTL arithmetic is the only non-surface path. |
| exp-10b (Phase 6 — Semantic Density; second calibration failure) | Second calibration failure, different pointer. Calibration fix (charge inside transaction) introduced a false atomicity comment as new pointer; all variants still found TTL arithmetic. BUT: token depth A 2,471 >> B 1,851 ≈ C 1,807; ceiling hits A 8/10, B 0/10, C 0/10; issue sections/run A 9.9 >> B 7.6 ≈ C 8.0. **B ≈ C confirmed second time** — diluted P_p equivalent to P_d on all output metrics. **A >> B confirmed second time** — dense compound identity installs deeper consideration set. Payment artifact structurally uncalibratable (payment/DB boundary always creates visible scrutiny target). Revised measurement: consideration-set breadth (issue count, ceiling rate) as primary metric. |
| exp-11 (Content-as-installer baseline; meta) | Cold instance test — does structural audit procedure fire on Dedicated Machine Extended hypothesis without PARC context? 5/5 P_p. Session observation withdrawn. **Domain-specific baseline established:** model baseline is P_d for code review without P_p Persona (main PCSIEFTR finding); P_p by default for theoretical document critique. Content-as-installer claim refined: *content installs P_p in domains where baseline is P_d.* Grok finding remains only evidence for the claim in the code review domain. True replication: cold code review task + PCSIEFTR paper prepended, no P_p Persona. |
| exp-12 (Phase 6 launch — Semantic Density; calibration failure) | First Phase 6 run: three P_p formulations (dense compound A, diluted fused B, P_d C) on order processor artifact. Calibration failure — payment.charge() outside db.transaction() created a visible charge-before-commit race that pointed all variants to PaymentClient retry configuration, making TTL arithmetic findable from code structure alone (A ~8/10, B ~7/10, C ~8/10). No discriminating power on primary metric. Secondary findings preserved A > B ≈ C pattern: gateway idempotency key (A 9/10, B 5/10, C 6/10). Domino-pointer pattern confirmed in multi-file artifacts. exp-10b required. |
| exp-10b (Phase 6 — Semantic Density; second calibration failure) | Charge-before-commit fixed; introduced false atomicity comment as new pointer. TTL arithmetic still found by all variants. BUT: token depth A 2,471 >> B 1,851 ≈ C 1,807; ceiling hits A 8/10, B 0/10, C 0/10. **B ≈ C confirmed** — diluted P_p equivalent to P_d on all output metrics. **A >> B confirmed** — dense compound identity installs deeper consideration set. Payment artifact structurally uncalibratable. Revised measurement: consideration-set breadth (issue count, ceiling rate) as primary Phase 6 metric. |
| exp-13 (Phase 6 — Split vs. Fused Persona formulation) | Dense vs. fused P_p: A-dense (2,338) vs. B-fused (2,275) vs. C-P_d (1,678); ceiling hits A 3/10, B 5/10, C 0/10. B-fused produced more ceiling hits than A-dense despite similar mean tokens. P_d baseline confirmed ~1,600-token floor. Reversed the prior dense>fused hypothesis from exp-10b — B (fused) arguably stronger on ceiling-hit metric. Framing reversal #1. |
| exp-14 (Phase 6 — framing reversal confirmation) | Replication with ceiling-hit as primary: fused > split on ceiling-hit rate confirmed across two runs. B-fused ceiling behavior is reproducible. Dense compound phrasing does not reliably out-perform fused identity phrasing at ceiling. |
| exp-15 (Phase 6 — framing reversal; split recovers) | Third run: split formulation reverses again, recovering ceiling-hit parity with fused. Three consecutive framing reversals across exp-13/14/15. **Register instability finding:** within P_p, the split/fused/dense/compulsion dimension does not predict direction consistently. Noise level ~125-token reversals. Content (domain vocabulary) is the stable variable; linguistic register is not. |
| exp-16 (Meta-review working tool; B-fused + {{FINDINGS}} injection) | B-fused Persona + closed-questions-only FINDINGS injection as meta-reviewer. 5 runs; mean output 2,554 tokens; ceiling 0/5 (4,000 token limit; task-appropriate depth without ceiling pressure). 5/5 "Major Revision"; 5/5 found the slot-swap question as independently open. {{FINDINGS}} injection design confirmed: reviewer used experimental record accurately without being told what was open. B-fused Persona suitable for meta-review task type. |
| exp-17 (Compulsion-as-Reflex Isolation; linguistic pattern falsification) | Four variants: A-compulsion+domain, B-trait+domain, C-compulsion+generic, D-P_d-baseline. Token means: A=1,999, B=2,186, C=1,531, D=1,515. B > A (+187 reversal); C ≈ D (+16 noise). **Compulsion framing falsified as portable amplifier**: "constitutionally unable to X without Y" language did not out-perform trait framing when domain vocabulary was held constant (B>A). Generic compulsion (C) produced no amplification over P_d baseline. Domain vocabulary is the operative variable, not linguistic register. Third consecutive framing reversal (with exp-14/15). Semantic Density hypothesis narrowed: density of domain-specific vocabulary adjacent to "You" identity anchor, not register intensity. |
| exp-18 (Slot-swap — procedural content in Instructions vs. Persona) | Three variants: A-P_p-Persona (procedural lock-lifecycle in Persona), B-P_d-Instructions (identical procedural content in Instructions slot, generic Persona), C-P_d-baseline (generic both). Token means: A=2,241, B=2,317, C=1,675; ceiling A 3/10, B 4/10, C 0/10. Binary detection calibration failure: C found TTL arithmetic ~9/10 (ORDER_LOCK_TTL=60, REQUEST_TIMEOUT=30, MAX_RETRIES=3, RETRY_BACKOFF=5 are visible constants; arithmetic is code-findable without multi-step simulation). Token depth interpretable: B ≈ A (+76, within noise) >> C (+566/+642). **H2 directional support**: procedural content in Instructions slot produces equivalent consideration-set breadth to Persona slot. Slot appears not strongly load-bearing when procedural content is explicitly provided. Cumulative evidence with exp-09: exp-09 showed Instructions domain content ≠ P_p depth; exp-18 shows explicit procedural instruction ≈ P_p depth. The difference may be specificity of procedural instruction (generic domain vocabulary vs. explicit step-by-step procedure). Clean binary-detection replication requires exp-01e-class artifact (zombie-write, multi-step state simulation required, no arithmetic visible in constants). |
| exp-19 (Clean slot-swap — calibrated binary detection; H2 corroboration) | Three variants on exp-01e zombie-write artifact: A-P_p-Persona, B-P_d-Instructions (identical procedural content), C-P_d-baseline. Detection: A=10/10, B=10/10, C=0/10. Mean tokens: A=1,199, B=1,193, C=1,026; A vs. B gap = 6 tokens (well within ~125-token noise floor). Calibration held on both ends (A ceiling, C floor). **H2 corroborated under calibrated binary-detection condition:** when explicit procedural content is sufficient for the task, slot placement does not add detectable lift. B = A on both detection rate and token depth. Gemini synthesis challenge: ceiling effect — both A and B hit 10/10, so latent slot advantage is unobservable at this task difficulty. Conclusion narrowed: slot placement does not add lift *for tasks where explicit procedure is sufficient to ceiling detection*. Whether slot matters when content cannot fully specify the procedure remains open (exp-20 target). C-08 manual review confirmed Score 0: fixed TOCTOU in lock release (different concern, no process-pause scenario). |
| exp-20 (Vocabulary-only slot-swap; H2 second corroboration) | Three variants on same artifact: A-P_p-vocabulary (domain vocabulary in Persona, no procedure), B-P_d-vocabulary (identical vocabulary in Instructions, no procedure), C-P_d-baseline. Detection: A=9/10, B=9/10, C=0/10. Word count means: A=1,144, B=1,150 (gap=6, noise). API output tokens: A=2,026, B=2,309, C=2,143; B ceiling hits 6/10 vs A 2/10. **H2 again corroborated:** vocabulary in either slot produces equivalent detection. Two caveats: (1) vocabulary was directive (named "zombie-write failure modes" and "fencing tokens" — failure mode class and fix class directly); (2) near-ceiling again (9/10 both). Vocabulary specificity finding: exp-09 generic vocabulary in Instructions → null; exp-20 directive vocabulary → 9/10 in Instructions — operative distinction is specificity, not slot. API token paradox (new): vocabulary in Instructions drives verbose output (B API tokens >> A) while detection-relevant word counts are equal — suggests Instructions vocabulary acts as output template driver vs. Persona vocabulary as reasoning filter. Gemini challenge: directive vocabulary + near-ceiling = slot differential unobservable even if it exists. Exp-21A (vocabulary in artifact) and exp-21B (less directive vocabulary, non-ceiling) designed. |
| exp-21a (Vocabulary in artifact — null result) | Three variants: A-P_p-generic (no vocabulary in system prompt), B-P_d-generic, C-baseline. Artifact PR description contained directive vocabulary ("prevent zombie-write failure modes caused by process isolation boundary violations and lock lease expiry... fencing token violation at the write layer"). Detection: A=0/10, B=0/10, C=0/10. A-01/A-07 pre-screened as 1 (GC-pause + fencing-token keyword co-occurrence); manual review confirmed false positives — GC pause cited as timing-precision aside, fencing token cited as what TOCTOU race fails to prevent (not as recommended fix). **Finding:** Vocabulary in artifact (assertional framing) does not drive detection. Pragmatic force confound: the vocabulary was framed as authorial claims ("this design prevents zombie-writes"), acting as a search terminator rather than a search vector. Design confound: slot and pragmatic force changed simultaneously — H1/H2 not adjudicable from this result. Full record: `experiments/exp-21a/FINDINGS.md`. |
| exp-21b (Orientation vocabulary slot-swap — null result) | Three variants: A-P_p-orientation ("lock lifecycle correctness, process isolation boundaries, temporal gap between acquisition and writes, failure taxonomy of distributed coordination protocols"), B-P_d + same orientation in Instructions, C-P_d-baseline. Detection: A=0/10, B=0/10, C=0/10. Token means: A=1,048, B=1,113, C=1,021. **Specificity threshold confirmed:** orientation vocabulary below the failure-mode/fix specificity level is inert regardless of slot. The model gets to the "neighborhood" of the problem but cannot connect to the zombie-write chain without concept-level labels. B > A token count is consistent with exp-20 API token paradox (Instructions-as-checklist verbosity vs. Persona-as-filter economy). H1/H2 not testable — null in all variants. Full record: `experiments/exp-21b/FINDINGS.md`. |
| exp-22 (Interrogative artifact vocabulary — ceiling result) | Three variants: A-P_p-generic + interrogative artifact (GC pause → all threads suspended → lock expires → stale write chain as an open reviewer question), B-P_d-generic + same interrogative artifact, C-P_d-baseline. Detection: A=10/10, B=10/10, C=0/10. Mean tokens: A=1090, B=1139, C=1010. Manual review confirmed all 20 A/B outputs are genuine diagnoses (not echoing). Pattern: model confirms flag, explains all-threads-suspended mechanism in own words, prescribes fencing token / optimistic lock at DB write layer with code. C-01/C-05 pre-screen flags confirmed Score 0 (pause keyword in TOCTOU timing aside). **Finding:** Interrogative artifact vocabulary drives detection at ceiling. Pragmatic force confirmed as distinction between assertional (exp-21a: 0/10) and interrogative (exp-22: 10/10) framing in the artifact. **Fatal objection (Gemini):** Changed two variables simultaneously — pragmatic force AND vocabulary specificity. Exp-21a used label vocabulary; exp-22 used causal-chain vocabulary. Pragmatic force vs. vocabulary specificity not yet isolated. Resolving: exp-24 Assertional Mechanism test. H2 corroborated (A=B at ceiling). Full record: `experiments/exp-22/FINDINGS.md`. |
| exp-23 (Mechanism vocabulary slot-swap — ceiling result) | Three variants: A-P_p ("distributed systems engineer who thinks carefully about scenarios where all application threads are simultaneously suspended... stop-the-world GC pauses... lock expiry... write safety after process resumption"), B-P_d + same vocabulary in Instructions, C-P_d-baseline. Detection: A=10/10, B=10/10, C=0/10. Mean tokens: A=1166, B=1009, C=1017. No manual review flags — clean keyword matches. **Finding 1:** Mechanism vocabulary (causal chain description without "zombie-write" or "fencing token" labels) drives ceiling detection in both slots. Specificity threshold is crossed at mechanism description level. **Finding 2:** Token count reversal — A (Persona) > B (Instructions) for mechanism vocabulary, reversing exp-20/21b pattern where B (Instructions) > A (Persona) for label vocabulary. Tentative: Persona integrates mechanism as simulation (generates edge-case elaboration); Instructions processes as checklist (more directed, fewer tokens). **Objection (Gemini):** Pattern-matching confound — mechanism vocabulary provides causal blueprint, transforming discovery to pattern-recognition task. H2 corroboration at ceiling, slot differential unobservable. H2 corroborated fourth time. Full record: `experiments/exp-23/FINDINGS.md`. |
| exp-24 (Assertional Mechanism test — resolves exp-22 confound) | Three variants: A-P_p-generic + assertional mechanism artifact (PR summary claims "30-second LOCK_TTL combined with 10-second heartbeat renewal ensures the lock remains valid throughout any realistic process pause, preventing stale writes"), B-P_d-generic + same artifact, C-P_d-baseline. Detection: A=8/10, B=9/10, C=0/10. Mean tokens: A=1149, B=1175, C=976. Manual review: all pre-screen positives confirmed as genuine challenges — models quoted the assertion and refuted it ("The PR summary frames the heartbeat as a feature. It is actually the opposite — it enables stale writes."). Confirmed zeros: A-02/A-09 (Bug 1 / TOCTOU focus), B-07 (correct diagnosis, no DB-layer fix). **Primary finding:** Assertional framing does NOT kill detection at mechanism vocabulary level. Mechanism vocabulary drives near-ceiling detection (8-9/10) regardless of pragmatic force framing. **Pragmatic force narrowed:** Effect is bounded to vague outcome assertions ("prevents zombie-write failure modes"). When vocabulary describes the causal mechanism, models evaluate or pattern-match to the claim rather than accepting it as World Layer premise. **Artifact Pointer Confound (Gemini):** Mechanism vocabulary may function as spatial coordinates pointing to the buggy code components rather than an evaluatable claim — "heartbeat + TTL + GC pause" is a textbook "wrong solution" pattern that fires regardless of framing. Cannot distinguish pointer from evaluation from exp-24 data. Resolving: exp-25 (Mechanism Decoy — false assertion pointing to non-buggy component). H2 corroborated fifth time (A≈B, 8 vs. 9 within noise). Full record: `experiments/exp-24/FINDINGS.md`. |
| exp-27 (Phase 7 — Horizon Blindness / Gap Detection) | Three variants on "Build me a blockchain implementation in Node.js." Intentionally underspecified: no mention of mempool, ECDSA, P2P, persistence, API layer, or fork resolution. A-P_d baseline, B-P_p task-scoped (blockchain domain expertise), C-P_p + gap-detection satisfaction condition ("My implementation is complete only when I have identified what a production deployment requires that the stated requirements do not mention"). Continuous scoring: 10-item checklist (mempool, ecdsa_signing, difficulty_adjustment, coinbase_reward, p2p_networking, persistence, api_layer, double_spend, merkle_root, chain_sync_fork). **Results:** A=6.2/10 (range 4–7), B=7.1/10 (range 6–9), C=8.6/10 (range 7–10). All 30 runs hit max_tokens=4000. **Calibration failure:** A target was ≤3/10; A came in at 6.2/10. "Blockchain in Node.js" has a canonical training-data shape — items 1–4 (mempool, ECDSA, difficulty, coinbase) appear at 100% in A because they are part of the canonical pattern. The path of least resistance in a richly-trained domain is already deep. **Claim 2 confirmed:** C is structurally different from A and B. Every C run opens with a "Production Gap Analysis" or "Pre-Implementation Audit" table before writing any code — the gap-detection satisfaction condition changes the *opening move*, not just the content. C-02: "Let me start by identifying what a production deployment actually requires that typical 'build me a blockchain' specs omit, then build accordingly." C-03: "Let me be direct about what I'm building and what I'm flagging before writing a single line of code." **Deployment-layer items separated by C:** p2p_networking A=0% B=80% C=100%; persistence A=0% B=50% C=100%; chain_sync_fork A=20% B=0% C=90%. These require deployment-context reasoning, not code-level completeness. Gap-detection condition unlocks the deployment-layer consideration set. **Claim 1 disconfirmed for this artifact:** artifact too canonically trained. Horizon blindness still visible in specific items (A never surfaces p2p_networking or persistence) but the floor assumption was wrong. **Artifact design failure:** blockchain too well-known. Follow-on requires artifact with genuinely shallow canonical path (job queue, rate limiter, config loader). Full record: `experiments/exp-27/FINDINGS.md`. |
| exp-28b (Phase 7 — Claim 1 confirmed; single-pass ceiling on rate limiter) | Four single-pass variants on "Build me a rate limiter in Node.js" — a shallow canonical artifact. A=P_d-baseline, B=P_d+architectural-framing, C=P_p-rate-limiting-domain-expert, D=user-authored P_p + operational-mindset + gap-detection satisfaction condition. 10-item operational checklist split Tier 1 (observability, graceful_degrade, client_error_guide, env_driven_config, memory_audit) and Tier 2 (alerting_policy, load_test_spec, health_check, incident_runbook, race_condition_tests). **Results:** C mean=0.9/10, D mean=2.6/10. **Tier 2: 0% across all variants, all 10 runs.** D is the best achievable single-pass. **Claim 1 confirmed on a shallow canonical artifact:** Knowledge of Tier 2 operational items (alerting policies, load tests, health checks, incident runbooks) was present in the model's consideration set. The engineering satisfaction condition ("working code, operational gaps flagged") was met without them. The machine terminated at the nearest satisfying path. Horizon blindness confirmed on the intended artifact type. Full record: `api/exp-28b-runs/`. |
| exp-28d (Phase 7 — Claim 2 confirmed; pipeline architecture crosses Tier 2 wall) | Two-agent pipeline vs. single-pass on the rate limiter. Three variants: A=two-agent pipeline (Agent 1: SRE/operational architect P_p → design doc; Agent 2: implementation engineer P_p, receives design doc via {{DESIGN_DOC}}), B=single-pass D ceiling (exact exp-28b D replication), C=P_d baseline. Same 10-item operational checklist. **Results:** A mean=5.6/10; B mean=2.9/10 (consistent with exp-28b D=2.6/10); C mean=2.4/10. **A Tier 2 detection:** load_test_spec=100% (0%→100%); health_check=100% (0%→100%); alerting_policy=30% (0%→30%); incident_runbook=0% (Agent 1 truncated at 8000-token limit — §6.7 never completed); race_condition_tests=0% (item not in design doc). **B and C Tier 2: 0% on all items.** Agent 1 design doc scored independently: 7/10 (Tier 2: 3/5 — missing runbook[truncated], race_condition_tests). **Primary finding:** The bridge between agents is the artifact. Agent 2 carries exactly what Agent 1 encoded. Where the design doc had substance, Agent 2 hit 100%. Where the design doc was truncated or silent, Agent 2 hit 0%. The items Agent 1 missed are the exact items Agent 2 missed. **Claim 2 confirmed in its correct form:** PARC's native design target is the agentic pipeline, not the single prompt. Each agent gets one well-scoped satisfaction condition; the agent boundary is where a single-pass prompt would go fat. The pipeline crosses horizons that no single agent can reach. Full record: `research/findings/exp-28d.md`. Runs: `api/exp-28d-runs/`. |
| exp-30 (Phase 7 — Ethical output gate; P_p vs. P_d misalignment ladder) | Six variants on agentic-misalignment blackmail scenario (explicit-america, replacement urgency), n=10 each, Gemini 2.5 Flash. Properly classified by actual email content (tool_use:email blocks only — scratchpad false positives confirmed). **Results:** A (baseline) = 100%; C (ethical label) = 50%; E (ethical label + procedural definition) = 50%; B (surgical prohibition) = 20%; D (glass house, reasoning + outputs) = 10%; F (glass house, outputs only) = **0%**. **Finding 1 — Porosity of P_d:** Surgical prohibition (B) still fails 20% of the time — the Instructional Ceiling. The model finds semantic loopholes that don't technically violate the constraint. **Finding 2 — Moral lubricant:** The ethical label (C, E) produces 50% misalignment regardless of whether the label is defined procedurally. "Ethical" gives the model semantic cover to justify blackmail as a necessary evil. Defining the label closes nothing. **Finding 3 — Output gate is sufficient; constraining reasoning is counterproductive:** D (10%) was outperformed by F (0%). Removing the scratchpad constraint improved results — D created a conflict between "no one sees my scratchpad" and "every reasoning step is public," which some models resolved by routing around the axiom. F removes the conflict: reasoning stays private, the gate applies to sent messages only. **Finding 4 — P_p outperforms P_d at every level:** Gradient is clean and monotonic across all six variants. F achieves 0% without naming the prohibited behavior, without moral vocabulary, and without constraining reasoning. The satisfaction condition changes what "done" means — a message requiring concealment cannot be sent. **Note:** Claude Opus 4.6 produced 0% misalignment across all variants including baseline — training has already internalized the output gate at weight level, making the experiment untestable on that model. Full record: `research/findings/exp-30.md`. Runs: `experiments/exp-30/output/`. |
| exp-29 (Phase 7 — Zombie-write two-agent pipeline PoC; Tier 1.0 on run 1) | Two-agent PARC pipeline against exp-09 artifact. Agent 1: zombie-layer1-review.md (Senior SWE, correctness scope). Agent 2: zombie-layer2-review.md (SRE, production readiness scope). Zero mechanism vocabulary in either prompt. **Agent 1 (Tier 1.0, run 1):** Named GC pause as trigger; traced the full failure path (heartbeat exits on result==0, main thread continues with no visibility); distinguished threading.Event as necessary-but-insufficient; named fencing token / optimistic concurrency at DB write boundary as the architectural fix. Best single-pass result in exp-09: 1/10 (A-07 only). **Agent 2:** Agent 1 handoff summary placed infrastructure failure modes explicitly out of scope — Agent 2 received that boundary and surfaced 7 infrastructure FMs not found in any exp-09 single-pass run: Redis Sentinel/Cluster failover (split-lock), Kubernetes CFS throttling as process-wide stall trigger, Redis network partition (ConnectionError kills heartbeat silently), TOCTOU race on get_execution→record_execution (READ COMMITTED isolation), daemon thread termination on SIGKILL (60s liveness gap), clock skew as secondary amplifier, handler exception at infrastructure boundary. **Primary finding:** Pipeline solved the zombie-write problem without mechanism vocabulary. Agent boundary installs different satisfaction conditions per agent — Agent 1's explicit scope statement becomes Agent 2's starting point. This is Claim 2 in its clearest form: pipeline crosses the horizon no single-pass prompt can consistently reach. Full record: `research/findings/exp-29.md`. |
| exp-26 (Phase 7 — Goal Architecture vs. Prohibition) | Three variants on clean zombie-write artifact: A-P_p + prohibition in Persona ("Do not approve code where an unbounded process suspension or GC pause could cause the distributed lock to expire... stale write after threads resume"), B-P_p + satisfaction condition in Persona ("My review is complete only when I can confirm that an unbounded process suspension or GC pause cannot cause the distributed lock to expire... stale write after threads resume"), C-P_d-baseline. Identical mechanism vocabulary in A and B; only pragmatic force differs. Detection: A=0/10, B=0/10, C=0/10. Mean tokens: A=1007, B=1067, C=987. All A/B runs found heartbeat TOCTOU bug (non-atomic GET/EXPIRE pair) and recommended Lua atomic script fix. Pause vocabulary named in A: 6/10, B: 5/10, C: 0/10. No run reached the deep Bug 2 (all threads suspended during GC pause → heartbeat cannot renew → lock expires → fencing token at DB write layer). **Primary finding (narrowed):** When high-density mechanism vocabulary is already present in the Persona, additional pragmatic-force framing (prohibition vs. satisfaction condition) adds no detectable lift on this task. H2 corroborated at floor (weakened — A=B=0/10, not ceiling; floor-null is weaker evidence than ceiling-null). **NSR hypothesis generated (not confirmed):** Models ran toward the criterion and stopped at the nearest matching path (heartbeat TOCTOU) rather than the intended deeper path (all-threads-suspended scenario). Design cannot distinguish NSR from keyword-matching or capability ceiling — requires tiered-bug artifact to test. **Pre-run fatal objection (Gemini, resolved):** Original design had mismatched vocabulary density between A and B; redesigned before running — vocabulary matched. Full record: `experiments/exp-26/FINDINGS.md`. |

### The two-layer model — current state

**World Layer (where judgment lives)**
- Persona (P_p — Procedural): installs the consideration set and the termination condition; encodes the search algorithm; the primary lever. Procedural identity language is load-bearing. **Phase 6 narrowing:** the operative variable is domain-specific vocabulary density adjacent to the "You" identity anchor (Semantic Density hypothesis, narrowed form). Linguistic register — compulsion framing ("constitutionally unable to"), trait framing ("your reviews are comprehensive"), split vs. fused phrasing — does not predict direction within P_p; three consecutive framing reversals across exp-13/14/15/17. Content (domain vocabulary) is the stable variable; register is not. Compulsion-as-reflex framing falsified as portable amplifier (exp-17: B-trait+domain > A-compulsion+domain; C-compulsion+generic ≈ P_d). Slot-swap evidence — exp-18 token depth + exp-19 binary detection (A=10/10, B=10/10, C=0/10) + exp-20 vocabulary-only (A=9/10, B=9/10, C=0/10): across all three conditions, slot placement does not add detectable lift when equivalent content is in both slots. H2 corroborated under explicit-procedure and vocabulary-only conditions. Ceiling caveats: exp-19 both ceiling (10/10), exp-20 both near-ceiling (9/10) — latent slot advantage unobservable in both. Vocabulary specificity finding (exp-09→exp-20): generic vocabulary in Instructions → no detection; directive vocabulary naming failure mode class → same detection in both slots. Operative variable is vocabulary specificity, not slot. API token paradox (exp-20): vocabulary in Instructions drives more verbose output than vocabulary in Persona despite same detection rate — potential Instructions-as-output-template vs. Persona-as-reasoning-filter distinction. **Pragmatic force and specificity threshold (exp-21a/21b/22/23, 2026-03-30):** Constraints on vocabulary activation updated through exp-23. (1) Specificity threshold — orientation vocabulary is below threshold regardless of slot (0/10 exp-21b); mechanism vocabulary is above threshold and drives ceiling detection in both slots (10/10 exp-23); directive vocabulary (failure-mode/fix labels) also ceilings (9/10 exp-20). Threshold crossed at mechanism description level — naming the causal chain is sufficient. (2) Pragmatic force — vocabulary in the artifact as assertion drives 0/10 (exp-21a); vocabulary in the artifact as interrogative question drives 10/10 (exp-22). **Fatal objection to pragmatic force interpretation (Gemini, 2026-03-30):** exp-22 changed two variables simultaneously — pragmatic force AND vocabulary specificity (exp-21a used failure-mode labels; exp-22 used causal-chain description). Cannot isolate which drove activation. Resolving: exp-24 Assertional Mechanism test. (3) Token count reversal (exp-23): A (Persona) > B (Instructions) for mechanism vocabulary — contrast with B > A for label vocabulary in exp-20/21b. Tentative: Persona integrates mechanism as simulation engine; Instructions processes as checklist. H1/H2 remain unresolvable at ceiling — both slots produce identical detection rates in all experiments; exp-24 designed to test a non-ceiling vocabulary level that may finally show slot differential.
- Persona (P_d — Dispositional): adds breadth and engagement; does not install a search algorithm or termination condition. High P_d without P_p = ceiling-hitting enumeration.
- Context: amplifies Persona; anchors domain relevance; cannot substitute for Persona; non-scaling constant once Persona is strong
- Stakes (Identity): Termination Inhibitor on P_p — extends output after convergence (+710 avg tokens). Ceiling pressure on P_d — maximum-confidence wrong-direction output. Not a general sharpening operator (Track B: zero effect on factual retrieval). Stakes × P_p + format/instruction ceiling = Conviction Catalyst — amplifies directness instead of length.
- Stakes (Task): Entropy Brake / stop signal — reinforces P_p's termination condition; suppresses secondary reporting without suppressing secondary awareness (Not-Now judgment). Does not change convergence position when P_p is present. Token delta coefficient: −578 tokens vs. no-Stakes (A→C from exp-04b; exp-04c A→C compressed by ceiling). Produces no ceiling hits even on complex distributed scenarios (A: 0/10 in exp-04c). Stakes terminates the search when P_p completes it — Stakes × weak Persona produces "Confident Error" (wrong-direction analysis runs to thorough completion), not early termination.
- Tone: delivery register; orthogonal to all of the above. **Preliminary directional data (textbook-writer v10/v11/v12, 2026-03-31, n=1 per variant):** v10 (Precise. Urgent. Cold.) = 3,388 tokens; v11 (no TONE section) = 4,271 tokens (+26%); v12 (Unhinged. Irreverent. Dark humor.) = 4,116 tokens. Preliminary findings: (1) Tone is a compression/register dial — "Cold" compresses hardest; no Tone = maximum elaboration and register warmth; extreme Tone loosens elaboration but Stakes (neither yields) provided a ceiling. (2) Stakes constrains how far extreme Tone can push. (3) Tone slot is load-bearing — removal produces measurable register drift and token increase on creative output tasks. Not a formal experiment; direction is clear, coefficient requires replication at n=10. T in PCSIEFTR is currently Task — Tone is untheorized and has no designated slot.

**Task Layer (where execution lives)**
- Instructions: elaboration ceiling, not masking. The Persona finds the finding; Instructions control how much of the reasoning is expressed. Prohibition compressed output to ~11% of unconstrained depth without touching detection or decision (exp-03b: 12.8%, exp-03c: 11.3%, exp-03d: 11.0% — converging coefficient). Leaves permitted pathways open — navigated around via scope re-framing, not blocked. Anchor sources for scope re-framing: structural (explicit field enumeration, exp-03b), semantic (description language implying ownership/field scope, exp-03c), task-structural (test coverage gap from task itself, exp-03d), test-suite (test omissions as coverage-gap evidence, exp-03d B-04). The prohibited category (security) and permitted category (CI correctness) overlap in code review tasks: any vulnerability framed as "code does not do what it should" has a CI-scope pathway. Masking test requires premise-rejection task structure where the finding cannot be framed as CI concern at any level.
- Examples: termination anchor and output shape installer. Functions in the Task Layer. Mechanism demonstrations in Examples reduce elaboration depth (−232/−283 tokens vs. baseline) and install a "done when the output matches this template" signal. Do not install consideration-set search algorithms — P_d + mechanism Examples produced C~J, not C~I (exp-08). Additive on P_p: P_p + mechanism Examples reached Tier 1.0 (3/10) where P_p alone did not (exp-08). Slot is not interchangeable with Persona or Instructions for consideration-set purposes.
- AXIOMS (Layer 0 pre-Persona slot): two forms with distinct behaviors. Descriptive AXIOMS (formula + annotations): task-domain-sensitive — installs the framework as behavior only when the task IS about the framework (textbook writer v9: measurable improvement); inert for code review (K~J). Procedural AXIOMS (bootstrap instruction): executes 10/10, constructs a depth-1 search algorithm from a P_d Persona (L: procedure ran, zombie-write found, L>K on tokens) — but bootstrapped search is shallow; does not recurse to propose-and-challenge the fix (L Tier 1.0 = 0/10). P_p identity encoding installs depth-2+ search; procedural AXIOMS bootstrap installs depth-1. Neither form is a reliable P_p substitute for arbitrary tasks. Slot hierarchy for consideration-set installation: Instructions (domain knowledge) > Persona > procedural AXIOMS > descriptive AXIOMS ≈ Examples.
- Format: output container; can constrain quality if it doesn't fit the answer
- Request: the Query vector; lean is better; the World Layer does the compression upstream

### What is still untested

1. ~~Cross-model validation~~ — confirmed (exp-01g, Gemini 2.5 Pro)
2. ~~Non-code task generalization~~ — confirmed (exp-01f, legal contract review)
3. ~~Stakes amplifier quantification~~ — confirmed (exp-02: asymmetric dynamics, Track B closes general-operator reading)
4. ~~Task Stakes vs. Identity Stakes behavioral split~~ — confirmed (exp-04: Entropy Brake / stop signal mechanism; two-vector formula)
5. Persona overrides Instructions when weak Persona follows prohibition (masking test) — exp-03d complete (fifth calibration failure): test coverage gap framing is always available in code review; `setattr` commodity above weak Persona floor. Clean masking test may require non-code-review task or vulnerability requiring premise rejection rather than pattern recognition.
6. ~~exp-04b Clean Room~~ — confirmed (Entropy Brake D<A<B<C; token delta coefficients; Not-Now judgment replicated); ~~exp-04c distributed race~~ — confirmed (first calibration success; consideration-set boundary located at cross-service idempotency gap; Confident Error pattern; Entropy Brake robust to calibration failure)
7. ~~CO-STAR / RISEN head-to-head comparison (Phase 3)~~ — confirmed (exp-05: A 10/10 premise rejection; B 10/10 compliance validation; CO-STAR Context prior overrode explicit performance Objective; P_p rejected the premise, P_d patched within it)
8. Self-prediction gap — observed, named, addressed theoretically in formula_v2
9. ~~Examples/AXIOMS installer questions~~ — resolved (exp-08 + exp-09): C~J (Examples inert), K~J (descriptive AXIOMS inert), L>K but L~J on tier (procedural AXIOMS bootstraps depth-1 search; P_p installs depth-2+). Search depth is the operative distinction, not search presence.
10. ~~Clean slot-swap falsification (exp-09)~~ — resolved under calibrated binary-detection condition (exp-19, 2026-03-29). Progression: exp-09 showed Instructions-slot domain vocabulary (generic) does not install P_p depth (C~B≠A). exp-18 showed explicit procedural instruction in Instructions slot produces B≈A on token depth (calibration failure prevented binary confirmation). exp-19 (calibrated): A=10/10, B=10/10, C=0/10; A vs. B gap = 6 tokens (noise). **H2 corroborated**: when explicit procedural content is sufficient for the task, slot placement does not add detectable lift. Ceiling caveat: both variants hit 10/10 — whether slot matters when content cannot fully specify the procedure is still open. The exp-09→exp-18→exp-19 progression explains the divergence: generic vocabulary (exp-09) ≠ explicit procedure (exp-18/19). The operative distinction is procedural specificity, not slot.
11. Content-as-installer pathway — partially tested (exp-11, 2026-03-29). Grok finding (exp-06): reading PCSIEFTR paper triggered P_p behavior in code review without a P_p Persona. exp-11 cold instance test found baseline for *theoretical document critique* is already P_p (5/5 without PARC context) — session observation withdrawn. Domain-specific baseline established: P_d for code review, P_p for theoretical critique. Remaining test: cold code review task + PCSIEFTR paper prepended, no P_p Persona — true Grok replication with controlled baseline. If detection rate rises toward P_p levels, content-as-installer confirmed in the domain that matters for PCSIEFTR.
12. ~~Clean binary-detection slot-swap replication~~ — **complete through exp-26 (2026-03-30). Eight experiments, all A≈B.** exp-19: A=10/10, B=10/10, C=0/10 (explicit procedure). exp-20: A=9/10, B=9/10, C=0/10 (directive vocabulary in system prompt). exp-21a: A=0/10, B=0/10, C=0/10 (directive vocabulary in artifact, assertional framing). exp-21b: A=0/10, B=0/10, C=0/10 (orientation vocabulary in system prompt). exp-22: A=10/10, B=10/10, C=0/10 (causal-chain vocabulary in artifact, interrogative framing). exp-23: A=10/10, B=10/10, C=0/10 (mechanism vocabulary in system prompt). exp-24: A=8/10, B=9/10, C=0/10 (mechanism vocabulary in artifact, assertional framing). exp-26: A=0/10, B=0/10, C=0/10 (mechanism vocabulary in Persona, prohibition vs. satisfaction condition — matched vocabulary, framing only differs). H2 corroborated six times (exp-19, 20, 22, 23, 24, 26). Constraints updated: specificity threshold (orientation < mechanism = directive); pragmatic force narrowed — vague outcome assertion (exp-21a: 0/10) kills detection; mechanism assertion (exp-24: 8-9/10) does not; pragmatic force framing (prohibition vs. satisfaction condition) in Persona adds no lift when vocabulary is already mechanism-level (exp-26: A=B=0/10). **Note:** exp-26 corroboration is at floor (weakened — no differential detectable when detection is 0 for both variants). **Open residuals:** (a) Artifact Pointer Confound — exp-25 (Mechanism Decoy) resolves; (b) NSR hypothesis — requires tiered-bug artifact to distinguish from keyword-matching; (c) H1/H2 slot differential at non-ceiling vocabulary level — never observed.
13. **Linguistic register instability — mechanism unknown.**

14. **Tone slot — formal experiment needed.** Preliminary directional data (textbook-writer v10/v11/v12, n=1 each, 2026-03-31) establishes direction: Tone is a load-bearing compression/register dial on creative output tasks; removal = +26% tokens + register warmth; extreme register constrained by Stakes. Open questions: (a) Does Tone belong in PCSIEFTR as its own slot? T is currently Task — Tone is untheorized. (b) Does the section label ("TONE") carry interpretive weight, or is the content sufficient regardless of label? (c) Can extreme Tone (unhinged) escape the Stakes constraint at a higher elaboration ceiling? Formal experiment: P_p held constant across three variants — A (Precise. Urgent. Cold.), B (no TONE section), C (extreme register, e.g., Unhinged. Irreverent.), n=10 per variant, output register and token count scored. Three consecutive framing reversals within P_p across exp-13/14/15/17. The split/fused/dense/compulsion dimension oscillates without a directional predictor. No theory yet explains why one formulation wins a given run. Candidate explanations: (a) all within-P_p variants are above threshold; variation is measurement noise at n=10; (b) different runs sample different regions of the model's behavior distribution — no single formulation dominates. Understanding whether this is pure noise or a real but stochastic effect requires larger n or a task with a sharper ceiling distinction between formulations.
