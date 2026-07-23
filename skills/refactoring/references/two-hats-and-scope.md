# Two hats and scope

## Two hats (Martin Fowler)

You wear **one** hat at a time:

| Hat | Allowed | Tests |
|-----|---------|--------|
| **Add feature** (or fix bug) | New behavior, contracts, UI | May go **RED** then **GREEN** |
| **Refactor** | Structure only | Must stay **GREEN** between steps |

**Do not** mix in the same edit batch:

- “I’ll extract this method *and* add validation” → two hats → split commits or split time order: **refactor first** (green throughout), **then** feature (or reverse if feature must land first for tests to exist — still **sequential** clarity).

---

## Refactor is not debugging

- If behavior is **wrong**, use **bugfix** workflow: reproduce, failing test, minimal fix.
- Refactoring assumes behavior is **correct** (or correct enough) and the problem is **shape** / **cost of change**.

---

## Proximity and appetite

Like TDD’s refactor proximity:

- **High willingness**: code you must touch for the current goal; immediate neighbors.
- **Lower willingness**: cross-cutting renames, repo-wide style, unrelated modules.

For wide cleanups, **schedule** a refactor session with its own goal and branch — still **small commits**, not a vague “cleanup week.”

---

## Composing with other skills

- **`skills/tdd`**: after GREEN, **REFACTOR** uses this skill’s loop inside a micro-cycle.
- **`skills/bugfix`**: after GREEN on the fix, optional **refactor** pass for clarity — **separate** commit.
- **`skills/atdd`**: acceptance still passes unchanged after refactor; if it fails, you changed behavior or broke a **structural** test (fix test design per [tests-and-design.md](tests-and-design.md)).
- **`skills/new-feature`**: after each committed increment, **post-increment review** mode ([post-increment-review.md](post-increment-review.md)) — explain, suggest, optional tiny applies only.

---

## Agent / PR discipline

- Title and description should say **refactor** when the hat is refactor-only.
- Reviewers should see **no** requirement or ticket that implies **new** capability unless you **explicitly** switched hats in a **separate** commit.
