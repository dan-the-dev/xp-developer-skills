# Tests and design (Valentina Cupać)

Valentina Cupać’s teaching on TDD and architecture reinforces sustainable refactoring:

- Tests should be **coupled to the behavior** of the code.
- Tests should be **decoupled from the internal structure** of the code.

When tests assert **how** something is implemented (private methods, call order, internal flags), **moving bricks** during refactoring breaks tests even though the **spaceship still flies** — that is a **test design** problem, not a reason to avoid refactoring.

---

## For refactoring sessions

- Prefer assertions on **public** outcomes, contracts, and stable seams.
- If a refactor requires **only** test updates (same behavior), treat that as **test refactor** steps: still **one** change at a time, **green** after each.
- If production **must** change to satisfy tests after a “refactor,” you probably **changed behavior** or **revealed** a bug — **stop** and **switch hats** (bugfix / feature).

---

## Further reading

- Cupać’s [Quality Software Faster](https://valentinacupac.com/) and Optivem / TDD Handbook material on refactoring inside RED–GREEN–REFACTOR.

This repository’s **`skills/tdd`** encodes the REFACTOR step; this **`skills/refactoring`** skill generalizes the same discipline for larger or standalone sessions.
