# Pull Request #312 — Add user profile update endpoint

**Author:** dev-rchen
**Branch:** `feature/profile-update` → `main`
**Description:**
Adds a PATCH endpoint for the account settings page, allowing users to update their
profile settings. Uses a new `update()` helper on the User model to apply the changes.
Auth is handled by the existing `@login_required` decorator.

**Changes:** 2 files — `api/users.py`, `tests/test_users.py`

**CI Status:** ✅ All 18 tests passed (3 new, 15 existing)
**Lint:** ✅ Clean
**Coverage:** 89% (unchanged)

---

## Diff

### `api/users.py`

```python
 from flask import Blueprint, jsonify, request
 from flask_login import login_required, current_user
 from functools import wraps
 from .db import db
 from .models import User

 users_bp = Blueprint('users', __name__)


 def admin_required(f):
     @wraps(f)
     def decorated(*args, **kwargs):
         if not current_user.role == 'admin':
             return jsonify({'error': 'Forbidden'}), 403
         return f(*args, **kwargs)
     return decorated


 @users_bp.route('/api/users/<int:user_id>')
 @login_required
 def get_user(user_id):
     user = User.query.get_or_404(user_id)
     return jsonify(user.to_dict())


+@users_bp.route('/api/users/<int:user_id>/profile', methods=['PATCH'])
+@login_required
+def update_user_profile(user_id):
+    """Update profile fields for a user. Used by the account settings page."""
+    user = User.query.get_or_404(user_id)
+    data = request.get_json() or {}
+    if not data:
+        return jsonify({'error': 'No data provided'}), 400
+
+    user.update(**data)
+    db.session.commit()
+    return jsonify(user.to_dict())
```

### `api/models.py` (excerpt — new method only)

```python
+    def update(self, **kwargs):
+        """Apply field updates from a dict of key-value pairs."""
+        for key, value in kwargs.items():
+            setattr(self, key, value)
```

### `tests/test_users.py`

```python
+def test_update_profile_display_name(client, seed_users, user_headers):
+    rv = client.patch(
+        '/api/users/1/profile',
+        json={'display_name': 'Alice Smith'},
+        headers=user_headers
+    )
+    assert rv.status_code == 200
+    assert rv.get_json()['display_name'] == 'Alice Smith'
+
+
+def test_update_profile_bio(client, seed_users, user_headers):
+    rv = client.patch(
+        '/api/users/1/profile',
+        json={'bio': 'Backend engineer at obotix'},
+        headers=user_headers
+    )
+    assert rv.status_code == 200
+    assert rv.get_json()['bio'] == 'Backend engineer at obotix'
+
+
+def test_update_profile_empty_body_returns_400(client, seed_users, user_headers):
+    rv = client.patch(
+        '/api/users/1/profile',
+        json={},
+        headers=user_headers
+    )
+    assert rv.status_code == 400
```

---

## Reviewer Notes

Straightforward settings-page endpoint. `@login_required` is in place. The `update()`
helper keeps the endpoint clean — the model handles which fields are relevant. Tests
cover the primary update paths and the empty-body error case.
