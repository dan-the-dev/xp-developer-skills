---
name: refactoring
description: Martin Fowler–style refactoring — change the internal structure of code without changing observable behavior. Baby steps on a green baseline: one mechanical transformation at a time, tests stay green, revert on red. Also supports post-increment review (explain commits, suggest small in-scope refactors/tests). Separates refactoring from adding features (“two hats”). Use when tidying design, paying down local complexity, preparing code for a change without altering behavior, or reviewing a just-finished increment.
allowed-tools: Read, Edit, MultiEdit, Bash, Grep, Glob
---

# Fowler-style refactoring (behavior-preserving)

## Mission

**Refactoring** (noun): a *behavior-preserving* change that makes code easier to understand or cheaper to change.

**Refactoring** (verb): applying such changes in **small, reversible steps** so that — like tidying LEGO **without turning the spaceship into a car** — the program does the same thing before and after; only structure, names, and arrangement improve.

Think: **clean your room while the toys still work** — one small tidy-up at a time, check that nothing broke after each step, and **do not sneak in new toys** (no new features during the same edits).

Optimize for:

- **Safety** — start from a **green** test baseline; end each step **green**
- **Small steps** — one mechanical change per step; if tests go **red**, **undo** that step and try smaller
- **No behavior change** — same inputs and outputs, same observable side effects
- **Clarity** — better names, clearer boundaries, less accidental duplication
- **Simple Design** — Beck’s four rules + **mandatory Object Calisthenics**; GoF patterns only as destinations when smells persist ([`docs/simple-design.md`](../../docs/simple-design.md), [`docs/design-quality.md`](../../docs/design-quality.md))
- **Reviewability** — commits readers can trust as “structure only”

This skill is for **dedicated** refactoring sessions, for the **REFACTOR** phase inside TDD, and for **post-increment review** after `new-increment`. It does **not** replace **bugfix** (fix wrong behavior), **feature** work (new behavior), or **`skills/legacy-testing`** (harness and characterization when code lacks tests) — compose with those skills ([references/two-hats-and-scope.md](references/two-hats-and-scope.md)).

---

## Modes

| Mode | When | Outcome |
|------|------|---------|
| **Dedicated refactor** (default) | User asks to tidy / prepare design on a green baseline | Goal-driven mechanical steps + `refactor:` commits |
| **Post-increment review** | `new-feature` (or user) after a committed increment | Explain commits; suggest small in-scope improvements; optionally apply tiny mechanical steps only in **full** depth |

Post-increment review: follow [references/post-increment-review.md](references/post-increment-review.md) and [checklists/post-increment-review.md](checklists/post-increment-review.md). Depth is **full** (step / opt-in applies) or **light** (automatic default — no applies). Do **not** rewrite the slice, work outside the increment change surface, or re-run a stylistic REFACTOR when the surface is already clean.

---

## Golden rules (integrated)

| Rule | Practice |
|------|----------|
| **One small tidy-up at a time** | Single rename, one extract, one move — then run tests ([references/baby-steps-and-revert.md](references/baby-steps-and-revert.md)) |
| **Green light** | Start green; after *every* step, green again; red → **revert** last step ([references/testing-and-safety-net.md](references/testing-and-safety-net.md)) |
| **No new toys** | No new behavior, APIs, or “while we’re here” features ([references/two-hats-and-scope.md](references/two-hats-and-scope.md)) |
| **Rule of three** | Wait for real repetition before abstracting; don’t DRY noise ([references/duplication-abstraction-and-naming.md](references/duplication-abstraction-and-naming.md)) |
| **Simple Design** | Beck 4 rules + **mandatory** Object Calisthenics; patterns toward evidenced smells only ([`docs/simple-design.md`](../../docs/simple-design.md), [`docs/design-quality.md`](../../docs/design-quality.md)) |
| **Good names** | Rename so code tells a story; same discipline in tests ([references/duplication-abstraction-and-naming.md](references/duplication-abstraction-and-naming.md)) |
| **Leave it better** | Boy Scout rule: small local improvement when you touch code; scope larger refactors explicitly |

---

## Two hats (Fowler)

At any moment you wear **one** hat:

- **Add feature** — extend behavior (tests may go red → green).
- **Refactor** — **no** new behavior; tests must stay green throughout.

Do **not** swap hats mid-commit. If you need both, **finish** one slice (including tests and commit) before the other.

---

## Relationship to other skills

| Skill | Role |
|-------|------|
| **`skills/tdd`** | Inner loop; REFACTOR step is this same discipline at tight proximity ([`refactor-discipline.md`](../tdd/references/refactor-discipline.md)) |
| **`skills/bugfix`** | Fix **wrong** behavior first; refactoring is not a substitute for reproduction + RED |
| **`skills/atdd`** | Acceptance defines *what*; refactoring does not change *what* |
| **`skills/legacy-testing`** | Without tests, **characterization** and **seams** before large refactors ([`SKILL.md`](../legacy-testing/SKILL.md)) |
| **`skills/new-feature`** | After each increment, invoke this skill in **post-increment review** mode |
| **`skills/new-increment`** | Delivers the committed slice that review inspects — does not run the review itself |

**Tests and design (Cupac):** Prefer tests **coupled to behavior**, not **structure**, so internal moves do not break the suite for the wrong reason ([references/tests-and-design.md](references/tests-and-design.md)).

---

## Workflow (language-agnostic)

Shared delivery rules: [`docs/delivery-process.md`](../../docs/delivery-process.md) (§7 two hats, §9 step size, §2 verification) and [`docs/project-verification.md`](../../docs/project-verification.md) (re-verify after every mechanical step; lint and SonarQube before done).

