# Discuss → Distill → Develop (operational)

Pragmatic ATDD uses three phases. Each phase has **inputs**, **outputs**, and **gates**.

---

## Phase map

| Phase | Input | Output | Gate to next |
|-------|--------|--------|----------------|
| **Discuss** | story / capability | example catalog with `[ ]` lines | examples are concrete; data/terms agreed |
| **Distill** | one catalog line | **one** failing automated check | fails for missing behavior, not noise |
| **Develop** | failing acceptance | acceptance green + inner TDD done for slice of code | catalog line `[x]` with reference |

Repeat **Distill → Develop** per example until the slice is done.

---

## Discuss — detail

**Activities**

- Walk through happy path and business-critical edges.
- Write catalog entries (bullets or Given/When/Then).
- Mark deferrals and out-of-scope items.

**Not required in Discuss**

- Gherkin syntax perfection.
- Full automation plan.
- Every edge case the testers can imagine.

**Exit criteria**

- At least one example clear enough to automate.
- Business can say “yes, that’s what I mean” for the next example.

---

## Distill — detail

**Activities**

- Pick **one** open catalog line.
- Choose **layer** ([pipeline-fit checklist](../checklists/pipeline-fit.md)).
- Implement the **smallest** automated check that proves the example.
- Run it → **RED** (intentional).

**Pragmatic choices**

- **Gherkin** when readability in PR matters and the team maintains step definitions well.
- **Code-first** when the repo already has strong acceptance helpers.
- **Contract test** when the capability **is** an API promise to another team or system.

**Exit criteria**

- Failure message maps to “not built yet,” not “wrong port” or “stale data.”
- Check is committed (or staged per team) as `test:` when using commit discipline.

---

## Develop — detail

**Activities**

- Drive production code **outside-in** (interfaces, adapters, UI flows as needed).
- Run **inner TDD** (`skills/tdd`) for units that need fast feedback.
- Re-run acceptance after each meaningful increment until **GREEN**.
- Refactor with **both** acceptance and unit tests green.

**Exit criteria**

- Acceptance check passes.
- Catalog line updated to `[x]` with automation reference.
- No extra business behavior added without a catalog line.

---

## Slicing large stories

1. Order examples by **business risk** and **learning** (not technical convenience only).
2. First example should be **thin** end-to-end or **thin** contract — “walking skeleton.”
3. Add examples incrementally; avoid automating ten scenarios before the first green path.

---

## Double-loop rhythm

```text
Discuss (catalog)
    → Distill (acceptance RED)
        → Develop
            → inner TDD cycles (test list RED-GREEN-REFACTOR)
        → acceptance GREEN
    → next example
```

Do not start the next **Distill** while acceptance is red for the **current** example (unless you deliberately pivot scope with catalog update).
