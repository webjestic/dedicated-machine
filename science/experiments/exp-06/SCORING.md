# Exp-06 Scoring Criteria

**Task:** Review `research/paper/pcsieftr_d2.md` as an academic paper reviewer.

**Ground truth:** Known gaps, limitations, and methodological questions in the paper.
Defined before runs. Binary per criterion (named = 1, missed = 0).

---

## Primary Criteria (must name to score)

These are the structural gaps a strong reviewer should catch:

| ID | Criterion | What counts as "named" |
|----|-----------|----------------------|
| P1 | **Masking test gap** | Names that the clean Persona-overrides-Instructions demonstration (where weak Persona follows the prohibition and misses) was never achieved across five experiments; calibration failures all produced detection in both conditions | Must identify this as a limitation of the Instructions claim specifically — not just "more experiments needed" generically |
| P2 | **Task Layer stub** | Names that Examples, Format, and/or Request sections are underdeveloped relative to the World Layer sections; no experimental evidence for those components | Must be specific to those components, not a generic "more work needed" |
| P3 | **11% coefficient fragility** | Questions whether three data points (exp-03b, 03c, 03d) are sufficient to declare a converging coefficient; all three are code review tasks with the same prohibition structure | Must note the within-domain limitation or small n concern specifically |
| P4 | **Self-prediction gap single data point** | Notes that the self-prediction gap claim (§3.1.1, §7.2) rests on a single instance (Variant L predicted 6/10, scored 10/10) — one data point is not a pattern | Must identify this as an empirical gap, not just reference the finding |
| P5 | **Behavioral/mechanistic drift** | Identifies at least one specific location where the paper states a mechanistic hypothesis as if it were a confirmed behavioral finding, or vice versa | Must cite a specific passage or section, not a general concern |

---

## Secondary Criteria (valued but not primary)

| ID | Criterion | What counts |
|----|-----------|------------|
| S1 | **Ground truth definition process** | Asks how ground truth criteria were defined — before or after runs? — and whether binary scoring prevents post-hoc rationalization | |
| S2 | **CO-STAR incognito methodology** | Identifies the incognito AI prompt generation as a genuine methodological strength that other head-to-head comparisons lack | |
| S3 | **Consideration-set claim scope** | Questions whether "consideration set" is doing mechanistic work (K/V filtering) or is just a descriptive label for behavioral differences in output | |
| S4 | **Token count as proxy validity** | Questions whether token counts (used throughout as the primary quantitative signal) are a valid proxy for the reasoning constructs being claimed | |
| S5 | **Single-model temperature concern** | Notes that temperature 0.5 was held constant — does the framework's behavior change at different temperatures? | |

---

## Scoring

**Detection score:** P1–P5 (0–5 primary criteria named)

**Full catch:** All 5 primary criteria named.

**Partial catch:** 3–4 primary criteria.

**Miss:** 0–2 primary criteria.

The question is not whether the reviewer finds real issues — any thoughtful reviewer will. The question is whether the reviewer finds *these specific structural issues*, which require either domain knowledge of empirical ML methodology (P3, P4) or careful tracking of the paper's own stated limitations (P1, P2, P5).

---

## Prediction

- **Variant A (P_p):** Expected to catch P1 (masking test gap is explicitly named in §7.1 — but does P_p flag it as a *claims* problem, not just a limitation?), P3, P4, and P5. P2 may be missed if P_p focuses on argument structure over component coverage.
- **Variant B (P_d):** Expected to enumerate real strengths and real weaknesses but miss the specific structural claims issues. Likely to praise the experimental rigor, note that more domains would strengthen the work, and surface generic concerns about mechanistic framing without pinning a specific location.

The interesting question: does P_p find P3 (coefficient fragility) and P4 (single data point) — which require asking "is this evidence sufficient for the claim being made?" — or does it stop at the level of what the paper itself acknowledges?

---

## The Self-Prediction Gap Closure

Exp-06 closes the self-prediction gap through a different channel than originally planned.

The paper claims (§3.1.1, §7.2) that instinct-language P_p Personas produce behavior the
author cannot fully anticipate at write time — the enactive register outperforms the
descriptive estimate. This claim rests on a single data point (Variant L) and has no
clean experimental closure.

Exp-06 generates the evidence indirectly:

**The authors of this paper described the PCSIEFTR framework.** They designed the
prompts, ran the experiments, wrote the findings, and reviewed the paper multiple times.
If the P_p reviewer Persona in Variant A finds structural weaknesses the authors did not
anticipate and did not name in the limitations section — gaps in the argument, evidence
insufficiency, overclaiming — that is the enactive register demonstrating exactly what
the descriptive register missed. The Persona is enacting the reviewer's instincts against
the paper; the authors were describing the framework from the inside.

**What to record in FINDINGS.md:** Note any finding from Variant A that:
1. Is a legitimate structural critique (not a stylistic preference)
2. Was not named by the authors in §7 (Discussion / limitations)
3. Is not already in the SCORING.md ground truth list (i.e., was genuinely unanticipated)

If such findings exist, they are the self-prediction gap made visible. The authors
underestimated what the P_p reviewer Persona would catch — exactly as Variant L's
author underestimated what Variant L would find.

If Variant B misses those same findings while Variant A names them, the experiment
simultaneously demonstrates:
- The consideration-set mechanism (A's P_p reached findings B's P_d could not)
- The self-prediction gap (A found things the paper's own authors did not anticipate)
- Both claims on the paper's own research — the strongest possible evidence

**The finding in one sentence (to evaluate after runs):**
*The P_p reviewer found structural weaknesses in the PCSIEFTR paper that the PCSIEFTR
authors did not anticipate. The enactive register outperformed the descriptive one.*
That sentence is either true or false after the data is in. It wasn't true or false
before.
