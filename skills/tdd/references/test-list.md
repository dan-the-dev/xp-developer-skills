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

## Format (in the repo file)

```markdown
# Test list — <short feature title>

Branch: <optional>
Updated: <optional ISO date>

## Cases

- [ ] <behavior / scenario in plain language>
- [x] <another case — done when test exists and passes>
```

Optional: `## Removed / out of scope` with dated one-line reasons for dropped lines.

---

## Rules of use

1. **Create the file first** — before the first RED for the slice (Law 2 still applies: first test is minimal).
2. **Pick one open `[ ]` line** — implement exactly one minimal failing test for it.
3. After R–G–R for that case, flip the line to `[x]` in the **same** commit wave as documentation hygiene allows (or immediately after squash per team habit — but the file must stay **true**).
4. **Append** new `[ ]` lines when new **behavior** is discovered.
5. **Slice complete** when every behavior line is `[x]` (or explicitly removed) and tests are green.

---

## Relationship to the Three Laws

The file is **planning and scope** for **behavior**. Each cycle still obeys the Three Laws. The file does **not** replace RED: you still write only enough test to fail, then enough code to pass.

---

## Anti-patterns

- No on-disk file (list only in chat).
- Test list file in `.gitignore` (it should be **versioned** unless the project forbids it — then escalate to the user).
- **Refactor / tech-debt** lines mixed into the test list (pollutes “done”).
- Marking `[x]` before an automated test exists and passes.
- Stale file (not updated as cases complete or new behavior appears).
