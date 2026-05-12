# Narrative example — test list and one R-G-R cycle (language-agnostic)

This is a **story**, not live code. Replace names with project-native files and commands.

---

## Feature slice

Order totals should reflect **shipping** when weight exceeds a threshold.

---

## Test list (first step)

Created **before** the first RED:

```markdown
## Test list — shipping by weight

- [ ] total includes shipping line when weight > 10kg
- [ ] total excludes shipping when weight ≤ 10kg
- [ ] boundary: exactly 10kg (document expected rule)
```

Work proceeds **one open item at a time**. New ideas append new lines.

---

## First cycle (first list item)

### RED (local commit `test:`)

- Write **only** enough test to fail for the first bullet (Law 2) — e.g. assert **observable** total with weight 11kg.
- Run focused test command → **fails** (shipping not applied).
- Commit **tests only**:

```text
test: add spec for shipping over 10kg threshold
```

Mark the list item in progress in the summary; mark **[x] done** only after GREEN passes.

### GREEN (local commit `feat:`)

- Production code **only** to pass this test (Law 3), e.g. minimal rule in order total path; **fake** a fixed shipping amount if that is smallest.
- Run the same focused command → **passes**.
- Commit **production files only**:

```text
feat: apply shipping line when weight exceeds 10kg
```

### REFACTOR (local commit `refactor:`)

Goal: clarify threshold naming; **stay in** order-total / shipping helper code touched by GREEN — no unrelated modules.

- One extraction → run tests → green.
- One rename → run tests → green.
- On any red: **undo** last edit.

```text
refactor: clarify shipping threshold helper naming
```

Update test list: first bullet **[x] done**.

### Squash then push

Squash the three commits; title aligns with GREEN `feat:`. Push once.

---

## Next cycles

Pick the **next open** list item (e.g. weight ≤ 10kg), repeat R–G–R + squash. When **all** bullets are **[x]** and tests are green, the **slice is complete**.
