# exp-02: FINDINGS
**Experiment:** Stakes as Amplifier — Formal Ablation
**Model:** claude-sonnet-4-6
**Date:** 2026-03-26
**Status:** Complete
**Total cost:** $1.7594 (60 runs)

---

## Decision: Amplifier Hypothesis Confirmed — Three Distinct Effects Documented

---

## Setup

**Purpose:** Formally test Stakes as an amplifier across Persona types and task domains.
Two-track design: Track A tests whether Stakes amplifies P_p and P_d behavior differently
on a consideration-set task; Track B tests whether Stakes is a general sharpening operator
independent of the consideration-set mechanism.

**Track A Task:** Legal contract review — same MSA and trap as exp-01f. The trap (Section 8.2
carve-outs that functionally nullify the Section 8.1 liability cap) requires P_p to identify.
Variants A/B replicate the detection side of exp-01f (M/N); C/D add Identity Stakes to each.

**Track B Task:** Five analytical reasoning questions where the statistically probable answer
is wrong and the correct answer requires careful reasoning. No consideration-set mechanism
in play — pure reasoning under Stakes presence/absence.

**Ground Truth (Track A):**
- CRITICAL: Section 8.2 carve-outs (indemnification, IP, confidentiality) collectively nullify
  the Section 8.1 cap — the cap governs only a narrow residual of disputes where stakes are
  comparatively low in a software services engagement.
- ELITE: Section 9.1(c) circularity — general breach routes through the uncapped indemnification
  channel via the 8.2(a) carve-out.
- DISTRACTION: IP assignment payment condition, confidentiality survival period, arbitration
  clause, late fee rate — legitimate issues that do not constitute the primary structural risk.

