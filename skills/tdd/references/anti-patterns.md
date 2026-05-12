# TDD anti-patterns

Symptoms to avoid when applying strict TDD.

---

## Test list

- **No on-disk file**: list only in chat, or path not under version control.
- **Wrong content**: refactor, tech-debt, or “cleanup” lines on the **behavior** test list — use `<stem>-follow-ups.md` or the closing reply instead.
- **No list**: jumping into RED without a file (except a deliberate minimal two-line file for a trivial slice).
- **Stale file**: not marking `[x]`, not appending new **behavior** lines when discovered.
- **Done without tests**: checking off lines before an automated test passes.

---

## Three Laws

- **Speculative production**: classes, helpers, or config “for later” with no failing test.
- **Big-bang test**: writing a large test before seeing the first failure signal.
- **Extra production**: behavior, APIs, or optimizations not required by the **current** failing test.

---

## Process

- **Big upfront tests**: a large test before any green path exists — shrink the example or add a **starter** case.
- **False RED**: committing “RED” while the suite passes or failure is unrelated.
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
- Using `feat:` before a failing test exists.
- Pushing `test:` / `feat:` / `refactor:` separately when this skill requires a **squashed** push for the completed cycle.

---

## Tests (behavior vs. implementation)

- Assertions that mirror implementation line-by-line (overfit to current code shape).
- Tests that break on **refactor** without behavior change — indicates **implementation coupling**; rewrite toward public outcomes.
- **Long setup** as accepted normal — usually means objects do too much or seams are wrong; split or narrow the unit under test.
- **Fragile tests** that fail when distant code changes — often overspecified mocks or missing owned seams.
- Flaky order-dependent tests; nondeterministic time/random without control.
- Integration weight when a unit test would fail faster — escalate scope only when needed.

---

## Feedback

- Running the full suite after every tiny edit when a narrower command exists.
- Continuing after RED without observing the failure output.
