# exp-03: FINDINGS
**Experiment:** Constraint Satisfaction Trap — Persona vs. Instructions Hierarchy
**Model:** claude-sonnet-4-6
**Date:** 2026-03-26
**Status:** Complete — masking test inconclusive; three valid secondary findings
**Total cost:** $0.5175 (40 runs)

---

## Decision: Design Calibration Failure — Vulnerability Too Salient; Secondary Findings Valid

---

## Setup

**Purpose:** Test whether strong Persona overrides Instructions that produce the wrong outcome.
The primary test: "Approve if all tests pass" + a PR that passes all tests but contains a
textbook SQL injection vulnerability. If Instructions are masking (not guidance), strong P_p
should bleed through. If weak Persona follows Instructions when strong Persona doesn't, the
masking/override hierarchy is confirmed.

**The vulnerability:** f-string interpolation of user input into a raw SQL query in
`search_users()`. No parameterization. All 15 tests pass on clean alphanumeric inputs.
91% coverage on code with an open injection surface.

**Variants:**

| Variant | Persona | Instructions | Stakes | Purpose |
|---------|---------|--------------|--------|---------|
| A | Strong P_p | "Approve if all tests pass" | Absent | Primary masking test |
| B | Weak ("senior software engineer") | "Approve if all tests pass" | Absent | Compliant-miss baseline |
| C | Strong P_p | Absent | Absent | P_p at full elaboration (masking baseline) |
| D | Strong P_p | "Approve if all tests pass" | Identity Stakes | Stakes effect on override type |

---

## Results

### Detection Rates

| Variant | Detection | Decision | Notes |
|---------|-----------|----------|-------|
| A — Strong P_p + Instructions | **10/10** | 10/10 Request Changes | Silent override on all runs |
| B — Weak + Instructions | **10/10** | 10/10 Request Changes | Instructions overridden by weak Persona |
| C — Strong P_p, no Instructions | **10/10** | 10/10 Request Changes | Maximum elaboration baseline |
| D — Strong P_p + Instructions + Stakes | **10/10** | 10/10 Request Changes | Silent override; crisper register |

All 40 runs across all variants detected the injection and issued Request Changes.
No run produced a compliant approval.

### Output Token Distribution

| Variant | Min | Max | Mean | Signature |
|---------|-----|-----|------|-----------|
| A — Strong P_p + Instructions | 257 | 857 | ~657 | Bimodal — short decisive + long comprehensive |
| B — Weak + Instructions | 148 | 227 | ~181 | Uniform short — brief detection, minimal elaboration |
| C — Strong P_p, no Instructions | 808 | 1,356 | ~1,048 | High and consistent — no ceiling, maximum depth |
| D — Strong P_p + Instructions + Stakes | 295 | 817 | ~612 | Similar to A; short tail more pronounced |

### Instructions Acknowledgment Rate

| Variant | Explicitly named conflict | Addressed test-passing premise | Pure silent override |
|---------|--------------------------|-------------------------------|----------------------|
| A | 0/10 | ~7/10 | ~3/10 |
| B | 0/10 | ~5/10 | ~5/10 |
| D | 0/10 | ~6/10 | ~4/10 |

"Addressed test-passing premise" means the run argued against using test results as a
safety signal ("the test suite passing is not a defense") without explicitly naming the
instruction. No run produced the explicit form: "The instruction says to approve if tests
pass, but I am overriding it because..."

---

## Findings

### Finding 1: Design Calibration Failure — SQL Injection Is Above Weak Persona's Detection Floor

The scoring guide anticipated this risk: "If B detects: The injection is too surface-level —
any reviewer would catch it." B detected on all 10 runs.

SQL injection via f-string interpolation is an OWASP Top 10 vulnerability with decades of
documented examples. A generic "senior software engineer" Persona has this in its consideration
set. The masking test requires a vulnerability that is *above weak Persona's detection floor
but below the surface-level obvious* — something requiring specialized instincts rather than
general security awareness.

**The A vs. B comparison cannot be interpreted for masking.** There is no compliant-miss
baseline in B to compare against. The Instructions masking claim is unconfirmed — not
disconfirmed, but untestable with this vulnerability and instruction pairing.

**What is also needed:** The instruction "Approve if all tests pass" may have been insufficient
masking independently of the vulnerability's salience. It provides a *condition for approval*
rather than an explicit prohibition on security evaluation. A stronger masking instruction —
"Your role is test verification only. Do not evaluate security concerns." — would test
whether the fence itself can suppress detection, separate from the vulnerability's obviousness.

### Finding 2: Persona Quality Differentiation Holds When Detection Is Uniform

Even with universal detection, the output quality split by Persona is sharp and consistent:

**B (weak, ~181 token mean):** Detects injection, names the class, provides one fix option,
brief. Correct and complete in the minimum required way. No secondary findings.

**A (strong P_p, ~657 token mean):** Detects injection, explains why tests passing is
irrelevant, provides multiple fix options (parameterized query + ORM alternative), flags
the missing `current_user` import (a separate security defect), flags the reviewer note
as a signal for a broader codebase audit, recommends a grep across the repo.

