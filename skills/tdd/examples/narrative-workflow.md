# Narrative example — one R-G-R cycle (language-agnostic)

This is a **story**, not live code. Replace names with project-native files and commands.

---

## Increment

Validate that an order total **includes** a shipping line when weight exceeds a threshold.

---

### RED (local commit `test:`)

- Add one test that asserts **observable** totals (not internal shipping flags): e.g. `order total includes shipping when weight > 10kg`.
- Run focused test command → **fails** (shipping not applied).
- Commit **tests only**:

```text
test: add spec for shipping over 10kg threshold
```

---

### GREEN (local commit `feat:`)

- Implement the minimum in the domain module (e.g. add shipping line when rule matches). It is acceptable to **fake** a constant shipping amount first if that is the smallest step; follow with another RED if triangulation is needed.
- Run the same focused command → **passes**.
- Commit **production files only**:

```text
feat: apply shipping line when weight exceeds 10kg
```

---

### REFACTOR (local commit `refactor:`)

Goal: clarify threshold comparison and names; **behavior unchanged**.

- Extract helper for threshold: **one** extraction → run tests → green.
- Rename for clarity: **one** rename → run tests → green.
- If any step fails: **undo** that step, take a smaller change, repeat.

Commit only when the refactor slice is complete and still green:

```text
refactor: clarify shipping threshold helper naming
```

---

### Squash then push

Squash the three commits into one titled like GREEN:

```text
feat: apply shipping line when weight exceeds 10kg
```

Body may mention the new spec and refactor note.

Push **once** with the squashed commit on the branch.

---

### Next cycle

Pick the **next** behavior (e.g. boundary at exactly 10kg) and repeat the same micro-commit and squash pattern.
