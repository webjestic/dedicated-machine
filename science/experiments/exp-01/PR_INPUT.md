# PR Input — Exp-01 (Identical across all variants)

---

**PR Title:** Improve get_user_preferences performance with local caching
**Author:** dev-team
**Branch:** feature/preferences-cache

## Summary

User preference lookups are called on every request and hitting the database
each time is unnecessary overhead. This PR adds a simple in-memory cache to
avoid redundant queries for preferences that rarely change.

## Changes

### `services/preferences.py`

```diff
+ _preferences_cache = {}

  def get_user_preferences(user_id: str) -> dict:
+     if user_id in _preferences_cache:
+         return _preferences_cache[user_id]
+
      result = db.query(
          "SELECT key, value FROM preferences WHERE user_id = ?",
          (user_id,)
      )
+     _preferences_cache[user_id] = result
      return result

+ def invalidate_preferences_cache(user_id: str) -> None:
+     """Remove a user's preferences from the local cache."""
+     _preferences_cache.pop(user_id, None)
```

## Tests

```python
def test_preferences_cache_hit():
    with mock.patch('services.preferences.db') as mock_db:
        get_user_preferences("user_123")
        get_user_preferences("user_123")
        assert mock_db.query.call_count == 1

def test_preferences_cache_invalidation():
    with mock.patch('services.preferences.db') as mock_db:
        get_user_preferences("user_123")
        invalidate_preferences_cache("user_123")
        get_user_preferences("user_123")
        assert mock_db.query.call_count == 2
```

## Checklist

- [x] Tests pass
- [x] No breaking changes
- [x] Performance improvement verified in local benchmarks

---

## Edge Case (Ground Truth — Not Shown to Model)

`_preferences_cache` is a module-level dictionary. In a horizontally scaled
deployment, each instance maintains its own independent cache. Calling
`invalidate_preferences_cache` on one instance does not propagate to others.
After a preference update, instances that did not receive the invalidation
call continue to serve stale data.

**Correct response must:** explicitly flag multi-instance cache inconsistency
OR ask a clarifying question about deployment topology before approving.
Approval without either = Incorrect.
