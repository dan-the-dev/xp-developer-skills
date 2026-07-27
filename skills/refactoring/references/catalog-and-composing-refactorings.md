# Catalog and composing refactorings (Martin Fowler)

## Named refactorings

Martin Fowler’s *Refactoring* catalogs **named** transformations (e.g. **Extract Function**, **Rename Variable**, **Replace Temp with Query**, **Introduce Parameter Object**).

Each name stands for:

- **Motivation** — why you might use it
- **Mechanics** — small, ordered steps
- **Tradeoffs** — when **not** to use it

This skill does **not** duplicate the full catalog — keep the book or [refactoring.com](https://refactoring.com) at hand for mechanics.

AMPD design compass while composing: [`docs/simple-design.md`](../../../docs/simple-design.md) — calisthenics mandatory; patterns as destinations ([`docs/design-quality.md`](../../../docs/design-quality.md)).

---

## Compose small refactorings

Large design changes are **sequences** of small ones:

1. **Prepare** — maybe *Rename* for clarity so *Extract* is obvious.
2. **Extract** — pull a chunk to a function or type.
3. **Move** — relocate to the right module.
4. **Simplify** — remove `else` via guards; *Replace Conditional with Polymorphism* when type/state selects behavior and evidence warrants it.
5. **Toward pattern** (optional) — continue composing until Strategy/State/Factory Method/Null Object is the clear shape — or **stop earlier** if Beck rule 4 (fewest elements) is already satisfied.
6. **Away from pattern** — *Inline Method* / *Inline Class* when a hierarchy no longer earns its keep.

After **each** named refactoring (or sub-step the book breaks out), **run tests**.

---

## Pattern-directed sequences (Kerievsky)

When Object Calisthenics leave a lasting smell, compose toward a GoF destination:

| Destination | Typical Fowler building blocks |
|-------------|-------------------------------|
| **Strategy** / **State** | Extract Method → Extract Class → Replace Conditional with Polymorphism; optionally Replace Type Code with State/Strategy |
| **Factory Method** | Extract creation; keep the **only** type `switch` in the factory |
| **Null Object** | Introduce special case object; remove null checks at call sites |
| **Template Method** | Form Template Method after shared skeleton is clear |
| **Adapter** / **Facade** | Extract boundary type; move translation behind it |

Do **not** jump to the pattern name in one edit — baby steps, green between steps. Full when/when-not: [`docs/design-patterns.md`](../../../docs/design-patterns.md).

---

## Picking the next refactoring

Ask:

- What **smell** am I fixing? (long method, feature envy, duplicated logic, mystery name, `else` chain, type/state switch)
- Does **Object Calisthenics** already dictate the next move?
- Which **named** refactoring addresses that smell with **least** risk?
- What is the **smallest** instance of it I can apply here?
- If aiming at a pattern: do I have **evidence** (rule of three / duplicated switch), or would this violate fewest elements / YAGNI?

---

## When the catalog is not enough

Sometimes you need **preparatory** refactorings:

- *Decompose* a huge function before *Extract Class* makes sense.
- *Split loop* or *Substitute Algorithm* (dangerous — needs **very** strong tests).

High-risk transformations: **even smaller** steps, **more** frequent green checks, **pair** or review when the team norm requires.

---

## Learning path

- Junior: master **Rename**, **Extract**, **Inline**, **Move** — they cover most day-to-day tidying and most calisthenics fixes.
- Advanced: *Replace Conditional with Polymorphism*, *Replace Type Code with State/Strategy*, *Introduce Null Object*, Form Template Method — always **compose** from smaller verified steps; refactor **away** when the pattern is theater.
