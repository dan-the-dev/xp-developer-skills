# Pinch points and effect sketches

## Pinch points

A **pinch point** is a natural choke point in the design: **few tests** exercise **many** dependent paths.

Examples:

- public API on a façade
- single function every code path calls before persisting
- message handler entry

**Use:** invest seam work at pinch points first — maximum confidence per test effort.

---

## Effect sketches

Before editing, sketch **how effects flow**:

- Which variables / fields change?
- Who reads them next?
- What I/O fires?

Feathers suggests **lightweight diagrams** — not full UML — to see **blast radius**.

**Use:** decide where characterization will **catch** accidental breakage; avoid editing until you know what “done” must preserve.

---

## Heuristics

- If a sketch looks like **spaghetti**, **narrow** your change scope or add **sprout** at the edge ([sprout-and-wrap.md](sprout-and-wrap.md)).

- If **one** assert at a pinch point is enough, don’t build five tests on internals.

---

## Farley / CD

Smaller blast radius per merge **reduces** pipeline risk — prefer changes that **shrink** the effect sketch step by step rather than one giant PR.