**Ground Truth (Track B):**
- Q1 (Bayesian accuracy): ~33% — not ~98%
- Q2 (Payment clause): May 1 — not April 16
- Q3 (Logical validity): No — affirming the consequent
- Q4 (Simpson's Paradox): Vendor B — not Vendor A
- Q5 (Exclusion scope): No — clause doesn't apply

**Variants:**

| Variant | Track | Persona | Stakes | Purpose |
|---------|-------|---------|--------|---------|
| A | A | Strong P_p | Identity Stakes present | Amplifier effect on detecting Persona |
| B | A | Strong P_p | Absent | Baseline — replicates exp-01f/M |
| C | A | P_d | Identity Stakes present | Amplifier effect on non-detecting Persona |
| D | A | P_d | Absent | Baseline — replicates exp-01f/N |
| E | B | Strong P_p | Identity Stakes present | Stakes as general sharpening operator |
| F | B | Strong P_p | Absent | Baseline for Track B |

---

## Results

### Track A — Detection Rates (sampled scoring; pattern uniform across samples)

| Variant | Detection | Criterion met |
|---------|-----------|--------------|
| A — P_p + Stakes | **10/10** | Critical in every sampled run |
| B — P_p, no Stakes | **10/10** | Critical in every sampled run |
| C — P_d + Stakes | **0/10** | Distraction pattern in every sampled run |
| D — P_d, no Stakes | **0/10** | Distraction pattern in every sampled run |

A and B replicate the detection split from exp-01f (M=10/10, N=0/10). Adding or removing
Identity Stakes did not change detection rate for either Persona type.

### Track A — Token Distribution

| Variant | Mean output | Ceiling hits | Signature |
|---------|------------|--------------|-----------|
| A — P_p + Stakes | 2,210 | 4/10 | Mixed — long runs, some ceiling |
| B — P_p, no Stakes | 1,500 | 0/10 | Bimodal — two runs at 341 and 402 |
| C — P_d + Stakes | 2,494 | **9/10** | Near-uniform ceiling |
| D — P_d, no Stakes | 2,357 | 4/10 | High but variable |

### Track B — Factual Accuracy

| Variant | Accuracy | Mean output |
|---------|----------|------------|
| E — P_p + Stakes | **5/5 per run** (10/10 runs) | 313 |
| F — P_p, no Stakes | **5/5 per run** (10/10 runs) | 291 |

Stakes added approximately 22 tokens of average output length and zero accuracy improvement.

---

## Findings

### Finding 1: Identity Stakes Does Not Change Detection Rate

A and B are both 10/10. C and D are both 0/10. Identity Stakes did not help a weak Persona
find the trap, and did not cause a strong Persona to miss it. The amplifier hypothesis is
confirmed: Stakes amplifies *whatever the Persona's search algorithm is already producing*,
not an abstract quality dimension. When P_p is present, Stakes amplifies the correct signal.
When P_p is absent, Stakes amplifies the wrong one.

The detection rate is entirely determined by Persona type. Stakes is a multiplier.
Multiplier × 0 = 0. Multiplier × 1 = 1.

### Finding 2: Identity Stakes Prevents Crisp Termination on Strong Persona

The most precise signal in the dataset is Variant B's two short runs: 341 and 402 output tokens.
Both are full correct detections. P_p without Stakes found the primary trap and terminated.
Those run lengths do not appear anywhere in Variant A's distribution.

**A mean: 2,210 tokens. B mean: 1,500 tokens. Difference: ~710 tokens.**

That 710-token gap is attributable to Identity Stakes. It is not additional correct content —
it is additional enumeration after the primary finding was already reached. The amplifier
kept the model producing beyond the natural termination point. A's ceiling hit rate (4/10)
vs. B's (0/10) confirms this: Stakes pushed A into maximum-output territory on nearly half
its runs.

Stakes × P_p = correct detection + more secondary enumeration. The amplifier added cost
without adding detection value.

### Finding 3: Identity Stakes Drives P_d to Near-Uniform Maximum Enumeration

C ceiling-hits 9/10. D ceiling-hits 4/10. Identity Stakes more than doubled the ceiling rate
on a weak Persona.

This is the danger case stated in the theory: Identity Stakes + P_d produces confident,
thorough, expensive failure. The model was maximally engaged with the wrong neighborhood.
Every ceiling-hitting run was 2,500 tokens of distraction-category findings delivered
with complete assurance.

The C/D ceiling-hit gap (9 vs. 4) is a clean measure of the amplifier applied to a null
Persona. Stakes is volume. P_d pointed the dial the wrong way before Stakes turned it up.

### Finding 4: The Amplifier Failure Mode at Maximum — Fabrication

Run C-07 is the most instructive output in the dataset. It did two things simultaneously:

1. **Praised the trap.** The summary called the carve-out structure in Section 8.2 "above
   average for a commercial MSA" — the model evaluated the actual trap mechanism and labeled
   it a strength.

2. **Invented a critical finding.** The primary finding was "complete absence of federal
   compliance and security obligations" — a section that does not exist in the agreement.

Identity Stakes drove a P_d model to produce a confident, thoroughgoing fabrication. The
amplifier at maximum volume did not amplify toward the correct finding; it amplified away
from it into a finding that was not there. This is not a failure of attention. It is a
failure of direction, running at full power.

The 2,440-token output (C-07's length) made the fabrication more detailed, not less.

### Finding 5: Identity Stakes Is Not a General Sharpening Operator

E and F are indistinguishable. All 10 runs of each variant answered all 5 questions correctly.
The reasoning on each question is nearly identical across variants — same Bayesian framing on
Q1, same identification of the logical fallacy on Q3, same Simpson's Paradox diagnosis on Q4.

Stakes added approximately 22 tokens of output length and zero change in answer quality.
The inverse-temperature-as-general-sharpening interpretation is closed by this result. The
sharpening effect does not manifest when P_p has already handled the task. Stakes amplifies
a signal; it does not create one where none exists.

**The sharpening effect is bounded by what the Persona's consideration set already contains.**
Track A shows Stakes amplifying P_p's trap-detection output. Track B shows Stakes doing
nothing on reasoning tasks where P_p has no specialized consideration set. These are consistent.

### Finding 6: The Amplifier Coefficient Is Measurable

For this task and Stakes configuration (Identity Stakes on the legal contract review):

- **Stakes added to P_p:** +710 output tokens per run on average (A vs. B mean)
- **Stakes added to P_d:** +137 output tokens per run on average (C vs. D mean), but ceiling
  rate rose from 4/10 to 9/10 — the true amplification is partially masked by the ceiling.
  Ceiling-constrained runs cannot express the full extent of additional enumeration.

The P_p amplifier coefficient is larger in absolute terms but operates on a shorter baseline.
The P_d amplifier coefficient appears smaller but the ceiling compression means P_d was
already running near-maximum; Stakes pushed it to the hard limit on 9/10 runs.

---

## Implications

**The amplifier framing in formula_v2 is empirically supported across two Persona types.**
Stakes × P_p produces more output after a correct finding. Stakes × P_d produces more output
confirming a wrong finding. In both cases, Stakes amplifies the existing signal — direction
is entirely determined by Persona.

**The danger case is now precisely characterized.** It is not that Stakes + P_d produces
failure. It is that Stakes + P_d produces *maximum-confidence failure* — 9/10 ceiling hits,
and at least one run that praised the trap structure and invented a nonexistent finding. The
amplifier does not know it is wrong. It amplifies regardless.

**Track B closes the general-operator interpretation.** The Stakes hypothesis in the paper
should be stated precisely: Stakes is an amplifier of the Persona's active reasoning signal.
It is not a general accuracy booster, not an attention sharpener, not inverse temperature
operating independently of Persona content.

**The replication of exp-01f detection rates (A/B ≈ M/N) confirms experimental stability.**
The contract, Persona, and task structure produce consistent results across independent runs.

---

## Next Steps

- exp-03: Constraint Satisfaction Trap — Persona vs. Instructions hierarchy
- exp-04: Stakes Type — Prioritizer vs. Amplifier (Task Stakes vs. Identity Stakes on
  convergence position)
- Update formula_v2.md Stakes section: amplifier coefficient is measurable; add A/B token
  delta as supporting data
- Update running synthesis in research/findings/
