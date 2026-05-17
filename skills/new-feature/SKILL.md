---
name: new-feature
description: Slice a whole capability into ordered releasable increments (increment backlog in increments/<stem>.md). Delegate each slice to skills/new-increment. Use for an entire feature or epic (e.g. full FizzBuzz), not for implementing one increment.
allowed-tools: Read, Edit, MultiEdit, Bash, Grep, Glob
---

# New feature (increment planning)

## Mission

Plan a **whole feature** as **ordered, releasable increments**. **Implement** one increment at a time via **`skills/new-increment`** (ATDD + TDD per slice).

**First step:** create **`increments/<feature-stem>.md`** (see [references/increment-backlog.md](references/increment-backlog.md)).

**Not done until** every in-scope increment is `[x]` on that backlog — each completed via **`skills/new-increment`**.

---

## Workflow

1. Clarify capability and whole-feature definition of done.
2. If feasibility unknown → **`skills/spike`** on `spike/…` branch; promote before slicing.
3. Write **ordered** increment lines in `increments/<stem>.md`.
4. For the **next open** `[ ]` line only → hand off to **`skills/new-increment/SKILL.md`**.
5. Repeat until backlog complete.

See [examples/fizzbuzz-increments.md](examples/fizzbuzz-increments.md).

---

## Composition

| Need | Skill |
|------|--------|
| One slice delivery | **`skills/new-increment`** |
| Untested area | **`skills/legacy-testing`** (before or per increment) |
| Green prep | **`skills/refactoring`** |
| Unknown tech | **`skills/spike`** |

This skill does **not** run ATDD/TDD itself — **`new-increment`** does.

---

## Anti-patterns

- One backlog line for the entire feature
- Implementing multiple `[ ]` increments without finishing one
- No on-disk `increments/` file

See [references/anti-patterns.md](references/anti-patterns.md).

---

## Additional resources

- [references/increment-backlog.md](references/increment-backlog.md)
- [references/slicing-increments.md](references/slicing-increments.md)
- [references/anti-patterns.md](references/anti-patterns.md)
- [examples/fizzbuzz-increments.md](examples/fizzbuzz-increments.md)
