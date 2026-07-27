# Seams, sensing, and separation

## Seams (Feathers)

A **seam** is a place where you can **alter behavior** without editing the program at that exact line — by changing what gets linked, injected, or compiled in.

Rough categories:

| Type | Idea | Examples (vary by language) |
|------|------|-----------------------------|
| **Preprocessing / compile-time** | Replace or include code via build | conditional compilation, build flags (use sparingly) |
| **Link / load-time** | Substitute a module or binary | dependency order, dynamic linking, classpath ordering |
| **Object / runtime** | Swap collaborators objects use | polymorphism, DI, factory, test doubles |

Most day-to-day work optimizes for **object seams**: parameterize construction, extract interface, override method in test subclass.

---

## Sensing vs separation

When breaking dependencies you usually want one or both:

**Sensing** — **observe** what happens inside code that hides results (writes to globals, private fields, logs without return). You add a seam to **capture** outputs or effects in tests.

**Separation** — run code **without** the real database, clock, HTTP, hardware. You substitute **fakes** or **mocks** so tests are fast and deterministic.

Do **not** confuse **fake** (working simplification) with **mock** (expects interactions). Pick the smallest double that gives **signal** without overspecifying internals.

---

## Fakes, mocks, stubs (pragmatic)

Vocabulary aligns with Meszaros via [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html): **fake** (working shortcut), **stub** (canned answers), **mock** (pre-programmed call expectations / behavior verification).

- Prefer **fakes** when you need **return values** or in-memory behavior; prefer **stubs** for canned query responses.
- Prefer **real** awkward collaborators when a **sandbox/test** env makes that practical (especially owned vendor adapters — [`test-strategy-selection.md`](../../../docs/test-strategy-selection.md) §3a).
- Use **mocks** when **interactions** (calls made) are the contract — but in **characterization**, don’t invent ideal APIs; record what **happens now** if that is the legacy contract.
- Avoid mocking **everything**; you lose confidence that real wiring works. Lean on pinch points and narrow integration when cheap. Do not mock **third-party SDK types** directly — wrap first, then fake/stub your port.

---

## Cupac / stable tests

Tests that assert **internal** structure break when you add seams. Prefer **behavior** at the new boundary ([`tests-and-design.md`](../../refactoring/references/tests-and-design.md)): **Given** setup, **When** act through public or seam surface, **Then** observable outcome.
