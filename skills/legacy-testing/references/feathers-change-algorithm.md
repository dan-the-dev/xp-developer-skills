# The change algorithm (five phases)

Feathers’ sequence for **safe** changes. Treat it as **mandatory order** for unfamiliar, untested areas.

---

## 1. Identify change points

- What **behavior** must differ after your work?
- Which **classes / functions / modules** must gain, lose, or alter logic?
- Mark the **smallest** edit surface that could satisfy the goal (avoid “refactor the world”).

**Output:** one or a few concrete locations (paths, symbols).

---

## 2. Find test points

- Where can you **invoke** that behavior with reasonable setup?
- Where can you **observe** results (return values, fields written, messages sent, DB rows in test DB)?
- Which pinch points ([pinch-points-and-effect-sketches.md](pinch-points-and-effect-sketches.md)) cover the blast radius?

**Output:** candidate test location(s) and assertion ideas.

---

## 3. Break dependencies

Legacy often **constructs** collaborators inline, uses globals, statics, or hard-coded I/O — impossible to run in isolation.

Use **seams** ([seams-sensing-separation.md](seams-sensing-separation.md)) and **catalog** techniques ([dependency-breaking-techniques.md](dependency-breaking-techniques.md)):

- Introduce parameters, interfaces, or overrides **only as much** as the next test needs.
- Prefer **one** seam at a time; compile/run after each.

**Output:** code callable from tests; collaborators replaceable.

---

## 4. Write tests

- **Characterization:** assert **current** behavior you must preserve ([characterization-tests.md](characterization-tests.md)).
- **Bug:** if behavior is **known wrong**, a failing test encodes desired outcome — then use **`skills/bugfix`** discipline after the harness exists.

Start **narrow**; widen only when pinch points demand it.

**Output:** green suite on **unchanged** production (characterization baseline).

---

## 5. Modify and refactor

- Implement the **new** behavior (feature or fix) — tests may go red then green.
- **Refactor** with `skills/refactoring` — behavior-preserving steps only.

Separate commits by **hat** when practical.

---

## Looping

Large goals repeat phases 2–5 on **smaller** slices:

- Break dependencies for **one** method
- Characterize **one** outcome
- Change **one** branch

Small batches integrate better with CD ([aligned-practices.md](aligned-practices.md)).
