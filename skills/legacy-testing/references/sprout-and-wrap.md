# Sprout Method, Sprout Class, Wrap Method, Wrap Class

When you **cannot** refactor deeply yet, **add** new structure with minimal intrusion.

---

## Sprout Method

**What:** Add a **new method** (or private helper extracted outward) that holds new logic; the legacy method calls it.

**When:** Old method is a mess but you only need **one** clean place for new behavior.

**Why:** Limits diff size; new code is test **directly**; legacy flow stays recognizable.

**Watch:** Don’t sprout fifty tiny methods without eventually consolidating — use sprout to **earn** coverage, then refactor.

---

## Sprout Class

**What:** New class holds logic; legacy references it (constructor, static factory, or method-local `new` — improve later).

**When:** New rules deserve their own unit; method would balloon otherwise.

---

## Wrap Method

**What:** Wrap existing method: **pre/post** hooks in a new method that calls the old (or rename old to `…Core`, new entry uses legacy name).

**When:** Cross-cutting concerns (logging, transaction, guard) must wrap legacy **without** editing its body yet.

---

## Wrap Class (Decorator-style)

**What:** New class implements same logical role as legacy, **delegates** to inner instance, adds behavior.

**When:** Class is huge or unstable; you need an **outer** seam for tests or new paths.

**Why:** Matches Open/Closed spirit: extend without rewriting monster internals immediately.

---

## Composition

Sprout/wrap pairs well with **characterization** on the **outer** entry and **unit tests** on **sprouted** code.

---

## Fowler / Beck angle

These are **transition patterns** — not the final design. Plan follow-up **refactor** passes ([`skills/refactoring`](../../refactoring/SKILL.md)) once tests exist.
