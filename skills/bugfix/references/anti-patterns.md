# Anti-Patterns

These behaviors reduce safety, reviewability, and reproducibility.

Avoid them completely.

---

## Fixing Without Reproduction

Never modify production code before:

- reproducing the issue
- understanding failure conditions

Without reproduction:

- correctness cannot be validated
- regressions become invisible

---

## Refactoring During Bugfixing

Bugfixing is not cleanup work.

Avoid:

- renaming
- moving files
- restructuring
- abstraction changes
- formatting-only edits

unless strictly required for the fix itself.

---

## Large Multi-Purpose Changes

A bugfix must remain focused.

Avoid:

- unrelated edits
- opportunistic cleanup
- multiple fixes in one branch

---

## Mixing RED and GREEN

Never combine:

- failing test
- production fix

into the same commit.

Separate commits improve:

- debugging
- reviewability
- revert safety

---

## Weak Assertions

A test that passes incorrectly is dangerous.

Avoid:

- vague assertions
- indirect validation
- assertions unrelated to behavior
- assertions that only check “an error happened” without stating the **correct outcome or invariant** once fixed

---

## Symptom fixes (silencing vs restoring invariants)

A **symptom** is what users or logs show (crash, 500, wrong label). The **invariant** is what the system should **guarantee** (correct totals, auth rules, ordering, idempotency, etc.).

**Symptom fix** (reject):

- swallowing exceptions, returning `null`/`0`/`""` to hide the failure, or adding a guard that skips bad input **without** making wrong cases correct
- loosening assertions or removing expectations so the test passes without proving the contract
- changes that stop the noise but leave **wrong results** for other inputs in the same code path

**Correct fix**:

- the failing test encodes the **expected observable behavior** (or public contract) under the failing conditions
- production change **restores that contract** with minimal edits

If you cannot state the invariant in one sentence, the bug is not understood enough to fix safely — return to reproduction and clarification.

---

## Ignoring Existing Conventions

Do not impose new patterns during a bugfix.

Respect:

- repository structure
- naming conventions
- test organization
- tooling conventions

---

## Blind Full-Suite Execution

Avoid running expensive full suites repeatedly.

Prefer:

1. focused validation
2. incremental expansion

---

## Over-Engineering the Fix

Avoid:

- generic frameworks
- speculative abstractions
- future-proofing

Fix today's problem safely.

---

## Continuing After Completion

Once:

- fix validated
- branch pushed

STOP.

Do not:

- continue exploring
- optimize further
- expand scope
