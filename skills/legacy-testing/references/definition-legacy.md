# Legacy code — Feathers definition

## What “legacy” means here

Michael Feathers defines **legacy code** as code **without tests** — not necessarily old.

If there are **no automated checks** that fail when behavior regresses in the area you touch, you are working **without a safety net**. Every edit is guesswork: you might improve structure, **or** introduce a subtle regression nobody spots until production.

---

## Why modification is risky

- Human reasoning does not scale to full call graphs and implicit state.
- “It looks right” ≠ **same** outputs and side effects as before.
- Refactoring **without** tests is not Fowler-style refactoring — it is **redesign with hope** ([`skills/refactoring`](../../refactoring/SKILL.md)).

---

## What this skill delivers

A path from **unprotected** to **pinned behavior** so normal engineering skills apply:

1. Know **where** you must change.
2. Know **where** to observe behavior.
3. **Break dependencies** until you can run code under tests.
4. Write tests that describe **today** (characterization) or **wrong** (bug repro).
5. **Then** change and refactor with confidence.

---

## Not legacy (for this workflow)

Code with **adequate** automated coverage at the seams you need — use **`skills/refactoring`** or **`skills/bugfix`** directly.

“Legacy” is about **test deficit relative to the change**, not calendar age.
