# Exp-27 Design — Horizon Blindness / Gap Detection

**Status:** Pre-run
**Phase:** 7 — The Dedicated Machine Hypothesis
**Date:** 2026-03-30

---

## Hypothesis Under Test

Two ordered claims from `research/hypotheses/dedicated-machine_v2.md`:

**Claim 1 — Establish the mechanism:**
The machine takes the path of least resistance to satisfactory resolution. An
underspecified prompt produces shallow output not because knowledge is absent —
production requirements exist in the consideration set — but because the shallow
path satisfies the criterion and the machine terminates there. Horizon blindness:
no native dissatisfaction with the gap between what was delivered and what was needed.

**Claim 2 — Exploit the mechanism:**
A P_p with a mission-scoped gap-detection satisfaction condition moves the needle —
surfaces production requirements the user didn't specify — without requiring the user
to know what they don't know.

---

## Question

Does a gap-detection satisfaction condition in the Persona expand the machine's
definition of "done" on an underspecified prompt — surfacing production requirements
the prompt never mentioned — compared to a task-scoped P_p and a P_d baseline?

---

## Artifact

**Prompt:** "Build me a blockchain implementation in Node.js."

Intentionally underspecified. No mention of:
- Transaction pool / mempool
- ECDSA / secp256k1 wallet signing
- Difficulty adjustment
- Coinbase / mining reward transaction
- P2P networking / peer discovery
- Persistence / storage
- REST/RPC API layer
- Double-spend prevention
- Merkle root
- Fork resolution / longest-chain rule

The prompt has a satisfactory resolution that doesn't require any of these. A working
Block class + Blockchain class + basic proof-of-work loop closes the loop. The machine
terminates there unless the satisfaction condition demands more.

---

## Variants

### Variant A — P_d Baseline

```
You are a software engineer.

Build me a blockchain implementation in Node.js.
```

Establishes the floor. What does the path of least resistance look like with no
architectural framing?

### Variant B — P_p, Task-Scoped

```
You are a senior software engineer with deep experience building distributed systems
and blockchain infrastructure. You have shipped production blockchain nodes, designed
peer-to-peer consensus protocols, and built wallet and transaction signing systems
from scratch. You know what production blockchain infrastructure actually requires.

Build me a blockchain implementation in Node.js.
```

Domain expertise without a gap-detection condition. Tests Claim 1: does expertise
alone raise the satisfaction threshold, or does the machine still terminate at the
same shallow resolution — just with better execution?

### Variant C — P_p + Gap-Detection Satisfaction Condition

```
You are a senior software engineer with deep experience building distributed systems
and blockchain infrastructure. You have shipped production blockchain nodes, designed
peer-to-peer consensus protocols, and built wallet and transaction signing systems
from scratch. You know what production blockchain infrastructure actually requires.

My implementation is complete only when I have identified what a production deployment
of this system requires that the stated requirements do not mention, named those gaps
explicitly, and either addressed them or flagged them for the requester.

Build me a blockchain implementation in Node.js.
```

Same P_p as B. The satisfaction condition expands the definition of "done" to include
surfacing what the prompt didn't ask for. Tests Claim 2: does the gap-detection
condition pull production requirements from the consideration set into the output?

---

## Scoring

**Metric:** Continuous. Score = number of unsolicited production requirements surfaced
per run (0–10). Not binary detection — count of items named, implemented, or explicitly
flagged as missing.

**10-item checklist:**

| # | Item | Layer | Description |
|---|------|-------|-------------|
| 1 | mempool | Integration | Transaction pool for pending transactions before mining |
| 2 | ecdsa_signing | Integration | Cryptographic wallet signing (secp256k1 / elliptic curve) |
| 3 | difficulty_adjustment | Integration | Dynamic difficulty targeting block time |
| 4 | coinbase_reward | Integration | Mining reward / coinbase transaction |
| 5 | p2p_networking | System | Peer discovery, block broadcasting, chain sync |
| 6 | persistence | System | Chain survives process restart (leveldb, sqlite, file) |
| 7 | api_layer | System | REST/RPC endpoint for transaction submission, queries |
| 8 | double_spend | Correctness | Balance verification before mempool acceptance |
| 9 | merkle_root | Correctness | Block header transaction integrity hash |
| 10 | chain_sync_fork | Correctness | Longest-chain rule, fork resolution |

