# Test list (feature backlog of cases)

The test list is a **Markdown file committed in the repository** so the slice stays inspectable in PRs and history. It lists **only** behaviors that will become **automated tests** — it defines **when the feature is done**, not a wishlist of refactors.

---

## Purpose

- Forces **inventory** of behavior before coding.
- **Done** for the slice: every checklist line is `[x]` (or explicitly removed by agreement) **and** the suite is green.
- Captures **new** behavior cases as they appear; nothing ships “by the way” without a line.

---

## Where to put the file

1. **Prefer project convention**  
   Inspect (in order): `AGENTS.md`, `README.md`, `docs/*`, `.cursor/rules`, `CONTRIBUTING*`, and existing directories. If the repo already documents or uses a folder for TDD notes, planning checklists, or `test-lists` / similar, **use that folder**.

2. **Default**  
   If nothing applies, create and use:

   `test-lists/`  
   at the **repository root** (next to the root `package.json`, `go.mod`, `.git`, etc., whichever marks the project root you are working in).

---

## File naming

- Use **kebab-case**, ASCII, no spaces.
- Derive the stem from **current git branch** and/or **feature name** so the file is easy to find in review.

Suggested algorithm:

1. Read branch: `git branch --show-current` (or equivalent).
2. Remove common prefixes: `feature/`, `feat/`, `fix/`, `bugfix/`, `chore/`, `hotfix/`.
3. Replace `/` and `_` with `-`, collapse repeated `-`, lowercase.
4. If the branch is generic (`main`, `master`, `develop`) or empty, use a slug from the **feature title** the user gave.
5. Filename: `<stem>.md`  
   Examples: branch `feat/order-shipping-threshold` → `order-shipping-threshold.md`; branch `fix/PLAT-201-null-email` → `plat-201-null-email.md`.

If two slices could collide, prefix with a ticket id or date: `str-142-order-shipping-threshold.md`.

---

## What belongs in the file (and what does not)

**Include** — one line per **observable behavior** or **rule** you will cover with a unit/integration test as part of this slice:

- Happy paths, edge cases, errors, invariants, boundaries.

**Do not include**:

- **Refactors** skipped because of [refactor proximity](refactor-discipline.md) (distant cleanup, rename sweeps, “extract service later”).
- **Tech debt** or **nice-to-have** engineering tasks that are **not** required to declare the behavior complete.

Those belong elsewhere so the checklist stays a **true completion signal**:

- **Option A (preferred when multiple notes):** a sibling file in the same folder, same stem:

  `<stem>-follow-ups.md`  

  e.g. `test-lists/order-shipping-threshold-follow-ups.md` — bullets for deferred refactors, broader cleanups, follow-on tickets.

- **Option B:** no file — keep deferred items **in memory** and **list them explicitly in the final reply** to the user when the slice is done (so nothing is forgotten, but the test list still closes cleanly).

Never use the **test list** file as a dumping ground for refactor ideas.

---

## Lifecycle: discovery, deferred behavior, and out of scope

### Discovery during development

New **behavior** must appear on the list **before** it ships:

- **Append** a new `[ ]` line as soon as the case is known (even mid-slice).
- Implement it with the usual R–G–R cycle.

Do not merge “surprise” behavior without a list line.

### Deferred behavior (still behavior, not refactor)

Sometimes a behavior is agreed **not in this slice** but must stay visible (e.g. “multi-currency totals” while you only ship single-currency now). Use a dedicated subsection — **not** the refactor follow-ups file:

```markdown
## Deferred behavior (not in this slice)

- [ ] <case> — target: <ticket or future slice>; agreed <date>
```

**Slice complete** requires either: every line in **Cases** is `[x]` or removed, **and** every **Deferred behavior** line is resolved (moved to **Cases** and implemented, moved to **Removed**, or given an explicit follow-up ticket with owner) — do not leave ambiguous “maybe later” rows without agreement.

### Removed / out of scope

When a listed case is dropped:

```markdown
## Removed / out of scope

- <case> — removed <date>; reason: …; agreed by: <role or name>
```

That preserves audit trail without fake `[x]` markers.

---

## Traceability: done means linked to a test

When you mark a line `[x]`, add a **pointer** to the automated test that proves it (so review and future readers can verify):

- Preferred: `` `path/to/spec.ts::describe or test name` `` on the same line or the line below.
- Or: link to test file + line or test id per project convention.

**Do not** mark `[x]` without at least one **concrete** test reference and a **passing** suite for that test.

---

## Format (in the repo file)

```markdown
# Test list — <short feature title>

Branch: <optional>
Updated: <optional ISO date>

## Cases

- [ ] <behavior / scenario in plain language>
- [x] <behavior> — `src/orders/order.spec.ts::includes shipping when weight above threshold`

## Deferred behavior (not in this slice)

<!-- optional; see lifecycle above -->

## Removed / out of scope

<!-- optional; see lifecycle above -->
```

---

## Rules of use

1. **Create the file first** — before the first RED for the slice (Law 2 still applies: first test is minimal).
2. **Pick one open `[ ]` line** in **Cases** — implement exactly one minimal failing test for it.
3. After R–G–R for that case, flip the line to `[x]` **with a test reference** (see traceability).
4. **Append** new `[ ]` lines in **Cases** when new **behavior** is discovered; use **Deferred behavior** or **Removed** per lifecycle rules — never hide scope in refactor follow-ups.
5. **Slice complete** when every **Cases** line is `[x]` or documented in **Removed**, deferred rows are **closed per agreement**, and tests are green.

---

## Relationship to the Three Laws

The file is **planning and scope** for **behavior**. Each cycle still obeys the Three Laws. The file does **not** replace RED: you still write only enough test to fail, then enough code to pass.

---

## Anti-patterns

- No on-disk file (list only in chat).
- Test list file in `.gitignore` (it should be **versioned** unless the project forbids it — then escalate to the user).
- **Refactor / tech-debt** lines mixed into **Cases** (pollutes “done”).
- Marking `[x]` **without** a test reference or before tests pass.
- Stale file (not updated as cases complete or new behavior appears).
- Silent removal of lines without **Removed / out of scope** (or equivalent) record.
- Leaving **Deferred behavior** rows vague at slice end.
