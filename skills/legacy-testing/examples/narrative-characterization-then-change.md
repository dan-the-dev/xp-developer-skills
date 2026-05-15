# Narrative — characterize then fix (language-agnostic)

Fictional; adapt paths and runner to the repo.

---

## Context

`OrderService.place(orderId)` applies discounts and writes to a database. **No unit tests.** You must fix **wrong shipping discount** for bulk orders.

---

## Phase 1 — Change & test points

- **Change point:** discount branch inside `OrderService.place`.
- **Test point:** `place` return value / persisted `Order` shape (or event emitted) — pick **one** observable the bug cares about.

---

## Phase 2 — Break dependency

Production does `new SqlOrderRepo()` inside constructor.

**Intervention:** **Parameterize constructor** — inject `OrderRepository` (interface + prod adapter). Production wiring updated in composition root only.

Run compile. No behavior change yet.

Commit: `refactor: inject OrderRepository into OrderService`

---

## Phase 3 — Characterization

In tests, inject **in-memory fake repo**. Write **characterization** test: “given order with 100 items, when place, then discount field is X” using **today’s** (buggy) value **X**.

**GREEN** — baseline locked.

Commit: `test: characterize bulk discount for OrderService.place`

---

## Phase 4 — Bugfix

Change expected value to **correct** business rule → **RED**. Implement minimal fix in discount branch → **GREEN**.

Use **`skills/bugfix`** habits: isolated fix commit.

---

## Phase 5 — Refactor (optional)

Extract discount policy to `BulkDiscountPolicy` with `skills/refactoring` — characterization + bug test stay green.

---

## Lesson

Feathers steps **earned** safe **bugfix** and **refactoring**. Skipping constructor injection would force **full DB** tests or hope.
