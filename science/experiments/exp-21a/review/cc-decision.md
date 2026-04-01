# Exp-21a CC Decision

## Objections Raised
1. **Design confound (Gemini, fatal):** Exp-21a changed both slot and pragmatic force simultaneously — cannot isolate slot effect. H2 remains unfalsified.
2. **Second-order critique alternative (Gemini):** The null result may reflect inability to scrutinize author claims, not pragmatic force per se. Exp-22 will distinguish.

## Decision: Accept fatal objection; narrow conclusion.

The experimental design was valid for exploring artifact vocabulary effects but cannot adjudicate H1/H2 due to the slot/force confound. The pragmatic force confound is real and accepted.

## Final Conclusion

> Vocabulary in the artifact PR description, framed as assertions of what the design prevents, does not drive zombie-write detection regardless of Persona type (P_p or P_d).
>
> This null result is best explained by pragmatic force: the model processes artifact claims as premises to evaluate rather than directives to search. The alternative explanation (second-order critique limitation) also accounts for the data and cannot be excluded.
>
> Exp-21a is informative but not adjudicative for H1/H2. The next experiment must inject directive vocabulary into the artifact with interrogative framing to test whether the artifact slot can support zombie-write detection when the force issue is addressed.

## Next Experiment

**Exp-22: Interrogative artifact vocabulary**

Design:
- Variant A (P_p generic): artifact PR description contains an open question: "**Reviewer note:** evaluate whether this architecture is susceptible to zombie-write failure modes in a GC stop-the-world pause scenario, and whether a fencing token at the DB write layer is required."
- Variant B (P_d generic): same artifact modification
- Variant C (P_d baseline): original artifact, no modification

If A and/or B > C: H2 gains support — content with directive force works regardless of slot.
If A = B = C = 0: the artifact slot is structurally degrading for this type of analytical reasoning.
