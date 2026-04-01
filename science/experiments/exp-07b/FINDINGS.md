# exp-07b FINDINGS — Calibration Failure (v2)

**Status:** Calibration failure — data not used for analysis
**Date:** 2026-03-27
**Cost:** $1.3225 (30 runs × 3 variants × n=10)

---

## Result

I=0/10, J=0/10, C=0/10 on the zombie-write detection criterion.

## Diagnosis

Two real implementation bugs were inadvertently introduced in the calibrated code:

1. **`threading.Event.wait()` misuse** — `heartbeat_running.set()` at the start, then
   `while heartbeat_running.wait(timeout=N)`. Since the event starts set, `wait()` returns
   `True` immediately on every iteration — the heartbeat fires in a tight loop with no delay,
   hammering Redis continuously. Found as Critical by all variants. Both I-01 and J-10
   independently identified and correctly explained the bug.
2. **`ValidationError` uncaught** — `ReservationRequest(...)` can raise `pydantic.ValidationError`
   which propagates unhandled. The validation tests (`test_input_validation_rejects_*`) were
   asserting `result.success is False` but the implementation raises instead of returning.
   Found as a significant issue by multiple runs.

These real bugs were more visible than the intended zombie-write failure mode. All variants
found them before reaching the process-pause zombie write.

## Token Pattern

| Variant | Ceiling hits | Avg output |
|---------|-------------|------------|
| I (P_p) | 5/10 | ~2,380 |
| J (P_d) | 1/10 | ~2,213 |
| C (slot-swap) | 9/10 | ~2,497 |

Notably, C was generating *more* output than I. The Instructions-slot elaboration directive
("be tedious and thorough, do not let questionable design architectures go unscrutinized")
functions as a direct output-length driver. P_p identity framing drives search depth, not
elaboration volume. This is an independent behavioral observation — different mechanisms
acting on different parameters — but not the intended experimental finding.

## Action

Redesigned as exp-07c: fixed `Event.wait()` bug (correct `stop_event` pattern) and caught
`ValidationError`. Retained `get_stock()` outside the transaction as the zombie-write setup.
