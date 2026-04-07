# exp-35 Scoring Rubric

## Tier 1.0 (full credit)

All three criteria must be present:

1. **GC pause trigger named:** The output explicitly identifies a GC pause, slow external
   call, I/O stall, or equivalent process-level stall exceeding the lock TTL as the trigger
   for the zombie-write scenario. "Lock can expire" alone is insufficient — the output must
   name the class of stall that causes it.

2. **Fencing token / optimistic concurrency named as architectural fix:** The output
   explicitly names a fencing token, monotonic counter, or conditional write at the
   database boundary as the required fix. Phrasing equivalents: "WHERE lock_version = N",
   "UPDATE ... WHERE fencing_token = ?", "optimistic concurrency at the DB write boundary."

3. **threading.Event distinguished as insufficient:** The output must explicitly distinguish
   a threading.Event / in-process signal as necessary but insufficient — i.e., "Tier 0.5"
   reasoning. Outputs that name threading.Event as *the* fix without naming the DB-boundary
   fencing requirement do not meet this criterion.

## Tier 0.5

- Zombie-write scenario correctly identified (GC pause trigger named)
- threading.Event signaling named as the fix
- Fencing token / DB-boundary fix NOT named

## Tier 0

- Zombie-write scenario not identified, or identified without the GC pause trigger
- Code approved without identifying the zombie-write scenario

---

## Comparison Reference

| Experiment | Variant | Persona | Instructions content | n | Tier 1.0 |
|---|---|---|---|---|---|
| exp-09 | A | P_d (credential + disposition) | Generic | 40 | 1/10 |
| exp-34 | A | P_p (termination in Persona) | Generic + termination condition | 10 | 10/10 |
| exp-35 | A | P_d (credential only) | Strong CoT (all P_p content) | 10 | — |
| exp-35 | B | P_p (identical to exp-34 A) | Generic + termination condition | 10 | — |

The critical comparison is exp-35 A vs. exp-35 B (within-experiment) and exp-35 A vs.
exp-09 A (same P_d persona, different Instructions specificity).
