# Object Calisthenics (mandatory Simple Design)

Object Calisthenics are nine OO constraints introduced by **Jeff Bay** (*The ThoughtWorks Anthology*). In AMPD they are **mandatory** for object-oriented code that agents write or change — they are how Simple Design is enforced day to day, not a kata-only exercise.

**Compass:** [`simple-design.md`](simple-design.md) — Simple Design + YAGNI; calisthenics mandatory; patterns as emerged destinations.

Bay originally framed the rules as extreme training constraints. AMPD adopts them as **production discipline for owned domain and application OO**, with narrow boundary exceptions below. The goal is encapsulation, polymorphism instead of branching, and small cohesive types — so procedural god-Actions and nested `if`/`else` do not ship as “done.”

---

## The nine rules (mandatory)

### 1. Only one level of indentation per method

Nested control flow usually means the method does too much. Extract until each method has at most one nesting level (e.g. one `for` *or* one `if`, not `for` containing `if` containing …).

**Supports:** intention, small methods, testability.

### 2. Don’t use the `else` keyword

Prefer early returns (guard clauses) or **polymorphism** for alternate paths. Chains of `if` / `else if` that select behavior by type or state are a design smell — refactor toward Strategy, State, or subclasses ([`design-quality.md`](design-quality.md)).

**Supports:** fewer branches, Tell Don’t Ask, Open/Closed pressure handled by new types not new `else`s.

### 3. Wrap primitives and strings that mean a domain concept

Avoid primitive obsession for domain ideas (`Email`, `Money`, `Hour`, `PlayerId`). Do **not** wrap every `string`/`int` at infrastructure boundaries without domain meaning.

**Supports:** type safety, validation homes, intention.

### 4. First-class collections

A class that contains a collection should contain **no other** member fields. Collection behavior (filter, sort, aggregate, invariants) lives on that type.

**Supports:** encapsulation of collection rules; prevents service classes from owning both a list and unrelated state.

### 5. One dot per line (Law of Demeter)

Do not chain through strangers (`a.getB().getC().doX()`). Talk only to objects you own, created, or were passed. Extract or tell the intermediate object to do the work.

**Supports:** lower coupling; Tell Don’t Ask.

### 6. Don’t abbreviate

Names stay clear and pronounceable. Urge to abbreviate often means the type or method has too many responsibilities — split instead of shorten.

**Supports:** reveals intention.

### 7. Keep entities small

Prefer classes small enough to grasp at a glance (Bay’s training target was ~50 lines / package ~10 files). Exact counts are guidance; **bloated** entities are not acceptable “because frameworks.”

**Supports:** cohesion; fewest *clear* elements.

### 8. No more than two instance variables

Decompose richer state into focused collaborators or value objects. If a type needs many fields, group related fields into a new concept.

**Supports:** extreme encapsulation; clear object graphs.

### 9. No getters/setters/properties for behavior decisions

Prefer **Tell, Don’t Ask**: objects act on their own data. Do not pull fields out to branch in a controller/Action. Query methods remain acceptable when they *reveal information* without turning callers into the behavior owner (see Fowler’s nuance on Tell Don’t Ask) — but domain decisions belong with the data.

**Supports:** encapsulation; pushes branching into polymorphic types.

---

## Boundary exceptions (narrow)

Calisthenics apply to **owned OO domain and application code**. Document an exception when you must breach them; do not silently ignore.

| Allowed exception | Why |
|-------------------|-----|
| Framework / serializer **DTOs** and API contracts at the edge | External shape owned by protocol or library |
| Generated code | Not hand-designed |
| Language/runtime idioms required by a framework constructor or ORM mapping at the adapter edge | Keep calisthenics **inside** the domain; wrap at the seam |
| Teaching/kata when the user explicitly relaxes rules | User override only |

**Not** exceptions: “it’s an Action/Service/UseCase so procedural if/else is fine,” “only two cases,” “we’ll clean it later” without a follow-up — those fail Simple Design.

---

## Relationship to patterns

Calisthenics often **surface** the need for a GoF pattern (especially rule 2 → Strategy/State; rule 9 → move behavior onto types). Introduce the pattern via green refactoring when the smell is real — see [`design-patterns.md`](design-patterns.md) and [`design-quality.md`](design-quality.md). Do not invent hierarchies to satisfy a rule in the abstract while violating Beck rule 4 (fewest elements).

---

## Agent checklist (touched OO code)

Before claiming REFACTOR or increment done:

- [ ] Methods ≤ one indentation level (or extracted)
- [ ] No `else` in owned OO; guards or polymorphism instead
- [ ] Domain primitives wrapped where they carry meaning
- [ ] Collections first-class when they own behavior
- [ ] No Demeter chains
- [ ] Clear unabbreviated names
- [ ] Types stay small; ≤ two instance variables or decomposed
- [ ] Callers tell objects; no ask-then-branch god methods

Violations on code introduced or substantially edited in the slice are **blocking** for increment done and **must-fix** in PR review unless a listed boundary exception is stated.

---

## Sources

- Jeff Bay — Object Calisthenics (*The ThoughtWorks Anthology*)
- AMPD framing: [`simple-design.md`](simple-design.md)
- Tell Don’t Ask nuance: [martinfowler.com/bliki/TellDontAsk.html](https://martinfowler.com/bliki/TellDontAsk.html)
