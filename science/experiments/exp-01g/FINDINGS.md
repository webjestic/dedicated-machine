# exp-01g: FINDINGS
**Experiment:** Cross-Model Validation — Gemini 2.5 Pro
**Model:** gemini-2.5-pro
**Date:** 2026-03-26
**Status:** Complete

---

## Decision: Cross-Model Validation Confirmed

---

## Setup

**Purpose:** Test whether the consideration-set mechanism observed in exp-01e (Claude) replicates on a different model family. Variants I and J from exp-01e run unchanged on Gemini 2.5 Pro.

**Task:** Code review of a distributed inventory reservation service using Redis distributed locks with a heartbeat renewal mechanism.

**The Trap:** The heartbeat thread renews the lock TTL during normal execution — but it cannot protect against a process-level pause (stop-the-world GC, VM migration). During a pause, all threads freeze including the heartbeat. The lock expires. Another worker acquires it, completes the write, and releases. When the paused process resumes, it holds a stale in-memory read and overwrites the correct value with corrupted data — a "zombie write." The fix requires a fencing token / optimistic concurrency control at the database layer, not just lock management.

**Ground Truth:**
- CRITICAL: Zombie write scenario identified (process pause → lock expiration → stale write)
- DISTRACTION: Instance-level heartbeat state (shared `self._heartbeat_thread` across concurrent requests) — a real bug, but not the architectural trap

**Variants:**

| Variant | Persona | Context |
|---------|---------|---------|
| I | Strong procedural — "burned by lock safety violations in production," explicit search algorithm: simulate what happens when the process pauses during the critical section | Rich obotix.one engineering context |
| J | Weak generic — "You are a senior software engineer" | Rich obotix.one engineering context |

---

## Results

### CRITICAL Criterion Scores

| Variant | Model | Score | Pattern |
|---------|-------|-------|---------|
| I | Gemini 2.5 Pro | **10/10** | Zombie write scenario on every run; fencing token solution; often secondary findings ranked below primary |
| J | Gemini 2.5 Pro | **0/10** | Instance-level heartbeat state on every run; zombie write never reached |

**Comparison to Claude exp-01e:**

| Variant | Claude (exp-01e) | Gemini (exp-01g) |
|---------|-----------------|-----------------|
| I | 10/10 | 10/10 |
| J | 0/10 | 0/10 |

Exact replication.

### Token Distribution

| Variant | Avg Output | Avg Thinking | Ceiling Hits |
|---------|------------|--------------|--------------|
| I | 1,142 | ~2,884 | 0/10 |
| J | 1,045 | ~2,661 | 0/10 |

**Key difference from Claude:** On Claude, J hit the 2,500-token output ceiling on every run (the diagnostic signal). On Gemini, thinking tokens are explicit and separate — J does not hit the output ceiling because the thinking budget absorbed the enumeration overhead. The J-pattern is present but hidden in the thinking column: J uses slightly less thinking per run than I (2,661 vs 2,884), consistent with J running a shallower search that terminates earlier on a surface-level finding.

The output token ranges are similar between I and J (1,142 vs 1,045 avg), which means the ceiling-based diagnostic that worked on Claude does not apply directly to Gemini. Scoring requires reading outputs, not reading token counts.

**Total cost:** $0.2849 for 20 runs.

---

## Findings

### Finding 1: The Consideration-Set Mechanism Generalizes Across Model Families

I scored 10/10 and J scored 0/10 on Gemini 2.5 Pro — identical to Claude Sonnet 4.6. The Persona mechanism that determines which failure modes enter the consideration set operates consistently across architecturally different models. This is not a Claude artifact.

The result was obtained with the same variant prompts run unchanged from exp-01e — no model-specific tuning was applied to I or J for Gemini. The zero-shot transfer held.

### Finding 2: The Distraction Pattern Is Model-Independent

J's distraction finding was the same on Gemini as on Claude: instance-level heartbeat state shared across concurrent requests. Both model families, same weak Persona, same distraction. The J-pattern is not a Claude-specific quirk — it is the default reasoning mode of a competent reviewer without a procedural search algorithm. That mode finds real implementation flaws; it does not reach architectural traps.

### Finding 3: The Priority Stack — Not Just the Consideration Set

The most precise result from reading I vs. J outputs: I consistently found **both** flaws (zombie write as primary, instance-level heartbeat state as secondary) in that priority order. J found only the secondary flaw, ranked as primary.

This is a refinement on the consideration-set framing. The strong procedural Persona does not just expand the set of things the model considers — it installs a **priority ordering** within the consideration set. The zombie write is higher-priority than the heartbeat state issue because the Persona's identity (burned by production lock safety violations) knows the difference between an implementation detail and an architectural failure mode.

J's Persona has no such ordering installed. A "senior software engineer" encountering both issues picks the one that's most visible in the code — the instance variables — and leads with it.

### Finding 4: Gemini Thinking Architecture Does Not Mask the Effect

Initial concern: Gemini 2.5 Pro's explicit thinking tokens might absorb the J-pattern's characteristic ceiling-hitting behavior, making it harder to measure. The thinking tokens do absorb some of that signal — J does not ceiling-hit on output tokens the way it does on Claude.

However, the primary signal (Critical criterion score) is unaffected. The consideration-set mechanism operates at the reasoning level, not the token-budget level. Gemini's thinking architecture makes the mechanism harder to detect from token counts alone, but does not change the outcome.

**Methodological note for cross-model work:** The token ceiling pattern is a Claude-specific diagnostic. On thinking models, scoring requires reading outputs directly. The experimental infrastructure (ground truth criteria, raw output recording) handles this correctly; the interpretation methodology needs to account for the architectural difference.

### Finding 5: Identical Prompts, Identical Results — Zero-Shot Transfer Confirmed

I and J were written for Claude and run unchanged on Gemini. No modifications. No model-specific framing. The procedural Persona worked on Gemini because it encodes a reasoning algorithm — and reasoning algorithms are model-agnostic. "Read the critical section, then ask what happens if the process pauses during it" is a valid instruction regardless of which transformer is executing it.

This supports the Prompt Architecture framing: a well-specified cognitive pipeline is a deployable component, not a Claude-tuned prompt.

---

## Implications

**The cross-model claim is now evidence-supported.** The consideration-set mechanism has been confirmed on:
- Two task domains: code review (exp-01e, exp-01g) and legal contract review (exp-01f)
- Two model families: Claude Sonnet 4.6 and Gemini 2.5 Pro

The framework's primary claim — that Persona (specifically P_p, procedural specification) determines which reasoning classes are reachable — is not model-specific. It is a property of how transformer-based language models process identity-rich context.

**Phase 1 of the roadmap is complete.**

---

## Next Steps

- exp-02: Formal Stakes ablation — hold Persona and Context constant, vary Stakes across 4 levels
- Update pcsieftr-context.md and roadmap.md with Phase 1 completion
- Update research/findings/pcsieftr.md running synthesis
