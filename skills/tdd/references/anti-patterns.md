# TDD anti-patterns

Symptoms to avoid when applying strict TDD.

---

## Test list

- **No on-disk file**: list only in chat, or path not under version control.
- **Wrong content**: refactor, tech-debt, or “cleanup” lines in **Cases** — use `<stem>-follow-ups.md` or the closing reply instead.
- **No file**: jumping into RED without a file (except a deliberate minimal two-line file for a trivial slice).
- **Stale file**: not updating `[x]` / `[ ]`, not appending new **behavior** lines when discovered.
- **`[x]` without proof**: checked off without a **test reference** or before tests pass.
- **Silent drops**: removing a case from **Cases** without a **Removed** (or equivalent) line.
- **Vague deferred**: **Deferred behavior** rows left without closure at slice end.

---

## Three Laws

- **Speculative production**: classes, helpers, or config “for later” with no failing test.
- **Big-bang test**: writing a large test before seeing the first failure signal.
- **Extra production**: behavior, APIs, or optimizations not required by the **current** failing test.

---

## Process

- **Big upfront tests**: a large test before any green path exists — shrink the example or add a **starter** case.
- **False RED**: committing “RED” while the suite passes, failure unrelated to the case, or mistaking a **flake/timeout/env** for a behavior gap.
- **Green without refactor discipline**: piling conditionals; skipping the refactor step habitually.
- **Refactor in RED**: changing structure while a failing test represents incomplete behavior (finish GREEN first unless the team explicitly uses a different discipline).
- **Refactor without guardrails**: multiple edits before running tests; **continuing** after a failure instead of reverting the last step.

---

## Refactor scope

- **Drive-by refactors** in modules far from the code that turned the last test green.
- **Global** renames or style sweeps bundled into a feature slice without their own list items or workflow.

---

## Commits

- Mixing test and production files in one commit during the cycle.
- Using `feat:` / `fix:` before a failing test exists.
- Pushing `test:` / `feat:` / `fix:` / `refactor:` separately when this skill requires a **squashed** push for the completed cycle.

---

## Tests (behavior vs. implementation)

- **Over-mocking** or strict call sequences that lock **implementation** instead of asserting outcomes at a **stable seam**.
- **Non-deterministic** tests: real time, random seeds, network, shared global state without control.
- Assertions that mirror implementation line-by-line (overfit to current code shape).
- Tests that break on **refactor** without behavior change — indicates **implementation coupling**; rewrite toward public outcomes.
- **Long setup** as accepted normal — usually means objects do too much or seams are wrong; split or narrow the unit under test.
- **Fragile tests** that fail when distant code changes — often overspecified mocks or missing owned seams.
- **Heavy logic in tests** (loops, branching) hiding why RED failed — use [test-quality.md](test-quality.md).
- Flaky order-dependent tests.
- Integration weight when a unit test would fail faster — escalate scope only when needed.

---

## Feedback

- Running the full suite after every tiny edit when a narrower command exists.
- Continuing after RED without observing the failure output.
