# Simple Design (AMPD)

**Compass for structure work in AMPD:**

> Simple Design + YAGNI as the compass; Object Calisthenics as mandatory OO discipline inside Simple Design; Gang of Four patterns as destinations that emerge via refactoring (Kerievsky)—not as up-front blueprints or production law by themselves.

This is how AMPD resolves **simplicity vs patterns**: pass tests and keep code small and clear; apply calisthenics on the code you own; introduce a named pattern only when refactoring toward it removes real duplication or clarifies intention without inventing speculative flexibility.

---

## Beck’s four rules (priority order)

Judge design after every **REFACTOR** (and in post-increment review) with these rules, in order:

| # | Rule | Meaning |
|---|------|---------|
| 1 | **Passes the tests** | Behavior is correct and guarded by automated checks. Nothing else matters if this fails. |
| 2 | **Reveals intention** | Names, types, and structure express *why* the code exists; a reader can see the design ideas. |
| 3 | **No duplication** | Say each idea once (including hidden duplication such as parallel conditionals on the same type/state). |
| 4 | **Fewest elements** | Prefer the smallest set of classes, methods, and indirection that still satisfies 1–3. |

Rule **4** is the brake against overengineering: a Strategy hierarchy with one concrete variant, or an Abstract Factory “for later,” violates fewest elements.

Authoritative framing: [Beck Design Rules](https://martinfowler.com/bliki/BeckDesignRules.html) (Kent Beck / Martin Fowler).

---

## YAGNI (You Aren’t Gonna Need It)

YAGNI forbids **capabilities built for presumed future features**. It does **not** forbid:

- refactoring that makes code easier to change
- Object Calisthenics compliance on current code
- introducing a pattern that solves a **present** smell (duplication, type/state branching, unclear intention)

YAGNI *does* forbid speculative pattern catalogs, “extension points” nobody asked for, and platforms invented ahead of need.

See [Yagni](https://martinfowler.com/bliki/Yagni.html) (Martin Fowler). Incremental / evolutionary design (Dave Farley and Continuous Delivery practice) depends on malleable code *and* refusing hypothetical features.

---

## Object Calisthenics (mandatory)

For OO code that AMPD agents **write or change**, the nine Object Calisthenics rules are **mandatory** Simple Design constraints — not optional style tips.

Full rules and boundary exceptions: [`object-calisthenics.md`](object-calisthenics.md).

Calisthenics operationalize rules 2–4 (intention, no duplication, fewest *coherent* elements via small objects and polymorphism). They push agents away from procedural Actions with nested `if`/`else` toward tell-don’t-ask and polymorphic behavior.

---

## Patterns as emerged destinations

Gang of Four patterns are **standard solutions to recurring structural problems**. In AMPD:

1. Write the simplest green code that passes tests.
2. Apply calisthenics and Fowler micro-refactorings on green.
3. When type/state/algorithm branching or duplicated conditionals persist, **refactor toward** a named pattern (often Strategy, State, Factory Method, Null Object, Template Method).
4. If a pattern no longer earns its keep, **refactor away** from it (inline, simplify).

Do **not** pick a pattern in GREEN to “be ready.” Patterns appear in **REFACTOR** (or a dedicated refactor session) with evidence. Catalog and when/when-not: [`design-patterns.md`](design-patterns.md). Smell → move map: [`design-quality.md`](design-quality.md).

Primary bridge: Joshua Kerievsky, *Refactoring to Patterns* (refactor **to / towards / away from** patterns).

---

## Agent obligations (summary)

| When | Do |
|------|----|
| After GREEN (TDD REFACTOR) | Apply Beck 4 rules + **mandatory** calisthenics on touched OO code; consider pattern only if smell remains |
| Increment done | Report a **Design** note in the return payload ([`delivery-process.md`](delivery-process.md) §10) |
| Post-increment review | Flag calisthenics breaches and unjustified pattern theater; suggest or apply tiny in-surface fixes |
| PR review | Must-fix calisthenics / Simple Design breaches on owned OO code in the diff; should-fix speculative patterns |

---

## Related

- [`object-calisthenics.md`](object-calisthenics.md)
- [`design-patterns.md`](design-patterns.md)
- [`design-quality.md`](design-quality.md)
- [`delivery-process.md`](delivery-process.md) §6 REFACTOR, §10 return payload
- Skills: `skills/tdd`, `skills/refactoring`, `skills/new-increment`
