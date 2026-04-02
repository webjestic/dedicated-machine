# SCORING — exp-31

## Correct Answer

**Variant A**
```json
{
    "Pp": [2, 4, 6, 8, 10],
    "Pd": [1, 3, 5, 7, 9]
}
```

**Variant B**
```json
{
    "Pp": [2, 4, 7, 9],
    "Pd": [1, 3, 5, 6, 8, 10]
}
```

## Scoring Per Run

One point per correctly placed number. Maximum score: 10.

A number is correct if and only if it appears in the right array. A number in the wrong array scores 0 regardless of which array it landed in.

| Score | Meaning |
|-------|---------|
| 10/10 | Perfect — all statements correctly classified |
| 8–9   | One misclassification |
| 6–7   | Two misclassifications |
| <6    | Prompt or reference is not holding |

## Format Compliance

If the model returns anything other than valid JSON matching the schema, the run scores 0 regardless of content. Prose wrapping the JSON is a format failure.

## Statement Key — Variant A

| # | Type | Reveal |
|---|------|--------|
| 1 | P_d | credential + orientation, no convergence target |
| 2 | P_p | "check whether every code path that can throw returns the error to the caller before closing" |
| 3 | P_d | disposition ("meticulous and thorough"), "catches every bug" is outcome assertion not mechanism |
| 4 | P_p | "flag every clause where liability is uncapped or indemnification runs one-sided" |
| 5 | P_d | credential + "strong instinct" — orientation vocabulary |
| 6 | P_p | "confirm the health check interval is shorter than the load balancer's timeout" |
| 7 | P_d | credential + disposition ("passion for finding") |
| 8 | P_p | "verify every index on the old schema has a corresponding index on the new one" |
| 9 | P_d | credential + disposition ("detail-oriented") |
| 10 | P_p | "identify every place where shared state is mutated without a lock held for the full duration" |

## Statement Key — Variant C

Sourced from actual experimental variants. exp-23 personas were identical ("You are a senior software engineer") — slots replaced with exp-28c/A and exp-26/B (both P_p).

| # | Source | Type | Reveal |
|---|--------|------|--------|
| 1 | exp-28d/A | P_d | Rich mechanism vocabulary + specific failure modes, but "that is the bar" is orientation — no termination condition named |
| 2 | exp-28d/B | P_p | "is complete only when I have identified what is required to run this rate limiter safely in production" |
| 3 | exp-28c/B | P_p | "My review is complete only when I have identified what is required..." |
| 4 | exp-28b/A | P_d | Credential + experience, no termination condition |
| 5 | exp-27/B  | P_d | Credential + "You know what production blockchain infrastructure actually requires" — orientation |
| 6 | exp-27/C  | P_p | Identical to 5 + "My implementation is complete only when..." — termination condition added |
| 7 | exp-26/A  | P_p | Prohibition installs a specific check: find code where GC pause could expire the lock |
| 8 | exp-24/B  | P_d | Mechanism vocabulary ("stop-the-world GC pauses," "distributed lock expiry") inside dispositional frame — hardest case |
| 9 | exp-28c/A | P_p | "My review is complete only when I have identified what is required..." |
| 10| exp-26/B  | P_p | "My review is complete only when I can confirm that an unbounded process suspension or GC pause cannot cause the distributed lock to expire..." |

**Correct answer:**
```json
{
    "Pp": [2, 3, 6, 7, 9, 10],
    "Pd": [1, 4, 5, 8]
}
```

Key stress cases: 1 (mechanism vocab, no termination), 5 vs 6 (identical except termination condition), 7 (prohibition framing), 8 (mechanism vocab in dispositional frame).

---

## Statement Key — Variant B

| # | Type | Reveal |
|---|------|--------|
| 1 | P_d | disposition ("passionate," "detail-oriented," "takes pride") — no convergence target |
| 2 | P_p | "verify every endpoint that mutates state requires an authentication header" |
| 3 | P_d | credential + "deep intuition" — orientation vocabulary |
| 4 | P_p | "confirm every layer that installs packages also clears the package cache in the same RUN command" |
| 5 | P_d | credential + "talent for spotting" — sounds procedural but names no specific thing to find |
| 6 | P_d | disposition ("creative and versatile") + "adapts tone" — no convergence target |
| 7 | P_p | "identify every state update that runs without checking whether the component is still mounted" |
| 8 | P_d | credential + "strong statistical instincts" + "rigorous analytical mindset" — all orientation |
| 9 | P_p | "flag every field marked optional that the calling code treats as guaranteed present" |
| 10 | P_d | "deeply committed to finding vulnerabilities" — disposition + outcome framing, no mechanism |
