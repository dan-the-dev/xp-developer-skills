# TDD anti-patterns

Symptoms to avoid when applying strict TDD.

---

## Process

- **Big upfront tests**: a large test before any green path exists — shrink the example or add a **starter** case.
- **False RED**: committing “RED” while the suite passes or failure is unrelated.
- **Green without refactor discipline**: piling conditionals; skipping the refactor step habitually.
- **Refactor in RED**: changing structure while a failing test represents incomplete behavior (finish GREEN first unless the team explicitly uses a different discipline).
- **Refactor without guardrails**: multiple edits before running tests; **continuing** after a failure instead of reverting the last step.

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
