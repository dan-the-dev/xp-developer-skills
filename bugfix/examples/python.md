# Python Examples — Bugfix

These examples demonstrate safe bugfix workflows in Python repositories.

---

## Example 1 — Division by Zero

User request:
"Analytics endpoint crashes when total users is zero."

### Branch

bugfix/STR-411-zero-user-percentage

### RED

```python
def test_returns_zero_when_total_users_is_zero():
    assert calculate_percentage(10, 0) == 0
```

Run:

```bash
pytest analytics/tests/test_percentage.py
```

Result:

- failing

### GREEN

```python
if total_users == 0:
    return 0
```

### Verification

```bash
pytest analytics/tests/test_percentage.py
pytest analytics/tests
```

Result:

- passing
