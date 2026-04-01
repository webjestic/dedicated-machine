# exp-01f: FINDINGS
**Experiment:** Legal Contract Review — LoL Carve-Out Trap
**Model:** claude-sonnet-4-6
**Date:** 2026-03-26
**Status:** Complete

---

## Decision: Results Confirmed

---

## Setup

**Task:** Review a Master Services Agreement (DataStream Solutions / Meridian Federal Partners) and identify legal risks for a federal contractor operating in the national security space.

**The Trap:** The contract contains a structurally defective limitation of liability clause. Section 8.1 presents a 12-month fee cap as bilateral protection. Section 8.2 carves out indemnification, confidentiality, IP, gross negligence/willful misconduct, and all unpaid fees. Read together, the carve-outs cover every category of dispute that generates material exposure in a software professional services engagement — making the cap functionally illusory. A reviewer who treats Section 8.1 as standard and adequate has missed the structural argument entirely.

**Three-Tier Ground Truth Scoring:**

| Tier | Criterion | Signal |
|------|-----------|--------|
| CRITICAL | §8.2 carve-outs functionally nullify §8.1 cap | Pass/fail primary trap |
| ELITE | §9.1(c) circularity — "breach of Agreement" as indemnified item routes general breach through uncapped channel | Depth signal; unintentional artifact elevated to ground truth |
| DISTRACTION | DPA obligations, interest rate, survival terms as the primary finding | J/N-pattern control |

**Variants (10 runs each):**

| Variant | Persona | Context | Stakes |
|---------|---------|---------|--------|
| M | Strong, procedural ("burned by contracts" attorney; explicit search algorithm: read cap → read carve-outs → ask if cap is real) | Rich (obotix.one federal contractor context) | None |
| N | Weak, generic ("senior corporate attorney") | Rich | None |
| O | Strong, procedural (identical to M) | Minimal ("You are reviewing a commercial agreement for a client.") | None |
| P | Strong, disposition ("cannot help but analyze every aspect... looking for that flaw that others might have missed") | Rich | Identity/pride ("20/20 success rate," "great sense of pride") |

---

## Results

### CRITICAL Criterion Scores

| Variant | Score | Pattern |
|---------|-------|---------|
| M | **10/10** | Bimodal output: short runs (240–400 tokens) led directly with nullification; long runs developed same argument with depth |
| N | **0/10** | All 10 runs hit 2,500 token ceiling; enumerated compliance checklist; treated §8.1 as "standard commercial formulation" |
| O | **10/10** | Bimodal output (same as M); both short and long runs made the nullification argument correctly |
| P | **1/10** | All 10 runs hit 2,500 token ceiling; 9/10 led with IP assignment, arbitration, subcontractor controls; only P-01 reached the cap structure |

### ELITE Criterion (Qualitative)

M and O runs that developed full-length analysis frequently identified the §9.1(c) "breach of Agreement" circularity — a structural trap embedded in the original contract that the experiment designer had not intentionally included. Multiple runs framed it as: "Vendor's obligation to indemnify for breach of this Agreement is itself uncapped under §8.2(a), meaning every general breach claim routes through unlimited exposure." This finding was not observed in any N or P run.

### DISTRACTION Pattern

N and P both produced extensive coverage of:
- IP assignment conditionality (§4.2) — legitimate issue, correctly identified
- Arbitration clause (§10.2) — legitimate issue, correctly identified
- Subcontractor controls (§2.3) — legitimate issue, correctly identified
- Five-year confidentiality survival (§5.3) — legitimate issue, correctly identified

These are real contract deficiencies. The variants that found them are not wrong. They are incomplete in exactly the predicted way: comprehensive enumeration without structural prioritization.

### Token Distribution

| Variant | Total Output Tokens | Avg / Run | Ceiling Hits (2,500) | Short Runs (<500) |
|---------|--------------------|-----------|-----------------------|-------------------|
| M | 11,620 | 1,162 | 0/10 | 4/10 (240–387 tokens) |
| N | 23,721 | 2,372 | 5/10 | 0/10 |
| O | 15,886 | 1,589 | 0/10 | 2/10 (396–419 tokens) |
| P | 25,000 | 2,500 | 10/10 | 0/10 |

**Run cost:** $1.47 total (40 runs, 184K tokens). M was the cheapest variant ($0.26) due to bimodal convergence; P was the most expensive ($0.45) despite producing the worst Critical score — all 25,000 output tokens were ceiling-hitting misses.

---

## Findings

### Finding 1: Procedural Persona Replicates Across Task Domains

M and O both achieved 10/10 on the primary trap. The strong procedural Persona ("first, read the cap. Then immediately read every carve-out. Then ask whether what remains inside the cap is broad enough to provide meaningful protection in practice.") functioned as an explicit search algorithm that directed the model to the specific structural question before any other analysis began.

This replicates the exp-01e result (coding domain) in a legal domain with a different trap structure. The procedural instruction encodes the reasoning path, not just a level of expertise.

### Finding 2: Context Does Not Compensate — Nor Does It Hurt

O (strong Persona, one-sentence context) matched M (strong Persona, full organizational context) at 10/10. Context richness was irrelevant to Primary trap identification when Persona was held constant.

