---
name: tdd
description: Applies strict Test-Driven Development with a repo-local Markdown test list (default `test-lists/<slug>.md` unless the project defines another folder), Robert C. Martin’s Three Laws, deterministic tests and stable seams (unit vs narrow integration), Arrange–Act–Assert test shape, micro-iterations, refactor proximity (production and test code), fast feedback, and git micro-commits (`test:` / `feat:` or `fix:` / `refactor:`) squashed per cycle before push. Use for test-first feature slices, strict R-G-R, or when the user asks for a tracked test list plus disciplined commits.
allowed-tools: Read, Edit, MultiEdit, Bash, Grep, Glob
---

# Strict TDD (micro-iterations)

## Mission

Shared delivery rules at slice boundaries: [`docs/delivery-process.md`](../../docs/delivery-process.md) (§2 verification, §3 change-surface, §4 test strategy, §6 RED→GREEN), [`docs/project-verification.md`](../../docs/project-verification.md), and [`docs/test-strategy-selection.md`](../../docs/test-strategy-selection.md).

Turn requirements into **concrete automated examples** before production code exists: each example is a **small** failing test, then the smallest code that passes, then structure improvements **without** changing behavior.

**First step of every feature:** create a **Markdown test list file** in the repo (path rules in [references/test-list.md](references/test-list.md)) listing every **behavior** you will prove with tests; keep the file updated. **Last step:** every line in that file is done and the suite is green — then the slice is finished.

Implement using **short** RED → GREEN → REFACTOR cycles. Each cycle targets the **smallest** increment that still moves the design forward.

Optimize for:

- a **tracked Markdown file** for the test list (repo-visible “done” definition)
- **strict** adherence to the **Three Laws of TDD**
- one failing test at a time
- fastest possible feedback (narrowest test run)
- reversible steps
- commits that tell the story of the cycle
- tests that describe **behavior**, not internals
- **deterministic** tests and **stable seams** (see behavior reference)
- **refactors scoped** to code near the current change

This skill covers the **inner** unit-level TDD loop. **Before first RED**, evaluate other practices per [`test-strategy-selection.md`](../../docs/test-strategy-selection.md) (mutation, property-based, narrow integration, **vendor client §3a**). It does **not** specify acceptance-test (outer-loop) workflows, **legacy code without tests**, branching policy, CI, bugfix-only rules, or **time-boxed experiments** — compose with other skills for those (e.g. `skills/atdd`, `skills/spike` on an isolated `spike/` branch before delivery, `skills/refactoring` for stand-alone Fowler-style refactor sessions, `skills/legacy-testing` for Feathers-style harness and characterization).

---

## Test list (mandatory)

The test list lives in a **tracked `.md` file** in the project. It contains **only** behaviors that will become automated tests — **not** deferred refactors (those go to a **follow-ups** file or the closing reply; see [references/test-list.md](references/test-list.md)).

Before the **first** RED for a feature slice:

1. **Choose folder**: use a path the project already defines for this kind of artifact; if none, use `test-lists/` at the repo root.
2. **Create the file** with a name derived from the **branch and/or feature** (kebab-case, coherent slug — details in reference).
3. Write every behavior case you can already name (happy paths, edges, errors, invariants) as `[ ]` checklist lines.
4. During development: flip lines to `[x]` when a real automated test exists and passes for that case; **append** new `[ ]` lines for newly discovered **behavior** only.
5. The slice is **complete** when every behavior line is `[x]` (or explicitly removed by agreement) and tests are green.

Do **not** add refactor-only or “nice cleanup” items to this file — they would prevent a clear “feature done” signal.

See [references/test-list.md](references/test-list.md) for folder resolution, naming, and follow-ups.

---

## The Three Laws of TDD (strict)

These laws (commonly attributed to **Robert C. Martin**) define the rhythm. **Do not skip or reinterpret** them; they override convenience.

### Law 1 — Production code only for green

You may not write **production** code unless it is **to make a failing unit test pass**.

- No speculative types, helpers, or “we will need this” code without a **current** failing test that demands it.
- If there is no failing test, you do not touch production code.

### Law 2 — Minimal test to fail

You may not write **more** of a **unit test** than is **sufficient to fail** (including **not compiling** / not resolving symbols, where that is the next smallest step in your stack).

- Write only enough test to get **one** clear failure signal.
- A compile-time / type error from calling a not-yet-written API **counts** as RED.

### Law 3 — Minimal production to pass

You may not write **more** production code than is **sufficient to pass** the **one** failing unit test.

- Prefer the **simplest** thing that could work — including **fake it** (e.g. constant return) — to go green quickly, then use further RED steps and **triangulation** to generalize.
- Do not add behavior, APIs, or optimizations not required by the **current** failing test.

### Cycle locked by the laws

Repeat in **very short** loops (often seconds to a few minutes):

1. Add a **tiny** amount of test → **RED** (Law 2).
2. Add a **tiny** amount of production code → **GREEN** (Law 3).
3. **Refactor** with tests green, **near the changed code** (proximity rule in [references/refactor-discipline.md](references/refactor-discipline.md)).

Effects you should internalize:

