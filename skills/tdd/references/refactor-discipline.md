# Refactor discipline — tests never break

REFACTOR happens only on a **fully green** baseline. During refactoring, **behavior must not change**; tests are the guardrail.

---

## Non-negotiables

- **Start green**: no refactor while any targeted test is red (including from unrelated unfinished work).
- **Tests must stay green**: if a test fails after a change, **that change was not a refactor** (or the suite was too narrow). **Revert or undo** the last edit immediately, then reassess.
- **One small mechanical step at a time**: rename, extract method, move, inline — then **run tests**. Do not stack multiple risky edits before running.
- **Widen test scope when touching shared code**: after local green, run the next broader scope the repo uses (module, package, CI subset).

---

## Micro-step loop

Repeat until refactor goal is reached:

1. Decide the **smallest** next transformation (single extraction, single rename, one dependency inversion).
2. Apply it.
3. Run the **same** test command as before (then widen if needed).
4. If **any** failure: **stop**, restore green (revert / reset the step), shrink the step, retry.

Never “fix forward” under failing tests during a refactor pass unless you are explicitly abandoning refactor mode and returning to a failing-test workflow (not this step).

---

## What counts as refactor

- Renaming for clarity
- Moving code without changing observable outcomes
- Extracting methods/classes/modules
- Removing duplication when the pattern is clear (see **rule of three** in [micro-iterations.md](micro-iterations.md))

What is **not** refactor here:

- New observable behavior or new public contract
- Changed algorithms that alter outputs or side effects
- Loosened assertions to make tests pass

---

## Duplication and abstraction

- Prefer **evidence-based** extraction: remove duplication when it is real and recurring, not speculative.
- Avoid premature frameworks: let structure emerge from repeated tests and green code; over-abstracting is a design smell visible through hard-to-write tests.
