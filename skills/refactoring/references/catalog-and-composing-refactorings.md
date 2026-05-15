# Catalog and composing refactorings (Martin Fowler)

## Named refactorings

Martin Fowler’s *Refactoring* catalogs **named** transformations (e.g. **Extract Function**, **Rename Variable**, **Replace Temp with Query**, **Introduce Parameter Object**).

Each name stands for:

- **Motivation** — why you might use it
- **Mechanics** — small, ordered steps
- **Tradeoffs** — when **not** to use it

This skill does **not** duplicate the full catalog — keep the book or [refactoring.com](https://refactoring.com) at hand for mechanics.

---

## Compose small refactorings

Large design changes are **sequences** of small ones:

1. **Prepare** — maybe *Rename* for clarity so *Extract* is obvious.
2. **Extract** — pull a chunk to a function or type.
3. **Move** — relocate to the right module.
4. **Simplify** — inline or replace conditional with polymorphism **only** when behavior stays identical.

After **each** named refactoring (or sub-step the book breaks out), **run tests**.

---

## Picking the next refactoring

Ask:

- What **smell** am I fixing? (long method, feature envy, duplicated logic, mystery name)
- Which **named** refactoring addresses that smell with **least** risk?
- What is the **smallest** instance of it I can apply here?

---

## When the catalog is not enough

Sometimes you need **preparatory** refactorings:

- *Decompose* a huge function before *Extract Class* makes sense.
- *Split loop* or *Substitute Algorithm* (dangerous — needs **very** strong tests).

High-risk transformations: **even smaller** steps, **more** frequent green checks, **pair** or review when the team norm requires.

---

## Learning path

- Junior: master **Rename**, **Extract**, **Inline**, **Move** — they cover most day-to-day tidying.
- Advanced: *Replace Conditional with Polymorphism*, *Introduce Phase*, etc. — always **compose** from smaller verified steps where possible.
