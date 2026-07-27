# Bibliography — `skills/tdd` skill

This note ties the repository’s **TDD** agent skill to published sources. The skill text under `skills/tdd/` avoids **book titles** in the body; it may name **public formulations** when they are part of the workflow (e.g. the Three Laws, commonly attributed to Robert C. Martin). Humans maintaining the skill use this page for traceability and deeper reading.

---

## Primary references

- **Beck, Kent.** *Test-Driven Development: By Example.* Addison-Wesley, 2003.  
  Canonical treatment of the RED–GREEN–REFACTOR rhythm, very small steps, “fake it till you make it,” triangulation, shaping APIs from tests, and test smells as design feedback.

- **Santos, Pedro M.; Consolaro, Marco; Di Gioia, Alessandro.** *Agile Technical Practices Distilled: A Learning Journey in Technical Agility and Lean Software Development.* Packt Publishing, 2019.  
  Covers TDD as analysis and design, nested feedback loops with acceptance-level tests, strategies in the GREEN phase, continuous refactoring, and collaboration with broader agile technical practice.

- **Fowler, Martin.** [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html) (2007).  
  Distinguishes **state** vs **behavior** verification; classical vs mockist TDD; Meszaros’s **test double** vocabulary (dummy, fake, stub, spy, mock). AMPD prefers classical style: real collaborators when practical (including vendor sandbox), else fake/stub with state verification — not mocks of third-party SDK types.

---

## Related material (concepts echoed in skill design)

- **Martin, Robert C.** *Clean Code: A Handbook of Agile Software Craftsmanship.* Prentice Hall, 2008.  
  Often cited in discussions of ultra-short feedback loops and disciplined refactoring alongside tests.

- **Fowler, Martin.** [Beck Design Rules](https://martinfowler.com/bliki/BeckDesignRules.html); [Yagni](https://martinfowler.com/bliki/Yagni.html).  
  Simple Design as the REFACTOR compass; YAGNI forbids speculative features, not malleability.

- **Bay, Jeff.** Object Calisthenics — mandatory OO discipline during REFACTOR in AMPD ([`object-calisthenics.md`](object-calisthenics.md)).

- **Kerievsky, Joshua.** *Refactoring to Patterns* — patterns emerge after green, when smells persist.

- **Martin, Robert C.** — **The Three Laws of TDD** (widely reproduced essays and talks).  
  The skill encodes these laws literally: no production without a failing test; minimal test to fail; minimal production to pass the current failing test.

- **Test-Driven Development (community / conference material, e.g. 2021).**  
  Useful for framing real-world friction (legacy code, team dynamics, tooling) versus kata-style practice; this skill defers acceptance workflows to **`skills/atdd`** and **untested-area** work to **`skills/legacy-testing`** (Feathers).

---

## How this maps to the skill (maintenance hint)

| Skill emphasis | Supported by |
|----------------|--------------|
| Short R–G–R cycles, smallest steps | Beck; distilled agile TDD chapters |
| GREEN strategies (fake / obvious / triangulation) | Beck; distilled “implementation strategies” |
| Refactor only on green, micro-steps, revert on red | Beck; *Clean Code* refactoring discipline |
| Simple Design + mandatory calisthenics; patterns only toward smells | Beck Design Rules; Bay; Kerievsky; [`docs/simple-design.md`](simple-design.md) / [`docs/design-quality.md`](design-quality.md) |
| Tests specify **behavior**, not structure | Beck (tests drive design); distilled outside-in framing |
| Test doubles only to isolate behavior | Common testing practice summarized in distilled / Beck contexts; **Fowler** *Mocks Aren't Stubs* (classical preference; fake/stub vs mock) |
| Owned vendor client: sandbox then manual fake/stub; prefer SDK | AMPD policy in `docs/test-strategy-selection.md` §3a; classical “real when practical” from Fowler |
| Rule of three before extracting duplication | Distilled continuous-refactoring guidance |
| Double-loop (outer acceptance, inner unit) | Distilled; skill keeps **inner** loop only and composes with **`skills/atdd`** |
| Code **without** tests at change seam | **Feathers**; compose with **`skills/legacy-testing`** before relying on RED–GREEN alone |
| **Test list** as backlog of cases | Beck’s task/test list habit in *TDD by Example*; planning chapters in *Agile Technical Practices Distilled*; repo file convention is AMPD skill policy |
| **Determinism / stable seams** | Common TDD teaching; aligns with fast feedback and trustworthy RED |
| **AAA / readable tests** | Widely taught practice (e.g. industry checklists); supports Law 2 clarity |
| **Three Laws** rhythm | Robert C. Martin’s formulation; summarized alongside Beck-style R–G–R in many TDD courses and articles |

When evolving `skills/tdd/SKILL.md`, prefer updating this bibliography if new canonical sources are adopted.
