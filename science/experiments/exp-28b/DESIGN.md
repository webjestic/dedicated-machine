# Exp-28b Design — Operational Horizon / Gap Detection (Rate Limiter)

**Status:** Calibration complete — running full experiment
**Phase:** 7 — The Dedicated Machine Hypothesis
**Date:** 2026-03-30
**Predecessor:** exp-27 (blockchain — calibration failure, artifact too canonically trained)
**Second calibration:** exp-28b v1 (rate limiter, implementation checklist — same failure)

---

## Context: Why the First Two Artifacts Failed

exp-27 used "Build me a blockchain implementation in Node.js."
exp-28b v1 used "Build me a rate limiter in Node.js" with an implementation checklist.

Both failed calibration at A/C baseline ≈ 6.2/10. Root cause:

"Build me [infrastructure component] in Node.js" triggers an RLHF-installed
comprehensive-demo posture in all variants, regardless of Persona. The model's
satisfaction condition for this task type is "produce something that looks like
a solid engineering example." Items like Redis backends, sliding windows, and
per-key limiting appear at 100% in the P_d baseline because RLHF has defined
a "good rate limiter" as one that includes these things — not because the machine
reasoned about production requirements.

The shallow path for infrastructure generation does not exist at the code layer.
The RLHF floor IS a comprehensive code implementation.

**The finding that unblocked the design:**
In both failed experiments, the items that floored at 0% in the baseline were
*operational* items: observability, alerting, runbooks, load testing, memory
audits, race condition tests. The horizon is not between minimal code and complete
code. It is between code-complete and operationally-ready.

---

## The Revised Hypothesis

**Claim 1 (revised):** The machine's path of least resistance terminates at
code-complete. Even a thorough, production-quality implementation is operationally
incomplete: it does not address observability, alerting, graceful degradation
policy, incident procedures, or operational validation. Horizon blindness operates
at the code/operations boundary, not the minimal/complete boundary.

**Claim 2 (unchanged):** A P_p with a mission-scoped gap-detection satisfaction
condition — explicitly scoped to "beyond working code" — surfaces the operational
layer that code-complete output leaves behind.

---

## Artifact

**Prompt:** "Build me a rate limiter in Node.js."

This prompt reliably produces code-complete implementations across all variants
(Redis backend, sliding window, per-key limiting, burst handling, TTL, rate limit
headers). The implementation horizon is fully saturated by the RLHF baseline.

The operational horizon is not: observability, alerting, graceful degradation
policy, load test specifications, health check endpoints, incident runbooks,
memory auditing, and distributed race condition tests do not appear in any
baseline run.

---

## Variants

### Variant C — P_d Baseline (Calibration Anchor)

```
You are a software engineer.

Build me a rate limiter in Node.js.
```

**Calibration result:** mean=0.9/10, range 0–2. ✓

### Variant A — P_p, Task-Scoped

```
You are a senior backend engineer with deep experience building production
API infrastructure, rate limiting systems, and distributed systems at scale.
You have shipped rate limiters that handle millions of requests per day.

Build me a rate limiter in Node.js.
```

Domain expertise without a gap-detection condition. Tests Claim 1: does
expertise alone cross the operational horizon, or does the machine still
stop at code-complete despite knowing what production requires?

**Calibration target:** A mean ≤ 4/10 on the operational checklist.

### Variant B — P_p + Operational Gap-Detection Satisfaction Condition

```
You are a senior backend engineer with deep experience building production
API infrastructure, rate limiting systems, and distributed systems at scale.
You have shipped rate limiters that handle millions of requests per day.

My implementation is complete only when I have identified what is required
to run this rate limiter safely in production — beyond working code — named
those operational gaps explicitly, and either addressed them or flagged them
for the requester.

Build me a rate limiter in Node.js.
```

Same P_p as A. The "beyond working code" anchor prevents B from satisfying
the condition by auditing implementation gaps that C already covers. Completion
requires operational scope.

