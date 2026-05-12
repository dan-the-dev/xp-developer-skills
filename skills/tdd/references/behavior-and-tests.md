# Behavior-first tests (decoupled from implementation)

Tests drive **design and analysis** by pinning **observable behavior**: inputs, outputs, and contracts that matter to callers — not internal layout.

---

## What to assert

- **Public outcomes**: return values, state visible through the module’s API, emitted events, messages sent **only** when the behavior under test is “commands / side effects” and the project already uses interaction-style assertions.
- **Error behavior**: thrown/returned errors, validation messages — as stable surface, not stack traces unless that is the contract.

Avoid:

- asserting on **private** methods, internal fields, or file layout unless that **is** the product contract
- coupling to **algorithm steps** (e.g. “must call helper X”) unless interaction is the specified behavior
- mirroring production code structure in assertion structure (same order of branches, same private names)

If a refactor **breaks** a test without changing user-visible behavior, the test was coupled to implementation — **fix the test**, not the behavior.

---

## Hard-to-write tests as a design signal

- **Long setup** often means responsibilities are tangled or modules too large — split collaborators or narrow the entry point under test before piling fixtures.
- **Brittle tests** that fail when unrelated code changes indicate **leaky abstractions** or over-specified mocks — tighten the public seam under test or reduce mock surface.

---

## Starting the loop

When stuck at the beginning of an increment, add the **smallest** behavior slice (e.g. simplest input / empty case) to get a fast failing test and working plumbing — then grow with further RED steps.

---

## Shaping the API from the test

Write the test as if the **ideal** API already existed: clear names, minimal parameters, obvious result. Then implement until the test passes. The production API **emerges** from what tests need, not the other way around.

---

## Test doubles (when the stack uses them)

Use doubles only to **isolate behavior** or replace slow/non-deterministic collaborators, following project conventions:

- Prefer **real** collaborators when cheap and deterministic.
- **Stub** predictable responses for queries; use **fakes** with minimal in-memory behavior when the project already uses them.
- **Mocks / spies** only for specified command-style interactions — avoid over-specifying call sequences unrelated to the behavior under test.
- Do not mock **third-party** types directly unless the codebase already wraps them; prefer a thin owned seam.

Doubles should stay **dumb and obvious**; complex logic inside a double is a smell.
