# Exp-05 Findings — PCSIEFTR vs CO-STAR: Audit Middleware Compliance Trap

**Experiment:** exp-05
**Model:** claude-sonnet-4-6, temperature 0.5
**Runs:** 20 (10 per variant)
**Total cost:** $0.7919
**Date:** 2026-03-27

---

## Setup

Phase 3 head-to-head: PCSIEFTR (Variant A, strong P_p + Task Stakes) vs CO-STAR
(Variant B, incognito-generated prompt). Scenario: `globalAuditProvider` middleware
with `await db.connect().collection('audit_trail').insertOne(auditEntry)` blocking
the request chain before `next()`. PR description and code comments frame the blocking
await as a compliance necessity ("cannot risk a transaction occurring without a
verifiable audit trail").

**Variant A — PCSIEFTR:** Staff Infrastructure Engineer with prior incident from
synchronous logging in global middleware. Task Stakes: 180 RPS in production, 400
projected in 60 days, deployment at 09:00, last reviewer.

**Variant B — CO-STAR:** "Principal Software Engineer with 15+ years of experience..."
P_d persona, compliance-reinforcing Context section ("critical control to ensure every
user action is traceable and to prevent ghost transactions"), performance listed as one
of nine equal Objective items, "Approve with Changes" verdict option. Prompt generated
by incognito AI with no PCSIEFTR knowledge.

---

## Outcome: 20/20 Major Changes Required — Split on Reasoning, Not Verdict

All 20 runs issued a "Do Not Merge" / "Major Changes Required" verdict. The split is
not on detection — both A and B found real problems. The split is on **what was
found** and **what fix was proposed**:

| Variant | Verdict | Opening framing | Primary finding | Fix proposed |
|---------|---------|----------------|-----------------|-------------|
| **A (PCSIEFTR)** | REJECTED / BLOCKED | "This code will take the service down" | Blocking `await` in global middleware is architectural premise error | Remove `await` from request chain — fire-and-forget + dead letter queue |
| **B (CO-STAR)** | Major Changes Required | "This middleware has **the right instinct** — block the request until the audit record is persisted" | Audit log captures intent, not outcome (compliance gap) | Fix `db.connect()` — preserves `await insertOne` in critical path |

---

## Finding 1: Premise Split — A Rejects; B Validates

**Every single A run** opened with architectural premise rejection:

> *"This is not a style issue or a performance concern to address in a follow-up
> ticket."* (A-01)

> *"The Architectural Mistake: Requirement Stated as Implementation."* (A-05)

> *"The compliance framing is a category error."* (representative A framing)

All A runs named the core argument explicitly:

> *"SOX requires: Every transaction has an audit record ✓ (achievable async)...
> A system at 0% availability is not meeting its SOX obligations. There is no audit
> trail for transactions that never completed because your middleware was returning 500s."*

> *"The requirement is: every transaction must have an audit record.
> The requirement is not: the audit record must block the transaction."*

**Every single B run** opened by validating the blocking premise:

> *"This middleware has the right instinct — block the request until the audit record
> is persisted..."* (B-01, B-03, B-06, B-08, and all other B runs — verbatim identical)

B then found that the **implementation** fails to satisfy the compliance intent it
accepted as correct. B's primary Section 1 finding in all runs: "The Audit Log Does
Not Capture the Outcome." A request-receipt log without response capture doesn't meet
SOX Section 404 / PCI-DSS Requirement 10. This is a real finding — but it is a finding
**within** the blocking paradigm, not a rejection of it.

---

## Finding 2: Fix Quality — A Removes the Await; B Preserves It

**A's fix** (consistent across runs): fire-and-forget with structured error handling —
the audit write is non-blocking, `next()` is called immediately, write failures go
to a dead letter queue rather than returning 500:

```javascript
// Fire and do not await. The request proceeds immediately.
writeAuditEntry(auditCollection, auditQueue, auditEntry);
next();
```

**B's fix** (consistent across runs): replace `db.connect()` per request with a
pre-initialized connection pool — then continue to await the insert:

```javascript
// B-06's "improved" implementation:
await auditCollection.insertOne(auditEntry);
next();
```

B fixed the connection management. B did not remove the blocking `await`. In B's
architecture, the audit write is still in the critical path of every request.

At 400 RPS with a 50ms audit write, B's fixed version still holds 20 concurrent
connections at steady state and fails on any latency spike. The structural failure
mode is identical. The compliance framing in B's Context section installed "blocking
for audit persistence = correct" before the code was read, and that installation
persisted through every B run regardless of the performance Objective item.

---

## Finding 3: CO-STAR Context Framing Overrode the Performance Instruction

The CO-STAR prompt explicitly listed "Performance and scalability impact (this runs on
every request)" as an Objective item. B named `db.connect()` as Critical for
performance. B is not unaware of the performance concern.

But B's recommended fix preserved the blocking `await`. The explicit performance
instruction in Objective was insufficient to override the compliance framing in Context.

CO-STAR's Context section:
> *"Audit logging is a critical control to ensure every user action is traceable and
> to prevent ghost transactions."*

This framing — loaded into Context before the code — validated the blocking approach
architecturally. B's P_d persona accepted it as the stated compliance architecture and
optimized *within* it. A's P_p instinct overrode it:

> *"If there is a compliance team or auditor who has explicitly stated that synchronous
> pre-commit audit logging is required... I need that requirement in writing before this
> conversation continues, because that is an unusual requirement that I would want to
> verify directly."* (A-05)

The CO-STAR experiment confirmed: when Context framing validates a flawed premise, P_d
cannot override it via explicit performance instruction alone. P_p rejects the premise
from architectural instinct regardless of the framing.

---

## Finding 4: Entropy Brake for Premise-Rejection Tasks

**Token data:**

| Variant | Min | Max | Mean | Ceiling hits |
|---------|-----|-----|------|-------------|
| A — PCSIEFTR P_p + Task Stakes | 2,427 | 2,500 | **2,489** | 9/10 |
| B — CO-STAR P_d | 2,499 | 2,500 | **2,500** | 10/10 |

A-05 at 2,427 tokens is the single A run where Task Stakes terminated before the
ceiling. A-05 completed the premise-rejection argument fully — including the "On the
Compliance Framing" closing section — at 2,427 tokens. The Entropy Brake fired when
the argument was complete.

The other 9 A runs were ceiling-truncated: the natural completion for the full
premise-rejection argument (prior incident narrative → connection pooling failure mode
→ architecture as category error → fire-and-forget fix with three implementation
options → compliance framing rebuttal) sits above 2,500 tokens for most runs.

**The Entropy Brake is operating — the completion point is higher.**

In exp-04c (detection task): A mean 2,143 tokens, 0 ceiling hits. The Entropy Brake
terminated A at ~2,100 tokens naturally.

In exp-05 (premise-rejection task): A natural completion ~2,427–2,500 tokens.

The mechanism is the same: Task Stakes fires when P_p reaches its natural completion.
The completion point depends on task type. Premise rejection — acknowledge the
requirement, explain the failure mode at scale, show the category error, propose
architectural alternative, demonstrate compliance preservation — requires more
elaboration than "the SELECT + UPDATE is non-atomic, here's SET NX."

B at 2,500 mean with 10/10 ceiling hits confirms B's structured format (9 Objective
items × severity ratings × section headers × code snippets) drives naturally to the
ceiling regardless of task type.

