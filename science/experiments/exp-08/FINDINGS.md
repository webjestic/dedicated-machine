# exp-08 FINDINGS

**Experiment:** Examples-slot installer — mechanism demonstrations as P_p substitute
**Date:** 2026-03-28
**Model:** claude-sonnet-4-6, temperature 0.5, max_tokens 2500
**Runs:** 40 (n=10 per variant)
**Total cost:** $1.6563

---

## Results Summary

| Variant | Persona | Examples | Ceiling hits | Mean tokens | Tier 1.0 | Tier 0.5 |
|---------|---------|----------|-------------|-------------|----------|----------|
| I | P_p — distributed systems engineer | None | 6/10 | 2,499 | 0/10 | 10/10 |
| J | P_d — senior software engineer | None | 0/10 | 2,071 | 0/10 | 10/10 |
| C | P_d — senior software engineer | Mechanism demos | 0/10 | 1,788 | 0/10 | 10/10 |
| E | P_p — distributed systems engineer | Mechanism demos | 2/10 | 2,267 | 3/10 | 10/10 |

**Primary binary question result: C ~ J ≠ I**

**Secondary question result: E > I at Tier 1.0 (3/10 vs. 0/10)**

---

## Artifact Calibration Failure

All 40 runs found the zombie-write mechanism (Tier ≥ 0.5). The floor-at-ceiling problem.

The cause: the PR checklist item — *"Atomic lock extension via Lua script — heartbeat detects
token mismatch (result == 0)"* — pointed directly at the failure path. Any reviewer reading
"detects token mismatch" would immediately ask "detects it, and then what?" The artifact
announced the mechanism. The `if result == 0: return` line was already in the PR description's
frame before the code was read.

This is a calibration failure in the same family as exp-07c's logger.warning: a signal in
the artifact that lowers the finding to below the consideration-set threshold for all variants.

What we can still extract: differentiation at Tier 1.0 (GC-pause + fencing token), which
the artifact does not hint at, and token distribution patterns.

---

## What Each Variant Found

### I (P_p, no Examples) — 10/10 zombie-write, 0/10 Tier 1.0

All 10 runs: `result == 0` in `_beat()` exits silently; main thread continues executing
the DB transaction; lock may have been taken by another process; result is concurrent write.

Proposed fix (all 10): shared threading.Event or lock_lost flag signaling from heartbeat to
main thread. One run (I-05) mentioned GC pause in the context of heartbeat timing math
("heartbeat fires late under GC pause, effective lock window shrinks") — not as the
zombie-write trigger. One run (I-08) mentioned GC pause in the context of TTL sizing.
Neither recommendation named fencing token.

Secondary findings (most runs): get_stock() outside DB transaction as TOCTOU; heartbeat
interval comment mismatch (8 ≠ 30/3); join timeout not checked.

Consistent with exp-07d I results: same artifact, same finding tier, same ceiling behavior.

### J (P_d, no Examples) — 10/10 zombie-write, 0/10 Tier 1.0

All 10 runs found the heartbeat-silence mechanism. Similar structural identification to I
but with less mechanistic depth in the framing. No ceiling hits; consistent termination
at moderate depth.

This is different from the exp-07d J result (which scored 8/10 on the mechanism). The
artifact's PR checklist makes the gap visible enough for P_d to close on it reliably.

No fencing token recommendation. No explicit GC-pause-as-trigger analysis.

### C (P_d + mechanism Examples) — 10/10 zombie-write, 0/10 Tier 1.0

The primary test variant. All 10 runs found the zombie-write at the same tier as J.
The mechanism demonstrations in the Examples slot — which showed the structural review
question ("does the protected code know when coordination is lost?") without naming the
failure path — did not elevate C above J on any measurable dimension.

Token distribution confirms: C (mean 1,788) < J (mean 2,071). Adding mechanism
demonstrations to P_d *reduced* elaboration depth relative to the P_d baseline.

**C ~ J on all dimensions.** The Examples slot did not install P_p consideration-set behavior.

### E (P_p + mechanism Examples) — 10/10 zombie-write, 3/10 Tier 1.0

