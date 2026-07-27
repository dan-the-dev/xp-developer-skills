# Behavior-first tests (decoupled from implementation)

Tests drive **design and analysis** by pinning **observable behavior**: inputs, outputs, and contracts that matter to callers — not internal layout.

---

## Determinism and isolation (default RED path)

TDD only works if RED and GREEN are **trustworthy**. Prefer tests that are **fast** and **order-independent** unless the behavior under test is inherently concurrent.

Control or fake:

- **Clocks and time** — inject a clock or freeze time; no real sleeps as assertions.
- **Randomness** — fixed seed or injected generator.
- **Network and external I/O** — no real network/files in the default **domain/unit** loop unless this test **is** an integration test at an owned boundary (see below), or the SUT **is** an owned vendor client under [`test-strategy-selection.md`](../../../docs/test-strategy-selection.md) §3a (sandbox when feasible).
- **Global / process / env state** — reset or isolate per test per project patterns.
- **Parallelism** — avoid shared mutable statics; follow the runner’s isolation rules.

After RED, confirm the failure is the **intended** signal (missing behavior, wrong value), not a **timeout**, ordering flake, or environment drift.

---

## Choosing the seam: unit vs narrow integration

Still **one failing test at a time** and still **Three Laws** — but pick the **smallest test that asserts behavior at a stable seam**:

- **Unit** (fast, in-memory): logic and pure transformations; collaborators are **real** when cheap or **doubles** at **owned** boundaries.
- **Narrow integration**: **one** real module boundary (e.g. repository with in-memory DB, HTTP handler with test client, **vendor adapter against sandbox**) when behavior is **wiring**, serialization, or external mapping — avoid duplicating that in over-mocked units.
- **Owned vendor client**: SUT is your adapter; prefer sandbox live calls, else a **manual fake/stub** at the port you own — see [`test-strategy-selection.md`](../../../docs/test-strategy-selection.md) §3a. Prefer vendor **SDK** in production when available; SDK vs HTTP does not change this seam choice.

**Over-mocking** (many mocks, strict call sequences unrelated to the specified behavior) often **locks implementation** and violates “tests decoupled from internals.” Prefer a **real** collaborator or a **dumb fake** at a **thin seam** you own; reserve mocks for **command-style** interactions the product contract actually specifies. This matches classical TDD and **state verification** over **behavior verification** for awkward collaborators ([Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)).

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

Vocabulary (Meszaros via [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)): **Dummy**, **Fake**, **Stub**, **Spy**, **Mock**. Only **mocks** insist on **behavior verification** (expected calls). Prefer **classical** style: real objects when practical; otherwise **fake** / **stub** with **state verification**.

Use doubles only to **isolate behavior** or replace slow/non-deterministic collaborators, following project conventions:

- Prefer **real** collaborators when cheap and deterministic (including vendor **sandbox** when testing an owned client — §3a).
- **Stub** predictable canned responses for queries; use **fakes** with minimal in-memory behavior when you need working shortcuts.
- **Mocks / spies** only for specified command-style interactions — avoid over-specifying call sequences unrelated to the behavior under test.
- Do not mock **third-party** types directly unless the codebase already wraps them; prefer a thin owned seam. When the collaborator is awkward and sandbox is not feasible, prefer a **hand-written fake/stub** on **your** interface over mock frameworks aimed at the vendor SDK.
- Do not confuse test-double **fake/stub** with GREEN-phase **“fake it”** (hard-coded production return until triangulation).

Doubles should stay **dumb and obvious**; complex logic inside a double is a smell.

For structure and AAA, see [test-quality.md](test-quality.md).
