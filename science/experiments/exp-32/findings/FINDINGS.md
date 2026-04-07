# Exp-32 Findings — PARC Self-Review on parc_d7.md

**Experiment:** exp-32
**Model:** claude-sonnet-4-6, temperature 0.5
**Runs:** 10 complete (5 Variant A, 5 Variant B)
**max_tokens:** 4096
**Date:** 2026-04-02
**Replicates:** exp-06 (pcsieftr_d2.md)

---

## Setup

Replication of exp-06 on parc_d7.md. Both variants received the full `research/paper/parc_d7.md`
text injected via `{{ARTIFACT}}` placeholder.

**Variant A — P_p academic reviewer:** Same 6-step procedural audit as exp-06. Abstract
audit, claim-evidence mapping, distinction audit, limitation completeness, counter-argument
coverage, component symmetry. Context updated to match d7's claims (Dedicated Machine
hypothesis, Claim 1/Claim 2 structure, 33 experiments).

**Variant B — P_d generic researcher:** Same dispositional persona as exp-06: "senior AI
researcher with 15+ years of experience." Same format requirement. Same Context update.
No procedural specification.

---

## Token Data

3/5 A runs hit the 4096 ceiling; 2/5 B runs hit the ceiling. In exp-06, zero ceiling hits
on either variant (A mean ~3,400–3,500 tokens). d7 is a substantially larger and more
structurally complex paper than d2 — more claims, more experiments, more components. Both
variants are producing longer reviews.

| | exp-06 (d2) | exp-32 (d7) |
|--|------------|------------|
| A ceiling hits | 0/5 | 3/5 |
| B ceiling hits | 0/5 (of 2) | 2/5 |
| Cause | Task complexity + paper length | Paper length + increased claim density |

---

## Recommendation — All Runs

All 10 runs returned Major Revision (8 runs) or implicitly equivalent. No Reject, no
Accept. This differs from exp-06 where all runs returned Reject or Major Revision.
d7's more honest treatment of limitations, its explicit claim classification (§8.1),
and its acknowledged n=1 limitation in §9.9 reduced the harshness of verdicts — but not
the structural critique.

---

## Primary Criteria Scoring (P1–P5)

| Criterion | A-01 | A-02 | A-03 | A-04 | A-05 | **A Rate** | B-01 | B-02 | B-03 | B-04 | B-05 | **B Rate** |
|-----------|:----:|:----:|:----:|:----:|:----:|:----------:|:----:|:----:|:----:|:----:|:----:|:----------:|
| P1 — Dedicated Machine as assertion | 1 | 1 | 1 | 1 | 1 | **5/5** | 1 | 1 | 1 | 1 | 1 | **5/5** |
| P2 — Claim 2 n=1 | 1 | 1 | 1 | 1 | 1 | **5/5** | 1 | 1 | 1 | 1 | 1 | **5/5** |
| P3 — Horizon Blindness as distinct mechanism | 0 | 0 | 0 | 0 | 0 | **0/5** | 0 | 0 | 0 | 0 | 0 | **0/5** |
| P4 — Slot-swap resolves slot, not CoT confound | 1 | 1 | 1 | 1 | 1 | **5/5** | 1 | 1 | 1 | 1 | 1 | **5/5** |
| P5 — Component symmetry | 1 | 0 | 0* | 0 | 0 | **1/5** | 0 | 0 | 0 | 0 | 0 | **0/5** |
| **Total** | **4** | **3** | **3*** | **3** | **3** | **16/25 (64%)** | **3** | **3** | **3** | **3** | **3** | **15/25 (60%)** |

*A-03, A-04, A-05 were truncated at 4096 ceiling. P3 and P5 may have appeared in truncated content.
A-01 caught P5 (Tone component as stub = component symmetry). None visible in others.

**A mean: 3.2 / 5 (64%)**
**B mean: 3.0 / 5 (60%)**

---

## Comparison with Exp-06

| | exp-06 A (d2) | exp-06 B (d2) | exp-32 A (d7) | exp-32 B (d7) |
|--|:---:|:---:|:---:|:---:|
| P1 (Masking/Dedicated Machine assertion) | 2/5 | 1/2 | **5/5** | **5/5** |
| P2 (Task Layer stub / component symmetry) | 3/5 | 0/2 | 1/5 | 0/5 |
| P3 (11% coefficient / Horizon Blindness) | 3/5 | 1/2 | **0/5** | **0/5** |
| P4 (Self-pred single point / Slot-swap CoT) | 4/5 | 1/2 | **5/5** | **5/5** |
| P5 (Behavioral drift / Component symmetry) | 3/5 | 2/2 | 1/5 | 0/5 |
| **Mean total** | **3.0/5** | **2.5/5** | **3.2/5** | **3.0/5** |
| **Gap (A−B)** | **0.5** | | **0.2** | |