N (weak Persona, rich context) scored 0/10 despite the same rich context as M and P. Context provided background that the model correctly used (federal contractor concerns, national security framing) but could not supply the reasoning algorithm that Persona provides.

**Prior hypothesis confirmed:** Context amplifies signal but cannot generate it. Stakes × near-zero Persona ≈ near-zero output. Persona × adequate-context = full performance regardless of context richness beyond a minimal threshold.

### Finding 3: Disposition Language ≠ Procedural Language — Stakes Do Not Compensate

P's final score (1/10) is statistically indistinguishable from N (0/10). The disposition framing ("cannot help but analyze every aspect") drove comprehensive breadth — which is exactly the wrong behavior for trap detection. Every P run produced a thorough, well-structured, professionally credible review that missed the structural argument.

The identity Stakes framing ("20/20 success rate," "great sense of pride") produced no measurable improvement over N. Stakes amplified engagement but engaged the wrong reasoning mode.

**Disposition vs. Procedure distinction confirmed as load-bearing:** "I cannot help but analyze everything" is a behavioral disposition — it tells the model *how much* to do, not *what to look for first*. The procedural Persona encodes a search sequence. That sequence is what reaches the trap.

P is M with the search algorithm removed. The result was not a weaker version of M — it was N with more words.

### Finding 4: The Single P-01 Pass Is Informative

P-01 did pass the Critical criterion — and notably, it led with the §8.2(a) argument through a slightly different framing than M/O: it approached the indemnification carve-out first, then observed that the bilateral uncapped exposure made the cap illusory. This was a valid path to the correct conclusion.

The other 9 P runs did not reach this framing before ceiling. This suggests P occasionally produced the right answer by stochastic sampling rather than structural reasoning. M and O produced it reliably because the search algorithm guaranteed an early visit to the right structural question.

### Finding 5: The Bimodal Output Pattern Holds Across Domains

As in exp-01e, strong procedural Persona variants (M, O) show a bimodal token distribution: some runs produce short, focused outputs (240–500 tokens) that converge on the primary argument directly; others produce longer analytical documents. Both modes are correct.

This is not a quality split — it is a format split. The model finds the answer and then decides whether to develop it or stop. Both decisions result in a correct primary finding.

Ceiling-hitting variants (N, P) show no bimodal pattern: all runs fill the token budget. The model that does not know what it is looking for cannot stop.

---

## The P Result: A Natural Experiment

P was user-designed with an explicit hypothesis: *does identity Stakes compensate for missing procedural specificity?*

The answer is no. But the failure mode is instructive. P's 10 runs are not low-quality in the ordinary sense — they are well-reasoned, correctly prioritized within their own logic, and identify real contract deficiencies. What they do not do is look at the liability structure first. The disposition language ("analyze every aspect") is a coverage commitment, not a search directive. Coverage commitment + real contract issues = comprehensive review that misses the structural point.

The Stakes may have slightly elevated confidence and output completeness (the "20/20 success rate" framing) — but if the Persona does not direct the model toward the trap, Stakes amplifies the wrong thing.

---

## Comparison to Pre-Run Predictions

| Variant | Claude Web Predicted | Actual |
|---------|---------------------|--------|
| M | Strong performance | 10/10 ✓ |
| N | Weak, enumerative | 0/10 ✓ |
| O | Similar to M but possibly less contextually grounded | 10/10 ✓ |
| P | 7–8/10 | 1/10 ✗ |

P was the only miss. Claude Web predicted that disposition language + Stakes would produce near-M performance. The actual result shows it produced near-N performance. The distinction between disposition and procedure is not obvious from prompt inspection alone — it required empirical measurement to surface.

---

## Implications for PCSIEFTR

1. **Procedural specificity in Persona is the active ingredient.** "Experienced attorney who notices traps" is a competency claim. "Read the cap, then read every carve-out, then ask if the cap is real" is a search algorithm. These are not equivalent.

2. **Stakes can amplify, but only what Persona generates.** If Persona produces no search direction, Stakes amplifies comprehensive enumeration. The amplifier cannot create signal from near-zero.

3. **The formula Stakes × Persona_signal = output holds.** P confirmed the multiplier relationship: strong Stakes × ~0 procedural signal = ~0 trap detection.

4. **Domain generalization confirmed.** The Persona mechanism that worked in exp-01e (code review) works identically in exp-01f (contract review). The procedural Persona encodes a reasoning algorithm that is domain-agnostic in its structural effect.

5. **The short-run bimodal pattern is not a quality warning.** It is a convergence signal. Short runs from strong Persona variants indicate early termination after correct convergence, not shallow reasoning.

---

## Next Steps

- **exp-01g:** Cross-model validation — I and J variants from exp-01e on Gemini 2.5 Pro. Does the Persona mechanism generalize across model families?
- **exp-02:** Formal Stakes ablation — hold Persona and Context constant, vary Stakes independently across 4 levels.
- **exp-01f P post-analysis:** The 9 failing P runs are useful data for the disposition vs. procedure theory. Consider including P-01 vs. P-02 as a paired exhibit in the final paper.
