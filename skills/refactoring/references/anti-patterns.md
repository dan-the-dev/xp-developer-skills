# Refactoring anti-patterns

## Process

- **Big bang cleanup** — many renames and moves before any test run.
- **Red refactor** — continuing “refactor” while tests fail (without hat switch).
- **Fix forward** — loosening assertions or tweaking outputs to force green during a refactor pass.
- **Mixed hats** — new feature disguised as “just cleanup.”

---

## Design

- **Premature abstraction** — extracting after the first duplicate without a third use.
- **Golden hammer** — forcing one pattern (e.g. every `if` → strategy) without local benefit.
- **Refactor to “clever”** — shorter code that is harder to read.

---

## Testing

- **Structure-coupled tests** — tests that break on every safe move.
- **No tests** — large refactor with hope and manual clicks only.
- **Ignoring flake** — refactoring on an unstable baseline.

---

## Organizational

- **Endless refactor ticket** — no goal, no done; use a **clear outcome** (e.g. “extract pricing module”, “rename confusing domain terms in orders bounded context”).
- **Silent behavior drift** — API changes or bugfixes snuck into refactor PR without review focus.
- **Post-increment rewrite** — using “review” to redesign the slice or pull in the next backlog line.
- **Drive-by cleanup** — applying refactors outside the increment change surface during post-increment review.
- **Second stylistic REFACTOR** — applying taste-only tidy when the increment’s TDD REFACTOR already left a clean surface.
- **Applies in light depth** — modifying code during automatic light review.
- **Hiding blocking gaps** — continuing signal when tests/strategy holes belong to this increment.

---

## Messaging

Calling something **refactor** when observables changed — misleads reviewers and future maintainers. **Rename the work** (feature / fix) and follow the right skill.
