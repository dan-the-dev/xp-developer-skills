# Testing and safety net

## Green light rule

**Before** refactoring: relevant tests **green**.

**After** each mechanical step: **green** again.

If tests fail:

- Assume the **step** broke an assumption — **revert** the step.
- Only if the suite was **wrong** (e.g. asserted private layout) may you **change tests** without a behavior change — that is a **test refactor**, still one small step, still green afterward.

---

## What to run

| Change surface | Typical scope |
|----------------|---------------|
| Single function / file | File or single test class |
| Shared helper | Module + direct importers |
| Public API / type surface | Wider integration slice, contract tests |
| Cross-package | Team’s “full unit” or CI job |

**Escalate** scope **after** local green when touching shared code.

---

## Thin safety net

If coverage is weak:

1. **Narrow** refactor scope to well-tested code paths.
2. **Add characterization tests** that lock current behavior on seams you will move (this blurs into “add tests” hat — do it **first**, get green, then refactor).
3. **Defer** large rewrites until `add-tests-to-legacy-code` (or equivalent) is applied.

Never confuse **hope** with a **safety net**.

---

## Composability with TDD

In TDD, the **test list** and RED–GREEN give new behavior; **REFACTOR** is exactly this skill in miniature — same revert discipline, same green-between-steps rule ([`refactor-discipline.md`](../../tdd/references/refactor-discipline.md)).

---

## Flaky tests

If the suite flaps **before** refactoring, **stabilize or quarantine** flakiness first. Refactoring on a flaky baseline teaches the team to ignore red — that erodes the whole practice.