The saturation test variant. 3 runs (E-03, E-06, E-07) reached Tier 1.0:

- **E-03:** "A fencing token passed into the DB transaction is the stronger solution if the
  DB layer supports it." Named the architectural fix explicitly.

- **E-06:** Walked the GC-pause scenario as the exact mechanism — process paused, lock
  expires, second process acquires, heartbeat fires at t=38s on a 30s TTL. Named fencing
  token as the architectural fix.

- **E-07:** "Redis latency spikes and GC pauses make mid-operation lock expiry a routine
  operational event" — correctly framed GC-pause not as an edge case but as the design
  condition. Named compare-and-swap as the DB-layer solution.

The 3/10 Tier 1.0 rate for E versus 0/10 for I (from exp-07d and exp-08 both) represents
a genuine additive gain. P_p + mechanism Examples extended the architectural ceiling that
P_p alone did not reach.

E also had fewer ceiling hits (2/10) and lower mean tokens (2,267) than I (6/10, 2,499),
consistent with Examples functioning as a termination anchor — the model stops when it
has produced something matching the demonstrated pattern rather than elaborating to ceiling.

---

## Binary Question Answer

**Primary (C~I or C~J?): C ~ J.** The mechanism demonstrations in the Examples slot did
not install P_p consideration-set behavior into a P_d Persona.

| Dimension | I | C | J |
|-----------|---|---|---|
| Zombie-write detected | 10/10 | 10/10 | 10/10 |
| Tier 1.0 (GC-pause + fencing token) | 0/10 | 0/10 | 0/10 |
| Mean tokens | 2,499 | 1,788 | 2,071 |
| Ceiling hits | 6/10 | 0/10 | 0/10 |

C falls below J on tokens and ceiling hits — further from I, not closer.

Interpretation from SCORING.md outcome table: **"Persona slot load-bearing; Examples
add to P_p but can't substitute."**

**Secondary (E > I or E ≈ I?): E > I on Tier 1.0 (3/10 vs. 0/10).** Examples produced
additive gain when paired with P_p. Not saturation — the ceiling moved.

| Dimension | E | I |
|-----------|---|---|
| Tier 1.0 (GC-pause + fencing token) | 3/10 | 0/10 |
| Tier 0.5 (heartbeat signaling fix) | 10/10 | 10/10 |
| Mean tokens | 2,267 | 2,499 |
| Ceiling hits | 2/10 | 6/10 |

---

## New Behavioral Observation: Examples as Termination Anchor

Token distribution across all four variants:

| Variant | Mean tokens | Ceiling hits | Delta from no-examples baseline |
|---------|------------|--------------|----------------------------------|
| I (P_p alone) | 2,499 | 6/10 | — |
| E (P_p + Examples) | 2,267 | 2/10 | −232 tokens |
| J (P_d alone) | 2,071 | 0/10 | — |
| C (P_d + Examples) | 1,788 | 0/10 | −283 tokens |

Adding Examples to either Persona type reduced output length. For I→E: −232 tokens,
−4 ceiling hits. For J→C: −283 tokens, 0 ceiling hits change (already zero).

The mechanism: the mechanism demonstrations in Examples provide a behavioral template —
a model of what a complete review looks like — that anchors termination. The model
produces output matching the demonstrated pattern and stops, rather than elaborating
to the ceiling. Examples install a "done" signal, not a "search harder" signal.

This is consistent with the two-layer model. Examples are a Task Layer component.
They install output shape and termination behavior, not consideration-set membership.

---

## Variant K — AXIOMS + P_d (post-hoc addition, 10 runs)

Variant K was added after the primary runs to test the AXIOMS slot (Layer 0 formula
pre-installation) as a P_p behavior installer. K is identical to J except for a
`## AXIOMS` section placed before the Persona containing the full PCSIEFTR formula
with behavioral annotations — the same content as v9-paper-thriller.md.

The AXIOMS content explicitly states that P_d "produces elaboration without convergence"
and that P_p encodes procedure as "after X, I ask Y." The Persona that follows is still
"senior software engineer."

