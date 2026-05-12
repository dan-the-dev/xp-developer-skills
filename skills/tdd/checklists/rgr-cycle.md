# RED → GREEN → REFACTOR cycle checklist

Use before squash and push.

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
- [ ] Staged changes are refactor-only
- [ ] Commit: `refactor: …` (or omit if truly nothing to improve)

---

## Squash and push

- [ ] Squash micro-commits for **this** cycle into one
- [ ] Final title aligns with GREEN `feat:` intent
- [ ] Tests re-run after squash
- [ ] Single push of the squashed commit (per branch policy)

---

## Discipline

- [ ] No production code before RED exists
- [ ] No more test than needed to fail; no more code than needed to pass
- [ ] Fastest practical test command used after each RED, GREEN, and refactor micro-step
- [ ] Tests assert **behavior**, not private implementation details
