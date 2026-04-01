# Exp-24 CC Decision

**Date:** 2026-03-30

## Objection Assessment

The Artifact Pointer Confound is accepted as a live alternative, not a fatal
objection to the primary finding.

The primary finding stands: assertional mechanism vocabulary does not kill
detection (8-9/10). The confound addresses the mechanism of detection, not
the detection itself. Whether the model "evaluates the assertion" or
"pattern-matches to the bug via vocabulary coordinates" — both interpretations
are consistent with the data. The operative variable (vocabulary specificity at
mechanism level) drives detection regardless of which explanation is correct.

What the confound does kill: the claim that "models evaluate specific technical
assertions." That's an over-mechanized claim that the data doesn't support.
The behavioral finding is sound; the mechanistic explanation is not.

## Pragmatic Force — Accepted with Narrowing

The pragmatic force boundary is now more complex than assertional vs.
interrogative:

1. **Vague outcome assertion** ("prevents zombie-write failure modes") →
   search terminator. Established exp-21a. Uncontested.
2. **Mechanism assertion** ("TTL + heartbeat ensures lock validity during GC
   pause") → does NOT terminate search. Established exp-24.
3. **Interrogative mechanism** ("Does this prevent stale writes?") → search
   activator. Established exp-22.

The confound (pointer vs. evaluation) means we cannot cleanly separate
"mechanism assertion overrides pragmatic force" from "mechanism vocabulary
redirects attention regardless of assertion." Both accounts predict the same
result in exp-24. Resolving experiment: exp-25 (Mechanism Decoy).

## H2 Status

Corroborated fifth time. Slot produces no observable differential at mechanism
vocabulary level in artifact framing. Content remains the operative variable.

## Next

- **Exp-25 (Mechanism Decoy):** Places a false mechanism assertion pointing to a
  non-buggy component. Resolves pointer vs. evaluation. Design required before
  build.
- Alternatively: accept current pragmatic force narrowing as sufficient for the
  paper and route to other open gaps (operationalization, few-shot confound).
  Exp-25 is a mechanistic refinement, not required for the behavioral claim.
