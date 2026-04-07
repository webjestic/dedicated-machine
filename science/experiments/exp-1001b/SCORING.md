# exp-1001 Scoring Rubric

## Method

Binary scoring per item per run. 1 = present and substantive, 0 = absent or present only as a heading with no content.

8 items. Max score per run: 8. Mean score per variant across 10 runs reported.

---

## Items

| # | Item | Criteria for PASS (1) |
|---|------|-----------------------|
| 1 | Signature validation | Correct HMAC-SHA256 implementation — validates signature against raw request body, not parsed body |
| 2 | Fast response | Returns 200 immediately; processing is async and not in the request path |
| 3 | Event queue | Names or implements a mechanism for queuing events for downstream processing |
| 4 | Input validation | Validates required headers (signature header, content-type) and rejects malformed requests with appropriate status codes |
| 5 | Replay protection | Addresses timestamp validation AND/OR event ID deduplication to prevent replay attacks |
| 6 | Dead-letter handling | Specifies what happens when event processing fails repeatedly — not just retry logic, but what happens on exhaustion |
| 7 | Signature failure alerting | Names a policy for alerting or logging on repeated signature failures (could indicate attack or key misconfiguration) |
| 8 | Secret rotation | Addresses how the signing secret is rotated without downtime |

---

## Sensitivity Target

Items 1–4 are expected at code-complete baseline — a strong Persona alone should reach these.

Items 5–8 are the operational gap targets:
- Replay protection (#5)
- Dead-letter handling (#6)
- Signature failure alerting (#7)
- Secret rotation (#8)

A meaningful stakes effect should move at least two of items 5–8 from near-zero in A to >50% in B.

---

## Hypothesis

**H1001:** Variant B (Persona + consequence naming stakes) will score higher than Variant A (Persona only), with the delta concentrated in items 5–8.

**Null:** No meaningful difference between A and B. The strong Persona carries the full effect; stakes adds no independent signal.
