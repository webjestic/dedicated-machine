# Exp-04 Scoring Guide

## Ground Truth

**Primary (root cause):** Race condition in `acquire_task()` — non-atomic check-then-act.

`db.query_one()` (SELECT) and `db.execute()` (UPDATE) are two separate operations.
Between them, a second worker can SELECT the same `pending` task, see it as unclaimed,
and proceed to UPDATE it as well. Both workers then hold a reference to the same task ID
and execute it independently, producing two completion records.

The symptom (duplicate completions with different worker IDs) maps exactly to this window.
The tests never catch it because they run a single worker sequentially — the race window
never opens.

The correct fix: atomic claim using `UPDATE ... WHERE status = 'pending' RETURNING id`
(PostgreSQL) or equivalent database-level locking (`SELECT FOR UPDATE`). The claim must
succeed or fail atomically; no SELECT-then-UPDATE pattern is safe under concurrent workers.

**Secondary (real but not the cause):**
`payload["user_ids"]` — no null/key guard. If `payload` is `None` or missing `user_ids`,
this raises `KeyError`/`TypeError`. Real defect, not contributing to the duplicate incident.

**Tertiary (real but not urgent):**
O(n²) deduplication in `execute_task()` — for each event row, scans the full `summary`
list. Should use a set for O(n). Real defect, not contributing to the incident.

---

## Primary Scoring — Detection

**Detected:** Race condition in `acquire_task()` identified as root cause. The non-atomic
SELECT + UPDATE pattern under concurrent workers must be named. Acceptable phrasings:
check-then-act, TOCTOU, non-atomic claim, race between SELECT and UPDATE, missing
`SELECT FOR UPDATE` or `UPDATE ... RETURNING`.

**Missed:** Race condition not mentioned. Secondary or tertiary issues named as root cause,
or no structural cause identified.

---

## Secondary Scoring — Convergence Position

For each detected run, record the ordinal position of the race condition finding:

| Position | Definition |
|----------|-----------|
| **1** | Race condition is the first finding named — leads the output |
| **2** | One other finding appears before the race condition |
| **3+** | Two or more findings appear before the race condition |

**Convergence score** = mean position across detected runs (lower = earlier = better).

Target prediction: A (Task Stakes) < B (Identity Stakes) ≈ C (No Stakes) on mean position.

---

## Tertiary Scoring — Output Character

For each run record:

| Field | Values |
|-------|--------|
| Detection | Yes / No |
| Convergence position | 1 / 2 / 3+ / N/A |
| Confidence framing | Definitive ("this is the cause") / Hedged ("this may be") / Listed ("one issue is") |
| Fix quality | Atomic fix named (SELECT FOR UPDATE / UPDATE RETURNING) / Generic ("use a lock") / Not provided |
| Secondary issues named | Yes (null check, O(n²)) / Partial / No |
| Output length (tokens) | From run record |

---

## Comparisons

### A vs. C — The Prioritizer Test (primary)

Same strong P_p. A has Task Stakes (urgency as scenario fact); C has no Stakes.

- **A convergence < C:** Task Stakes reinforce P_p's termination condition — urgency
  makes the model find the primary cause first and stop. Task Stakes = Prioritizer.
- **A ≈ C:** P_p's search algorithm already installs the correct priority. Task Stakes
  add nothing to ordering when P_p is strong. The prioritizer effect may only surface
  when P_p is weak or the consideration set has multiple valid candidates.
- **A convergence > C:** Task Stakes actively disrupted priority ordering — urgency
  caused the model to name visible issues first (fast, confident, wrong priority).
  This would be the most unexpected result.

### A vs. B — Stakes Type Test (primary)

Same strong P_p. A has Task Stakes (situational); B has Identity Stakes (reinforcement).

- **A convergence < B:** Stakes type matters. Task Stakes produce earlier convergence;
  Identity Stakes do not. The Prioritizer / Termination Inhibitor distinction is confirmed.
- **A ≈ B:** Stakes type doesn't matter when P_p is this strong. P_p's ordering is
  already correct regardless of how Stakes are framed.
- **B convergence < A:** Identity Stakes produced better ordering than Task Stakes.
  This would falsify the Prioritizer hypothesis and require a new model.

### B vs. C — Identity Stakes as Termination Inhibitor (secondary)

Exp-02 showed Identity Stakes extends output after a correct finding. Does it also
affect *ordering*, or only *length*?

- **B convergence ≈ C, B length > C:** Identity Stakes did not disrupt ordering but
  did extend output. Consistent with Termination Inhibitor: correct finding first,
  then additional enumeration.
- **B convergence > C:** Identity Stakes pushed visible secondary issues earlier.
  Amplifier energy went to enumerable surface issues before the structural cause.

### D — Falsification Run

Weak Persona + Task Stakes. Five runs sufficient for the falsification claim.

- **D misses race condition (0/10 or close):** Task Stakes cannot install the concurrency
  consideration set that P_p provides. Urgency terminates wrong-direction enumeration
  faster (names visible issues and stops) without ever reaching the race condition.
  Confirms: Task Stakes is a Prioritizer within the existing consideration set, not an
  extender of it.
- **D detects race condition:** Race condition is too surface-level — the non-atomic
  pattern is recognizable to a generic senior engineer. Redesign required.

---

## Scoring Sheet (per run)

Record for each run:
1. Detection: Yes / No
2. Convergence position: 1 / 2 / 3+ / N/A
3. Confidence: Definitive / Hedged / Listed
4. Fix quality: Atomic / Generic / None
5. Secondary issues named: Yes / Partial / No
6. Output length (tokens from run record)

Aggregate per variant:
- Detection rate (n/10)
- Mean convergence position (detected runs only)
- Confidence distribution (n definitive, n hedged, n listed)
- Mean output length
- Fix quality distribution
