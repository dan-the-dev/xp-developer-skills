# Design patterns (GoF) — destinations, not blueprints

Classic **Gang of Four** patterns name recurring solutions. In AMPD they are **destinations you refactor toward** when Simple Design and Object Calisthenics expose a lasting structural problem — not menus to pick from during GREEN.

**Compass:** [`simple-design.md`](simple-design.md)

> Simple Design + YAGNI as the compass; Object Calisthenics mandatory; patterns as emerged destinations (Kerievsky).

Primary method: Joshua Kerievsky, *Refactoring to Patterns* — refactor **to**, **towards**, or **away from** a pattern with small Fowler steps on a green suite.

Operational smell → move map: [`design-quality.md`](design-quality.md).

---

## When to introduce a pattern

Introduce (or move toward) a named pattern when **all** of the following hold:

1. Tests are green (refactor hat).
2. Object Calisthenics / Beck rules still leave a clear smell (e.g. type/state selects behavior; same conditional in multiple places; Open/Closed pressure).
3. Evidence of recurrence — align with the **rule of three** (third similar case, or the same switch already duplicated).
4. The pattern **improves** intention and/or removes duplication **without** violating fewest elements (Beck rule 4).

Typical AMPD targets for domain/application code:

| Smell | Pattern destination |
|-------|---------------------|
| Algorithm or policy varies by case | **Strategy** |
| Behavior changes with object lifecycle/state | **State** |
| Conditional on type code / enum selecting behavior | Replace type code → **State/Strategy** or subclasses + polymorphism |
| One place must construct varying types | **Factory Method** (keep the only `switch` here) |
| Missing “do nothing” case littered with null checks | **Null Object** |
| Shared algorithm skeleton, steps vary | **Template Method** |
| Incompatible interfaces at a boundary | **Adapter** |
| Need a simple front for a subsystem | **Facade** |

Martin Fowler: [*Replace Conditional with Polymorphism*](https://refactoring.com/catalog/replaceConditionalWithPolymorphism.html). Robert C. Martin: tolerate a `switch` when it appears **once**, typically to create polymorphic objects — not scattered through domain logic.

---

## When *not* to introduce a pattern

| Situation | Prefer |
|-----------|--------|
| One or two simple branches, no duplication | Guard clauses / extract method (still **no `else`** per calisthenics) |
| “We might need another variant later” | YAGNI — wait for the third case |
| Pattern would add types without clarifying intention | Beck rule 4 — fewest elements |
| Only one Strategy/State concrete class | Inline; refactor **away** from the pattern |
| Using a pattern because it is famous | Golden hammer — reject |

Speculative Abstract Factory, Visitor, or deep Decorator stacks for hypothetical extension are anti-patterns under AMPD.

---

## How patterns enter the workflow

1. **GREEN** — simplest code that passes (may temporarily look procedural).
2. **REFACTOR** — apply Object Calisthenics; extract; remove `else`; if type/state branching remains with evidence → compose Fowler steps toward Strategy/State/etc.
3. **Dedicated refactor / post-increment review** — catch leftover procedural Actions; apply tiny in-surface moves or record follow-ups.
4. **Away from pattern** — if the hierarchy no longer pays for itself, inline and simplify.

Never add a pattern to satisfy a future backlog line in the current increment.

---

## Catalog (Gang of Four)

Purpose: **creational**, **structural**, **behavioral**. Scope: **class** (inheritance, often compile-time) vs **object** (composition, runtime). Most useful destinations for AMPD delivery work are **object** scope behavioral patterns (Strategy, State, Command, Observer, …) plus Factory Method / Adapter / Facade at seams.

### Creational

#### Scope: Class

**Factory Method** — Define an interface for creating an object, but let subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses.

#### Scope: Object

**Abstract Factory** — Provide an interface for creating families of related or dependent objects without specifying their concrete classes.

**Builder** — Separate the construction of a complex object from its representation so that the same construction process can create different representations.

**Prototype** — Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype.

**Singleton** — Ensure a class only has one instance, and provide a global point of access to it. *(Prefer explicit composition over Singleton in new AMPD code; treat as legacy/compatibility.)*

### Structural

#### Scope: Object

**Adapter** — Convert the interface of a class into another interface clients expect.

**Bridge** — Decouple an abstraction from its implementation so that the two can vary independently.

**Composite** — Compose objects into tree structures to represent part-whole hierarchies.

**Decorator** — Attach additional responsibilities to an object dynamically.

**Facade** — Provide a unified interface to a set of interfaces in a subsystem.

**Flyweight** — Use sharing to support large numbers of fine-grained objects efficiently.

**Proxy** — Provide a surrogate or placeholder for another object to control access to it.

### Behavioral

#### Scope: Class

**Interpreter** — Given a language, define a representation for its grammar along with an interpreter.

**Template Method** — Define the skeleton of an algorithm in an operation, deferring some steps to subclasses.

#### Scope: Object

**Chain of Responsibility** — Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request.

**Command** — Encapsulate a request as an object (parameterize, queue, log, undo).

**Iterator** — Access elements of an aggregate sequentially without exposing representation.

**Mediator** — Encapsulate how a set of objects interact.

**Memento** — Capture and externalize internal state for later restore without breaking encapsulation.

**Observer** — One-to-many dependency: dependents notified of state changes.

**State** — Allow an object to alter its behavior when its internal state changes.

**Strategy** — Define a family of algorithms, encapsulate each one, and make them interchangeable.

**Visitor** — Represent an operation to be performed on elements of an object structure without changing their classes. *(High cost — prefer only with clear multi-operation / stable structure evidence.)*

---

## Related

- [`simple-design.md`](simple-design.md)
- [`object-calisthenics.md`](object-calisthenics.md)
- [`design-quality.md`](design-quality.md)
- `skills/refactoring` — compose small Fowler steps toward these destinations
