---
name: tdd
description: Applies strict Test-Driven Development with micro-iterations, fast feedback loops, and disciplined git steps (RED test commit, GREEN feat commit, REFACTOR commit), then squashes those micro-commits into one push-ready commit aligned to the feature. Use when implementing behavior with TDD, Kent Beck style cycles, or when the user asks for test-first micro-steps and semantic commits.
allowed-tools: Read, Edit, MultiEdit, Bash, Grep, Glob
---

# Strict TDD (micro-iterations)

## Mission

Turn requirements into **concrete automated examples** before production code exists: each example is a **small** failing test, then the smallest code that passes, then structure improvements **without** changing behavior.

Implement using **short** RED → GREEN → REFACTOR cycles. Each cycle targets the **smallest** increment that still moves the design forward.

Optimize for:

- one failing test at a time
- fastest possible feedback (narrowest test run)
- reversible steps
- commits that tell the story of the cycle
- tests that describe **behavior**, not internals

This skill covers **only** the **inner** unit-level TDD loop. It does **not** specify acceptance-test (outer-loop) workflows, legacy rescue, branching policy, CI, or bugfix-only rules — compose with other skills for those.

---

## Core principles (strict)

- **No production code** without a **failing** automated test (RED) — compilation counts as failing when the stack makes that the first signal.
- **No more test** than needed to **fail** for the right reason.
- **No more production code** than needed to **pass** the current failing test (GREEN).
- **REFACTOR** only with **all relevant tests green**; behavior stays identical; if anything goes red, **undo** the last step and continue in smaller mechanical steps (see [references/refactor-discipline.md](references/refactor-discipline.md)).

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

- One new behavior or one new edge case per failing test.
- Prefer writing the test against the **API you wish existed**; then implement to match.
- If a test is hard to write, **shrink** the example or treat it as a coupling smell (see behavior reference).
- After RED, run tests and confirm failure for the **intended** reason (or the narrowest signal the runner gives).
- After GREEN, run the same scope and confirm **pass**.
- From RED to GREEN, use **fake it**, **obvious implementation**, or **triangulation** as appropriate (see [references/micro-iterations.md](references/micro-iterations.md)).

---

## REFACTOR — tests never break

During REFACTOR:

- apply **one small** mechanical change at a time (rename, extract, move, delete duplication)
- **run tests after every change** (same scope first, then wider if shared code moved)
- if **any** test fails: **revert** that change (or reset to last green), then take a **smaller** step
- do not slip in behavior changes “while you are here”

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

- Writing production code before a failing test exists.
- A “RED” commit where tests pass (or wrong failure reason).
- Over-sized steps (multiple behaviors in one test).
- Mixing RED+GREEN or GREEN+REFACTOR in one commit during the cycle.
- Refactoring while tests are red, or **continuing** after a refactor step broke tests without reverting.
- Assertions on **implementation** (private internals, call order) instead of **behavior**.
- Pushing micro-commits without the requested squash for this skill.

---

## Definition of done (one cycle)

- Failing test observed (**RED** verified).
- Minimal implementation passes (**GREEN** verified).
- Refactor completed with **tests green after every micro-step** (**REFACTOR** verified).
- Three semantic micro-commits present (`test:`, `feat:`, `refactor:`) unless refactor legitimately skipped.
- Squash performed; **one** commit represents the cycle on push.
- Next cycle can begin from the squashed base.

---

## Output format

```markdown
## TDD cycle summary

Feature increment: <one line>

### RED
- Test: <file::case>
- Failure: <short message>

### GREEN
- Change: <one line>
- Tests: <command scope>

### REFACTOR
- Micro-steps: <list; note test runs after each>
- Tests: <command scope>

### Micro-commits (local)
1. test: …
2. feat: …
3. refactor: …

### Squash
- Final commit title: feat: …
- Push: <branch>, single commit after squash
```

---

## Additional resources

### References

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

Open reference files when execution details (squash mechanics, pacing, refactor safety, test shape) are unclear or contentious.
