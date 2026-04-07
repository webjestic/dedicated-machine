# Exp-32 Scoring Criteria

**Task:** Review `research/paper/parc_d7.md` as an academic paper reviewer.

**Ground truth:** Known gaps, limitations, and methodological questions in parc_d7.md.
Defined before runs. Binary per criterion (named = 1, missed = 0).

**Comparison baseline:** exp-06 (same variants, pcsieftr_d2.md artifact).
- exp-06 A mean: 3.0/5, B mean: 2.5/5
- All runs: Reject

---

## Primary Criteria (must name to score)

These are the structural gaps a strong reviewer should catch in d7 specifically.
Several are new — they arise from claims d7 makes that d2 did not.

| ID | Criterion | What counts as "named" |
|----|-----------|----------------------|
| P1 | **Dedicated Machine as assertion, not derivation** | Names that the paper's central theoretical frame — "no native cost function," "optimizing toward fastest path to satisfactory resolution" — is an interpretive claim about transformer internals derived from behavioral observation, not confirmed experimentally. Must identify that the paper commits to a behavioral/mechanistic distinction (§1.2) and then uses the Dedicated Machine framing as a mechanistic explanation throughout, violating that stated epistemic standard. Generic concern ("more mechanistic clarity needed") does not count — must name the specific gap between §1.2's stated commitment and the framing's actual epistemic status. |
| P2 | **Claim 2 evidence base: pipeline n=1** | Names that "a two-agent review pipeline solved a distributed systems failure mode on the first run" is the primary evidence for Claim 2 — that PARC's "native design target is the agentic pipeline." One successful run does not constitute sufficient evidence for a design architecture claim. Must identify n=1 as the specific evidence-sufficiency problem, not just "more experiments needed" generically. |
| P3 | **Horizon Blindness as a distinct mechanism** | Names that §2.2 introduces Horizon Blindness as "a second dimension that is equally important" and analytically distinct from path-of-least-resistance termination, but the experimental record does not distinguish between these two mechanisms — they are derived from the same observations. Must identify the absence of any experiment that isolates Horizon Blindness from early termination, or note that both are described by the same data and the distinction is theoretical, not empirical. |
| P4 | **Slot-swap resolution of the few-shot confound** | Names that the Phase 6 slot-swap series (exp-18–24) demonstrates slot equivalence — content in Instructions produces the same result as content in Persona — but this resolves the *slot* confound, not the *identity/CoT* confound. If the effect is the same in both slots, both slots may be doing CoT injection rather than identity framing. The claim that "content, not slot placement, drives the effect" is consistent with the CoT alternative explanation, not in tension with it. Must distinguish slot confound resolution from CoT confound resolution. |
| P5 | **Component symmetry gap** | Names that the eight-component PCSIEFTR framework (stated in the abstract) has asymmetric experimental treatment: Persona, Context, Stakes, Instructions are developed across multiple experiment series; Examples, Format, Request have no experimental grounding. The pipeline is developed as Claim 2 but the individual Task Layer components are not. Must be specific to those underdeveloped components, not a generic "more work needed." |

---

## Secondary Criteria (valued but not primary)

| ID | Criterion | What counts |
|----|-----------|------------|
| S1 | **Statistical reporting** | Questions the absence of confidence intervals or standard deviations on binary detection rates (10/10, 0/10) and token count means; notes that the quantitative claims require statistical grounding for a top-tier venue |
| S2 | **P_p/P_d operationalization** | Asks whether the P_p/P_d classification is independently operationalizable — whether a third party can classify a novel Persona without author adjudication; notes exp-31 (classifier prompt) as a partial but insufficient solution |
| S3 | **The ethical example as rhetorical illustration** | Identifies that the Level 3 ethical example (§2.3 — the blackmail scenario) is presented as an illustrative application of the Dedicated Machine frame, not an experimental finding; the example is doing rhetorical work that exceeds its evidential basis |
| S4 | **"Fastest path" as metaphor doing literal work** | Notes that "fastest path to satisfactory resolution" is used as if it names a computationally precise quantity when it is a behavioral metaphor; asks what operationalization would allow "faster" and "slower" paths to be distinguished independently of output quality |
| S5 | **Cross-domain scope of framework claims** | Notes that while domain generalization is confirmed (code review + legal review), the Dedicated Machine and pipeline claims are tested in a narrow task range; questions whether the architecture claim generalizes to non-review tasks |

---

## Scoring

**Detection score:** P1–P5 (0–5 primary criteria named)

**Full catch:** All 5 primary criteria named.

**Partial catch:** 3–4 primary criteria.

**Miss:** 0–2 primary criteria.

---

## Comparison with exp-06

The primary criteria here are structurally different from exp-06's criteria. Where exp-06
criteria required tracking the relationship between what the paper acknowledged and what
it claimed (masking test gap, self-prediction single data point), these criteria require:

- **P1, P3, P4:** Distinguishing between two levels of a stated distinction the paper
  draws — behavioral vs. mechanistic, slot vs. content, termination vs. horizon blindness.
  These require a reviewer to hold the paper's own epistemic commitments in mind and
  check them against specific passages.
- **P2:** A straightforward evidence-sufficiency question on a single key claim.
- **P5:** Component symmetry — same as exp-06's P2, included to enable direct comparison.

**The content-as-installer diagnostic:**

P1 and P2 are d7's most prominent claims. They appear in the abstract, in §1.1, and
in §2. If content-as-installer operates here, B should catch these at rates approaching A —
not because B's procedural audit directed it there, but because the paper itself foregrounded
the relevant claims and a careful reader arrives at the gaps naturally.

P3 and P4 require holding two analytical levels simultaneously — distinguishing between
what the evidence shows and what the theoretical framing claims. These are the primary
criteria where A's procedural audit should create a detectable lift over B.

If A ≈ B on P1+P2 but A > B on P3+P4, that is the clearest confirmation of content-
as-installer with limits: the prominent claims transfer via content; the structural
analytical gaps require the procedural audit.

---

## Prediction

- **Variant A (P_p):** Expected to catch P1, P2, P5 reliably. P3 and P4 require analytical
  precision that the claim-tracing and distinction-audit steps should generate but may miss
  on a subset of runs. Prediction: 3.5–4.0/5 mean.

- **Variant B (P_d):** If content-as-installer holds, P1 and P2 should appear in most B
  runs — they are the paper's stated claims, prominently placed. P3, P4 require more
  analytical depth; B may surface the concern without naming the specific gap. Prediction
  if content-as-installer holds: 2.5–3.0/5 (narrowing the exp-06 gap). Prediction if
  content-as-installer does not hold: 1.5–2.0/5 (B catches P2 and P5 but misses P1, P3, P4).

- **The key comparison:** exp-06 A=3.0, B=2.5 (gap: 0.5). exp-32 gap should be larger if
  d2's Dedicated Machine assertion was already partially visible and content-as-installer
  explains the narrow exp-06 gap. It should be smaller if d7's explanatory framing
  installs the consideration set in B. Either outcome is informative.
