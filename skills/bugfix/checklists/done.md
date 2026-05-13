# Bugfix Completion Checklist

A bugfix is complete only if ALL items are satisfied.

---

## Repository

- [ ] Started from latest main
- [ ] Working tree clean before changes
- [ ] Dedicated bugfix branch created

---

## Reproduction

- [ ] Bug behavior understood
- [ ] Expected behavior identified
- [ ] **Invariant / contract** stated in one line (what must hold when fixed)
- [ ] Automated reproduction exists and asserts that invariant (not only “throws” or “fails”)
- [ ] Failing test confirmed (RED)

---

## RED Commit

- [ ] Only tests included
- [ ] Commit isolated
- [ ] Commit message correct

---

## GREEN Fix

- [ ] Minimal fix applied
- [ ] Fix restores the **violated invariant**, not only silences the symptom
- [ ] No unrelated edits
- [ ] No refactoring performed
- [ ] Existing conventions respected

---

## Verification

- [ ] Failing test now passes **without** weakened assertions
- [ ] Related regressions checked
- [ ] Validation executed incrementally
- [ ] No flaky behavior observed

---

## GREEN Commit

- [ ] Only fix changes included
- [ ] Commit isolated
- [ ] Commit message correct

---

## Git

- [ ] Branch pushed upstream
- [ ] No PR opened automatically
- [ ] No history rewriting performed

---

## Scope Discipline

- [ ] Scope remained focused
- [ ] No opportunistic cleanup added
- [ ] No architecture changes introduced

---

## Final State

- [ ] Bug resolved safely
- [ ] Reviewability preserved
- [ ] Changes reversible
- [ ] Skill stop condition respected
- [ ] **Root cause** (one short paragraph) and **recurrence prevention** (one short paragraph) recorded in the bugfix summary output
