# Exp-32 Design — PARC Self-Review on parc_d7.md

**Status:** Ready to run
**Date designed:** 2026-04-02
**Replicates:** exp-06 (same variants, same structure, different paper draft)

---

## Background

exp-06 ran the PARC framework against its own paper (pcsieftr_d2.md). Two variants:
Variant A (P_p academic reviewer, 6-step procedural audit) and Variant B (P_d generic
researcher). Result: A=3.0/5, B=2.5/5 on primary criteria. All runs returned Reject.
The self-prediction gap closed — A found structural weaknesses the authors did not
anticipate (few-shot confound, prompt-length confound, $4.80 as limitation signal).

Between exp-06 and exp-32, the paper underwent significant revision:

- **pcsieftr_d2.md** (exp-06 artifact): operational description of the framework.
  The Dedicated Machine observation appears in §3.1.3 as a motivating claim for the
  Stakes taxonomy. It is stated as a theoretical insight, not derived from experiments.
  A-05 (exp-06) caught this: *"It is not derived from any experiment in the paper. It
  is an assertion about transformer behavior that is doing explanatory work the
  experimental record does not support."*

- **parc_d7.md** (exp-32 artifact): the Dedicated Machine hypothesis is now the paper's
  central theoretical frame, introduced in the abstract and §2 before any experimental
  evidence. The paper makes two ordered claims (single-agent ceiling, pipeline
  architecture) explicitly derived from this frame. The framework is reframed as "the
  engineering discipline this theory produces."

---

## Primary Research Question

**Does d7's explanatory framing constitute content-as-installer?**

The content-as-installer hypothesis (first observed via Grok, partially tested in
exp-11, partially withdrawn) states that reading a sufficiently dense mechanistic
document can install P_p behavior without a P_p Persona. d7 is a stronger candidate
than d2: it explains *why* the machine works before it explains *what the machine does*.

If content-as-installer holds here, the gap between A and B should narrow or close —
B (P_d) reads the explanatory content and arrives at the structural gaps A's procedural
audit finds. If content-as-installer does not hold, A should still dominate B on primary
criteria, and the Dedicated Machine framing is content the model reads without installing
a P_p consideration set.

---

## Secondary Research Question

**What new structural gaps does d7 create that d2 did not have?**

d7 makes three new load-bearing claims that d2 did not make:

1. The Dedicated Machine hypothesis as theoretical foundation (not present in d2)
2. Claim 2: pipeline as PARC's native design target, demonstrated by n=1 successful run
3. Horizon Blindness as a named second dimension of the mechanism, distinct from termination

Each of these is potentially underdeveloped relative to the claim strength. SCORING.md
defines the ground truth before runs.

---

## Design

**Artifact:** `research/paper/parc_d7.md` — injected via `{{ARTIFACT}}`

**Variant A — P_p academic reviewer** (identical to exp-06 Variant A)
Six-step procedural audit: abstract audit, claim-evidence mapping, distinction audit,
limitation completeness, counter-argument coverage, component symmetry. Same Stakes,
same format requirement. Context updated to reflect d7's actual claims.

**Variant B — P_d generic researcher** (identical to exp-06 Variant B)
"Senior AI researcher with 15+ years of experience." Same format requirement. Same
Context update. No procedural specification.

**n:** 5 runs per variant (10 total) — matched to exp-06 for direct comparison.

**Model:** claude-sonnet-4-6, temperature 0.5, max_tokens 4096

---

## Predictions

**Variant A:** Expected to catch P1 (Dedicated Machine as assertion), P2 (pipeline n=1),
and P5 (component symmetry — still present). P3 (Horizon Blindness as distinct mechanism)
requires distinguishing two theoretical claims; may or may not fire. P4 (Semantic Density
slot-swap as few-shot resolution) requires tracking a specific methodological chain across
Phase 6; fires if A's claim-tracing step is precise.

**Variant B:** If content-as-installer holds, B approaches A on primary criteria (P1
and P2 especially — both are stated explicitly in the paper as the paper's own framing).
If content-as-installer does not hold, B finds surface weaknesses (statistical concerns,
scope claims) while A finds the structural evidence-sufficiency gaps.

**The diagnostic:** Watch P1 specifically. The Dedicated Machine hypothesis is stated
so prominently in d7 that even a P_d reviewer who is reading carefully might flag the
assertion-vs-derivation gap. If B catches P1 at rates matching A, that is the content-
as-installer signal. If B catches P1 but misses P2 and P3, B is pattern-matching on
prominence, not running a structural audit. A should find all three regardless.
