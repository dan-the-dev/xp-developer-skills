# Bibliography — `skills/refactoring` skill

Ties the **Fowler-style refactoring** skill to published sources. The skill body avoids long citations during procedures; use this page for depth and maintenance.

---

## Primary references

- **Fowler, Martin.** *Refactoring: Improving the Design of Existing Code* (2nd ed. w/ Kent Beck, 2018).  
  Core definitions, catalog of refactorings, “two hats,” composing small steps, connection to testing.

- **Fowler, Martin.** [Refactoring.com](https://refactoring.com/) — online catalog of techniques (names and mechanics).

- **Beck, Kent.** *Extreme Programming Explained*; *Test Driven Development: By Example*; *Implementation Patterns.*  
  Small reversible steps, continuous green, courage enabled by tests, simple design.

- **Fowler, Martin.** [Beck Design Rules](https://martinfowler.com/bliki/BeckDesignRules.html); [Yagni](https://martinfowler.com/bliki/Yagni.html); [TellDontAsk](https://martinfowler.com/bliki/TellDontAsk.html).  
  Four rules of simple design; YAGNI vs malleability; co-locate data and behavior without getter eradication dogma.

- **Kerievsky, Joshua.** *Refactoring to Patterns.*  
  Patterns as refactoring destinations — to / towards / away from — not up-front blueprints.

- **Gamma, Erich; Helm, Richard; Johnson, Ralph; Vlissides, John.** *Design Patterns* (GoF).  
  Named solutions; AMPD uses via [`design-patterns.md`](design-patterns.md) with when/when-not.

- **Bay, Jeff.** Object Calisthenics (*The ThoughtWorks Anthology*).  
  Mandatory OO constraints in AMPD Simple Design — [`object-calisthenics.md`](object-calisthenics.md).

- **Farley, David.** *Continuous Delivery* (with Jez Humble); talks and articles on batch size and pipeline discipline.  
  Integrating small safe changes; keeping the software always in a releasable state; avoid hypothetical platforms.

- **Cupać (Jemuović), Valentina.** [Quality Software Faster](https://valentinacupac.com/); TDD / Clean Architecture teaching (Optivem, handbook material).  
  Tests **coupled to behavior**, **decoupled from structure** — sustainable refactoring under changing internals.

---

## Related material

- **Feathers, Michael.** *Working Effectively with Legacy Code.*  
  For code **without** tests: seams, characterization, sprout/wrap before larger refactorings — see **`skills/legacy-testing`**.

- **Wake, William C.** *Refactoring Workbook.*  
  Practice-oriented exercises.

- **Martin, Robert C.** *Clean Code* — switch/polymorphism and Open/Closed; tolerate a single factory `switch`.

---

## Map to skill sections

| Skill topic | Sources |
|-------------|---------|
| Definition, two hats, catalog | Fowler |
| Baby steps, revert on red | Beck; Fowler mechanics |
| Green baseline, widen scope | Fowler; CD discipline; TDD skill cross-ref |
| Rule of three, naming | Community DRY nuance; Beck simplicity; Fowler smells |
| Simple Design, YAGNI, calisthenics, patterns-as-destinations | Beck; Fowler bliki; Bay; Kerievsky; GoF; [`docs/simple-design.md`](simple-design.md) |
| Tests vs structure | Cupać; Feathers when legacy |
| CD / small integrates | Farley, Humble |

When evolving `skills/refactoring/SKILL.md`, update this bibliography if new canonical sources are adopted.
