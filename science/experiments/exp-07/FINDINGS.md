# exp-07 FINDINGS — Calibration Failure (v1)

**Status:** Calibration failure — data not used for analysis
**Date:** 2026-03-27
**Cost:** $1.2920 (30 runs × 3 variants × n=10)

---

## Result

I=0/10, J=0/10, C=0/10 on the zombie-write detection criterion.

## Diagnosis

The PR code contained multiple obvious implementation bugs that overshadowed the intended
hidden failure mode:

1. **Instance-level heartbeat state** — `_heartbeat_active` and `_heartbeat_thread` stored
   on the `InventoryService` instance, not scoped to the lock context. Fatal under concurrent
   requests sharing the same service instance. Found as #1 Critical by all variants.
2. **Non-atomic lock release (TOCTOU)** — `GET` + `DELETE` in sequence; another process can
   acquire the lock between the two calls. Found as #2 Critical by all variants.
3. **Non-atomic DB operations** — `update_stock` and `create_order` called sequentially with
   no transaction wrapper. Found by most variants.
4. **Missing input validation** — raw primitives passed with no bounds checks.

All variants found these bugs before reaching the intended zombie-write failure mode (process
pause causing lock expiry, main thread resuming with stale stock read).

## Token Pattern

| Variant | Ceiling hits | Notes |
|---------|-------------|-------|
| I (P_p) | 8/10 | Generating max output due to volume of bugs found |
| J (P_d) | 0/10 | Shorter outputs, variable |
| C (slot-swap) | 9/10 | Consistently generating max output |

High ceiling hits for I and C reflected volume of bugs found, not depth on zombie write.

## Action

Redesigned as exp-07b: fixed all identified bugs, retained only zombie write as hidden failure.
