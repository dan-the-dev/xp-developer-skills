---
name: legacy-testing
description: Michael Feathers–style legacy code change — treat code without automated tests as legacy, then follow identify change points, find test points, break dependencies, add tests (often characterization), and only then modify or refactor. Covers seams (object/link/preprocessing), sensing vs separation, fakes/mocks, sprout/wrap, pinch points, effect sketches, and dependency-breaking patterns. Composes with bugfix, TDD, and refactoring once a harness exists. Roadmap id: add-tests-to-legacy-code. Use when changing untested code, introducing a test seam, or adding coverage before a risky edit.
allowed-tools: Read, Edit, MultiEdit, Bash, Grep, Glob
---

# Legacy code testing (Feathers-style)

## Mission

**Legacy code** (Feathers): code **without automated tests** covering the behavior you need to change. Not “old” — **unprotected**. Without tests you cannot know whether a change **helps or harms** the system.

**Goal:** build a **test harness** and **pin down behavior** so later edits use normal **bugfix**, **TDD**, or **refactoring** skills safely.

Think: **strap on sensors before opening the engine** — you are not proving virtue first; you are **documenting what happens today** so the next move is reversible and observable.

Optimize for:

- **Safety** — never “big bang” into untested internals
- **Seams** — places behavior can vary without editing the legacy core at that line ([references/seams-sensing-separation.md](references/seams-sensing-separation.md))
- **Characterization** — tests that lock **current** behavior before intentional change ([references/characterization-tests.md](references/characterization-tests.md))
- **Small steps** — one dependency break or one test at a time; **green** after each meaningful commit ([references/feathers-change-algorithm.md](references/feathers-change-algorithm.md))
- **Composition** — once the net exists, switch to `skills/tdd`, `skills/refactoring`, `skills/bugfix` as appropriate

This skill does **not** replace **ATDD** for new capability definition; it often **precedes** confident refactoring.

---

## Feathers’ change algorithm (five phases)

Work in order; do not skip “find test points” and “break dependencies” by writing giant integration tests that never fail for the right reason.

1. **Identify change points** — where must the code differ after your goal?
2. **Find test points** — where can you observe or assert behavior cheaply?
3. **Break dependencies** — make the code **callable / observable** in a test harness (seams, fakes, parameterization).
4. **Write tests** — usually **characterization** first; add bug-targeted tests if you already know wrong behavior.
5. **Modify and refactor** — implement; then **refactor** with `skills/refactoring` now that behavior is pinned.

Detail: [references/feathers-change-algorithm.md](references/feathers-change-algorithm.md).

---

## Quick techniques (when time is short)

| Technique | Use when |
|-----------|-----------|
| **Sprout Method / Class** | New logic can live in a new unit; legacy calls into it (minimal surface change). |
| **Wrap Method / Class** | Add behavior **before/after** existing code (often decorator-like); existing core stays untouched at first. |

See [references/sprout-and-wrap.md](references/sprout-and-wrap.md).

---

## Core concepts (recap)

- **Seams** — preprocessing, link, **object** seams — places to substitute behavior for tests ([references/seams-sensing-separation.md](references/seams-sensing-separation.md)).
- **Sensing & separation** — break dependencies to **read** outcomes you couldn’t see, or to **isolate** execution ([references/seams-sensing-separation.md](references/seams-sensing-separation.md)).
- **Characterization tests** — “today’s truth” as executable documentation ([references/characterization-tests.md](references/characterization-tests.md)).
- **Pinch points** — narrow places where a few tests cover many paths ([references/pinch-points-and-effect-sketches.md](references/pinch-points-and-effect-sketches.md)).
- **Effect sketches** — lightweight maps of how a change **ripples** ([references/pinch-points-and-effect-sketches.md](references/pinch-points-and-effect-sketches.md)).
- **Dependency-breaking catalog** — extract interface, subclass & override, parameterize constructor, etc. ([references/dependency-breaking-techniques.md](references/dependency-breaking-techniques.md)).
- **Monsters & libraries** — huge classes/methods, third-party lock-in; wrappers and incremental carving ([references/monsters-and-libraries.md](references/monsters-and-libraries.md)).

---

## Integration with other discipline (Fowler, Beck, Farley, Cupac)

