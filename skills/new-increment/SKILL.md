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

1. Lock scope to **one** `[ ]` backlog line; branch e.g. `feat/<feature>-<increment-slug>`.
2. Read README/Makefile/`AGENTS.md` for the **canonical test command** (e.g. `make test`, `npm test`).
3. **Choose layer** — [references/scoped-atdd-tdd.md](references/scoped-atdd-tdd.md) (TDD-only vs ATDD+TDD).
4. **Artifacts** — [references/artifact-policy.md](references/artifact-policy.md): one feature test list; no per-increment markdown sprawl.
5. **RED → GREEN → REFACTOR** per behavior; **one failing test at a time**; run tests between steps.
6. Update parent `increments/…` to `[x]` with link to test list section (and acceptance section if used).
7. **Cleanup** redundant slice-only markdown if created by mistake.
8. Return handoff; do not start the next increment.

Prep if needed: **`skills/legacy-testing`**, **`skills/refactoring`**, **`skills/spike`** — then resume.

---

## Definition of done

- One backlog line only; tests green for **this** scope
- RED observed before each production change (see scoped reference)
- Test list lines `[x]` only with passing tests referenced
- No duplicate acceptance + unit tests for the same behavior
- Parent increment line `[x]`
- No behavior from **future** increments

Checklist: [checklists/increment-done.md](checklists/increment-done.md).

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

- [references/scoped-atdd-tdd.md](references/scoped-atdd-tdd.md)
- [references/artifact-policy.md](references/artifact-policy.md)
- [references/anti-patterns.md](references/anti-patterns.md)
