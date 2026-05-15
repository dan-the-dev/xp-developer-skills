# ATDD checklist — scenario and test quality (Distill / before GREEN merge)

Use when adding or changing **one** automated acceptance example.

---

## Readability

- [ ] Name/scenario states the **business rule**, not the click path
- [ ] Given / When / Then (or equivalent) is clear to a non-programmer
- [ ] Catalog line links to automation (`file::scenario` or test name)

---

## Outcomes

- [ ] **Then** asserts observable business outcomes
- [ ] No assertion on private internals unless that **is** the published contract
- [ ] Failure messages would make sense to someone debugging “wrong feature”

---

## Scope

- [ ] **One** primary rule per scenario/test (split if multiple)
- [ ] Setup is minimal for this example
- [ ] Not duplicating unit-level branches already covered at unit layer without reason

---

## Distill (RED)

- [ ] Test fails for **missing/wrong behavior**, not env/config flake
- [ ] Re-run or inspect failure reason if unsure
- [ ] Layer matches prior [pipeline-fit](pipeline-fit.md) decision

---

## Develop (GREEN)

- [ ] Acceptance passes for this example
- [ ] Inner TDD cases for this slice are green or explicitly deferred with agreement
- [ ] Catalog line `[x]` with automation reference

---

## Maintainability

- [ ] Step definitions / helpers are domain-level (Gherkin) or shared fixtures (code-first)
- [ ] No hard-coded `sleep` without condition-based wait
- [ ] Test data isolated from other scenarios

---

## CI

- [ ] Tagged appropriately (`@smoke` etc.) if suite is split
- [ ] Runtime acceptable for intended pipeline stage
