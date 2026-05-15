# Duplication, abstraction, and naming

## Rule of three (pragmatic DRY)

**First time** — write it.

**Second time** — note duplication; sometimes still OK (symmetric concepts).

**Third time** — strong signal to **extract** a shared element (function, type, constant).

**Over-applying DRY** creates wrong abstractions: one “universal” brick pile that fits nothing well. Prefer duplication over **premature** coupling.

---

## What to deduplicate

Good candidates:

- Identical **business rules** or formulas
- Identical **error handling** patterns with same semantics
- Identical **setup** blocks in tests → test helpers (refactor test code with same green-between-steps rule)

Poor candidates:

- Coincidentally similar lines with **different reasons to change**
- “Utilities” that are only two lines and **opaque** when extracted

---

## Naming (clear boxes)

Names are the **labels on your LEGO bins**:

- Prefer **domain** words over `data`, `info`, `helper`, `x`
- Functions: **verb** phrases; types: **nouns**
- If a name needs a comment to explain, try a **better name** or **smaller** unit first

Rename is one of the **safest** refactorings when tests are green — use IDE rename to preserve consistency.

---

## Boy Scout rule

When you touch code for a feature or bugfix, **leave the campground cleaner**: one small rename, one tiny extract **in the same area** — still **refactor hat** if you commit separately or follow team rules.

Do not turn every ticket into a **mega** cleanup without scope.