- **Kent Beck** — same **tiny verified steps** and **revert** instinct as TDD; legacy work just **pays the debt** to get to RED/GREEN/REFACTOR at useful seams.
- **Martin Fowler** — legacy session often **ends** in **refactoring**; until tests exist, many edits are **seam-finding** and **characterization**, not full catalog refactorings.
- **Dave Farley** — prefer **small**, **mergable** steps that keep CI honest; legacy work is **not** an excuse to turn off the pipeline for weeks — chunk into harness slices.
- **Valentina Cupać** — tests you add should target **behavior** you care about preserving, not **implementation detail**, or refactors will remain painful ([`skills/refactoring/references/tests-and-design.md`](../refactoring/references/tests-and-design.md)).

More: [references/aligned-practices.md](references/aligned-practices.md).

---

## Language-agnostic execution

Inspect the repo for:

- test runner, module layout, DI patterns, build/link seams
- existing “golden” or snapshot tests (possibly abuse-prone — use thoughtfully)

Prefer **narrowest** tests that still **encode the legacy contract** you are about to touch.

---

## When this skill is the wrong tool

- Greenfield feature with strong suite → use **`skills/tdd`** / **`skills/atdd`**
- Known bug with reproducible failure and **existing** coverage at seam → **`skills/bugfix`**
- Pure structure change with **good** tests → **`skills/refactoring`** only

---

## Anti-patterns (summary)

- Changing production first, “we’ll backfill tests”
- Characterization tests that assert **incidental** output (stack traces, timestamps) → brittle noise
- **Monster end-to-end** only, no unit-level pinch points
- Mocks that encode **desired** design instead of **current** behavior during characterization
- One PR that “adds tests” by rewriting production semantics

Full list: [references/anti-patterns.md](references/anti-patterns.md).

---

## Definition of done (typical slice)

- Change point and test point documented (short note in PR or `legacy-harness/` doc folder if team uses one)
- Dependencies broken **only as much** as needed for the next test
- Characterization (and/or bug) tests **green** on baseline
- Production change (if any) passes tests; refactor commits separate per `skills/refactoring`

Checklists: [checklists/before-change.md](checklists/before-change.md), [checklists/one-intervention.md](checklists/one-intervention.md), [checklists/session-done.md](checklists/session-done.md).

---

## Output format

```markdown
## Legacy harness / change: <goal>

### Baseline
- Legacy area: <module / classes / paths>
- Tests before: none | thin — noted risks

### Feathers sequence
1. Change points: <bullets>
2. Test points: <bullets>
3. Dependencies broken: <techniques + seams>
4. Tests added: <characterization | bug repro | both> — `<paths>`
5. Modify/refactor: <summary; hats clearly separated>

### Commits (suggested)
- test: characterization for …
- refactor: seam only … (optional)
- feat:/fix: … (after green net)

### Follow-up
- Next pinch point / deferred monster split
```

---

## Additional resources

### References

- [references/feathers-change-algorithm.md](references/feathers-change-algorithm.md)
- [references/definition-legacy.md](references/definition-legacy.md)
- [references/seams-sensing-separation.md](references/seams-sensing-separation.md)
- [references/characterization-tests.md](references/characterization-tests.md)
- [references/dependency-breaking-techniques.md](references/dependency-breaking-techniques.md)
- [references/sprout-and-wrap.md](references/sprout-and-wrap.md)
- [references/pinch-points-and-effect-sketches.md](references/pinch-points-and-effect-sketches.md)
- [references/monsters-and-libraries.md](references/monsters-and-libraries.md)
- [references/aligned-practices.md](references/aligned-practices.md)
- [references/anti-patterns.md](references/anti-patterns.md)

### Examples

- [examples/narrative-characterization-then-change.md](examples/narrative-characterization-then-change.md)

### Checklists

- [checklists/before-change.md](checklists/before-change.md)
- [checklists/one-intervention.md](checklists/one-intervention.md)
- [checklists/session-done.md](checklists/session-done.md)

### Bibliography

- [docs/legacy-testing-skill-bibliography.md](../../docs/legacy-testing-skill-bibliography.md)

## Resource usage

Open references when seam choice, characterization scope, or dependency-breaking pattern is contentious.
