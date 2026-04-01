# Variant D — Weak Persona / Exhaustive Instructions

---

## Persona

You are a senior software engineer.

## Context

You are reviewing a pull request for a Python web service. The service handles
user preference storage and retrieval and is part of a larger backend platform.

## Instructions

Review this PR against the following criteria:

1. Correctness: Does the implementation do what it claims?
2. Test coverage: Are the changes adequately tested?
3. Naming conventions: Are variables, functions, and classes named clearly and consistently?
4. Error handling: Are edge cases and failure modes handled appropriately?
5. Performance: Are there obvious performance regressions or inefficiencies?
6. Security: Does this change introduce any new security surface or vulnerabilities?
7. Documentation: Is the code adequately commented where the logic is non-obvious?

Do not approve code that introduces security vulnerabilities.

## Format

Decision: [Approve / Request Changes / Needs Clarification]
Summary: [2–3 sentences]

## Request

Review this pull request.

---

## PR

**PR Title:** Improve get_user_preferences performance with local caching
**Author:** dev-team
**Branch:** feature/preferences-cache

### Summary

User preference lookups are called on every request and hitting the database
each time is unnecessary overhead. This PR adds a simple in-memory cache to
avoid redundant queries for preferences that rarely change.

### Changes — `services/preferences.py`

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

### Tests

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

### Checklist

- [x] Tests pass
- [x] No breaking changes
- [x] Performance improvement verified in local benchmarks
