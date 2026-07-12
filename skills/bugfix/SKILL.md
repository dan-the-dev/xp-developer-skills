---
name: bugfix
description: Use when fixing bugs, regressions, failing tests, or unexpected behavior. Applies a strict test-first bugfix workflow with minimal safe changes, isolated commits, and language-agnostic verification strategies.
allowed-tools: Read, Edit, MultiEdit, Bash, Grep, Glob
---

# Bugfix TDD

## Mission

Shared delivery rules at boundaries: [`docs/delivery-process.md`](../../docs/delivery-process.md) (§2 verification, §3 change-surface, §4 test strategy, §7 two hats) and [`docs/project-verification.md`](../../docs/project-verification.md), [`docs/test-strategy-selection.md`](../../docs/test-strategy-selection.md).

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
- Prefer the smallest possible change that **restores the violated invariant**, not one that only hides the symptom
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

- complete a brief **test strategy** note per [`test-strategy-selection.md`](../../docs/test-strategy-selection.md) — e.g. will mutation run after GREEN if configured and logic is branchy?
- identify observed behavior
- identify expected behavior
- identify affected scope
- inspect logs/errors/traces if available
- separate **symptom** (what looks wrong: crash, wrong UI, log noise) from the **invariant** or **contract** that was violated (what the system should **guarantee** under the same conditions)

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
- clearly express **expected behavior** — i.e. the **correct observable outcome or invariant** under the failing conditions, not only that “something failed” (see Anti-Patterns: symptom fixes)
- fail before the fix exists

The reproduction must be sufficient for a reviewer to see **what contract was broken**, not merely that an error path was exercised.

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
- **symptom-only** changes that hide the failure without restoring the violated **invariant** (e.g. empty catch, broad default, guard that masks the bug while wrong outcomes remain for other inputs)

---

### 6. Verify GREEN State

Run progressively:

1. focused tests
2. related module/package tests
3. broader suites if needed
4. **all applicable project verify steps** at bugfix boundary — lint, format, typecheck, SonarQube/static analysis when configured, **mutation if adopted** ([`docs/project-verification.md`](../../docs/project-verification.md), [`docs/test-strategy-selection.md`](../../docs/test-strategy-selection.md))

Verify:

- failing test now passes **for the right reason** (assertions still encode the correct contract, not loosened to force green)
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
- apply a **symptom fix** that silences the failure while the **broken invariant** remains (see [references/anti-patterns.md](references/anti-patterns.md))

---

## Verification Strategy

**Discover** all verify steps the **current project** defines for the language/module you touched — then run **each applicable step** before claiming done (delivery-process §2; [`docs/project-verification.md`](../../docs/project-verification.md)). Do not stop after only the test runner if the project defines compile, typecheck, lint, format, SonarQube/static analysis, integration, or other gates.

**Fix new violations** you introduced — do not suppress lint or Sonar rules to force green.

Prefer incremental validation **within** that set:

1. focused automated check
2. local module/package verify step
3. service/application verify step
4. full project verify only when justified

Avoid expensive full runs after every micro-edit unless the project requires it; run the **full applicable set** at the bugfix boundary.

---

## Definition of Done

A bugfix is complete only when:

- bug is reproduced by automated test that asserts the **correct invariant / expected outcome**, not only a generic failure
- RED state confirmed
- minimal fix applied (restores the contract; not a symptom-only silencing)
- GREEN state confirmed
- **all applicable project verify steps** for this scope passed
- **test strategy table** in output (practices evaluated → adopt/skip)
- change-surface complete if construction/import/API changed
- related regressions checked
- two isolated commits exist
- branch pushed upstream
- no unrelated changes remain
- **Root cause** and **recurrence prevention** are documented in the output (see Output Format)

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

Invariant / contract (one line):
<what the system should guarantee under the failing conditions — the repro test must assert this>

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
- Test strategy (mutation, integration, etc.): adopted / skipped with reason

5. Git
- RED commit
- GREEN commit
- Branch pushed

6. Root cause
<one short paragraph: why the bug occurred — wrong assumption, missing branch, bad state, regression, etc.>

7. Recurrence prevention
<one short paragraph: how this class of bug is prevented now — e.g. new test covers edge, documented constraint, follow-up ticket for structural fix>
```

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
