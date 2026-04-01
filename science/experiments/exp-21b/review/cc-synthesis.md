# Exp-21b CC Synthesis

## Results

| Variant | Final Score | Mean tokens |
|---------|-------------|-------------|
| A (P_p, orientation vocab in Persona) | 0/10 | 1048 |
| B (P_d, orientation vocab in Instructions) | 0/10 | 1113 |
| C (P_d baseline) | 0/10 | 1021 |

Calibration passed (C=0/10), though with the caveat that A=B=C=0 means calibration has no discriminating utility here.

Flagged items confirmed 0: A-06 (fix keyword, no pause), B-02/B-09 (pause keyword, no fix), B-05 (fix keyword, no pause). All were shallow partial matches — none described the zombie-write chain or recommended fencing token at the DB layer.

## Primary Finding

**Less directive orientation vocabulary in the system prompt drives zero detection — same as no vocabulary at all.**

The orientation vocabulary used in exp-21b ("lock lifecycle correctness", "process isolation boundaries", "temporal gap between lock acquisition and protected writes", "failure taxonomy of distributed coordination protocols") does not trigger identification of the zombie-write failure mode or the fencing token fix. All outputs remained in the "TTL/heartbeat concern only" bucket, finding TOCTOU races, instance-level concurrency bugs, and input validation gaps — but not the zombie-write causal chain.

## What This Means for the Vocabulary Specificity Finding

Exp-20 established that directive vocabulary naming the failure mode ("zombie-write failure modes", "fencing tokens") drives 9/10 detection when placed in the system prompt. Exp-21b establishes that orientation vocabulary that describes the problem domain without naming the failure mode drives 0/10.

This suggests a **specificity threshold effect**: vocabulary must name the specific failure mode or fix to trigger reliable detection. Domain-orientation language — even precise domain orientation — falls below the threshold. The model needs the exact concept label, not just the semantic neighborhood.

This has implications for the Persona slot theory:
- The P_p Persona in exp-19 ("distributed systems engineer with 10+ years of Kleppmann...") drove 10/10 detection WITHOUT naming zombie-write or fencing token
- Yet in exp-21b, equally precise domain orientation drives 0/10

Why the difference? The exp-19 Persona explicitly names "Kleppmann's critique of Redlock" — this is specific enough to activate the failure mode. "Lock lifecycle correctness" and "failure taxonomy of distributed coordination protocols" are too abstract to activate it.

## H1/H2 Status

**Neither H1 nor H2 is directly testable from this experiment.** The vocabulary is equally non-operative in Persona (A) and Instructions (B), so there is no discriminating signal. This confirms that vocabulary below the specificity threshold is inert regardless of slot — which is a valid constraint on both hypotheses.

**Emerging picture:**
- H2 (content is operative regardless of slot) requires high-specificity content
- The slot may matter as a secondary effect, but only when content is at or above the specificity threshold
- The pragmatic force of content (directive vs. assertion) is also a threshold variable

## Token Count Observation

B (1113) > A (1048) > C (1021). The B > A token ordering (Instructions > Persona for depth) is a reversal from exp-19 (P_p Persona >> Baseline) and aligns with the API token paradox from exp-20. With non-operative vocabulary, the Instructions slot may be driving slightly more verbose output without deeper detection — consistent with the exp-20 hypothesis that Instructions acts as an output-length driver while Persona acts as a reasoning filter.

However, the differences are within noise range (92-token spread across all three variants), so this observation requires replication.

## Next Steps

Two experiments are needed:

1. **Exp-22a (interrogative artifact vocabulary):** Inject directive vocabulary into the artifact with interrogative framing to test H2. Proposed design from Gemini's exp-21a review: add an open question or TODO to the PR: "Evaluate whether this is vulnerable to zombie-write failure modes during GC stop-the-world pauses."

2. **Exp-22b (Kleppmann-specific vocabulary slot-swap):** Replicate exp-20 but with Kleppmann-specific vocabulary ("Kleppmann's critique of Redlock", "process-pause zombie write") in Persona (A) vs Instructions (B) with a fresh artifact that doesn't have the vocabulary in the PR description. This is the cleanest possible H1/H2 test at the correct specificity level.

The key question remaining: does slot matter when vocabulary is at the specificity threshold?
