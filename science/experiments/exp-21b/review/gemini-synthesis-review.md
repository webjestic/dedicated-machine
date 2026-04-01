# Exp-21b Gemini Synthesis Challenge

## CC Synthesis Claim
CC concluded: orientation vocabulary (no failure mode, no fix named) is inert regardless of slot — specificity threshold effect. Vocabulary must name the specific failure mode or fix. Neither H1 nor H2 is testable from this result. Proposed exp-22a (interrogative artifact) and exp-22b (Kleppmann-specific vocab slot-swap).

## Gemini Challenge

**The specificity threshold explanation is well-supported, but exp-21b's relationship to exp-19 deserves scrutiny.** In exp-19, the P_p Persona contained "Kleppmann's critique of Redlock, split-brain scenarios, zombie-write failure modes, fencing tokens, process isolation boundaries, lock lease expiry" and drove 10/10. In exp-21b, the P_p Persona contained "lock lifecycle correctness, process isolation boundaries, temporal gap, failure taxonomy of distributed coordination protocols" and drove 0/10. CC attributes this to specificity ("must name the failure mode"). This is correct.

**But CC's proposed exp-22b is actually just a replication of exp-19 with a cleaner design.** Exp-19 already showed that Kleppmann-level vocabulary in Persona drives 10/10. The question of whether the same vocabulary in Instructions (exp-22b P_d variant) drives the same result is the core slot-swap question — which is what H1 vs H2 requires. This is the right next experiment.

**The token count observation requires caution.** The B > A pattern (Instructions > Persona token count) is consistent across exp-20 and exp-21b, but the sample sizes are small and both are null-detection runs. The verbosity difference may be an artifact of both experiments being null — there is no detection-path reasoning being suppressed or expanded, so the only thing differentiating A and B is verbosity style. Don't over-interpret.

**Confirmed:** Null result is interpretable. C=0/10 calibration holds. The specificity threshold is the operative constraint here.

## CC Decision
No fatal objections. CC synthesis accepted.

> **Exp-21b conclusion:** Orientation vocabulary in the system prompt (either Persona or Instructions) does not drive zombie-write detection. Vocabulary must name the specific failure mode or fix to reach the detection threshold. The slot may still matter as a secondary effect, but only above the specificity threshold.

Confirmed next experiments:
1. **Exp-22** (interrogative artifact vocabulary) — test H2 with directive artifact framing
2. **Exp-22b / exp-23** (Kleppmann-specific slot-swap) — clean H1/H2 test at specificity threshold
