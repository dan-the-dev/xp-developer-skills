# Refactor discipline — tests never break

REFACTOR happens only on a **fully green** baseline. During refactoring, **behavior must not change**; tests are the guardrail. **Test code** (helpers, builders, duplication in specs) is refactored with the **same** micro-step discipline as production code.

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

## Refactor proximity (stay in scope)

Refactoring effort should concentrate on **production and test code directly involved in the current change** (the types, functions, and files you touched to satisfy the latest failing test and its immediate collaborators).

- **High willingness**: same module/file as the GREEN change, immediate helpers introduced for that behavior, tests that directly assert the new case.
- **Medium willingness**: one hop out (e.g. small shared helper used only here) when duplication is obvious and tests still stay fast to run.
- **Low willingness**: distant modules, “while we are here” cleanups, global renames, cross-cutting style changes unrelated to making the current test list item pass.

The farther from the change, the **less** refactoring you do unless another **approved** workflow (ticket, tech-debt pass) explicitly schedules it. Proximity-skipped cleanups do **not** belong on the **behavior test list** — record them in **`<stem>-follow-ups.md`** (see [test-list.md](test-list.md)) or in the closing reply.

If a distant improvement is desirable, **add it to the follow-ups file** next to the test list, **or** your team’s external backlog — **not** the behavior test list file, which must stay a **done** signal for the slice.

---

## What counts as refactor

- Renaming for clarity (production **or** tests)
- Moving code without changing observable outcomes
- Extracting methods/classes/modules
- **Test code**: builders, object mothers, shared setup helpers, duplicate assertion extraction — same micro-step and revert rules as production
- Removing duplication when the pattern is clear (see **rule of three** in [micro-iterations.md](micro-iterations.md))

### Test-only refactor commit

If production is already clean but **test** setup or names need improvement, a **`refactor:`** commit may contain **only test files** (and test-only helpers). Laws still apply: **green** before starting; **no** behavior change.

What is **not** refactor here:

- New observable behavior or new public contract
- Changed algorithms that alter outputs or side effects
- Loosened assertions to make tests pass

---

## Duplication and abstraction

- Prefer **evidence-based** extraction: remove duplication when it is real and recurring, not speculative.
- Avoid premature frameworks: let structure emerge from repeated tests and green code; over-abstracting is a design smell visible through hard-to-write tests.
