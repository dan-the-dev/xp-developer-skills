# TDD checklist — feature slice and R–G–R

Use for the **whole slice** (test list) and each **cycle** before squash and push.

---

## Test list (before first RED)

- [ ] **Markdown file** created at resolved path (project convention **or** `test-lists/<slug>.md` at repo root)
- [ ] Filename stem matches **branch and/or feature** (kebab-case; see [test-list.md](../references/test-list.md))
- [ ] File is **tracked** (not only in chat); folder exists
- [ ] **Cases** list **behavior only** — no refactor-only or tech-debt lines (use `-follow-ups.md` or closing reply for those)
- [ ] Template includes optional **Deferred behavior** / **Removed** sections when needed
- [ ] Next open `[ ]` line in **Cases** chosen before writing the next failing test
- [ ] New **behavior** discoveries **appended** to **Cases**; deferred/out-of-scope handled per [test-list.md](../references/test-list.md)

---

## Three Laws (every cycle)

- [ ] **Law 1**: No production code except to satisfy a **current** failing test
- [ ] **Law 2**: Test code added only up to the point of **failure** (compile/type error counts)
- [ ] **Law 3**: Production code only enough to **pass that one** failing test (fake / obvious / triangulation OK)

---

## RED

- [ ] Single focused failing test added or extended
- [ ] Failure observed and is the **intended** signal (not flake, timeout, or wrong assertion)
- [ ] Only test (and test-local fixtures) staged
- [ ] Commit: `test: …`

---

## GREEN

- [ ] Smallest production change to pass (fake / obvious / triangulation as appropriate)
- [ ] Same narrow test scope passes
- [ ] No drive-by refactor mixed in
- [ ] Only production files for this fix staged
- [ ] Commit: `feat: …` **or** `fix: …` (use **fix** when the RED test encodes a bug/regression in existing behavior)

---

## REFACTOR

- [ ] All relevant tests green **before** starting
- [ ] **One small mechanical step** at a time; **tests run after each step**
- [ ] If any test fails: **reverted** or reset to last green before proceeding
- [ ] Behavior unchanged (structure, names, extraction, duplication removal in **production and/or tests**)
- [ ] **Proximity**: changes focused on code touched for this list item; no opportunistic distant cleanups
- [ ] **Simple Design** ([`docs/simple-design.md`](../../../docs/simple-design.md)): Beck 4 rules on touched code
- [ ] **Object Calisthenics** mandatory on owned OO touched this cycle ([`docs/object-calisthenics.md`](../../../docs/object-calisthenics.md)) — no `else`, one indent level, tell-don’t-ask, etc. (or stated boundary exception)
- [ ] **Patterns** only toward evidenced smells — not speculative ([`docs/design-quality.md`](../../../docs/design-quality.md))
- [ ] Staged changes are refactor-only (may be **test-only** files)
- [ ] Commit: `refactor: …` (or omit if truly nothing to improve)

---

## Squash and push

- [ ] Squash micro-commits for **this** cycle into one
- [ ] Final title aligns with GREEN subject (`feat:` or `fix:`)
- [ ] Tests re-run after squash
- [ ] Single push of the squashed commit (per branch policy)

---

## Slice complete

- [ ] Every **Cases** line `[x]` with **test reference** or documented in **Removed**
- [ ] No orphan `[ ]` in **Cases** unless intentionally blocked — then resolve per test-list lifecycle
- [ ] **Deferred behavior** rows closed (implemented, removed, or ticketed per agreement)
- [ ] Suite green

---

## Discipline

- [ ] Fastest practical test command used after each RED, GREEN, and refactor micro-step
- [ ] Tests assert **behavior** at a **stable seam**; avoid over-mocking (see [behavior-and-tests.md](../references/behavior-and-tests.md))
- [ ] Tests use clear structure (AAA, names); minimal logic in tests (see [test-quality.md](../references/test-quality.md))
