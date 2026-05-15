# Dependency-breaking techniques (catalog orientation)

Feathers catalogs many **mechanical** ways to introduce seams. Use the book for full recipes; this reference orients agents toward the **right family** of moves.

---

## Common patterns

| Technique | Rough idea |
|-----------|------------|
| **Extract Interface** | Client depends on interface; production uses real impl; tests inject fake. |
| **Subclass and Override Method** | Test subclass overrides e.g. DB access; use short-term if DI is far away. |
| **Parameterize Constructor / Method** | Stop `new` inside constructor; take collaborators from outside. |
| **Introduce Instance Delegation** | Replace static or global with instance collaborator. |
| **Wrapper / Facade** | Thin boundary around ugly API or third-party library ([monsters-and-libraries.md](monsters-and-libraries.md)). |

---

## Rules

- **One technique per step** where possible; compile + test after each.
- Prefer **parameterization** and **interfaces** over permanent deep subclass trees in production — subclasses for testing are a **transition** tactic sometimes.
- **Fowler** refactorings ([`catalog-and-composing-refactorings.md`](../../refactoring/references/catalog-and-composing-refactorings.md)) often implement these seams — but only after you can **run tests**; may need **sprout/wrap** first ([sprout-and-wrap.md](sprout-and-wrap.md)).

---

## Don’t confuse with feature work

Breaking dependency **only** to test is often **`refactor:`** or `test:` commits — **no** user-visible behavior change. Verify with characterization still green.

---

## External source

Michael Feathers, *Working Effectively with Legacy Code* — detailed mechanics and when to avoid each technique.
