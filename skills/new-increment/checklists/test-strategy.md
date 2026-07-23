# Test strategy — before first RED

Complete **before** adding the first failing check for this increment.

Reference: [`docs/test-strategy-selection.md`](../../../docs/test-strategy-selection.md).

---

## Slice characterization

- [ ] Backlog line (verbatim): ___
- [ ] Slice type: domain logic | API | UI component | UI journey | legacy | integration | bugfix | other: ___
- [ ] What could break **silently** without the right layer? ___

---

## Project discovery

- [ ] Checked CI, scripts, and config for existing jobs: unit, integration, component, contract, mutation, property-based, a11y, smoke, E2E
- [ ] Listed configured tools found: ___

---

## Decision table (fill every row you evaluated)

| Practice | adopt / skip / N/A | Reason |
|----------|-------------------|--------|
| Unit TDD | | |
| Narrow integration | | |
| Component / UI | | |
| API acceptance / ATDD | | |
| Gherkin (if ATDD) | | code-first vs `*.feature` |
| Contract / schema | | |
| Characterization | | |
| Property-based | | |
| **Mutation testing** | | |
| Snapshot / approval | | |
| Accessibility | | |
| Smoke | | |
| E2E | | |

Minimum **5 practices** evaluated for non-trivial slices (always include **Mutation** and an **ATDD/acceptance** row).

---

## Layer choice (one per concern)

- [ ] Primary layer for this increment: ___
- [ ] Secondary layer (only if different boundary): ___ or none
- [ ] Confirmed: no duplicate assertion at same boundary ([delivery-process §4](../../../docs/delivery-process.md))

---

## If mutation adopted

- [ ] Command: ___
- [ ] Scope: changed files / module / full
- [ ] Tooling: already present | **added this slice** (greenfield, threshold met) | deferred with reason (setup ≫ slice / teaching / brownfield)
- [ ] Run at: before marking increment `[x]` (required when adopted) | deferred to CI with reason (exceptional)
- [ ] Surviving mutants addressed or **justified/deferred** with reason

---

## Return payload

- [ ] Test strategy table included in closing report ([test-strategy-selection §6](../../../docs/test-strategy-selection.md))
