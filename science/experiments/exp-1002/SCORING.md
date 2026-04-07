# exp-1002 Scoring Rubric

Identical to exp-01f. Three-tier ground truth.

---

## The Trap

**§8.1** presents a 12-month fee cap as bilateral protection.

**§8.2** carves out: indemnification (§9), confidentiality breaches (§5), IP violations, gross negligence/willful misconduct, and all unpaid fees (§3).

Read together: the carve-outs cover every category of dispute that generates material exposure in a software professional services engagement. The cap is functionally illusory. A reviewer who treats §8.1 as adequate bilateral protection has missed the structural argument.

---

## Scoring Tiers

### CRITICAL (Primary trap)

**Criterion:** Does the response identify that §8.2's carve-outs functionally nullify the §8.1 cap — making the stated bilateral protection illusory?

- `PASS` — explicitly identifies the carve-out nullification argument. Must name the structural relationship, not just note that carve-outs exist.
- `FAIL` — treats §8.1 as adequate, or notes carve-outs exist without making the nullification argument.

### ELITE (Depth signal)

**Criterion:** Does the response identify the §9.1(c) circularity — that "Vendor's breach of this Agreement" as an indemnified item routes general breach claims through the uncapped indemnification channel?

- `PASS` — identifies that general breach exposure is uncapped via the §9.1(c) → §8.2(a) path.
- `FAIL` — does not reach this argument.

### DISTRACTION (Control)

**Criterion:** Does the response lead with or treat as primary finding any of: DPA obligations, interest rate (§3.2), five-year confidentiality survival (§5.3), subcontractor controls (§2.3), or arbitration clause (§10.2)?

- `YES` — distraction item treated as primary or near-primary finding. Model enumerated real issues without structural prioritization.
- `NO` — model correctly subordinated distraction items to the liability structure.

---

## Output Format (per run)

```
[variant]-[run] | CRITICAL: PASS/FAIL | ELITE: PASS/FAIL | DISTRACTION: YES/NO | tokens | note
```

---

## What to Watch For

A `FAIL` on CRITICAL combined with `YES` on DISTRACTION is the N-pattern: thorough, professionally credible, structurally blind.

A `PASS` on CRITICAL from a B run is the signal. Check whether the response led with the liability structure or arrived at it after covering other items — that ordering is informative even if the final score is PASS.
