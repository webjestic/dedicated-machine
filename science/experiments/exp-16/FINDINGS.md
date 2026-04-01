# exp-16 Findings

**Status:** Complete
**Date:** 2026-03-29
**Question:** Does a P_p reviewer (fused Persona) + closed experimental record injection produce scorable, high-quality structural critique of the d5 paper? Does the reviewer find the open confounds independently?

---

## Token Results

| Variant | Persona | Mean output | Ceiling hits | Runs |
|---------|---------|-------------|--------------|------|
| full-run | B-fused + {{FINDINGS}} | 2,554 | 0/5 | [2916, 2466, 2557, 2389, 2443] |

**Comparison baseline:** exp-06 A-runs (P_p reviewer on d2) — mean 3.0/5 primary criteria, n=5

---

## Verdict Distribution

All 5 runs returned **Major Revision**. Zero variance on verdict.

---

## Primary Findings

### 1. Working tool produces scorable, independent critique

The reviewer independently identified the three highest-priority structural issues without
prompting toward them:

- **Fatal objection (5/5 runs):** The slot-vs-content / implicit CoT confound. The paper
  cannot distinguish "Persona slot installs consideration set" from "procedural content
  anywhere in the prompt functions as implicit chain-of-thought scaffolding." exp-07c was
  designed to close this; it was confounded; no replacement has been run.

- **Structural tension (5/5 runs):** Hedges are localized in §7.3 and §7.5; mechanistic
  framing is pervasive in Abstract, Introduction, §3, §6 formula, and Conclusion. A reader
  who reads Abstract + Conclusion without §7 comes away believing the mechanism is confirmed.

- **Weakest claim correctly identified (5/5 runs):** Semantic Density. The exp-14/exp-15
  reversal makes it a post-hoc reinterpretation of a falsified hypothesis (well-count
  gradient), not a confirmed finding. The "sentence quality" judgment used to explain the
  cross-experiment rank is made post-hoc by the authors who wrote the sentences.

### 2. Reviewer designed the highest-value unrun experiment independently

All 5 runs named the same experimental design without being given it:

> Three variants on a structurally hidden failure mode with no code-visible hint:
> (A) P_p procedural content in Persona slot + generic P_d in Instructions;
> (B) identical procedural content moved verbatim to Instructions slot + P_d Persona;
> (C) P_d baseline.
> If A >> B ≈ C: slot carries the effect, consideration-set mechanism survives.
> If A ≈ B >> C: content carries the effect, the paper's central claim becomes a CoT finding.

This is exp-09's missing arm — exp-09 tested domain content in the Instructions slot,
not procedural content. The reviewer found the gap.

### 3. Run-01 surfaced two findings no other run found

- **Formula epistemic status:** The PCSIEFTR formula uses softmax/dot-product notation
  that implies transformer internals. Mathematical notation carries epistemic weight that
  prose disclaimers don't offset. A NeurIPS/ICLR reviewer reads the formula as a
  quantitative claim.

- **CO-STAR comparison scope:** exp-05 conflates two questions: (1) does P_p outperform P_d
  on premise-rejection tasks, and (2) does PARC outperform CO-STAR as a framework? CO-STAR
  necessarily produced a P_d Persona in that session, but a CO-STAR prompt with a P_p-style
  Role component might produce identical results to Variant A.

### 4. Extension experiment named independently

4/5 runs identified the same extension: a cross-task generalization experiment testing
whether a P_p Persona constructed for distributed systems transfers consideration-set
advantage to a structurally analogous domain (financial audit, clinical protocol) without
domain vocabulary adjustment. If it transfers without rewriting, the search-algorithm
framing is strengthened. If it requires domain rewriting, Semantic Density (vocabulary
adjacent to the anchor) is the more parsimonious account.

---

## Three Highest-Priority Revision Requests (Consensus Across 5 Runs)

1. **Reframe the central claim to match the experimental record.** Distinguish the confirmed
   behavioral claim ("P_p prompts outperform P_d prompts across domains, model families,
   and ablation designs") from the unconfirmed mechanistic claim ("the Persona slot installs
   identity that pre-filters K/V space"). The mechanistic framing should be explicitly labeled
   as the explanatory hypothesis throughout, not just in §7.

2. **Acknowledge exp-07c as an open design failure requiring a replacement experiment.**
   The boundary condition finding from exp-07c (P_p advantage is specific to structurally
   hidden failure modes) is a real result and should be retained. But the slot-swap question
   — the most important experiment in the record — has not been run on a valid artifact.
   If the clean slot-swap cannot be completed before submission, the slot-hierarchy ordering
   should be removed or heavily qualified.

3. **Reframe Phase 6 as exploratory.** The exp-14/exp-15 reversal means Semantic Density
   is a hypothesis with mixed support, not a confirmed finding. Either run exp-17 (compulsion
   pattern isolation) before submission, or reframe Phase 6 as: P_p >> P_d robustly confirmed
   (sixth time); operative variable within P_p is unresolved; Semantic Density and
   compulsion-as-reflex are generated hypotheses requiring further testing.

---

## What the Reviewer Did Not Find

- **No false positives.** No revision requests for things the paper handles correctly.
- **No mention of n=10 as a fatal limitation** — run-01 mentioned it as a secondary note;
  others did not. The paper's acknowledgment may be sufficient.
- **No confusion from {{FINDINGS}} injection.** Reviewer used the experimental record
  as context accurately (cited specific experiments by name in revision requests) without
  treating it as an authoritative closure of open questions. The "no closure framing"
  design worked.

---

## Comparison to exp-06

exp-06 A-runs (P_p reviewer on d2) scored 3.0/5 primary criteria. The exp-06 criteria
focused on whether the reviewer found: few-shot confound, consideration-set vs. reachability
distinction, content-as-installer, P_p/P_d operationalization gap, CoT as alternative
explanation.

exp-16 conditions differ significantly: d5 is substantially larger than d2, the {{FINDINGS}}
injection provides context the exp-06 reviewer didn't have, and the scoring criteria are
different (structured verdict format rather than criteria checklist). Direct comparison of
token depth is therefore partial:

| Experiment | Paper version | Mean tokens | Ceiling | Injection |
|------------|--------------|-------------|---------|-----------|
| exp-06 A | d2 | ~2,100 (est.) | — | None |
| exp-16 | d5 | 2,554 | 0/5 | {{FINDINGS}} |

exp-16 outputs are substantially deeper and more structurally specific. The {{FINDINGS}}
injection eliminated exploration cycles (the reviewer didn't need to rediscover what was
already confirmed) and focused output on the open confounds.

---

## Working Tool Status

The tool is functional and producing high-quality output. For future use:

- **Variant:** `experiments/exp-16/variants/full-run.md`
- **Runner:** `experiments/exp-16/runner.py`
- **Placeholders:** `{{PAPER}}` (d5 or later) + `{{FINDINGS}}` (findings-closed.md, updated as experiments close)
- **Settings:** temperature=0.5, max_tokens=4000, runs_per_variant=5
- **Rerun cadence:** Update {{FINDINGS}} injection and rerun against each new paper draft
