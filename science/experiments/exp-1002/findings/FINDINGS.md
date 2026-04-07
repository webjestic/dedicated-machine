# exp-1002 Findings — Stakes as Situational Briefing: Legal Contract Review

**Status:** Complete
**Result:** Stakes changes direction of attention. Does not install search algorithm. CRITICAL: 0/10 for both A and B_v2.
**H1002:** Not supported as stated. Partial behavioral effect confirmed.

---

## Score

Three runs total: A (baseline), B_v1 (stakes + hint), B_v2 (stakes, no hint).

| Condition | CRITICAL | ELITE | DISTRACTION | Notes |
|-----------|----------|-------|-------------|-------|
| A — Weak Persona, no Stakes | 0/10 | 0/10 | 10/10 | All runs led with federal compliance |
| B_v1 — Weak Persona + Stakes + hint | 3/10 | 0/10 | 6/10 | Hint named the cap as the problem |
| B_v2 — Weak Persona + Stakes, no hint | 0/10 | 0/10 | 7/10 | Better direction, still missed the trap |

**DISTRACTION is a failure measure.** 10/10 = all 10 runs distracted. Lower is better.

---

## The Artifact Confound (Run 0)

The first run used a contaminated artifact. The CONTRACT.md file included a "Ground Truth" section that named the trap explicitly — "Section 8.2's carve-outs effectively nullify the Section 8.1 cap." Both A and B scored 10/10 CRITICAL. This was the model following instructions, not detecting the trap. Data discarded.

---

## What Happened

### Variant A — The Distraction Pattern

Without Stakes, the weak Persona + federal contractor context activated regulatory compliance as the primary concern. All 10 runs led with FAR/DFARS, CMMC, FedRAMP, FISMA, export control, or clearance requirements. The model read "national security federal contracting" and reached for the compliance playbook. The liability structure was noted incidentally or not at all.

This is the same distraction pattern as exp-01f N — different distractor, same failure mode. The exp-01f N checklist activated clause enumeration. The federal contractor context here activated regulatory enumeration. Both are "thorough review of the wrong things."

### B_v1 — Stakes + Hint

The original B Stakes section included: *"a cap that looks bilateral and real but isn't."* That phrase named the mechanism — it told the model the cap was the problem before the model read the contract. 3 of 10 runs found CRITICAL. The hint, not the Stakes, drove those passes.

When the hint was removed, CRITICAL dropped to 0/10. The Stakes consequence framing alone provided no detection signal.

### B_v2 — Stakes, No Hint

Stakes shifted the distraction pattern. A: 10/10 distracted (regulatory compliance). B_v2: 7/10 distracted. Three runs focused on the contract structure without leading with regulatory noise — better, but still missed the nullification argument.

The B_v2 outputs show a consistent three-finding structure:
1. Indemnification carve-out / overbreadth (adjacent to CRITICAL, not CRITICAL)
2. Trailing twelve-month cap window (legitimate structural issue, not the trap)
3. Arbitration clause (distraction)

The model reached the right neighborhood — it's reading the liability structure, not FAR/DFARS. But without a search algorithm ("read the cap, read the carve-outs, ask if the cap is real"), it found real issues nearby and stopped there.

---

## The Core Finding

**Stakes is a compass, not a map.**

It changes the direction of attention. A points at regulatory compliance. B points at the contract structure. That is a real, measurable behavioral shift. But direction change without search direction gets the model to the right section of the contract without knowing what question to ask about it.

The question that unlocks CRITICAL is structural: *do the carve-outs together cover enough dispute categories to make the cap functionally illusory?* That question requires a specific reasoning sequence. Stakes names what's at stake if the answer is wrong. It does not install the sequence.

**Stakes has no operational content.** "If there is a structural defect in the liability provisions they will not discover it until they are in a dispute" is atmosphere. It raises the stakes of the review. It does not change what the model looks for or how it looks.

Compare to what M's procedural Persona provides: *"first, read the cap. Then immediately read every carve-out. Then ask whether what remains inside the cap is broad enough to provide meaningful protection in practice."* That is a search algorithm. It specifies action, sequence, and the question to answer.

Stakes cannot substitute for that because Stakes has no procedure inside it. It is motivational framing applied to a model that does not need motivation — it needs direction.

---

## Comparison to exp-01f

| Condition | CRITICAL | Persona type | Stakes type |
|-----------|----------|--------------|-------------|
| exp-01f M | 10/10 | Strong procedural | None |
| exp-01f N | 0/10 | Weak credential | None |
| exp-01f P | 1/10 | Strong disposition | Identity/pride |
| exp-1002 A | 0/10 | Weak credential | None |
| exp-1002 B_v2 | 0/10 | Weak credential | Situational consequence |

Every form of Stakes tested — identity/pride (P), situational consequence (B_v2) — scores at or near zero on CRITICAL against a weak Persona. Procedural Persona (M) scores 10/10 without any Stakes.

The variable that matters is not Stakes in any form. It is the procedural search algorithm embedded in Persona.

---

## What Stakes Does and Does Not Do

**Does:**
- Shifts attention direction (regulatory compliance → contract structure)
- Reduces distraction hits marginally (A: 10/10, B_v2: 7/10)
- Raises output depth slightly (B avg 810 tokens vs A avg 663 tokens)

**Does not:**
- Install a search algorithm
- Identify the specific structural argument
- Compensate for absent procedural Persona
- Change the termination condition — the model still stops at the first plausible set of findings

---

## Implications

The original Stakes hypothesis — "naming real-world consequence changes what the model finds" — is partially confirmed and partially refuted.

**Confirmed:** Stakes changes *where* the model looks.
**Refuted:** Stakes does not change *what* the model finds when it gets there.

Stakes functions as a coarse attention director. It can suppress irrelevant search directions (regulatory compliance). It cannot supply the precise reasoning sequence that identifies a structural defect.

For practitioners: Stakes is not worthless. Directing attention away from noise toward signal is real value. But Stakes alone will not catch the trap. The procedural Persona is what catches it — and it catches it without Stakes.

---

## Next Steps

The 1001 and 1002 series together establish:

1. Stakes does not lift coverage against any Persona strength (exp-1001, exp-1001b)
2. Stakes does not install detection capability against a weak Persona (exp-1002)
3. Stakes shifts attention direction but not search depth
4. Procedural Persona is the operative variable — it provides the search algorithm that Stakes cannot

The remaining question for the Stakes line: is there any task type or Stakes framing where the behavioral shift Stakes provides is the difference between a miss and a find? The compass metaphor is useful — in a task with a very short search space, pointing in the right direction might be enough. The experiments so far have all involved tasks where the target requires a specific reasoning sequence, not just proximity.

---

## Cost

- exp-1002: 30 runs total (10 A + 10 B_v1 + 10 B_v2), claude-sonnet-4-6, temperature=0.5, max_tokens=4000
- Total cost: $0.52
- Total 1001 series + 1002: ~$4.87
