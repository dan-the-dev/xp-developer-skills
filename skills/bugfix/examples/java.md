# Java Examples — Bugfix

These examples demonstrate safe bugfix workflows in Java repositories.

---

## Example 1 — Null User Status

User request:
"Application crashes when user status is null."

### Branch

bugfix/STR-601-null-user-status

### RED

```java
@Test
void returnsDefaultStatusWhenNull() {
    assertEquals("UNKNOWN", mapStatus(null));
}
```

Run:

```bash
./gradlew test
```

Result:
- failing

### GREEN

```java
if (status == null) {
    return "UNKNOWN";
}
```

### Verification

```bash
./gradlew test
```

Result:
- passing
