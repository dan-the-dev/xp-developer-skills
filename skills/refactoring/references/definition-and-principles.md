# Definition and principles

## The LEGO picture (same spaceship, neater bricks)

You can **rebuild the inside** of the model — group colors, reinforce joints, put the cockpit where everyone expects it — **without** changing what the spaceship *does* in play. If you swap a wing for a **new laser**, that is **not** refactoring; that is a feature.

**Refactoring** here means: **structure and readability improve, behavior stays the same.**

---

## Fowler-style definition

Martin Fowler’s core distinction:

- **Refactoring** (noun): *a change* that improves internal design without changing observable behavior.
- **Refactoring** (verb): *the process* of applying such changes **in small steps**, each keeping behavior intact.

The goal is **simpler change later** — not cleverness for its own sake. AMPD judges “simpler” with [`docs/simple-design.md`](../../../docs/simple-design.md): Beck’s four rules, **mandatory Object Calisthenics**, and GoF patterns only as destinations when smells persist.

---

## Observable behavior

**Same** after a refactoring step:

- Return values and outputs for the same inputs (including errors that are part of the public contract)
- User-visible flows that the code path implements
- Side effects the system is **meant** to have (I/O, messages) at the **same logical points** — unless the team explicitly treats a bugfix as out of scope (then **switch hats**)

**Not** sacred:

- Private helpers, class layout, names (if all call sites updated), internal call order when externals are unchanged

When in doubt, **tests** (and agreed examples) define “observable” for that module.

---

## Why baby steps

Small steps localize mistakes:

- If you change **one hundred** things and something breaks, you cannot tell **which** move failed.
- If you change **one** mechanical thing and tests fail, that step was **not** behavior-preserving — **undo** and retry smaller.

This matches Kent Beck’s emphasis on **reversible** edits and continuous **green** as feedback.

---

## Summary

Refactoring is **tidying without changing what the program does** — one safe step at a time, always able to **put the last brick back** if the “green light” goes off.
