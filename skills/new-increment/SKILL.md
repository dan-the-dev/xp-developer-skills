---
name: new-increment
description: Deliver one releasable increment — full skills/atdd then skills/tdd for that slice only (scoped acceptance-examples and test-lists). Use for one open line from increments/<feature>.md. Not for whole-feature planning (skills/new-feature).
allowed-tools: Read, Edit, MultiEdit, Bash, Grep, Glob
---

# New increment (one slice)

## Mission

Implement **exactly one** increment from `increments/<feature-stem>.md`.

**Every increment runs:**

1. **`skills/atdd/SKILL.md`** — scoped to **this slice** (`acceptance-examples/<increment-stem>.md`)
2. **`skills/tdd/SKILL.md`** — scoped to **this slice** (`test-lists/<increment-stem>.md`)

Then mark the parent backlog line **`[x]`** and **stop** unless asked to continue.

---

## Workflow

1. Lock scope to **one** backlog line; branch e.g. `feat/<feature>-<increment-slug>`.
2. **ATDD** — examples and acceptance for this slice only.
3. **TDD** — test list + R–G–R until acceptance and units green.
4. Update parent `increments/…` line to `[x]` with links.
5. Return handoff; do not start next increment.

Prep if needed: **`skills/legacy-testing`**, **`skills/refactoring`**, **`skills/spike`** — then resume this workflow.

See [references/scoped-atdd-tdd.md](references/scoped-atdd-tdd.md).

---

## Definition of done

- Scoped catalog + test list complete for **this** slice
- Suites green for this scope
- Parent increment line `[x]`
- No behavior from **future** increments

Checklist: [checklists/increment-done.md](checklists/increment-done.md).

---

## Additional resources

- [references/scoped-atdd-tdd.md](references/scoped-atdd-tdd.md)
- [references/anti-patterns.md](references/anti-patterns.md)