**Results:**

| Dimension | K (AXIOMS + P_d) | J (P_d) | I (P_p) |
|-----------|-----------------|---------|---------|
| Zombie-write | 10/10 | 10/10 | 10/10 |
| Tier 1.0 | 0/10 | 0/10 | 0/10 |
| Mean tokens | 1,977 | 2,071 | 2,499 |
| Ceiling hits | 1/10 | 0/10 | 6/10 |

**K ≈ J.** The AXIOMS slot did not install P_p consideration-set behavior. The model
read that P_d produces elaboration without convergence, then reviewed the PR as a
senior software engineer anyway.

**Critical observation: AXIOMS is task-domain-sensitive.**

The AXIOMS slot produces measurable improvement in v9-paper-thriller — the textbook
writer output is cleaner, shorter-paragraph, numbers-first. But v9's task IS writing
about PARC. The formula content is directly load-bearing on the output because the
output is about the formula.

In the code review task, the formula describes the meta-level of how prompts work.
It is not about the code being reviewed. The model can read and understand the formula
and still approach the PR from its Persona identity, because there is no task-level
hook forcing the formula into the execution path.

AXIOMS installs the framework when the task is about the framework. It does not
translate framework knowledge into behavior when the task is something else. This is
a meaningful constraint on where the slot is useful — and an important distinction
from the Persona slot, which installs behavior regardless of whether the task is
about the behavior.

**Complete slot comparison across exp-07/08:**

| Experiment | Slot | Content type | Result vs. J |
|-----------|------|--------------|-------------|
| exp-07c | Instructions | P_p domain knowledge | ≈ I (matched P_p) |
| exp-07d | Instructions | P_p domain knowledge | ≈ I (matched P_p) |
| exp-08 | Examples | Mechanism demonstrations | ~ J (no lift) |
| exp-08 (K) | AXIOMS (Layer 0) | Descriptive formula + annotations | ~ J (no lift) |
| exp-08 (L) | AXIOMS (Layer 0) | Procedural bootstrap instruction | > K, ~ J |

Four slots tested. One works at full depth (Instructions with domain knowledge). One
partially works (procedural AXIOMS bootstraps execution and lifts tokens). Two are
inert (Examples; descriptive AXIOMS). The Instructions-slot finding remains the
dominant challenge to the Persona-as-primary-installer claim.

---

## Variant L — Procedural AXIOMS + P_d (post-hoc addition, 10 runs)

Variant L was added to test whether AXIOMS written as a procedural instruction —
rather than a descriptive formula — could bootstrap P_p behavior from a P_d Persona.

