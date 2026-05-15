# Continuous delivery and refactoring (Dave Farley)

Dave Farley’s continuous delivery emphasis complements Fowler-style refactoring:

- **Integrate often** — small, **working** increments on the main line (or short-lived branches) reduce merge risk.
- **Keep the pipeline honest** — if refactoring is “free,” it must still **pass** the same quality gates as other changes.
- **Refactoring supports speed** — cleaner seams make **features** and **fixes** cheaper; deferred refactoring is **compound interest** on slowness.

---

## Practice implications

| Habit | Why |
|-------|-----|
| **Small refactor commits** | Easier bisect, clearer review, less batch risk |
| **Green before push** | Refactoring is not exempt from “don’t break the build” |
| **Automate verification** | Fast tests reward frequent small refactorings |

---

## Not covered here

Pipeline design, branching strategy, and release governance live in delivery-focused skills. This file only **links** habits: **refactor** in slices that respect **always-releasable** discipline where that is your team norm.
