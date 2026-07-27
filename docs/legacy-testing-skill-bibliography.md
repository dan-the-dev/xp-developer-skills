# Bibliography — `skills/legacy-testing` skill

Primary source and adjacent authorities referenced across AMPD skills.

---

## Primary

- **Feathers, Michael.** *Working Effectively with Legacy Code.* Prentice Hall, 2004.  
  Legacy definition (no tests), change algorithm, seams (preprocessing, link, object), sensing vs separation, characterization tests, sprout/wrap, pinch points, effect sketches, dependency-breaking catalog, monsters, libraries.

---

## Composed authorities (same voices as other skills)

- **Fowler, Martin.** *Refactoring*; refactoring.com — mechanical seam creation **after** harness exists. [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html) — fake/stub vs mock when wrapping third-party libraries; prefer real sandbox when testing the owned adapter.

- **Beck, Kent.** *Test Driven Development: By Example*; *Extreme Programming Explained* — small steps, tests enable design changes.

- **Farley, David / Humble, Jez.** *Continuous Delivery* — small batches, automated verification, releasable increments even during hardening work.

- **Cupać (Jemuović), Valentina.** Quality Software Faster / Optivem material — behavior-stable tests, ports & adapters as target seams.

---

## Adjacent

- **Khorikov, Vladimir.** *Unit Testing Principles, Practices, and Patterns* — doubles, test design, maintainable suites.

- **Freeman & Pryce.** *Growing Object-Oriented Software, Guided by Tests* — outside-in with emerging design (complements ATDD + legacy seams).

---

## Map to skill

| Section | Main source |
|---------|-------------|
| Definition & algorithm | Feathers |
| Seams, sprout/wrap, catalog | Feathers |
| Characterization | Feathers |
| Aligned table | Fowler, Beck, Farley, Cupać (AMPD synthesis) |
| Third-party libraries / vendor adapters | Feathers (wrappers); Fowler *Mocks Aren't Stubs*; `test-strategy-selection` §3a |

Update this file when the skill adopts additional canonical references.
