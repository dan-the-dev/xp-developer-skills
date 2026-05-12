---
name: tdd
description: Applies strict Test-Driven Development with a maintained upfront test list per feature, Robert C. Martin’s Three Laws, micro-iterations, refactor proximity to the changed code, fast feedback, and git micro-commits (test:/feat:/refactor:) squashed per cycle before push. Use for test-first feature slices, strict R-G-R, or when the user asks for a test list plus disciplined commits.
allowed-tools: Read, Edit, MultiEdit, Bash, Grep, Glob
---

# Strict TDD (micro-iterations)

## Mission

Turn requirements into **concrete automated examples** before production code exists: each example is a **small** failing test, then the smallest code that passes, then structure improvements **without** changing behavior.

**First step of every feature:** create and maintain a **test list** (all cases you can think of for that slice, updated as you learn). **Last step:** every list item is **done** and the suite is green — then the feature work for that slice is finished.

Implement using **short** RED → GREEN → REFACTOR cycles. Each cycle targets the **smallest** increment that still moves the design forward.

Optimize for:

- a visible **test list** as the backbone of progress
- **strict** adherence to the **Three Laws of TDD**
- one failing test at a time
- fastest possible feedback (narrowest test run)
- reversible steps
- commits that tell the story of the cycle
- tests that describe **behavior**, not internals
- **refactors scoped** to code near the current change

This skill covers **only** the **inner** unit-level TDD loop. It does **not** specify acceptance-test (outer-loop) workflows, legacy rescue, branching policy, CI, or bugfix-only rules — compose with other skills for those.

---

## Test list (mandatory)

Before the **first** RED for a feature slice:

1. Write a **test list**: every test case / scenario you can already name (happy paths, edges, errors, invariants).
2. During development: **mark items done** when a real automated test exists and passes for that case (after its R–G–R, per your commit rules); **add** new lines when ideas appear.
3. The slice is **complete** when the list has **no remaining open items** (all done) and tests are green.

The list is the **authoritative backlog** of examples for that slice. Do not treat “no list” as done.

Details: [references/test-list.md](references/test-list.md).

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

If refactoring breaks a test without changing behavior, the test was **implementation-coupled**; fix the test’s assertions or setup, not the production semantics.

See [references/behavior-and-tests.md](references/behavior-and-tests.md).

---

## Micro-iteration rules

- One new behavior or one new edge case per failing test, **chosen from the test list** (or added to the list first if newly discovered).
- Prefer writing the test against the **API you wish existed**; then implement to match.
- If a test is hard to write, **shrink** the example or treat it as a coupling smell (see behavior reference).
- After RED, run tests and confirm failure for the **intended** reason (or the narrowest signal the runner gives).
- After GREEN, run the same scope and confirm **pass**.
- From RED to GREEN, use **fake it**, **obvious implementation**, or **triangulation** as appropriate (see [references/micro-iterations.md](references/micro-iterations.md)).

---

## REFACTOR — tests never break, scope stays close

During REFACTOR:

- apply **one small** mechanical change at a time (rename, extract, move, delete duplication)
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
| RED       | tests only   | `test: …`     | Failing test proving missing behavior. |
| GREEN     | production   | `feat: …`     | Smallest change to satisfy the test. |
| REFACTOR  | any refactor | `refactor: …` | Structure/readability; **same behavior**; tests **remain green** throughout. |

Rules:

- RED commit: **only** test files (and test-only fixtures if the repo already separates them).
- GREEN commit: **only** production code required to pass.
- REFACTOR commit: **no** behavior change; if types/docs must adjust, follow team conventions for commit type or split commits.

If a cycle truly requires **no** refactor (rare but valid), you may omit the REFACTOR commit and still complete the squash step for RED+GREEN only.

---

## Squash before push (end of cycle)

When a **full** RED → GREEN → REFACTOR cycle is complete for the current increment:

1. Squash the micro-commits from that cycle into **one** commit (see [references/squash-and-push.md](references/squash-and-push.md)).
2. **Single push** after squash: the remote branch should show **one** commit per completed cycle (or follow the user’s branch strategy if they override).

Squashed commit message:

- **Title**: align with the **GREEN** `feat:` subject (same intent, may polish wording).
- **Body**: optional bullets summarizing tests added and notable refactor notes; keep the feature description primary.

This preserves local narrative during development and **reviewer-friendly** history upstream.

---

## Fast feedback discipline

- Prefer single-test or single-file runs immediately after RED, GREEN, and **each** refactor micro-step.
- Widen scope when touching shared modules or contracts; run a broader slice regularly as integration insurance.
- Never start the next RED while previous tests are failing.

---

## Anti-patterns (TDD-specific)

- Skipping the **test list** or starting RED before the list exists (except a trivial two-line list).
- Marking list items **done** without an automated test that passes.
- Violating any of the **Three Laws** (speculative production code, oversized tests, extra production beyond current RED).
- Writing production code before a failing test exists.
- A “RED” commit where tests pass (or wrong failure reason).
- Over-sized steps (multiple behaviors in one test).
- Mixing RED+GREEN or GREEN+REFACTOR in one commit during the cycle.
- Refactoring while tests are red, or **continuing** after a refactor step broke tests without reverting.
- **Wide refactors** unrelated to the code path for the current list item.
- Assertions on **implementation** (private internals, call order) instead of **behavior**.
- Pushing micro-commits without the requested squash for this skill.

---

## Definition of done

### One R–G–R cycle

- Failing test observed (**RED** verified).
- Minimal implementation passes (**GREEN** verified).
- Refactor completed with **tests green after every micro-step** (**REFACTOR** verified), **within proximity** of the change.
- Three semantic micro-commits present (`test:`, `feat:`, `refactor:`) unless refactor legitimately skipped.
- Squash performed; **one** commit represents the cycle on push.

### Feature slice (test list)

- Test list existed **before** first RED and was **updated** throughout.
- **Every** list item is **done** (implemented with passing tests) or explicitly removed by agreement.
- Suite green; no undeclared extra behavior.

---

## Output format

```markdown
## Feature: <name>

### Test list
- [ ] / [x] <case lines; keep in sync>

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
2. feat: …
3. refactor: …

### Squash
- Final commit title: feat: …
- Push: <branch>, single commit after squash

### Slice status
- Test list: <all done | N open>
```

---

## Additional resources

### References

- [references/test-list.md](references/test-list.md)
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

Open reference files when execution details (test list, laws, squash mechanics, refactor scope) are unclear or contentious.
