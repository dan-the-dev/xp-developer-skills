# TDD checklist — feature slice and R–G–R

Use for the **whole slice** (test list) and each **cycle** before squash and push.

---

## Test list (before first RED)

- [ ] **Markdown file** created at resolved path (project convention **or** `test-lists/<slug>.md` at repo root)
- [ ] Filename stem matches **branch and/or feature** (kebab-case; see [test-list.md](../references/test-list.md))
- [ ] File is **tracked** (not only in chat); folder exists
- [ ] File lists **behavior cases only** — no refactor-only or tech-debt lines (use `-follow-ups.md` or closing reply for those)
- [ ] Next open `[ ]` line chosen before writing the next failing test
- [ ] New **behavior** discoveries **appended** as new `[ ]` lines

---

## Three Laws (every cycle)

- [ ] **Law 1**: No production code except to satisfy a **current** failing test
- [ ] **Law 2**: Test code added only up to the point of **failure** (compile/type error counts)
- [ ] **Law 3**: Production code only enough to **pass that one** failing test (fake / obvious / triangulation OK)

---

## RED

- [ ] Single focused failing test added or extended
- [ ] Failure observed and matches intent (including compile-as-RED if applicable)
- [ ] Only test (and test-local fixtures) staged
- [ ] Commit: `test: …`

---

## GREEN

- [ ] Smallest production change to pass (fake / obvious / triangulation as appropriate)
- [ ] Same narrow test scope passes
- [ ] No drive-by refactor mixed in
- [ ] Only production files for this fix staged
- [ ] Commit: `feat: …`

---

## REFACTOR

- [ ] All relevant tests green **before** starting
- [ ] **One small mechanical step** at a time; **tests run after each step**
- [ ] If any test fails: **reverted** or reset to last green before proceeding
- [ ] Behavior unchanged (structure, names, extraction, duplication removal)
- [ ] **Proximity**: changes focused on code touched for this list item; no opportunistic distant cleanups
- [ ] Staged changes are refactor-only
- [ ] Commit: `refactor: …` (or omit if truly nothing to improve)

---

## Squash and push

- [ ] Squash micro-commits for **this** cycle into one
- [ ] Final title aligns with GREEN `feat:` intent
- [ ] Tests re-run after squash
- [ ] Single push of the squashed commit (per branch policy)

---

## Slice complete

- [ ] Every test list item **done** (or explicitly removed by agreement)
- [ ] Suite green

---

## Discipline

- [ ] Fastest practical test command used after each RED, GREEN, and refactor micro-step
- [ ] Tests assert **behavior**, not private implementation details