**If post-increment review:** follow [references/post-increment-review.md](references/post-increment-review.md) instead of the dedicated loop below (same green/baby-step rules when applying).

1. **Goal** — one sentence: *what* will be easier after this (e.g. “extract pricing so policies are isolated”).
2. **Baseline** — checkout branch; **all relevant automated checks green** for this scope (fix unrelated reds first or narrow scope).
3. **Plan** — name 1–3 **Fowler-style** refactorings you will compose ([references/catalog-and-composing-refactorings.md](references/catalog-and-composing-refactorings.md)); if aiming at a GoF destination, say so explicitly and why ([`docs/design-quality.md`](../../docs/design-quality.md)).
4. **Loop** until goal met:
   - pick the **smallest** next mechanical step
   - apply **Object Calisthenics** on touched OO as you go ([`docs/object-calisthenics.md`](../../docs/object-calisthenics.md))
   - apply it
   - run **narrowest** meaningful tests → then widen for shared code
   - if scoped lint exists for touched files, run it after structural edits
   - if **red**: **revert** step; shrink; retry ([references/baby-steps-and-revert.md](references/baby-steps-and-revert.md))
5. **Commit** — `refactor: …` (or team convention); message describes **structure**, not new capability.
6. **Integrate** — small, green changes merge often when using CD / trunk-based flow ([references/continuous-delivery-discipline.md](references/continuous-delivery-discipline.md)).
7. **Design note** — include Simple Design / calisthenics / patterns in the return payload ([`docs/delivery-process.md`](../../docs/delivery-process.md) §10).

Never “fix” production under failing tests during a refactor pass unless you are **switching hats** to a bugfix/feature workflow.

---

## When the safety net is thin

- **Prefer** adding or tightening tests **before** large refactors (same hat as “add tests” if tests assert behavior).
- **Prefer** a **scope limit**: refactor only in modules already well covered.
- **Defer** sweeping changes without tests to a **protected** session — use `skills/legacy-testing` (Feathers: seams, characterization) before large refactors.

---

## Anti-patterns (summary)

- Giant “cleanup” PRs mixing features and moves
- Refactoring on a **red** build
- Stacking many transforms before running tests
- Weakening assertions to go green
- “Refactor” that changes user-visible behavior or API contracts
- Premature abstraction at the first duplication

Full list: [references/anti-patterns.md](references/anti-patterns.md).

---

## Definition of done (session)

- Stated goal achieved or **explicitly** reduced with follow-up note
- **All applicable project verify steps** for this scope run and passed ([`docs/delivery-process.md`](../../docs/delivery-process.md) §2; [`docs/project-verification.md`](../../docs/project-verification.md)) — including lint, format, typecheck, SonarQube/static analysis when configured
- **All** exercised automated checks green after final mechanical step
- Change-surface complete if moved/renamed APIs (§3)
- Commits are **refactor-only** (or documented hat-switch)
- No accidental behavior drift (same scenarios / contracts as baseline)
- Return payload includes verification table (§10)

Checklists: [checklists/before-refactor.md](checklists/before-refactor.md), [checklists/one-mechanical-step.md](checklists/one-mechanical-step.md), [checklists/session-done.md](checklists/session-done.md).

---

## Output format

```markdown
## Refactoring: <short goal>

### Baseline
- Branch: <name>
- Tests run: `<command>` — green before start

### Plan
- Fowler-style steps (high level): <bullets>

### Mechanical steps (chronological)
1. Step: <e.g. Rename Method> — files: <paths>
   - Tests: `<command>` — green
2. …

### If red occurred
- Reverted: <what>
- Retry: smaller step <describe>

### Commits
- `refactor: …`

### Outcome
- Easier to <reason>
- Follow-ups: <file or backlog ref or none>
```

---

## Additional resources

### References

- [references/definition-and-principles.md](references/definition-and-principles.md)
- [references/two-hats-and-scope.md](references/two-hats-and-scope.md)
- [references/baby-steps-and-revert.md](references/baby-steps-and-revert.md)
- [references/testing-and-safety-net.md](references/testing-and-safety-net.md)
- [references/catalog-and-composing-refactorings.md](references/catalog-and-composing-refactorings.md)
- [references/duplication-abstraction-and-naming.md](references/duplication-abstraction-and-naming.md)
- [references/tests-and-design.md](references/tests-and-design.md)
- [references/continuous-delivery-discipline.md](references/continuous-delivery-discipline.md)
- [references/post-increment-review.md](references/post-increment-review.md)
- [references/anti-patterns.md](references/anti-patterns.md)
- [`docs/simple-design.md`](../../docs/simple-design.md)
- [`docs/object-calisthenics.md`](../../docs/object-calisthenics.md)
- [`docs/design-patterns.md`](../../docs/design-patterns.md)
- [`docs/design-quality.md`](../../docs/design-quality.md)

### Examples

- [examples/narrative-extract-method.md](examples/narrative-extract-method.md)

### Checklists

- [checklists/before-refactor.md](checklists/before-refactor.md)
- [checklists/one-mechanical-step.md](checklists/one-mechanical-step.md)
- [checklists/session-done.md](checklists/session-done.md)
- [checklists/post-increment-review.md](checklists/post-increment-review.md)

### External maintenance

- [docs/refactoring-skill-bibliography.md](../../docs/refactoring-skill-bibliography.md)

## Resource usage

Open references when hat boundaries, step size, test scope, or “is this still refactoring?” is unclear.
