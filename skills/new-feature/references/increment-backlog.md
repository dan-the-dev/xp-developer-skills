# Increment backlog

Default path: **`increments/<feature-stem>.md`** at repo root (or project convention).

```markdown
# Increments — <feature title>

## Increments (ordered)

- [ ] <one releasable slice — one sentence> — expected: <unit | mutation | ATDD at API | …>
- [x] <slice> — `test-lists/<feature-stem>.md` (§ <increment-slug>)
```

One line = one **`skills/new-increment`** invocation. Mark `[x]` only after that increment’s tests are green (full project verify) and work is committed.

Optional **`expected:`** notes are **planning hints** for greenfield tooling (mutation, ATDD) — not a contract. The **`new-increment`** test-strategy table remains authoritative for adopt/skip.

Optional second link when ATDD at a boundary was used:

```markdown
- [x] <slice> — `test-lists/<feature>.md` (§ slug) / `acceptance-examples/<feature>.md` (§ slug)
```

Do **not** link seven per-increment markdown files by default — use **one feature test list** with sections (see `skills/new-increment/references/artifact-policy.md`).
