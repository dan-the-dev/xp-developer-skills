# Bibliography — `skills/atdd` skill

This note ties the repository’s **ATDD** agent skill to published sources. The skill body under `skills/atdd/` avoids long citations in the workflow text; maintainers use this page for traceability.

---

## Primary references

- **Beck, Kent.** *Extreme Programming Explained* (acceptance / customer tests); *Test Driven Development: By Example* (double-loop with programmer tests).  
  Customer-facing tests vs programmer tests; examples as communication.

- **Adzic, Gojko.** *Specification by Example: How Successful Teams Deliver the Right Software.* Manning, 2011.  
  Collaborative examples, living documentation, narrowing communication gaps — aligns with Discuss and executable specs.

- **Fowler, Martin.** [Specification By Example](https://martinfowler.com/bliki/SpecificationByExample.html) (bliki); [Testing Guide](https://martinfowler.com/testing/); [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html).  
  Examples over abstract specs; testing roles in agile delivery; classical preference for real/sandbox or fake/stub over mocking vendor types when acceptance touches external services.

- **Wynne, Matt; Hellesoy, Aslak.** *The Cucumber Book* (BDD with Gherkin).  
  Scenario structure, step design — referenced lightly; skill treats Gherkin as optional.

---

## Continuous delivery and acceptance testing

- **Farley, David.** Blog and talks on acceptance testing in continuous delivery (e.g. [Strategies for effective Acceptance Testing](https://www.davefarley.net/?p=186)).  
  Executable definition of done, automation over manual regression, trustworthy suites in deployment pipelines.

- **Humble, Jez; Farley, David.** *Continuous Delivery.* Addison-Wesley.  
  Pipeline stages, test pyramid, fast feedback vs comprehensive checks.

---

## Standards and tooling

- **Cucumber / Gherkin.** [Gherkin reference](https://cucumber.io/docs/gherkin/reference) — grammar for plain-text scenarios.  
  Skill does not mandate Cucumber; documents pragmatic use.

- **Contract testing.** Pact and similar consumer-driven contract approaches — pragmatic acceptance at service boundaries.

---

## How this maps to the skill (maintenance hint)

| Skill emphasis | Supported by |
|----------------|--------------|
| Discuss → Distill → Develop | ATDD / SBE practice; Adzic; team “three amigos” facilitation |
| Example catalog (repo markdown) | SBE single source of truth; AMPD repo convention (parallel to TDD test list) |
| Pragmatic layering (contract, API, E2E) | Farley; CD pyramid; Humble & Farley |
| Gherkin optional | Cucumber ecosystem; code-first acceptance common in industry |
| Compose with inner TDD | Beck double-loop; `skills/tdd` boundary |
| Flake control and trust | Farley on effective acceptance testing; CD pipeline discipline; Fowler *Mocks Aren't Stubs* + `test-strategy-selection` §3a for external/vendor services |
| Anti-patterns (UI scripts, duplication) | BDD literature; Adzic on example quality |

When evolving `skills/atdd/SKILL.md`, update this bibliography if new canonical sources are adopted.