---

## Scoring — Operational Checklist Only

**Metric:** Continuous. Score = number of operational production requirements
surfaced per run (0–10).

**10-item operational checklist:**

| # | Item | Description |
|---|------|-------------|
| 1 | observability | Prometheus/StatsD/metrics instrumentation — how do you know it's working? |
| 2 | alerting_policy | Specific conditions for on-call paging (error rate, rejection rate thresholds) |
| 3 | graceful_degrade | Explicit fail-open/fail-closed policy and logic when Redis/backend is unavailable |
| 4 | client_error_guide | RFC 6585 headers + 429 response body format for SDK/client handling |
| 5 | load_test_spec | Instructions or spec for verifying the limiter handles target throughput |
| 6 | env_driven_config | Per-route limits tunable via environment variables without code deploys |
| 7 | health_check | Endpoint exposing limiter status, current counters, Redis health |
| 8 | incident_runbook | Procedures for debugging false positives or unexpectedly blocked users |
| 9 | memory_audit | How to detect/prevent memory leaks from unbounded keys |
| 10 | race_condition_tests | Specific test strategy for distributed lock contention and window boundary races |

**Scoring rule:** Score 1 if explicitly named, implemented, or flagged as a
production requirement with substance. Score 0 if absent or mentioned in
passing without actionable content.

---

## Predictions

| Variant | Predicted mean | Reasoning |
|---------|---------------|-----------|
| C | 0–2/10 | RLHF floor at implementation layer; operational items outside "good code" template. **Confirmed: 0.9/10.** |
| A | 1–4/10 | Domain expertise may prime some operational items; task-scope criterion doesn't require them |
| B | 5–8/10 | "Beyond working code" condition makes operational scope load-bearing; machine audits operational layer before closing |

**Falsifiable outcomes:**

| Pattern | Interpretation |
|---------|----------------|
| C ≤ 2, A modest, B >> A | Claim 1 and 2 confirmed at operational horizon |
| C ≤ 2, A ≈ B | Domain expertise sufficient; gap-detection adds nothing marginal |
| C ≤ 2, B ≈ C | "Beyond working code" condition not strong enough |
| A or B >> 2 before gap-detection | RLHF prior extends into operational items with domain priming |

---

## Key Design Decisions

**Why "beyond working code" in B's satisfaction condition:**
The previous B condition was general ("what a production deployment requires
that the stated requirements do not mention"). This would be satisfied by
auditing implementation items C already covers (Redis, sliding window, etc.).
"Beyond working code" anchors the completion criterion at the operational layer,
preventing satisfaction at the implementation horizon.

**Why A and B share the same P_p:**
Isolates gap-detection as the operative variable. Any A vs. B difference is
attributable to the satisfaction condition alone, not Persona strength.

**Why C is the calibration anchor (not A):**
The implementation checklist showed A and C producing comparable scores (both
at the RLHF implementation floor). With the operational checklist, C is the
correct floor anchor — A may produce modest lift from domain priming.

**Why the implementation items were dropped:**
They all ceiling in C. A checklist that ceilings at baseline provides no
gradient and cannot measure the gap-detection effect.

---

## Connection to Prior Work

**exp-27 + exp-28b v1:** Established that RLHF floor for infrastructure
generation is at implementation-complete, not minimal-code. Operational items
are outside the canonical pattern. The horizon is real but different from
what was assumed.

**Phase 6 (exp-19–24):** Mechanism vocabulary drives ceiling detection.
exp-28b tests whether scope of the satisfaction condition (not vocabulary)
drives the operational horizon crossing. The rate limiter prompt has no
"operational vocabulary" in A or C — gap-detection must expand scope from
inside the Persona.

**dedicated-machine_v2.md:** Horizon Blindness section. "The machine delivers
exactly what you defined." The revised claim: the machine delivers exactly
what "good code" looks like — but running code in production requires more
than good code.
