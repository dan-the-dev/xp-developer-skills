# Aligned practices (Fowler, Beck, Farley, Cupać)

This skill is **Feathers-first**, but the same voices as the rest of AMPD skills keep it honest.

---

## Martin Fowler

- **Refactoring** is **cheap** once you have a **green** characterization net — use `skills/refactoring` for mechanical improvement.
- **Two hats:** dependency-breaking seams may be **refactoring** (no behavior change) — keep commits honest.
- **Catalog** refactorings (Extract Method, Introduce Parameter Object) are often how you **install** seams after sprout/wrap.

---

## Kent Beck

- **Small steps** with **fast feedback** — even in legacy, don’t stack five untested changes.
- **Courage** comes from **tests** — legacy work is how you **buy** that courage.
- **TDD** applies **after** harness: new behavior still grows from failing tests.

---

## Dave Farley (Continuous Delivery)

- **Slice** legacy work so **main stays releasable** (or branch policy equivalent) — huge “test freeze” branches are a delivery smell.
- **Automate** verification: characterization belongs in CI like any other test.
- Prefer **feedback loops** measured in minutes, not days — lean on pinch points and fakes.

---

## Valentina Cupać

- Tests **coupled to behavior**, **decoupled from structure** — critical when adding seams; otherwise every seam triggers brittle breakage.
- **Clean/hexagonal** boundaries are a **target state**; sprout/wrap and adapters **move** toward ports without big-bang rewrites.

---

## Skill composition (default)

| Phase | Skill |
|-------|--------|
| Harness + characterization | **`legacy-testing`** (this) |
| Known defect | **`bugfix`** after repro runnable |
| New inner behavior | **`tdd`** |
| Structure only (green) | **`refactoring`** |
| Business-visible slice | **`atdd`** (if product-facing) |