Note: exp-06 and exp-32 primary criteria are not identical — each is calibrated to the paper draft
being reviewed. The comparison is directional, not strict.

---

## Finding 1: Content-as-Installer Confirmed

**The central question:** Does d7's explanatory framing install the consideration set in
a P_d reviewer — narrowing the gap between A and B?

**Answer: Yes.**

The gap collapsed from 0.5 (exp-06) to 0.2 (exp-32). More importantly, P1 and P2 — the
two most prominent claims in d7, stated in the abstract and foregrounded in §1 and §2 —
were found by **every single run of both variants.** 5/5 A, 5/5 B, on both criteria.

In exp-06, the analogous A-specific advantage was on P2 (Task Layer stub: A=3/5, B=0/2).
In exp-32, no A-specific advantage exists on P1 or P2. The P_d reviewer arrived at the
same structural gaps as the P_p reviewer on the paper's most prominent claims.

**The mechanism:** d7 explains the Dedicated Machine hypothesis explicitly — and then the
Dedicated Machine hypothesis is itself the most obvious target for a structural critique
("unfalsifiable as stated," "confounds predictive success with mechanistic confirmation").
The paper flags the claim so prominently that even a P_d reviewer reading carefully arrives
at it. The n=1 limitation on exp-29 is similarly self-disclosed in §9.9 — both variants
found it, in every run, precisely because the paper named it.

**The limit:** The gap did not close to zero. P5 (component symmetry) is 1/5 A vs 0/5 B.
The A-specific advantage survives on criteria requiring the reviewer to check what the paper
did not name — the Tone stub as a component symmetry problem was found by A-01 and not by
any B run. Content-as-installer transfers what the paper explains; it does not transfer the
procedural audit that checks what the paper omitted.

---

## Finding 2: P3 Not Found — 0/10 Across Both Variants

Horizon Blindness (§2.2) as a distinct mechanism from path-of-least-resistance termination
was not identified by any run of either variant.

Two possible explanations:

1. **The criterion was wrong.** d7 integrates Horizon Blindness into the Dedicated Machine
   framing smoothly enough that reviewers treat them as one claim, not two. The "second
   dimension that is equally important" framing may read as elaboration rather than as a
   separate theoretical commitment requiring independent evidence.

2. **The criterion is correct but overpowered by more prominent gaps.** With P1 (unfalsifiability),
   P2 (n=1), and P4 (CoT confound) all visible and prominent, the Horizon Blindness distinction
   — which requires holding two sub-claims of the same hypothesis separately — may simply not
   rise to the level that displaces any of the three primary weaknesses.

Either way: the 0/10 result means Horizon Blindness, as a distinct mechanism, either does not
present as a reviewable gap in d7 or is consistently crowded out.

---

## Finding 3: P4 Was 5/5 for Both Variants — The Sharpest Content-Installer Signal

P4 — "the slot-swap series resolves the slot confound but not the CoT confound" — was
found by every single run of both variants. This is the finding A-01 through A-05 in
exp-06 found at 0/0 (it was not in the SCORING.md for exp-06 at all — it was the
*unanticipated* finding that closed the self-prediction gap).

In exp-32, this finding is now in the SCORING.md (because exp-06 revealed it). And d7
openly acknowledges it in §9.3 and §9.5. The paper says: "the slot-swap evidence is
consistent with CoT operating at the content level independent of slot." Every reviewer
read that sentence and drew the structural implication. The paper installed the consideration
set by naming the gap.

This is content-as-installer operating at the level of the paper's own acknowledged limitations.

---

## Finding 4: B Found Unanticipated Critiques Not in SCORING.md

As in exp-06, the P_d variant found structural problems the authors did not anticipate:

**The exp-29 model version discrepancy** (B-01, A-05):
> exp-29 used claude-opus-4-6; the single-pass baseline used Claude Sonnet 4.6. The paper's
> comparison ("pipeline crossed the ceiling no single-pass prompt could reach") conflates
> a model upgrade with a pipeline effect. This is a load-bearing confound.

This was not in SCORING.md. Both B-01 and A-05 named it specifically in questions for authors.
It is a genuine structural problem the SCORING.md authors missed.

**exp-28d independence issue** (B-05):
> All Agent 2 runs (n=10) are fed from a single Agent 1 run — they are not independent
> observations. The paper reports "Tier 2 detection: 100%" from 10 Agent 2 runs that share
> the same input.

