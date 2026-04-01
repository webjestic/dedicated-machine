# CC Synthesis — exp-19

## Result

A: 10/10 | B: 10/10 | C: 0/10
Mean tokens: A = 1199, B = 1193, C = 1026
Gap A vs B: 6 tokens (noise floor ~125 tokens per Phase 6)

## What the data shows

Calibration held on both ends. A hit ceiling (10/10), C held floor (0/10). The experimental design is interpretable.

B matched A exactly — 10/10 detection with identical token depth. The procedural content installed in the Instructions slot is as effective as the same content embedded in the Persona slot. The 6-token gap between A and B is within noise and does not constitute a meaningful difference.

The evidence supports H2: procedural content is the operative variable. The Persona slot is not providing independent architectural lift when the Instructions slot carries identical procedural content.

## What this changes

This is the first clean slot-swap test against this artifact. Phase 4 introduced H2 as a confound (exp-12 through exp-15 showed domain vocabulary and procedural framing could carry detection without a strong P_p Persona). Exp-19 formalizes that finding against a calibrated binary detection task.

Prior to exp-19, the strongest counter-argument to slot-load-bearing was: "we haven't tested the same procedural content in both slots cleanly." We have now. The result is B = A.

## What this does not close

1. **The novel synthesis question.** Gemini names the right open question: does the slot distinction become load-bearing when the task requires synthesis beyond explicit procedural instruction? Exp-19 used a well-defined two-condition detection (pause scenario + fix). If the task required the model to discover what those conditions are rather than apply them, the slot might matter. That is a different experiment.

2. **The content-as-installer question.** Does the procedural content in the Instructions slot install a persistent consideration-set shift, or does it act as in-context guidance only? Exp-19 can't distinguish between "B found the bug because the instructions guided it there" and "B found the bug because the instructions altered its search algorithm for this session." Both produce the same output.

3. **The weak-content boundary.** Exp-19 used maximally explicit procedural content. We don't know where the threshold is — at what level of instruction specificity does slot placement start to matter?

## Recommendation

Update `pcsieftr.md` to record exp-19 as H2 corroboration: slot-swap under clean calibration conditions confirms content as operative variable. Do not retire H1 entirely — the novel synthesis question remains open and is the right target for exp-20.

Proposed exp-20 design: same zombie-write artifact, but with instructions stripped to domain vocabulary only (no procedure). A = P_p (vocabulary embedded in identity), B = P_d + vocabulary list in Instructions, C = P_d baseline. If slot matters at all, it should appear when the content provides orientation without procedure.
