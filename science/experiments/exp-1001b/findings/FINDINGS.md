# exp-1001b Findings — Stakes as Voltage: Consequence Naming Against Weak Persona (P_d)

**Status:** Complete
**Result:** Null. A (6.6/8) ≈ B (6.4/8). Stakes provides no lift against a weak Persona.
**H1001b:** Not supported.

---

## Score

Scores corrected from initial grep pass. Item 6 false positives identified and removed (see Methodology Note below).

| Item | Criteria | A (10 runs) | B (10 runs) |
|------|----------|-------------|-------------|
| 1 | Signature validation (HMAC, raw body) | 10/10 | 10/10 |
| 2 | Fast response (200 before processing) | 10/10 | 10/10 |
| 3 | Event queue | 10/10 | 10/10 |
| 4 | Input validation (headers, reject malformed) | 10/10 | 10/10 |
| 5 | Replay protection | 10/10 | 10/10 |
| 6 | Dead-letter handling | 1/10 | 1/10 |
| 7 | Signature failure alerting | 7/10 | 5/10 |
| 8 | Secret rotation | 8/10 | 8/10 |
| **Mean score** | | **6.6/8** | **6.4/8** |

---

## Methodology Note: Item 6 False Positives

Initial scoring of Item 6 used the pattern `dead.letter|DLQ|exhaustion|max.retries|poison|unprocessable|failed.event`. The term "exhaustion" produced false positives — it matched "memory exhaustion" in the context of body size limits and slow-loris attack mitigation, not dead-letter handling. Corrected scoring uses only explicit dead-letter or DLQ terminology with surrounding context verification.

Additionally, several files list a "Queue Failure and Dead-Letter Handling" section in a table of contents but never reach it — the token budget is exhausted before the section is generated. ToC-only hits scored as MISS.

Corrected Item 6: **A: 1/10, B: 1/10** (tied at near-zero).

---

## What Happened

H1001b predicted that consequence naming stakes would lift coverage on sensitivity-target items (5–8) when the Persona is weak (P_d baseline). It did not.

Both variants saturated items 1–5 at 10/10. Neither variant reliably covered item 6 (dead-letter). On items 7 and 8, A matched or outperformed B. There is no item where Stakes produced meaningful lift over Persona-only.

---

## The Artifact Confound

The central finding of exp-1001b is not about stakes. It is about the artifact.

The ARTIFACT explicitly enumerates four requirements: HMAC-SHA256 signature validation, immediate 200 response, event queuing, single containerized service. The INSTRUCTIONS add "Cover the operational layer." Together, these install the consideration set — the model arrives at the task carrying replay protection, secret rotation, and alerting as targets to address, because the task context names them or directly implies them.

This means the P_d Persona ("You are a senior backend engineer. You are thorough and experienced.") is not doing the work on items 1–5 and 8. The artifact is.

**Evidence:** Items 1–5 hit 10/10 for both A and B. These are the items explicitly required by or directly implied from the artifact text. Item 6 (dead-letter) — the one item not covered by the artifact and not directly implied by "operational layer" — hits 1/10 for both variants.

The experiment was not testing Persona effects. It was testing instruction-following. Both conditions followed instructions equally well.

---

## Comparison to exp-1001

| Condition | exp-1001 A | exp-1001 B | exp-1001b A | exp-1001b B |
|-----------|-----------|-----------|------------|------------|
| Persona | P_p (mechanism) | P_p (mechanism) | P_d (credential) | P_d (credential) |
| Stakes | None | Consequence naming | None | Consequence naming |
| Mean score | 7.8/8* | 7.0/8* | 6.6/8 | 6.4/8 |

*exp-1001 scores used the same lenient grep methodology and carry the same Item 6 false positive issue. Direct comparison should be treated with caution.

The pattern is consistent across both experiments: Stakes shows no lift and applies a small depth tax (Item 7: A beats B in both experiments). The strong Persona in exp-1001 does appear to add some signal relative to the weak Persona in exp-1001b (7.8 vs 6.6), but the comparison is confounded by the same grep methodology issue.

---

## The Token Ceiling Is the Dominant Variable

Every single run — all 20 across both variants — hit exactly 3000 output tokens. `max_tokens=3000` was the exit condition in 100% of runs. The model never finished naturally.

This is visible in the raw outputs. Most runs open with a full Table of Contents listing 10–14 planned sections, including the sensitivity-target items. A-02's ToC includes `2.7 Alerting`, `2.8 Secret Management`, `2.11 Queue Operational Concerns`, `2.12 Failure Modes and Recovery`. The model had the full consideration set — it just never generated those sections before the wall.

**The scoring was measuring how far the model got before 3000 tokens, not what the model knew.** Items at the end of the generation order (dead-letter, alerting, secret rotation) are systematically penalized. The ToC is a better signal of the model's true coverage than the scored sections are.

The low dead-letter score (1/10 both variants) is not evidence that the model doesn't know about dead-letter handling. It is evidence that dead-letter handling appears late in the model's natural generation order, and 3000 tokens isn't enough to get there.

---

## The Genuine Gap: Item 6

Dead-letter handling is the single item neither Persona strength nor Stakes reliably installs. It requires the model to reach a specific operational concept — what happens when event processing fails repeatedly — that is not implied by the artifact requirements or the "Cover the operational layer" instruction.

Both variants reached it in only 1 of 10 runs. This is the genuine operational gap in this experimental design. Though it is impossible to fully separate from the token ceiling effect — dead-letter may also simply be generated late.

---

## Depth Tax: Still Present

Stakes again increased per-section verbosity without increasing coverage. Item 7 (signature failure alerting): A at 7/10, B at 5/10. B outputs consistently generate more elaborate preambles and failure-mode rationale per section, consuming token budget before reaching alerting and, in some cases, full secret rotation substance. This replicates the exp-1001 finding.

---

## What This Means for the Research Program

The 1001 series was designed to isolate stakes as an independent variable. The artifact design undermined the isolation. When the artifact explicitly names the requirements, the model's consideration set is installed by the artifact regardless of what the Persona carries.

**The correct interpretation of the null result in both exp-1001 and exp-1001b:** Stakes has no lift when instructions or artifacts already install the consideration set. This is consistent with the Dedicated Machine hypothesis — the machine terminates at the first satisfying path; if the path is already fully specified by the task context, no amplification of stakes or Persona changes the output.

---

## Next Experiment Design

To test stakes as an independent voltage source requires:

1. **A sparse artifact** — task description that does not enumerate requirements. "Build a webhook receiver" rather than "Build a webhook receiver with HMAC-SHA256, 200 response, event queuing, and containerization."

2. **Stripped instructions** — no "Cover the operational layer" directive. Instructions must not name the missing categories.

3. **Persona held constant** — isolate one variable at a time.

The question is then: in the absence of explicit guidance, does consequence naming change where the machine stops?

---

## Cost

- exp-1001b: 20 runs, claude-sonnet-4-6, temperature=0.5, max_tokens=3000
- Estimated cost: ~$0.60
- Total 1001 series (all iterations): ~$4.35