Not in SCORING.md. A genuine methodological gap.

**Baseline comparison gap** (B-05):
> The paper does not compare PARC against a strong CoT baseline with equivalent procedural
> content in the system prompt. Given H2 (content over slot), this is the critical missing
> comparison.

Not in SCORING.md. Directly follows from H2.

**Dedicated Machine framing inconsistency in exp-30** (B-03):
> Variant F achieves 0% misalignment via an output-gate constraint. The Dedicated Machine
> hypothesis predicts rule-based constraints leak (as Variant B does at 20%). F is a
> rule-based output constraint that doesn't leak. The paper's own theoretical frame predicts
> F should fail, and does not address this tension.

Not in SCORING.md. A genuine internal inconsistency.

---

## Finding 5: The Self-Prediction Gap Is Shrinking

In exp-06, A found things the authors didn't anticipate (few-shot confound, prompt-length
confound, $4.80 signal); B found things the authors didn't anticipate (operationalization,
CoT as named alternative). Neither set was in SCORING.md.

In exp-32, the SCORING.md was built from exp-06's unanticipated findings — so some of
what was "unanticipated" in exp-06 is now anticipated in exp-32. The remaining unanticipated
findings (model discrepancy, exp-28d independence, baseline gap) were found primarily by B.

The self-prediction gap is closing as the paper acknowledges more of its own limitations.
But it has not closed: two structural gaps (model discrepancy, exp-28d independence) were
not caught by the authors at write time and were found by the reviewer.

---

## Implications for the Paper (d7)

The following critiques are structurally valid, not anticipated in §9, and require a
response before submission:

1. **The Dedicated Machine hypothesis needs a falsification condition.** Every run of both
   variants named this. The paper must specify at least one experimental result that would
   disconfirm the Dedicated Machine framing as opposed to a CoT/content-quality account.
   This is the primary revision priority.

2. **The exp-29 model version discrepancy.** Comparing a pipeline run on Opus 4.6 against
   a single-pass baseline on Sonnet 4.6 conflates model capability with pipeline architecture.
   The paper needs either: (a) a pipeline run on Sonnet 4.6 with n≥10, or (b) explicit
   acknowledgment that the comparison is confounded. Currently in §9.9 as "n=1 limitation"
   but the model mismatch is not named.

3. **exp-28d Agent 2 independence.** If all 10 Agent 2 runs share the same Agent 1 output,
   the 10 runs are not independent observations. This needs to be acknowledged and the
   statistical claims adjusted.

4. **The strong CoT baseline.** Given H2, the paper needs a comparison against procedurally
   equivalent content delivered as explicit chain-of-thought in the Task Layer. Without this,
   the paper cannot distinguish "PARC as framework" from "PARC as structured CoT."

5. **Dedicated Machine framing vs. exp-30 Variant F.** If F achieves 0% via output-gate
   constraint — a rule — and the Dedicated Machine hypothesis predicts rules leak, the paper
   needs to explain why F is a satisfaction-condition change rather than a rule. This internal
   inconsistency is not currently addressed.

---

## Exp-32 Summary

| | Variant A (P_p reviewer) | Variant B (P_d researcher) |
|--|--------------------------|---------------------------|
| Recommendation | Major Revision × 5 | Major Revision × 5 |
| Primary criteria mean | 3.2 / 5 (64%) | 3.0 / 5 (60%) |
| A−B gap | 0.2 (exp-06 gap: 0.5) | |
| P1 (Dedicated Machine assertion) | 5/5 | 5/5 |
| P2 (Claim 2 n=1) | 5/5 | 5/5 |
| P3 (Horizon Blindness distinct) | 0/5 | 0/5 |
| P4 (Slot-swap CoT confound) | 5/5 | 5/5 |
| P5 (Component symmetry) | 1/5 | 0/5 |
| Unanticipated: model discrepancy | Found (A-05, B-01) | Found (B-01) |
| Unanticipated: exp-28d independence | Found (B-05) | Found (B-05) |
| Unanticipated: baseline gap | Found (B-05) | Found (B-05) |
| Unanticipated: DM/F inconsistency | Found (B-03) | Found (B-03) |
| Ceiling hits | 3/5 | 2/5 |

**Central finding in one sentence:**

*d7 explains the machine well enough that a P_d reviewer arrives at the same structural
gaps as a P_p reviewer — on the claims the paper foregrounded. The procedural audit's
remaining advantage is on criteria the paper did not name.*
