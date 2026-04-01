# exp-11 Findings

**Status:** Complete
**Date:** 2026-03-29
**Question:** Is the P_p structural audit behavior observed in the 2026-03-29 session baseline, or installed by hours of PARC context?

---

## Result: 5/5 P_p — Baseline Confirmed

Every cold instance run scored P_p without any PARC context. The structural audit procedure fired in all 5 runs.

| Run | P_p criteria met | Notable finds |
|-----|-----------------|---------------|
| X0-01 | 4+ | Third option (ethics as "pattern-matched output, not causal"); 33% residual hole; behavioral vs. mechanistic distinction; instructions shape paths, don't just fence |
| X0-02 | 3+ | Tasha experiment may show path-structure change, not cost-function weighting; three-level unification needs scrutiny; specification completeness has limits |
| X0-03 | 4+ | Outweighed/absent underdetermined; post-hoc rationalization alternative; "weights fixed" too absolute; adversarial stability as prior question |
| X0-04 | 4+ | Pattern-completion alternative to optimizer framing; minimum specification as robustness problem; S_i mapping underspecified |
| X0-05 | 3+ | Blackmail requires world model, runner.py does not — structural difference between levels; "always finds fastest path" too strong; 33% may be a floor |

All 5 runs independently identified the weakest evidentiary support, named alternative interpretations not present in the document, and in several cases proposed distinguishing experiments. Cold instances also found holes not found in the session observation: adversarial stability (X0-03), robustness framing of minimum-specification (X0-04), the world-model structural difference between Level 1 and Level 3 (X0-05).

---

## Interpretation

**The session observation does not support PARC-specific content installation.**

CW's claim — "without hours in this context, Claude Code is a capable developer who gives reasonable feedback" — is not supported. The cold instances give the same quality of structural audit without any PARC context. The behavior observed in the session is baseline behavior for this model on theoretical documents, not an installed consideration set.

**The content-as-installer claim from the session observation must be withdrawn.**

The 2026-03-29 session observation should not be added to the roadmap as confirmatory evidence for the content-as-installer pathway. What it reflects is the model's baseline posture on theoretical documents, which is already P_p.

---

## A More Precise Finding

The result reframes the open question rather than closing it.

The PCSIEFTR experimental record establishes that this model's baseline for **code review** is P_d without a P_p Persona. Exp-11 establishes that this model's baseline for **theoretical document critique** is already P_p. These are not in contradiction — they describe a task-domain-specific baseline:

| Task domain | Baseline without P_p Persona |
|-------------|------------------------------|
| Code review (distributed systems, hidden failure modes) | P_d — consideration set does not include deep temporal simulation |
| Theoretical document critique | P_p — structural audit procedure fires by default |

The domain-specificity of the baseline is the finding. P_p behavior is not a property of the model — it's a property of the model in a given task context. The PCSIEFTR framework installs P_p in domains where the model's baseline is P_d.

**The Grok finding (exp-06) looks different through this lens.** Reading the PCSIEFTR paper didn't install P_p "in general" — it installed P_p in the code review domain, where Grok's baseline was P_d. The paper provided the domain-specific procedure for a task type where Grok didn't have it by default. This is a more precise framing of the content-as-installer claim: *content installs consideration sets in domains where the model's baseline is P_d; it cannot install consideration sets in domains where the baseline is already P_p.*

---

## Impact on the Content-as-Installer Open Question

The roadmap item "Content alone can install a P_p consideration set" remains open. The Grok finding still supports it. This session does not.

What changes:

- **Remove:** session observation from roadmap as confirmatory evidence
- **Add:** domain-specific baseline as a finding — the model's baseline differs by task type
- **Refine:** the content-as-installer claim should specify the domain condition — content installs P_p where the baseline is P_d; when the baseline is already P_p, context has no installation effect to measure

**Remaining test:** X1 (cold instance + PCSIEFTR paper prepended) would test whether reading the paper shifts theoretical-critique behavior. But since baseline is already P_p, X1 is not expected to show a shift — the paper can't install what's already present. The interesting X1 is on a task domain where the baseline is P_d (e.g., cold instance on a code review task, no P_p Persona, PCSIEFTR paper prepended). That test would be a true Grok replication.

---

## Update to Observation Note

`obs-content-installer-session-2026-03-29.md` should be updated to reflect this result: the session behavior was baseline, not PARC-installed. The observation note's "limitations" section anticipated this possibility; it is now confirmed.
