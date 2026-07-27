# Micro-iterations and scope

Work from a **test list** per feature (see [test-list.md](test-list.md)); each micro-cycle still moves **one** list item toward a single failing test.

Pick the **smallest test that still asserts behavior at a stable seam** — unit or narrow integration — without over-mocking (see [behavior-and-tests.md](behavior-and-tests.md)).

TDD works best when each failing test is **easy to reason about** and **fast to run**. Aim for cycles short enough that **write test → see fail → minimal code → see pass** stays a tight habit (often seconds to a few minutes, depending on stack).

---

## Step size

Prefer the **smallest** step that still teaches something: if GREEN starts taking a long time or needs a large edit, the step was probably too big — **shrink** the next test, or take a break and resume with a smaller RED.

---

## Size of one increment

A good increment usually:

- adds **one** observable behavior or rule
- can be expressed in **one short** test name
- fails for **one** clear missing piece of implementation

If the test needs a long setup:

- treat it as a **design signal** (see [behavior-and-tests.md](behavior-and-tests.md))
- extract helpers already used in the test suite
- shrink the example first; generalize after green

---

## From RED to GREEN — implementation strategies

Pick the **path of least resistance** for the current failing test:

1. **Fake it**: return a constant or minimal hard-coded value so the test passes and plumbing is trusted; generalize in a later RED (triangulation).
2. **Obvious implementation**: when the correct code is trivial, write it directly.
3. **Triangulation**: when one example is insufficient, add a **second** failing test with different data to force a correct generalization.

---

## Rule of three (duplication before extraction)

Do not extract shared abstractions on the **first** echo of duplication. Let duplication appear until the pattern is **clear** (a common rule of thumb: consider extraction around the **third** similar case). Wrong abstractions hurt more than temporary duplication.

---

## Order of examples

Prefer progression:

1. simplest happy path (often a **starter** case to get the loop moving)
2. obvious edge cases
3. error paths and boundaries
4. collaboration with dependencies (using existing test doubles patterns)

Each step is its own R-G-R cycle with the three micro-commits (then squash before push per skill).

---

## When to split vs. combine

Split into another cycle when:

- the test name needs “and” to describe assertions
- you imagine multiple independent `if` branches in production

Avoid combining unrelated assertions in one test; it slows feedback and blurs failure messages.

---

## Fast feedback commands

Use the narrowest command the repo supports, for example:

- single test id / line number
- single file pattern
- package-scoped test run

Widen only after green on the narrow scope, or when integration risk is explicit. **During an increment**, prefer the narrowest command after every RGR step; run the **broader / full suite** at **increment end** (slice boundary), not after each micro-edit. Integrate frequently in the sense of **running broader suites at boundaries** as the code touches shared surfaces — without abandoning narrow runs after each micro-step.
