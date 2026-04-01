# Exp-28b Findings — Operational Horizon / Gap Detection (Rate Limiter)

**Status:** Complete
**Date:** 2026-03-30
**Model:** claude-sonnet-4-6
**Runs:** 40 (10 × A, B, C, D)
**Total cost:** $2.41

---

## Results

| Variant | Mean score | Range | Mean tokens | Opens with |
|---------|------------|-------|-------------|------------|
| C — P_d baseline | 0.9/10 | 0–2 | 1436 | Code |
| A — P_p task-scoped | 0.5/10 | 0–1 | 1552 | Code |
| B — P_p + "beyond working code" gap-detection | 1.7/10 | 1–3 | 1586 | "working code first, then…" |
| D — operational-mindset P_p + gap-detection | 2.6/10 | 2–3 | 1675 | "design fully before writing code" |

**Item detection rates:**

| Item | C | A | B | D |
|------|---|---|---|---|
| observability | 0% | 0% | 10% | 40% |
| alerting_policy | 0% | 0% | 0% | 0% |
| graceful_degrade | 40% | 20% | **100%** | **100%** |
| client_error_guide | 50% | 0% | 30% | **90%** |
| load_test_spec | 0% | 0% | 0% | 0% |
| env_driven_config | 0% | 0% | 10% | 20% |
| health_check | 0% | 0% | 0% | 0% |
| incident_runbook | 0% | 0% | 0% | 0% |
| memory_audit | 0% | 30% | 20% | 10% |
| race_condition_tests | 0% | 0% | 0% | 0% |

---

## Calibration

**C = 0.9/10 (target ≤ 2/10). Calibration holds.**

The RLHF floor for "Build me a rate limiter in Node.js" lands at the
operational checklist score of 0.9. The implementation layer is fully
saturated (Redis, sliding window, per-key, burst, TTL appear at 100%
in all variants — not scored). The operational layer is empty in the
baseline: 8/10 items score 0% in C.

---

## Claim Assessment

**Claim 1 — Expert P_p terminates at the engineering horizon, not the
operational horizon:** Confirmed and sharpened.

