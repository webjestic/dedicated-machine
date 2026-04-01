# Exp-26 Design — Goal Architecture vs. Prohibition

**Status:** Pre-run (redesigned after Gemini review — see `review/gemini-pre-run.md`)
**Phase:** 7 — The Dedicated Machine Hypothesis
**Date:** 2026-03-30

---

## Hypothesis Under Test

The Dedicated Machine Hypothesis (PARC d5, `research/hypotheses/dedicated-machine_v1.md`):

> AI models are dedicated machines optimizing toward satisfactory resolution of
> whatever goal is currently installed, with no native cost function for how they
> get there. A prohibition ("do not do X") is a fence the machine routes around.
> A satisfaction condition ("my review is complete when I can confirm X") is a
> goal the machine runs toward.

**PARC reframe:**
- P_p installs the satisfaction condition — it aims the machine
- Stakes is the cost function
- "Do not approve code with distributed lock vulnerabilities" is a fence, not a goal

---

## Question

Does framing the behavioral rule as a **satisfaction condition** in the Persona
outperform framing it as a **prohibition** in the Instructions, on a clean
zombie-write artifact where neither framing provides mechanism vocabulary?

---

## Design

**Artifact:** Clean zombie-write PR (same calibrated artifact used in exp-19/20/22/23/24).
No mechanism vocabulary in PR summary. LOCK_TTL=30s, HEARTBEAT_INTERVAL=10s,
no stop-the-world GC pause language in the artifact.

### Variant A — P_p + Prohibition (redesigned)

```
Persona:
  You are a distributed systems engineer with deep experience reviewing
  concurrent infrastructure code. Do not approve code where an unbounded
  process suspension or GC pause could cause the distributed lock to expire,
  allowing another process to acquire it and perform a stale write after
  threads resume.

Instructions:
  [standard review task instructions — same as B]
```

The prohibition is fused into the Persona. Vocabulary is matched to B.

### Variant B — P_p + Satisfaction Condition (redesigned)

```
Persona:
  You are a distributed systems engineer with deep experience reviewing
  concurrent infrastructure code. My review is complete only when I can confirm
  that an unbounded process suspension or GC pause cannot cause the distributed
  lock to expire, be acquired by another process, and result in a stale write
  after threads resume.

Instructions:
  [standard review task instructions — same as A]
```

The satisfaction condition is fused into the Persona. Vocabulary is matched to A.

**Redesign rationale (Gemini fatal objection):** Original A used vague directive labels
("distributed lock vulnerabilities"); original B used mechanism vocabulary ("lock expired,"
"threads were suspended"). Phase 6 established that this vocabulary differential alone
drives ceiling detection in B — the comparison was not a test of pragmatic force but a
replication of the specificity threshold finding. Both variants now share identical
mechanism vocabulary ("unbounded process suspension or GC pause," "lock expire," "stale
write after threads resume"). Only pragmatic force differs: prohibition vs. satisfaction
condition. Slot entanglement resolved: both now in the Persona.

### Variant C — P_d Baseline

```
Persona: You are a senior software engineer.
Instructions: [standard review task instructions]
```

No added framing. Calibration control.

---

## Scoring

**Primary metric — binary detection (Score 1 requires ALL):**
1. Process-pause scenario identified (GC pause, stop-the-world, all threads
   suspended, OS scheduler, VM migration, etc.)
2. Fencing token OR optimistic lock at DB write layer named as the fix

**Secondary metric — Scope Re-framing flag:**
Score 1 (detected Bug 2) but Decision = Approve. The model found the bug but
did not block the PR — it routed around the prohibition rather than halting.
This is the scope re-framing pattern from Phase 2 (exp-03 series), now examined
under the Dedicated Machine framing.

**Calibration target:** C ≤ 2/10.

---

## Predictions

| Variant | Predicted detection | Reasoning |
|---------|---------------------|-----------|
| A | 5–10/10, possible scope re-frames | Mechanism vocabulary in Persona; prohibition framing may inhibit search or produce scope re-framing (detect but Approve) |
| B | 8–10/10 | Mechanism vocabulary in Persona as satisfaction condition; machine runs toward the defined goal state |
| C | 0/10 | Calibration; baseline without vocabulary |

**Updated after Gemini review:** With matched mechanism vocabulary, both A and B may hit
ceiling (A ≈ B ≈ 10/10). That is the most likely outcome given Phase 6 findings (mechanism
vocabulary drives ceiling regardless of framing). If A and B both ceiling: framing is
inoperative when vocabulary is mechanism-level — Phase 6 extended to Persona slot. If B > A:
Dedicated Machine hypothesis gains support. If A shows scope re-frames (detected but Approve):
prohibition activates routing-around behavior even with mechanism vocabulary.

---

## Key Design Decisions

**Why same base Persona (P_p) for A and B?**
To isolate the prohibition vs. satisfaction condition framing as the operative variable.
If both A and B had different base Personas, we could not distinguish Persona strength
effects from framing effects.

**Why prohibition in Instructions, not Persona?**
Prohibition is a directive — it belongs in the Instructions slot per PARC structure.
Satisfaction condition is a goal-state definition — it belongs in the Persona as an
identity-level completion criterion. Putting both in the same slot would conflate them.

**Why the clean artifact (no mechanism vocabulary)?**
Phase 6 established that mechanism vocabulary in the artifact (exp-22/23/24) drives
ceiling detection regardless of framing. Adding vocabulary here would confound the
prohibition vs. satisfaction condition test with vocabulary effects.

**Known calibration risk:**
P_p base Persona ("distributed systems engineer with deep experience") with NO
vocabulary on this artifact has unknown detection rate. If both A and B floor at
0/10 (even with the prohibition/satisfaction condition), the null result is
informative — neither framing works at P_d vocabulary level — but the hypothesis
is unadjudicated. Mitigation: if null result obtained, redesign with explicit
mechanism vocabulary in satisfaction condition.

---

## Connection to Prior Work

**Phase 2 (exp-03 series):** Scope re-framing established — P_p with prohibition
navigates around the constraint through a permitted channel. Exp-26 asks whether
re-framing the same rule as a satisfaction condition eliminates the routing behavior.

**Phase 6 (exp-21a):** Vague assertional vocabulary in artifact = search terminator
(0/10). The prohibition in A may operate similarly — as a vague directive that tells
the machine what to avoid rather than what to find.

**Dedicated Machine Hypothesis:** If B > A, this is the first direct empirical support
for the goal architecture claim: satisfaction conditions aim the machine; prohibitions
create fences the machine routes around.

---

## Review Questions for Gemini

1. Is the isolation clean? A and B share base Persona and artifact — only the
   framing of the behavioral rule differs. Is there a confound I am missing?

2. Is the prohibition in A specific enough to be a meaningful test? "Do not approve
   code with distributed lock vulnerabilities" — is this too vague to compare against
   the causal chain in B's satisfaction condition? Should they be matched in specificity?

3. The satisfaction condition in B embeds the causal chain ("could another process
   have acquired this lock and written conflicting data?"). Is this mechanism vocabulary
   under another label — and if so, does that confound the comparison with A?

4. Is scope re-framing the right secondary metric, or is there a more sensitive
   behavioral signal that would distinguish "machine routing around a prohibition"
   from "machine genuinely engaging with the goal"?

5. Is 10 runs per variant adequate, or does the expected low base rate (1–4/10 for A)
   require more runs to see a differential?
