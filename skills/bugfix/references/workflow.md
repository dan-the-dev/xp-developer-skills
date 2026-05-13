# Bugfix Workflow

This workflow defines the mandatory execution order for safe bug fixing.

The workflow is intentionally strict to:

- minimize regressions
- preserve reviewability
- ensure deterministic validation
- keep changes reversible

---

## Workflow Overview

1. Synchronize repository
2. Create isolated branch
3. Reproduce bug
4. Create failing test (RED)
5. Verify RED
6. Commit RED
7. Apply minimal fix (GREEN)
8. Verify GREEN
9. Commit GREEN
10. Push branch
11. Stop

---

## 1. Synchronize Repository

Always begin from the latest main branch state.

Required:

- checkout main
- pull latest changes
- verify clean working tree

Never start from:

- stale branches
- dirty worktrees
- unrelated feature branches

---

## 2. Create Isolated Branch

Every bugfix must be isolated.

Branch naming:

bugfix/STR-XXX-short-description

Examples:

- bugfix/STR-142-null-user-status
- bugfix/STR-201-invalid-date-format

Rules:

- lowercase
- hyphen-separated
- concise
- repository conventions first

---

## 3. Reproduce the Bug

Understand:

- actual behavior
- expected behavior
- affected scope
- runtime conditions
- the **invariant or contract** that is violated (one sentence) — distinct from the **symptom** (crash, log, wrong UI)

Prefer:

- automated reproduction
- deterministic reproduction
- smallest possible scope

Sources of evidence:

- failing tests
- logs
- traces
- screenshots
- telemetry
- stack traces

---

## 4. Create Failing Test (RED)

A bug is not considered reproducible until a test fails.

Preferred order:

1. unit test
2. integration/API test
3. e2e test

The test must:

- fail before fix exists
- fail for correct reason
- express **expected behavior** clearly — i.e. assert the **correct outcome or invariant** when fixed, not only that an error or exception occurred
- remain deterministic

---

## 5. Verify RED

Run minimal scope first.

Examples:

- single test
- single file
- single package/module

If the test unexpectedly passes:

- tighten assertions
- inspect execution path
- verify reproduction assumptions

Never continue without confirmed RED.

---

## 6. Commit RED

Commit ONLY the failing test.

Commit message:

test: reproduce bug STR-XXX

Goal:

- isolate reproduction
- preserve debugging history
- improve review clarity

---

## 7. Apply Minimal Fix (GREEN)

Modify the smallest amount of code possible.

Prefer:

- local fixes
- minimal condition changes
- existing abstractions

Avoid:

- cleanup
- optimization
- renaming
- restructuring
- broad edits

---

## 8. Verify GREEN

Execute incrementally:

1. focused tests
2. related module/package
3. broader suites if justified

Verify:

- failing test now passes
- no regressions introduced
- behavior remains stable

---

## 9. Commit GREEN

Commit ONLY production fix changes.

Commit message:

fix: resolve bug STR-XXX

Keep:

- reviewable diffs
- isolated behavior changes
- minimal scope

---

## 10. Push Branch

Push upstream.

Do NOT:

- squash
- rebase aggressively
- open PR automatically

---

## 11. Stop

Stop immediately once:

- bug fixed
- tests validated
- branch pushed

Do NOT:

- continue improving code
- expand scope
- refactor unrelated logic