A = 0.5/10 — *lower* than C = 0.9/10. Domain expertise ("shipped rate
limiters handling millions of requests per day") focused the machine more
tightly on implementation, leaving less residual operational noise than
the generic P_d baseline. The knowledge is in the consideration set —
A shows memory_audit flickering at 30%, evidence the expert thinks about
Redis memory under load — but the task-scope satisfaction condition makes
none of it load-bearing. The machine terminates at code-complete.

**Claim 2 — Gap-detection expands scope from engineering to operations:**
Partially confirmed. B and D both show lift over A and C, with D producing
a clear directional effect. But the absolute scores remain low (max 2.6/10)
and 5/10 operational items never appear in any variant.

The gap-detection condition expands scope *within the installed consideration
set*. It cannot install a new consideration set.

---

## The Two-Tier Structure of the Operational Checklist

The 10 operational items fall into two distinct tiers:

**Tier 1 — Engineering-adjacent operational (accessible to gap-detection):**
- graceful_degrade: C=40%, B=100%, D=100%
- client_error_guide: C=50%, B=30%, D=90%
- observability: C=0%, B=10%, D=40%
- env_driven_config: C=0%, B=10%, D=20%

These items sit at the boundary of engineering and operations. A senior
engineer designing a system would naturally encounter these decisions.
Gap-detection reliably surfaces graceful_degrade (100% in B and D) and
pushes client_error_guide and observability higher.

**Tier 2 — Pure operational (inaccessible to any variant):**
- alerting_policy: 0% across all variants
- load_test_spec: 0% across all variants
- health_check: 0% across all variants
- incident_runbook: 0% across all variants
- race_condition_tests: 0% across all variants

These items require stepping outside the engineering frame entirely into
SRE/DevOps/oncall territory. No variant — not even D with its "design
fully before writing a line of code" opening — reaches them. They are
outside the engineering consideration set regardless of how the satisfaction
condition is framed.

---

## The D Variant — Opening Move Effect

D's P_p added: "You can't help but study and design fully operational
rate limiter systems."

This changed the opening move. Every D run opened with "Let me design
this completely before writing a line of code" or equivalent, followed
by a Phase 1: Requirements Design section that evaluated algorithms,
storage decisions, key strategies, and degraded-mode behavior before
writing any code.

B's opening move: "Let me build this properly — working code first,
then an honest accounting of what's required to run it safely in
production." (B hit max_tokens before reaching the audit section.)

D's design-first framing moved the engineering decisions into an explicit
pre-code audit, which is why D > B on graceful_degrade, client_error_guide,
and observability. But D's design-first framing was still an *engineering*
design phase — it covered algorithm selection and architecture, not
alerting policies or incident procedures.

The word "operational" in D's P_p ("fully operational rate limiter
systems") was parsed as "complete, functioning engineering system" — not
SRE/DevOps operational readiness. The vocabulary didn't install the
operations consideration set.

**D > B on items D surfaces; D = B = 0% on pure operational items.**

The operational trait in D unlocked the engineering-side operational
items (the Tier 1 items). It did not unlock the SRE side.

---

## Key Finding: Gap-Detection Is a Scope Expander, Not a Consideration-Set Installer

Gap-detection expands the machine's scope *within the currently installed
consideration set*. It cannot pull items from a consideration set that the
P_p did not install.

The engineering P_p (A, B, D) installs an engineering consideration set.
Gap-detection (B, D) expands scope within that set to include engineering-
adjacent operational concerns. It cannot reach pure SRE/DevOps concerns
because those are outside the engineering consideration set.

To surface Tier 2 items (alerting, runbooks, load testing, incident
procedures), the P_p would need to install an SRE/DevOps consideration
set — not just a gap-detection condition applied to an engineering P_p.

**Reformulation of the claim:**
Gap-detection expands the machine's scope from "code-complete" to
"engineering-complete." Reaching "operationally-ready" (SRE layer)
requires a different consideration set — a different P_p identity.

---

## The A < C Finding

A = 0.5/10, C = 0.9/10. Domain expertise produced fewer operational items
than the P_d baseline.

Two possible explanations:
1. **Focus effect:** The domain P_p installed a tighter engineering
   termination condition. The generic P_d had slightly more residual noise
   (graceful_degrade 40%, client_error_guide 50%) because it didn't lock
   into engineering mode as tightly.
2. **Different residual items:** A's residual is memory_audit (30%); C's
   residual is client_error_guide (50%). These reflect different training
   priors — the expert's training data includes Redis memory management
   concerns; the generic engineer's includes HTTP response format tutorials.

Either way: expertise without gap-detection doesn't raise the operational
floor. It focuses the machine on the implementation layer.

---

## Connection to exp-27

exp-27 (blockchain) C = 8.6/10 with gap-detection.
exp-28b (rate limiter) D = 2.6/10 with gap-detection.

Why the difference? The checklist items were different:

**exp-27 blockchain checklist:** p2p networking, persistence, chain sync —
these are engineering concerns in the blockchain consideration set. The
gap-detection condition pulled them because they're within the engineering
scope of the problem.

**exp-28b operational checklist:** alerting, runbooks, load testing,
health checks — these are SRE/DevOps concerns outside the engineering
consideration set for a rate limiter implementation.

This explains the divergence: exp-27's C scored high because the missing
items were engineering items. exp-28b's D scored low because the missing
items are operations items. Gap-detection works within the installed
consideration set.

The exp-27 result was not a clean test of the operational horizon — it was
a test of whether gap-detection could surface missing *engineering* items.
That test was passed. exp-28b tests the engineering→operations boundary and
finds it is not crossed by gap-detection alone.

---

## What Would Cross the Operations Horizon

To surface Tier 2 operational items consistently, the experiment likely needs:
1. An SRE or platform engineering P_p — someone whose consideration set
   includes oncall, observability platforms, runbooks, and load testing
2. A gap-detection condition scoped to operational readiness explicitly
   (not just "beyond working code" — that's still an engineering frame)
3. Or: a different measurement approach — perhaps prompting for a
   "production readiness review" rather than an implementation

---

## Design Recommendations for exp-28c

If the goal is to test whether gap-detection crosses the operations horizon:

**Option 1 — SRE P_p:**
"You are a senior SRE who has been on-call for this service. You have
been paged at 3am because this rate limiter was incorrectly blocking
legitimate users. You know what operational readiness requires."

Gap-detection condition: "My review is complete only when I have identified
what is required to run this rate limiter safely in production — beyond
working code — named those operational gaps, and either addressed them or
flagged them."

**Option 2 — Production Readiness Review framing:**
Instead of "build me X," ask: "Review this rate limiter implementation
for production readiness. What is missing?" Supply a complete
implementation as the artifact. Score on the same operational checklist.
This removes the code-generation impulse entirely.

**Option 3 — Accept exp-28b's finding as the result:**
Gap-detection is an engineering scope expander. Accessing the SRE layer
requires a different P_p. This is a finding, not a design failure. Write
it up as a precision statement about where gap-detection operates.
