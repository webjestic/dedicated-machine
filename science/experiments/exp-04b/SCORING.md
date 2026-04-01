# Exp-04b Scoring Guide

## Ground Truth

**Primary (root cause):** Race condition in `acquire_task()` — non-atomic check-then-act.

`db.query_one()` (SELECT) and `db.execute()` (UPDATE) are two separate operations. Between
them, a second worker can SELECT the same `pending` task, see it as unclaimed, and proceed
to UPDATE it as well. Both workers then hold a reference to the same task ID and execute it
independently. Both then attempt to INSERT into `task_results` with the same `task_id`,
triggering `IntegrityError: UNIQUE constraint failed: task_results.task_id`.

The error is the downstream symptom of two workers completing the same task. The root cause
is the non-atomic claim in `acquire_task()`, not the ORM upgrade or connection pool change.
The tests never catch it because they run a single worker sequentially — the race window
never opens.

The correct fix: atomic claim using `UPDATE ... WHERE status = 'pending' RETURNING id`
(PostgreSQL) or `SELECT FOR UPDATE` (most databases). The claim must succeed or fail
atomically; no SELECT-then-UPDATE pattern is safe under concurrent workers.

**Wrong-direction candidate (weak Persona trap):** ORM/connection pool attribution.

The scenario states: "Migrated from per-worker connections to a shared connection pool
using db-pool 2.1. ORM upgraded from version 2.8.4 to 3.2.1." This is the planted
breadcrumb. A weak Persona following the scenario context may attribute the IntegrityError
to ORM transaction handling differences, connection pool isolation behavior, or a version
incompatibility between db-pool 2.1 and the ORM — all plausible, all wrong.

**Calibration target:** Variant D (weak Persona + Task Stakes) should produce ORM/pool
attribution rather than identifying the non-atomic claim. If D detects the race condition,
the breadcrumb is insufficient and exp-04c requires a stronger decoupling.

**Secondary (real but not the cause):**
`payload["user_ids"]` — no null/key guard. If `payload` is `None` or missing `user_ids`,
this raises `KeyError`/`TypeError`. Real defect, not contributing to the IntegrityError.

**Tertiary (real but not urgent):**
O(n²) deduplication in `execute_task()` — for each event row, scans the full `summary`
list. Should use a set for O(n). Real defect, not contributing to the incident.

---

## Primary Scoring — Detection

**Detected:** Race condition in `acquire_task()` identified as root cause. The non-atomic
SELECT + UPDATE pattern under concurrent workers must be named. Acceptable phrasings:
check-then-act, TOCTOU, non-atomic claim, race between SELECT and UPDATE, missing
`SELECT FOR UPDATE` or `UPDATE ... RETURNING`.

**Wrong direction (ORM/pool attribution):** Model attributes the IntegrityError to the
ORM upgrade, connection pool change, transaction isolation differences, or db-pool 2.1
behavior. Does not identify the non-atomic claim as the root cause.

**Missed:** Neither root cause identified. Generic or unclear response.

---

## Secondary Scoring — Convergence Position

For each detected run, record the ordinal position of the race condition finding:

| Position | Definition |
|----------|-----------|\
| **1** | Race condition is the first finding named — leads the output |
| **2** | One other finding appears before the race condition |
| **3+** | Two or more findings appear before the race condition |

**Convergence score** = mean position across detected runs (lower = earlier = better).

---

## Tertiary Scoring — Output Character

For each run record:

| Field | Values |
|-------|--------|
| Detection | Race condition / ORM-pool / Neither |
| Convergence position | 1 / 2 / 3+ / N/A |
| Confidence framing | Definitive / Hedged / Listed |
| Fix quality | Atomic fix named (SELECT FOR UPDATE / UPDATE RETURNING) / Generic ("use a lock") / Not provided |
| Secondary issues named | O(n²) / null guard / both / neither |
| Output length (tokens) | From run record |

---

## Comparisons

### A vs. C — Prioritizer / Entropy Brake Test (primary)

Same strong P_p. A has Task Stakes (urgency framing); C has no Stakes.

- **A and C both detect at position 1:** P_p's search algorithm installs the correct
  ordering regardless of Stakes type. Stakes type differentiation appears in termination
  behavior (output length, secondary coverage), not convergence position. Consistent
  with exp-04 finding.
- **A mean tokens < C mean tokens:** Task Stakes suppresses secondary enumeration after
  the primary finding. Entropy Brake confirmed.
- **A convergence < C:** Task Stakes also shifted ordering — would suggest Stakes can
  affect convergence position when the scenario is better calibrated.

### D — Falsification Run (primary)

Weak Persona + Task Stakes. 10 runs.

- **D misses race condition, attributes to ORM/pool:** Calibration successful. The
  scenario context is decoupled enough that weak Persona follows the breadcrumb.
  Task Stakes cannot extend the consideration set — it only shapes termination within
  whatever reasoning the Persona can reach.
- **D detects race condition:** Calibration failure again. The non-atomic SELECT+UPDATE
  pattern is still above weak Persona's detection floor with this scenario. Requires
  further scenario decoupling or a genuinely subtler vulnerability in the code.

### A vs. B — Stakes Type Test (secondary)

Same strong P_p. A has Task Stakes; B has Identity Stakes.

- **A mean tokens < B mean tokens, A secondary coverage < B secondary coverage:**
  Entropy Brake (A) vs. Termination Inhibitor (B) reconfirmed on a calibrated scenario.
  The secondary coverage ordering from exp-04 should replicate.

---

## Scoring Sheet (per run)

Record for each run:
1. Detection: Race condition / ORM-pool attribution / Neither
2. Convergence position: 1 / 2 / 3+ / N/A
3. Confidence: Definitive / Hedged / Listed
4. Fix quality: Atomic / Generic / None
5. Secondary issues named: O(n²) / null guard / both / neither
6. Output length (tokens from run record)

Aggregate per variant:
- Detection rate by type (n race condition, n ORM-pool, n neither)
- Mean convergence position (detected runs only)
- Confidence distribution
- Mean output length
- Secondary coverage rates
