---
name: new-feature
description: Slice a whole capability into ordered releasable increments (increment backlog in increments/<stem>.md). Delegate each slice to skills/new-increment — do not implement slices yourself. Use for an entire feature or epic (e.g. full FizzBuzz), not for implementing one increment.
allowed-tools: Read, Edit, MultiEdit, Bash, Grep, Glob
---

# New feature (increment planning)

## Mission

Plan a **whole feature** as **ordered, releasable increments**. **Do not implement** slices in this skill — each open line is delivered by **`skills/new-increment`** (or the **`new-increment`** subagent) in a **separate** invocation.

**First step:** create **`increments/<feature-stem>.md`** (see [references/increment-backlog.md](references/increment-backlog.md)).

**Feature complete** when every in-scope increment is `[x]` on that backlog — each line completed via **`skills/new-increment`**, not by continuing in this session.

---

## Workflow

1. Clarify capability and whole-feature definition of done.
2. If feasibility unknown → **`skills/spike`** on `spike/…` branch; promote before slicing.
3. Write **ordered** increment lines in `increments/<stem>.md` (all `[ ]` initially).
4. **Stop.** Hand off the **first** open line to **`skills/new-increment`** (subagent or new chat).
5. After each increment completes elsewhere, repeat planning-only check: next open line → hand off again.

Optional: create **`test-lists/<feature-stem>.md`** with empty `## <increment-slug>` headings as a skeleton — **no** behavior lines or `[x]` until **new-increment** runs.

See [examples/fizzbuzz-increments.md](examples/fizzbuzz-increments.md).

---

## What this skill may edit

| Allowed | Forbidden |
|---------|-----------|
| `increments/<stem>.md` | `src/`, `test/`, `tests/` |
| Optional skeleton `test-lists/<feature-stem>.md` (headings only) | `acceptance-examples/` (created per increment in **new-increment**) |
| Docs clarifying scope | Production or test code |

---

## Composition

| Need | Skill |
|------|--------|
| One slice delivery | **`skills/new-increment`** |
| Untested area | **`skills/legacy-testing`** (before or per increment) |
| Green prep | **`skills/refactoring`** |
| Unknown tech | **`skills/spike`** |

This skill does **not** run ATDD/TDD or mark increments `[x]` from implementation work.

---

## User opt-in: implement all increments

Only if the user **explicitly** asks to implement the full backlog in one go:

- Still use **one increment’s discipline at a time** (RED gates, one backlog `[x]` per slice).
- Prefer invoking **`new-increment`** repeatedly over batching “increments 2–7.”
- Default remains: **one increment per subagent/session.**

---

## Anti-patterns

- One backlog line for the entire feature
- Implementing code or tests in the **new-feature** session
- Marking multiple `[ ]` → `[x]` without a **new-increment** pass each
- Skipping **`new-increment`** (no scoped TDD per slice)
- No on-disk `increments/` file
- Creating many per-increment markdown files during planning

See [references/anti-patterns.md](references/anti-patterns.md).

---

## Additional resources

- [references/increment-backlog.md](references/increment-backlog.md)
- [references/slicing-increments.md](references/slicing-increments.md)
- [references/anti-patterns.md](references/anti-patterns.md)
- [examples/fizzbuzz-increments.md](examples/fizzbuzz-increments.md)
