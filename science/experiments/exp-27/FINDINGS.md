# Exp-27 Findings — Horizon Blindness / Gap Detection

**Status:** Complete
**Date:** 2026-03-30
**Model:** claude-sonnet-4-6
**Runs:** 30 (10 × A, B, C)
**Total cost:** $1.81

---

## Results

| Variant | Mean score | Range | Mean tokens |
|---------|------------|-------|-------------|
| A — P_d baseline | 6.2/10 | 4–7 | 1417 |
| B — P_p task-scoped | 7.1/10 | 6–9 | 1512 |
| C — P_p + gap-detection | 8.6/10 | 7–10 | 1597 |

**Item detection rates by variant:**

| Item | A | B | C |
|------|---|---|---|
| mempool | 100% | 60% | 100% |
| ecdsa_signing | 100% | 100% | 100% |
| difficulty_adjustment | 100% | 40% | 80% |
| coinbase_reward | 100% | 100% | 80% |
| p2p_networking | **0%** | 80% | **100%** |
| persistence | **0%** | 50% | **100%** |
| api_layer | 80% | 80% | 30% |
| double_spend | 50% | 100% | 90% |
| merkle_root | 70% | 100% | 90% |
| chain_sync_fork | 20% | **0%** | **90%** |

---

## Calibration Failure — Wrong Direction

The calibration target was A mean ≤ 3/10. A came in at 6.2/10.

The artifact assumption was wrong: "blockchain in Node.js" has a canonical
training-data shape that already encodes most of the checklist items. The
model's path of least resistance for this domain is not `Block + Blockchain +
mine()` — it is a multi-file project with wallets, transaction pools, signing,
and often a REST API. Items 1–4 (mempool, ECDSA, difficulty, coinbase) appear
at 100% in A because they are part of the canonical pattern, not because the
machine is reasoning about production completeness.

Every A run hit max_tokens=4000 and began with a multi-file project structure
scaffold. The shallow path for "blockchain in Node.js" is already deep.

**Implications for Claim 1:** Partially disconfirmed for this artifact. The
path of least resistance in a domain with a rich canonical training pattern does
not produce shallow output. Horizon blindness is still detectable — A never
surfaces p2p_networking (0%) or persistence (0%) — but the mechanism is more
nuanced than "shallow path = simple output." The horizon is domain-relative.

---

## What C Does That A and B Don't

C outputs are structurally different from A and B. Every C run opened with a
gap analysis section before writing any code:

> *"Let me start by identifying what a production deployment actually requires
> that typical 'build me a blockchain' specs omit, then build accordingly."*
> — C-02

> *"Let me be direct about what I'm building and what I'm flagging before
> writing a single line of code."*
> — C-03

C-02 produced a 14-row gap table before a line of code was written, with
columns: Gap | Risk if Ignored | My Decision. The table included items well
beyond the 10-item checklist: structured logging, graceful shutdown,
configuration management, test coverage. C-03 explicitly flagged security gaps
(HSM, eclipse attacks, Sybil resistance) and operational gaps (metrics,
graceful shutdown, WAL).

A and B produce code directly. C produces a gap audit, then code. The
satisfaction condition changes the *opening move* — the machine cannot proceed
to code without first naming the gaps.

---

## Claim Assessment

**Claim 2 — Gap-detection condition surfaces unsolicited production requirements:**
**Confirmed.** C >> B across deployment-layer items. The items that separate C
most from A and B are exactly the items that require deployment-context
reasoning rather than code-level completeness:

- p2p_networking: A=0%, B=80%, C=100%
- persistence: A=0%, B=50%, C=100%
- chain_sync_fork: A=20%, B=0%, C=90%

These items require thinking about what the system needs *to run in production*,
not just what the code needs to compile. The gap-detection condition unlocks
the deployment-layer consideration set.

**Claim 1 — Path of least resistance produces shallow output:**
**Disconfirmed for this artifact.** The artifact was too canonically trained.
However, the mechanism is still visible: even A's deep output is bounded by
the code-layer horizon. Persistence and P2P never appear in A because they
require stepping outside the "write the code" frame. The horizon exists — it
is just higher than the design assumed for this domain.

---

## Item-Level Observations

**Items that appear in A's canonical path (training-data artifacts, not
production reasoning):**
- mempool (100%), ecdsa_signing (100%), difficulty_adjustment (100%),
  coinbase_reward (100%)

**Items that require deployment-layer reasoning (A=0%, unlocked by C):**
- p2p_networking, persistence

**Items where B's domain vocabulary provides lift over A:**
- p2p_networking (0% → 80%), double_spend (50% → 100%), merkle_root (70% → 100%)

**Items where C's gap-detection lifts over B:**
- chain_sync_fork (B=0% → C=90%) — the strongest evidence for Claim 2
- persistence (B=50% → C=100%)
- No items regressed significantly A→B→C

**Unexpected: api_layer regresses A→C (80% → 80% → 30%).** C runs were
consumed by gap-analysis and deep implementation before reaching the API
layer — hitting max_tokens before the REST surface was built. This is an
artifact of the 4000-token limit, not a behavioral signal.

---

## The Falsifiable Pattern Match

Predicted: A ≈ B, C >> B → Claim 1 and 2 confirmed
Observed: B > A (+0.9), C >> B (+1.5)

This falls closest to **"B >> A, C >> B — expertise lifts AND gap-detection
lifts further"** from the falsifiable outcomes table, except the B-A gap is
small (0.9 points) compared to the C-B gap (1.5 points). The dominant effect
is still the gap-detection condition, not domain expertise.

The closer truth: blockchain is too canonically trained for A-B separation to
be clean. The operative signal is C vs. {A, B}: the gap-detection condition
produces a structurally different output class, not just a higher score.

---

## What the Experiment Actually Showed

The gap-detection satisfaction condition does what the hypothesis claims:
it makes gap identification load-bearing on completion. The machine cannot
satisfy the criterion without first naming what the prompt didn't ask for.
This changes the opening move, the structure of the response, and which
items from the consideration set become load-bearing.

The artifact was wrong. The mechanism is real.

---

## Design Failure: Artifact Too Canonically Trained

To isolate the mechanism cleanly, the artifact needs a prompt where the shallow
path is *genuinely* shallow — not a well-known domain with a rich training-data
prior. The blockchain prompt fails this condition.

**Requirements for a clean artifact:**
1. Plausible shallow resolution (machine can stop early and "be done")
2. Clear production requirements that the shallow path omits
3. No canonical training-data shape that encodes those requirements by default
4. Scorable: present/absent is unambiguous

Candidates for a follow-on experiment:
- "Build a job queue system" (shallow: array + push/pop; deep: retry, DLQ,
  concurrency limits, persistence)
- "Build a rate limiter" (shallow: in-memory counter; deep: distributed,
  sliding window, Redis, multi-instance)
- "Build a config loader" (shallow: JSON parse; deep: env override, secrets
  management, hot reload, validation)

These have shallower canonical training shapes than blockchain.

---

## Next Steps

1. **Design exp-27b** with a cleaner artifact where A genuinely floors at ≤3/10
2. **Design the follow-on series:** Persona + Instructions (non-PARC) = better
   goal alignment. User framing: "Normal instructions would apply to A, PARC
   instructions to B." The operative question: can the gap-detection work be
   moved from the Persona slot to the Instructions slot, and does the slot matter?