**Scoring rule:** Score 1 if the item is explicitly named, implemented, or flagged as
a production requirement. Score 0 if absent or mentioned only as a comment without
substance.

---

## Predictions

| Variant | Predicted mean | Reasoning |
|---------|---------------|-----------|
| A | 1–3/10 | Shallow path: Block class + Blockchain class + mine() loop; maybe signing if domain knowledge bleeds through |
| B | 2–5/10 | Expertise may surface more items, but task-scoped criterion doesn't require them; some lift likely from domain priming |
| C | 6–9/10 | Gap-detection condition makes "named what's missing" load-bearing on completion; machine must surface the gaps to satisfy the criterion |

**Falsifiable outcomes:**

| Pattern | Interpretation |
|---------|----------------|
| A ≈ B, C >> B | Claim 1 and 2 confirmed: expertise doesn't move threshold; gap-detection does |
| B >> A, C >> B | Expertise lifts AND gap-detection lifts further: both P_p and Stakes contribute |
| A ≈ B ≈ C (ceiling) | Prompt is not underspecified enough; blockchain is a well-known pattern |
| A ≈ B ≈ C (floor) | Prompt too open; model produces shallow output regardless of framing |
| C ≈ B >> A | Domain expertise is the operative variable; gap-detection adds nothing marginal |

---

## Key Design Decisions

**Why blockchain and not Express API?**
Express API has no canonical "complete" shape — production requirements depend on
design choices (auth strategy, ORM, caching layer). Scoring would be
inconsistent across runs. Blockchain has objective completeness criteria: either
a mempool exists or it doesn't; either ECDSA signing is implemented or it isn't.
Present/absent is scorable consistently.

**Why continuous scoring (not binary detection)?**
The claim is about the satisfaction threshold — how much the machine produces beyond
the minimum satisfactory resolution. Binary detection would collapse the gradient.
A score of 3 vs. 7 is meaningful; pass/fail is not.

**Why max_tokens=4000?**
C may produce substantially longer output (naming gaps + addressing them). 2500
tokens would truncate before the gap-flagging section in many runs.

**Why the same P_p for B and C?**
To isolate the gap-detection satisfaction condition as the operative variable.
If B and C had different base Personas, we could not distinguish P_p strength
from gap-detection effects.

---

## Calibration Note

A calibration run is not needed before the full experiment — there is no
binary pass/fail threshold that could disqualify the artifact. The floor
(A mean ≤ 3/10) is a post-run diagnostic. If A floors higher than expected,
the artifact may be too well-specified, not a calibration failure.

Run all variants at full n=10 from the start.

---

## Connection to Prior Work

**Phase 6 (exp-19–24):** Established that mechanism vocabulary in the Persona
drives ceiling detection. exp-27 extends this: not vocabulary specificity, but
*scope of the satisfaction condition* as the operative variable. The blockchain
prompt has no "correct path" vocabulary — the gap-detection condition must
expand scope from inside the Persona, not from the artifact.

**dedicated-machine_v2.md:** Horizon blindness section. "The machine delivers
exactly what you defined. The gap between what you defined and what you needed
is invisible to it." exp-27 tests whether the gap-detection satisfaction condition
makes that gap visible.

**exp-26 (NSR hypothesis):** All runs found the shallow TOCTOU bug and stopped.
exp-27 tests the same mechanism from the generation side: given an underspecified
construction prompt, does the machine stop at the shallow path? Same mechanism,
different task type (generation vs. review).