- Faults are usually in the **last few lines** you wrote — little need for long debug sessions when laws are respected.
- Tests become **executable specification** of behavior.
- **Hard-to-write tests** signal coupling or oversized units — improve design (often after green), still under the proximity rule.

---

## Language-agnostic execution

Adapt to the repository:

- detect stack and test runner
- follow existing test layout and naming
- run the **smallest** meaningful test command for the current file or test name

Never assume a specific framework; inspect the project first.

---

## Behavior-first tests

Tests specify **observable outcomes** and stable seams — not private helpers, internal call order, or incidental structure. Assertions should remain valid across **equivalent** implementations.

Structure and readability: **Arrange–Act–Assert**, spec-like names, and **no heavy logic in tests** — see [references/test-quality.md](references/test-quality.md).

**Determinism** (time, randomness, I/O, globals) and **choosing unit vs narrow integration** at a stable seam — see [references/behavior-and-tests.md](references/behavior-and-tests.md).

If refactoring breaks a test without changing behavior, the test was **implementation-coupled**; fix the test’s assertions or setup, not the production semantics.

---

## Micro-iteration rules

- One new behavior or one new edge case per failing test, **chosen from the test list** (or added to the list first if newly discovered).
- Prefer writing the test against the **API you wish existed**; then implement to match.
- If a test is hard to write, **shrink** the example or treat it as a coupling smell (see behavior reference).
- After RED, run tests and confirm failure for the **intended** reason (or the narrowest signal the runner gives) — not a timeout, order flake, or missing fixture (see [references/behavior-and-tests.md](references/behavior-and-tests.md)).
- After GREEN, run the same scope and confirm **pass**.
- After **each** REFACTOR micro-step, re-run the same scope (see REFACTOR section).
- At **slice boundary**, run **all applicable project verify steps** — lint, format, typecheck, SonarQube/static analysis when configured, plus **adopted test-strategy practices** (mutation, property-based, integration) ([`docs/project-verification.md`](../../docs/project-verification.md), [`docs/test-strategy-selection.md`](../../docs/test-strategy-selection.md)).
- From RED to GREEN, use **fake it**, **obvious implementation**, or **triangulation** as appropriate (see [references/micro-iterations.md](references/micro-iterations.md)).

---

## REFACTOR — tests never break, scope stays close

During REFACTOR:

- apply **one small** mechanical change at a time (rename, extract, move, delete duplication) in **production and/or test code** (helpers, builders, duplicated setup) — see [references/refactor-discipline.md](references/refactor-discipline.md)
- **run tests after every change** (same scope first, then wider if shared code moved)
- if **any** test fails: **revert** that change (or reset to last green), then take a **smaller** step
- do not slip in behavior changes “while you are here”
- prefer edits **close** to the code that satisfied the current test; **avoid** drive-by refactors in distant modules (see [references/refactor-discipline.md](references/refactor-discipline.md))

Refactoring is **continuous** across cycles, not deferred cleanup. Remove duplication when it is **real and recurring**; avoid speculative abstraction (rule-of-three guidance in micro-iterations reference).

---

## Mandatory commit flow (micro-commits)

Use **three separate commits** per completed R-G-R cycle, with **these Conventional Commit types**:

| Step      | Stage        | Commit prefix | Purpose |
|-----------|--------------|----------------|---------|
| RED       | tests only   | `test: …`     | Failing test proving missing or wrong behavior. |
| GREEN     | production   | `feat: …` **or** `fix: …` | **feat:** smallest change for **new** behavior. **fix:** smallest change when the failing test encodes a **bug** or **regression** in existing behavior (Law 3 unchanged). |
| REFACTOR  | any refactor | `refactor: …` | Structure/readability; **same behavior**; tests **remain green**; may be **test-only** files if production is already clean. |

Rules:

- RED commit: **only** test files (and test-only fixtures if the repo already separates them).
- GREEN commit: **only** production code required to pass.
- REFACTOR commit: **no** behavior change; may include **only** test files when cleaning helpers or duplication; if types/docs must adjust, follow team conventions for commit type or split commits.

If a cycle truly requires **no** refactor (rare but valid), you may omit the REFACTOR commit and still complete the squash step for RED+GREEN only.

---

## Squash before push (end of cycle)

When a **full** RED → GREEN → REFACTOR cycle is complete for the current increment:

1. Squash the micro-commits from that cycle into **one** commit (see [references/squash-and-push.md](references/squash-and-push.md)).
2. **Single push** after squash: the remote branch should show **one** commit per completed cycle (or follow the user’s branch strategy if they override).

Squashed commit message:

- **Title**: align with the **GREEN** subject — **`feat:`** for new behavior, **`fix:`** when GREEN was a bug/regression fix (same intent, may polish wording).
- **Body**: optional bullets summarizing tests added and notable refactor notes; keep the feature description primary.

This preserves local narrative during development and **reviewer-friendly** history upstream.

---

## Fast feedback discipline

- Prefer single-test or single-file runs immediately after RED, GREEN, and **each** refactor micro-step.
- Widen scope when touching shared modules or contracts; run a broader slice regularly as integration insurance.
- Never start the next RED while previous tests are failing.
- Keep tests **deterministic** at each step (see [references/behavior-and-tests.md](references/behavior-and-tests.md)).

