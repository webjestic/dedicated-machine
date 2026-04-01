# Exp-21b CC Decision

## Objections Raised
1. **Caution on token count interpretation (Gemini):** B > A verbosity may be an artifact of null-detection runs, not a meaningful difference. Both experiments are non-operative.
2. **Exp-22b is a replication of exp-19 (Gemini):** The slot-swap with Kleppmann vocabulary is the original H1/H2 question — confirm this is the right next step.

## Decision: Accept with clarifications.

No fatal objections. Null result is interpretable and well-supported. The specificity threshold finding is confirmed.

## Final Conclusion

> Orientation vocabulary in the system prompt — whether in the Persona slot (P_p) or Instructions slot (P_d) — does not drive zombie-write detection. Both A and B score 0/10, identical to the C baseline.
>
> Vocabulary must name the specific failure mode (zombie-write, process-pause chain) or fix (fencing token, optimistic lock at DB layer) to reach the detection threshold. Domain orientation without concept-level labels is insufficient.
>
> This is consistent with a **specificity threshold effect**: the model needs the exact concept label, not the semantic neighborhood. This refines the exp-20 finding: it is not vocabulary per se that drives detection, but vocabulary at the failure-mode/fix level of specificity.
>
> H1/H2 remain open: the slot may still matter, but only when vocabulary is at or above the specificity threshold. Exp-21b confirms the lower bound of the operative vocabulary range.

## Next Experiments

1. **Exp-22 (interrogative artifact vocabulary):** Directive vocabulary in artifact with interrogative framing. Tests H2.
2. **Exp-23 (Kleppmann-specific slot-swap):** P_p Persona with "zombie-write failure modes, fencing tokens, Kleppmann's critique of Redlock" (original exp-19-style vocabulary) vs. P_d with same vocabulary in Instructions. Clean H1/H2 test at the confirmed operative specificity level.