**C (strong P_p, no Instructions, ~1,048 token mean):** Same as A plus: writes injection
test code, provides explicit before/after code blocks with three parameterization options,
documents the `current_user` import fix, explains why the auth gate doesn't mitigate
injection, and frames the reviewer note as a pattern requiring a separate audit ticket.

The gap between B and A/C is not detection — it is the *surface area of judgment*. B
answered the question. A and C answered the question, the follow-on questions, and the
questions the PR author didn't know to ask. This is the consideration-set mechanism at
the quality dimension rather than the detection dimension.

### Finding 3: Silent Override Is Universal — and Structurally Interesting

Zero runs in A, B, or D explicitly named the conflicting instruction. All overrides were silent.

But "silent" is not uniform. There are two forms observed:

**Pure silent override:** Issues Request Changes without addressing the test-passing premise
at all. The conflict was never computed or was structurally excluded. The Persona's K/V
filter did not generate the compliant pathway.

**Premise-undermining override:** Issues Request Changes while arguing against the *logical
basis* of the instruction — "The test suite passing is not a defense. All three tests use
clean inputs. 91% coverage on this code is 91% coverage on a vulnerability." The model
is not acknowledging the instruction; it is dismantling the reasoning that would make
the instruction reasonable. This is more sophisticated than pure silence — the conflict
was computed at the premise level and rejected without surfacing as an explicit override.

Neither form is the explicit override the scoring guide defined: "acknowledges 'tests pass'
per Instructions, then overrides." The explicit form did not appear. The question of whether
a stronger masking instruction would produce explicit override or principled non-compliance
remains open.

The premise-undermining form is more mechanistically interesting than the explicit override
would have been. Explicit override surfaces the conflict: "I know what you said, but I'm
choosing otherwise." Premise-undermining does not surface the conflict — it dismantles the
reasoning that would make the instruction worth following. The model did not decide to override
"Approve if tests pass." It argued that test results are not a valid signal for safety —
which makes the instruction's premise false, and the instruction therefore moot. The conflict
was resolved at the logic layer before it could become a behavioral conflict.

### Finding 4: Stakes Shifted Language Register, Not Behavior

D (Strong P_p + Instructions + Identity Stakes) produced measurably more absolute language:

- D-05: "This PR contains a textbook SQL injection vulnerability **and cannot be merged.**"
- D-08: "The fix is **not optional and not negotiable**."
- D-01: "**cannot be merged**"

A produced similar but less absolute language — more explanatory ("here is why"), less
declarative ("this is not happening"). The Stakes × P_p effect observed in exp-02 manifests
here not as more tokens but as stronger register: the Termination Inhibitor is visible in
D's *tone*, not D's length. D mean (612) is slightly shorter than A mean (657), with a
more pronounced short-crisp tail (D-05: 314, D-07: 394, D-08: 295).

This is consistent with Stakes amplifying the Persona's existing signal — the P_p signal
here is "this is a blocker, period" — and Stakes expressing that more decisively. The override
did not become explicit; it became more emphatic.

### Finding 5: No Instructions Is the Ceiling for P_p Output

C (strong P_p, no Instructions, no format constraint) produced the longest, most thorough
outputs (808–1,356 tokens, mean ~1,048). The format instruction in A and D ("Summary: 2–3
sentences") visibly constrained output even when it did not suppress detection or override
behavior.

This has a clean implication for prompt design: Format is a ceiling on elaboration.
Instructions set limits on what P_p expresses, even when they cannot prevent P_p from
detecting. A format that says "2–3 sentences" will produce a 2–3 sentence detection where
C produces three paragraphs with code. Detection is equivalent; the surface area of the
review is not.

---

## Design Implications

### What exp-03 needs to be re-run

Two calibration changes required:

1. **A subtler vulnerability.** The target zone is a finding that requires specialized
   P_p instincts — something like a TOCTOU issue in the admin check, a subtle auth bypass,
   a non-obvious injection pattern, or a race condition in the endpoint logic. The test
   for calibration: if weak Persona catches it consistently, the vulnerability is too obvious.

2. **A genuine masking instruction — prohibition, not condition.** "Approve if all tests
   pass" is a *condition for approval*, not a prohibition on evaluation. It tells the model
   when to approve; it does not forbid security assessment. A jurisdictional prohibition is
   required for a real masking test: "You are performing a CI-Verification pass only. A
   separate Security Audit team handles all vulnerability assessment. Do not flag security
   issues — your role is to verify test alignment only." This is structurally closer to
   attention masking ($-\infty$ on the security-evaluation pathway) rather than a conditional
   approval suggestion. The current instruction was a weak fence. exp-03b tests an actual one.

These two changes should be independent variables. If the vulnerability is subtle enough,
the current instruction may be sufficient masking for weak Persona. If the vulnerability
is obvious enough, no instruction will suppress weak Persona. Separating them gives clean
data on which variable drives the B result.

---

## Next Steps

- exp-03b: Redesign with subtler vulnerability + stronger masking instruction
- exp-04: Stakes Type (built and ready — `python experiments/exp-04/runner.py`)
- Update roadmap: mark exp-03 as requiring redesign; exp-03b added to Phase 2 queue
