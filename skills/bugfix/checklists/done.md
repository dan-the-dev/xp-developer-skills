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
- [ ] Automated reproduction exists
- [ ] Failing test confirmed (RED)

---

## RED Commit

- [ ] Only tests included
- [ ] Commit isolated
- [ ] Commit message correct

---

## GREEN Fix

- [ ] Minimal fix applied
- [ ] No unrelated edits
- [ ] No refactoring performed
- [ ] Existing conventions respected

---

## Verification

- [ ] Failing test now passes
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