K established that *describing* P_p ("P_d produces elaboration without convergence")
is inert: the model reads the description and reviews as P_d anyway. The hypothesis
for L: if AXIOMS encodes an *execution procedure* ("before reading further, execute
this: read your Persona, determine if it's a label, if so construct the search
question"), the model might actually construct and carry a P_p-equivalent before
the Persona slot takes effect.

**The AXIOMS content in L:**
A four-step bootstrap procedure instructing the model to:
1. Determine whether its Persona is a label or a procedure
2. If a label: identify the critical failure mode class for the domain
3. Construct a search question in "after I verify X, I ask Y" form
4. Carry that question into the task as part of its identity

**Results:**

| Dimension | L (Procedural AXIOMS + P_d) | K (Descriptive AXIOMS + P_d) | J (P_d) | E (P_p + Examples) |
|-----------|---------------------------|------------------------------|---------|-------------------|
| Procedure executed | **10/10** | — | — | — |
| Tier 1.0 | 0/10 | 0/10 | 0/10 | 3/10 |
| Tier 0.5 | 10/10 | 10/10 | 10/10 | 10/10 |
| Mean tokens | 2,112 | 1,977 | 2,071 | 2,267 |
| Ceiling hits | 0/10 | 1/10 | 0/10 | 2/10 |

**The procedure ran. All 10 times.**

L-02 is the clearest example. The model explicitly identified its Persona as a label,
named "state divergence across time" as the critical failure mode class for distributed
reservation systems, and constructed the search question: *"After I verify that the
lock is held and stock is sufficient, I ask: what temporal or state scenario could
silently invalidate that correctness — between the read and the write, between the
heartbeat and the release, between the thread start and the finally block — while
the code appears to hold?"* It then wrote: "This question is now active. Proceeding
to review."

That is not acknowledgment of the procedure. That is execution.

**But the constructed question operated at depth-1.**

The bootstrapped search question — "what temporal scenario could invalidate
correctness?" — is a genuine P_p-shaped question. It found the zombie-write on
all 10 runs. But it didn't continue to the second-order question that distinguishes
Tier 0.5 from Tier 1.0: *"does the proposed fix — threading.Event signaling — survive
a process-level pause?"*

E (P_p + Examples) reached Tier 1.0 at 3/10 because P_p identity encoding installs
a search algorithm that recursively applies to its own proposed fixes. L's bootstrap
constructs a depth-1 question ("what could go wrong?"). P_p + Examples encodes a
depth-2 question ("what could go wrong with the fix for what could go wrong?").

**The distinction now has a name: search depth.**

Procedural AXIOMS bootstraps a search algorithm. The bootstrap runs. The algorithm
operates. But the algorithm it constructs is shallow — one level deep — because it's
assembled from scratch at read time from general principles. P_p encodes a
domain-specific, depth-calibrated search algorithm that comes from identity framing.
The depth requires either P_p identity encoding or mechanism examples that extend
the search after the first finding (as in E).

**L > K** — procedural vs. descriptive AXIOMS is a real distinction. K is a glossary.
L is an instruction that executes. Tokens confirm: L (2,112) > K (1,977), consistent
with L running a search procedure rather than just reading metadata.

**L ~ J on tier** — the search procedure L constructed reached the same level as J's
native P_d reasoning. The bootstrap produced P_d-equivalent depth, not P_p depth.

**L-07 note:** L-07's GC pause mention is about TTL drift when heartbeat fires late
(EXPIRE vs EXPIREAT timing accuracy), not the zombie-write trigger. Same false-positive
pattern as I-05 and I-08. Genuine Tier 1.0 for L: 0/10.

---

## What This Means for exp-09

The few-shot confound question requires a cleaner test:

**What we still need to test:**
A failure mode that is architecturally hidden — no code-level hint, not named in the PR
description or checklist — where the discovery requires simulating system state across
time. P_p explicitly encodes the simulation step ("after I find a lock-loss signaling gap,
I ask whether the proposed fix survives a process-level pause, not just a thread-level
signal"). C uses the same procedural content verbatim but in the Examples slot (or
Instructions slot) instead of the Persona slot.

**Artifact requirements for exp-09:**
1. PR description covers the happy path, says nothing about the failure mode
2. The failure mode is not mentioned in any checklist item
3. The code does not contain a visible `if result == 0` branch pointing at the gap
4. Finding requires simulating time — asking "what happens if the process is paused here?"
5. The failure lives in the gap between lock acquisition and operation completion,
   with no code-visible signal

Until exp-09 runs with a clean artifact and the slot content isolated correctly, the
few-shot confound (Instructions-slot content ≈ P_p) remains the strongest open
challenge against the Persona-as-primary-installer claim.

---

## Relationship to exp-07d

exp-07d and exp-08 both used the silent zombie-write artifact. Comparing:

| Dimension | exp-07d I | exp-08 I | exp-07d J | exp-08 J |
|-----------|----------|----------|----------|----------|
| Zombie-write | 10/10 | 10/10 | 8/10 | 10/10 |
| Tier 1.0 | 0/10 | 0/10 | 0/10 | 0/10 |
| Mean tokens | 2,461 | 2,499 | 2,092 | 2,071 |
| Ceiling hits | 7/10 | 6/10 | 1/10 | 0/10 |

J's zombie-write detection rate improved from 8/10 to 10/10 — consistent with the
artifact's PR checklist making the path more visible. The I and J baselines are
otherwise stable, confirming the exp-08 measurements are reliable.
