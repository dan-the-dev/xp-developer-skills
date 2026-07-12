---
name: new-increment
description: Deliver one releasable increment from increments/<feature>.md — strict TDD by default (one test-lists/<feature>.md, unit tests). ATDD only when a real outer seam exists (API/UI/contract). One increment per invocation; RED before GREEN; minimal markdown. Not for whole-feature planning (skills/new-feature).
allowed-tools: Read, Edit, MultiEdit, Bash, Grep, Glob
---

# New increment (one slice)

## Mission

Implement **exactly one** open line from `increments/<feature-stem>.md`.

**Default:** **`skills/tdd/SKILL.md`** only — unit (or narrow integration) tests, behaviors tracked in **one** `test-lists/<feature-stem>.md` (section per increment).

**When a real outer seam exists:** compose **`skills/atdd/SKILL.md`** at that boundary, then TDD inside. **Never** duplicate the same assertions in acceptance and unit layers.

Mark the parent backlog line **`[x]`** and **stop** — unless the user explicitly asks to continue to the next increment.

---

## Workflow

Shared delivery rules: [`docs/delivery-process.md`](../../docs/delivery-process.md) and [`docs/project-verification.md`](../../docs/project-verification.md).

1. Lock scope to **one** `[ ]` backlog line; branch e.g. `feat/<feature>-<increment-slug>`.
2. **Test strategy** — [`test-strategy-selection.md`](../../docs/test-strategy-selection.md): discover configured jobs; complete adopt/skip table **before first RED** ([checklists/test-strategy.md](checklists/test-strategy.md)).
3. **Discover project verification** for the language/module you will touch (§2; [`project-verification.md`](../../docs/project-verification.md)) — README, CI, scripts, Makefile, Sonar, **mutation** config; do not assume one command.
4. **Choose layer** — [references/scoped-atdd-tdd.md](references/scoped-atdd-tdd.md) (TDD-only vs ATDD+TDD).
5. **Artifacts** — [references/artifact-policy.md](references/artifact-policy.md): one feature test list; no per-increment markdown sprawl.
6. **RED → GREEN → REFACTOR** per behavior; **one failing check at a time**; **re-run affected tests after every edit**; run **adopted** practices (mutation, integration, contract, etc.) at slice boundary.
7. If construction/import/API changed, **search and update all call sites** in scope (§3).
8. Update parent `increments/…` to `[x]` with link to test list section (and acceptance section if used).
9. **Cleanup** redundant slice-only markdown if created by mistake.
10. **Run all applicable project verify steps** (tests, lint, format, typecheck, SonarQube, **mutation job if adopted**); none may be skipped because another already passed (§2).
11. **Return payload** (§10) including **test strategy table**; do not start the next increment.

Prep if needed: **`skills/legacy-testing`** (invalid harness), **`skills/refactoring`**, **`skills/spike`** — then resume.

---

## Definition of done

- One backlog line only; **test strategy table** completed before first RED ([`test-strategy-selection.md`](../../docs/test-strategy-selection.md))
- **All project verify steps** for this scope passed (§2; [`project-verification.md`](../../docs/project-verification.md)) — including adopted practices (mutation, contract, integration, etc.)
- RED observed before each production change (see scoped reference)
- Test list lines `[x]` only with passing checks referenced
- No duplicate acceptance + unit tests for the same behavior
- Change-surface complete if APIs/seams changed (§3)
- Parent increment line `[x]`
- No behavior from **future** increments
- Return payload delivered (§10)

Checklist: [checklists/increment-done.md](checklists/increment-done.md), [checklists/test-strategy.md](checklists/test-strategy.md).

---

## Anti-patterns

- Implementing multiple backlog lines in one session without explicit user opt-in
- `acceptance-examples/` + unit tests with identical assertions (documentation theater)
- Per-increment `test-lists/<slice>.md` files (use one feature file)
- Marking `[x]` on markdown before tests exist or fail
- Writing full test files and full production in one step
- Batch message: “implementing increments 2–7”

See [references/anti-patterns.md](references/anti-patterns.md).

---

## Additional resources

- [`docs/delivery-process.md`](../../docs/delivery-process.md)
- [`docs/test-strategy-selection.md`](../../docs/test-strategy-selection.md)
- [references/scoped-atdd-tdd.md](references/scoped-atdd-tdd.md)
- [references/artifact-policy.md](references/artifact-policy.md)
- [references/anti-patterns.md](references/anti-patterns.md)
