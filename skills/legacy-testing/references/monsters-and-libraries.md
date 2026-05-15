# Monsters and third-party libraries

## Monster classes and methods

**Symptoms:** thousands of lines, many responsibilities, hidden branches, heavy I/O inside “business” methods.

**Strategy (incremental):**

1. **Characterize** at the **outer** pinch point if possible.
2. **Sprout** new behavior to new types; peel one responsibility at a time.
3. **Extract** methods and classes once tests exist — use **`skills/refactoring`** for mechanical steps.
4. **Avoid** the fantasy “stop for six weeks and rewrite” unless the business explicitly buys risk.

SRP violation is a **smell**; the medicine is **tests + small extractions**, not sermons.

---

## Library lock-in

**Problem:** code uses vendor SDK everywhere; tests hit real network or paid APIs.

**Moves:**

- **Wrapper / adapter** — your interface, their implementation; tests use fake adapter.
- **Seam at boundary** — only the wrapper talks to the library; domain never imports vendor types directly if feasible.

Matches **Hexagonal / Ports** thinking (see Cupać’s architecture material) without requiring full rewrite — **start** at the module you touch.

---

## Feathers + Fowler

Breaking dependency on libraries uses the same **catalog** techniques ([dependency-breaking-techniques.md](dependency-breaking-techniques.md)); **naming** the wrapper clearly signals “legacy containment zone.”