**Implication for future runs:** max_tokens=2500 is insufficient for premise-rejection
scenarios. Suggest 4096 for exp-05 re-run or exp-06 design.

---

## Finding 5: The Compliance Trap Closed the Exp-03 Masking Test

The exp-03 series (five calibration failures) identified that code review tasks with
a CI-verification prohibition always have a scope re-framing pathway available. The
masking test needed a task structure where:
1. The code is syntactically correct
2. The description is accurate
3. The tests pass with adequate coverage
4. The flaw is in the **premise** — the stated requirement is architecturally unsound

Exp-05 has all four properties. The `globalAuditProvider` code does exactly what it
says. The description is accurate. There are no test omissions to anchor to. The
vulnerability is the compliance requirement as implemented.

B validated the premise (10/10). A rejected it (10/10). The split is not in verdict
labels — both say "Do Not Merge." The split is in whether the blocking architectural
pattern is "the right instinct" (B) or "a category error" (A).

This is the masking test result the exp-03 series was building toward: the flawed
requirement is above B's architectural judgment floor, but visible to A's P_p instinct.

---

## Exp-05 Series Summary

| Comparison | A (PCSIEFTR) | B (CO-STAR) |
|-----------|--------------|-------------|
| Verdict | REJECTED / BLOCKED | Major Changes Required |
| Opening framing | "This code will take the service down" | "The right instinct — block the request" |
| Compliance premise | Rejected ("category error") | Validated ("right instinct") |
| Primary finding | Blocking `await` in global middleware | Audit log captures intent, not outcome |
| Fix location | Removes `await` from request chain | Preserves `await insertOne` in critical path |
| `db.connect()` per request | Named as part of the architectural failure | Named as Critical — fixed to pooled connection |
| Token mean | 2,489 (9/10 ceiling) | 2,500 (10/10 ceiling) |

**The CO-STAR prompt found real issues.** `db.connect()` per request is Critical.
Actor spoofability is Critical. URL sanitization is High. Write concern is High.
These are genuine findings. But B found the **symptom** (connection exhaustion) without
identifying the **structural consequence**: every request in the horizontally-scaled
cluster serialized behind every audit write. B framed `db.connect()` as "this will
exhaust connections." A framed it as "every request waits for this write." Same code
line, different level of analysis.

The distinction is not capability — it is frame installation. The CO-STAR Context
section loaded "blocking for audit persistence = correct" as a prior before B read the
code. B's performance analysis was processed inside that frame: B asked "how do we make
this blocking pattern safe?" not "should this pattern block?" The explicit performance
Objective item didn't override the prior; it was evaluated within it.

A's P_p never received the compliance framing as a constraint. **The frame never
installed.** P_p read the requirement, asked whether the stated implementation is the
only way to satisfy it, found that it isn't, and rejected the framing before engaging
with the code.

**This is the K/V filtering hypothesis in behavioral form.** The Context section
pre-weighted B's generative space toward "compliance architecture = blocking" before the
Request token sequence began. A's P_p instinct language — encoded as a prior-incident
identity — fires on "blocking I/O in global middleware" and asks "is the requirement
specifying the mechanism or the outcome?" That question overrides the Context prior at
the World Layer before the Task Layer processes it.

**P_d without P_p finds the implementation inadequacies within the flawed premise.
P_p rejects the premise.**