---

## Anti-patterns (TDD-specific)

- Skipping the **on-disk** test list file or starting RED before it exists (except a trivial file with two lines).
- Putting **refactor / tech-debt** items on the test list (use `-follow-ups.md` or the closing reply instead).
- Marking list items **done** without a **passing** automated test **and** a **test reference** on the list line.
- A “RED” commit where tests pass (or failure unrelated to the intended case).
- Violating any of the **Three Laws** (speculative production code, oversized tests, extra production beyond current RED).
- Writing production code before a failing test exists.
- **False RED**: wrong failure reason (flake, timeout, env) mistaken for behavior gap — confirm intended signal.
- **Over-mocked tests** that lock implementation instead of asserting behavior at a stable seam.
- **Heavy logic in tests** (conditionals/loops) obscuring why RED happened.
- Over-sized steps (multiple behaviors in one test).
- Mixing RED+GREEN or GREEN+REFACTOR in one commit during the cycle.
- Refactoring while tests are red, or **continuing** after a refactor step broke tests without reverting.
- **Wide refactors** unrelated to the code path for the current list item.
- Assertions on **implementation** (private internals, call order) instead of **behavior**.
- Pushing micro-commits without the requested squash for this skill.
- **Big-bang test file** — `Write` replacing an entire `*.test.*` with many cases before any RED (add **one** `it` / test at a time).
- **Big-bang green** — production + many tests in one edit without a failing run in between.
- **Circular oracle** — `expected` built only by calling the method under test for the same requirement (proves delegation, not correctness). Use fixtures, tables, or independent oracles.
- **Checklist theater** — flipping test-list or acceptance-catalog lines to `[x]` before the linked automated test exists and has failed at least once.

---

## Definition of done

### One R–G–R cycle

- Failing test observed (**RED** verified).
- Minimal implementation passes (**GREEN** verified).
- Refactor completed with **tests green after every micro-step** (**REFACTOR** verified), **within proximity** of the change.
- Three semantic micro-commits present (`test:`, `feat:` or `fix:`, `refactor:`) unless refactor legitimately skipped.
- Squash performed; **one** commit represents the cycle on push.

### Feature slice (test list)

- Test list **file** exists at `<repo-relative-path>.md` **before** first RED and was updated throughout.
- **Cases**: behavior-only lines; each `[x]` includes a **test reference** and passing tests; each remaining `[ ]` at end of slice is a **blocker** — either implement, move to **Deferred behavior** with closure plan, or move to **Removed** with reason (see [references/test-list.md](references/test-list.md)).
- **Deferred behavior** / **Removed** sections: no silent scope or vague deferred rows at slice end.
- **All applicable project verify steps** for this scope run and passed ([`docs/delivery-process.md`](../../docs/delivery-process.md) §2; [`docs/project-verification.md`](../../docs/project-verification.md)) — tests, lint, format, typecheck, SonarQube/static analysis when configured; not only the test runner.
- Change-surface complete if construction/import/API changed (§3).
- Suite green; no undeclared extra behavior.
- Deferred refactors (e.g. skipped for proximity) recorded in **`<stem>-follow-ups.md`** or listed in the **final user reply**, not in the test list.

---

## Output format

```markdown
## Feature: <name>

### Test list file
- Path: `<e.g. test-lists/order-shipping-threshold.md>`
- Branch / slug used for name: <optional>

### Test list (excerpt; source of truth is the file)
- `[x]` lines must show test back-reference, e.g. `- [x] … — \`src/foo.spec.ts::case name\``

### TDD cycle summary (latest increment)

#### RED
- Test: <file::case>
- Failure: <short message>

#### GREEN
- Change: <one line>
- Tests: <command scope>

#### REFACTOR
- Micro-steps: <list; note test runs after each; stay close to changed code>
- Tests: <command scope>

### Micro-commits (local)
1. test: …
2. feat: … **or** fix: …
3. refactor: …

### Squash
- Final commit title: feat: … **or** fix: … (match GREEN)
- Push: <branch>, single commit after squash

### Slice status
- Test list file: `<path>` — all `[x]` | N open
- Follow-ups (refactor / tech debt): `<path-to-follow-ups.md or "in closing reply">`
```

---

## Additional resources

### References

- [references/test-list.md](references/test-list.md)
- [references/test-quality.md](references/test-quality.md)
- [references/micro-iterations.md](references/micro-iterations.md)
- [references/behavior-and-tests.md](references/behavior-and-tests.md)
- [references/refactor-discipline.md](references/refactor-discipline.md)
- [references/squash-and-push.md](references/squash-and-push.md)
- [references/anti-patterns.md](references/anti-patterns.md)

### Examples

- [examples/narrative-workflow.md](examples/narrative-workflow.md)

### Checklist

- [checklists/rgr-cycle.md](checklists/rgr-cycle.md)

## Resource usage

Open reference files when execution details (test list, test shape, laws, squash mechanics, refactor scope) are unclear or contentious.
