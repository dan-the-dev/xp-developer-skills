---
name: bugfix-tdd
description: Use when fixing bugs, regressions, failing tests, or unexpected behavior. Applies a strict test-first bugfix workflow with minimal safe changes, isolated commits, and language-agnostic verification strategies.
allowed-tools: Read, Edit, MultiEdit, Bash, Grep, Glob
---

# Bugfix TDD

## Mission

Fix bugs safely using a strict RED → GREEN workflow.

The goal is:

- reproduce the bug
- create a deterministic failing test
- apply the minimal safe fix
- verify no regressions
- preserve reviewability and isolation

This skill optimizes for:

- correctness
- reproducibility
- safety
- small reversible changes

NOT for:

- speed
- cleanup
- optimization
- refactoring

---

## Core Principles

- Tests are the source of truth
- Never fix behavior before reproducing it
- Every bugfix must be reproducible
- Prefer the smallest possible change
- Separate reproduction from resolution
- Preserve system stability
- Keep commits isolated and reviewable

---

## Language-Agnostic Rules

This skill MUST adapt to the current repository stack.

The agent should:

- detect the language and framework in use
- identify existing testing conventions
- reuse project-native tooling
- follow existing repository patterns

Examples:

- JavaScript/TypeScript → npm/pnpm/jest/vitest/playwright
- Python → pytest/unittest
- Go → go test
- Java → junit/maven/gradle
- Ruby → rspec
- Rust → cargo test

Never assume:

- package manager
- test runner
- framework
- directory structure

Always inspect the repository first.

---

## Mandatory Workflow

### 0. Synchronize Repository

Required steps:

1. checkout main branch
2. pull latest changes
3. create isolated bugfix branch

Branch format:

bugfix/{ticket}-{short-description}

Examples:

- bugfix/STR-142-null-email-validation

- bugfix/PLAT-201-invalid-date-format

- bugfix/fix-missing-user-mapping

Rules:

- lowercase

- hyphen-separated

- concise and descriptive

- description must summarize the bug behavior

- avoid generic names like:

  - fix-bug

  - issue-fix

  - quick-patch

Ticket handling:

- if a ticket identifier exists in the initial request, include it

- otherwise omit the ticket portion

The agent should automatically generate a meaningful short description derived from:

- observed failing behavior

- affected domain

- expected correction

---

### 1. Understand the Failure

Before writing code:

- identify observed behavior
- identify expected behavior
- identify affected scope
- inspect logs/errors/traces if available

Prefer:

- deterministic reproduction
- automated reproduction
- narrow reproduction scope

---

### 2. Reproduce the Bug with a Test (RED)

Create a failing test reproducing the issue.

Choose the lowest useful test level:

1. unit
2. integration/API
3. end-to-end

The test MUST:

- fail for the correct reason
- be deterministic
- clearly express expected behavior
- fail before the fix exists

If reproduction is impossible:

- STOP
- document constraints
- request clarification

---

### 3. Verify RED State

Run the minimal test scope first.

Examples:

- single test
- single file
- focused module

If the test passes unexpectedly:

- strengthen assertions
- improve reproduction
- verify execution path

Never continue without confirmed RED.

---

### 4. Commit RED State

Stage ONLY test files.

Commit message:

test: reproduce bug STR-XXX

The commit MUST:

- contain only reproduction logic
- clearly demonstrate the failure

---

### 5. Apply Minimal Fix (GREEN)

Modify only the code required to resolve the bug.

Prefer:

- local fixes
- minimal behavioral changes
- existing abstractions
- reversible changes

Avoid:

- refactoring
- cleanup
- renaming
- architectural changes
- unrelated edits

---

### 6. Verify GREEN State

Run progressively:

1. focused tests
2. related module/package tests
3. broader suites if needed

Verify:

- failing test now passes
- related behavior remains stable
- no regressions detected

---

### 7. Commit GREEN State

Stage ONLY fix-related files.

Commit message:

fix: resolve bug STR-XXX

The commit MUST:

- contain only the minimal fix
- preserve review clarity

---

### 8. Push Branch

Push branch upstream.

Do NOT:

- squash commits
- rewrite history
- open PR automatically

---

### 9. Stop

Once:

- RED reproduced
- GREEN verified
- branch pushed

STOP.

Do not:

- optimize
- refactor
- continue exploring
- expand scope

---

## Escalation Rules

STOP and escalate if:

- bug cannot be reproduced deterministically
- tests are flaky
- unrelated failures appear
- fix requires architectural changes
- repository conventions are unclear
- missing tooling prevents safe validation

Document:

- blockers
- attempted approaches
- observed behavior

---

## Anti-Patterns

Never:

- fix without a failing test
- mix refactoring with bugfixing
- create large fixes
- modify unrelated files
- combine RED and GREEN in one commit
- skip regression validation
- assume tooling without inspection

---

## Verification Strategy

Prefer incremental validation:

1. focused test
2. local module/package
3. service/application
4. full suite only when justified

Avoid expensive full-suite runs unless necessary.

---

## Definition of Done

A bugfix is complete only when:

- bug is reproduced by automated test
- RED state confirmed
- minimal fix applied
- GREEN state confirmed
- related regressions checked
- two isolated commits exist
- branch pushed upstream
- no unrelated changes remain

---

## Output Format

```markdown
Branch: <branch-name>

Bug:
<short description>

Observed Behavior:
<actual behavior>

Expected Behavior:
<expected behavior>

1. Reproduction
- <approach>

2. RED
- Test: <file::test>
- Result: failing as expected

3. GREEN
- Fix: <minimal change summary>
- Result: passing

4. Verification
- Commands executed
- Scope validated
- Regression status

5. Git
- RED commit
- GREEN commit
- Branch pushed

## Additional Resources

### Workflow References

- references/workflow.md
- references/heuristics.md
- references/verification.md
- references/anti-patterns.md
- references/language-agnostic-testing.md

### Examples

- examples/javascript.md
- examples/typescript.md
- examples/python.md
- examples/go.md
- examples/java.md

### Completion Checklist

- checklists/done.md

## Resource Usage Guidance

Open additional files only when needed.

Suggested usage:

- workflow.md
  → when execution order is unclear

- heuristics.md
  → when multiple fix strategies are possible

- anti-patterns.md
  → before large or risky changes

- verification.md
  → when validation scope is uncertain

- language-agnostic-testing.md
  → when repository tooling is unfamiliar

- examples/*
  → when repository language matches example ecosystem

- checklists/done.md
  → before finalizing work
