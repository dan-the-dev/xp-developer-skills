# Characterization tests

## Purpose

**Characterization tests** document **what the system does today** — not what you wish it did. They **freeze** behavior so the next edit creates a **trustworthy diff**.

They are the legacy counterpart of “RED for new behavior”: baseline is **GREEN** on current code; when you intentionally change behavior, **some** characterization tests should turn **RED** — then you decide whether to **update** the test (intended change) or **fix** the code (mistake).

---

## How to write them

1. **Pick a narrow pinch point** ([pinch-points-and-effect-sketches.md](pinch-points-and-effect-sketches.md)).
2. **Drive** production through real entry (public method, HTTP handler shim, CLI).
3. **Assert** observable outcomes: return value, collection contents, message payload fields, DB row in test database.
4. **Name** the test for the **behavior** (“returns total including tax for in-state orders”), not “method X line 40”.
5. **Avoid** brittle coupling: exact error message strings (unless contract), timestamps, random ids, full HTML dumps — normalize or assert structure.

---

## Golden tests and snapshots

Snapshot / approval testing can speed first pass — **review** diffs carefully; reject noise. Prefer **targeted** assertions once behavior is understood.

---

## When NOT to characterize everything

- **Dead code** — delete or prove unused first.
- **Exploratory spike** — time-box; don’t snapshot chaos.

---

## Relation to bugfix

If you **already know** wrong behavior:

- Add a **failing test** that states correct outcome — then use **`skills/bugfix`** discipline after the harness exists.

You may still need **Feathers steps 2–3** (test point + seam) before the test compiles/runs.

Characterization **plus** bug test: characterize surrounding behavior, then one **RED** for the defect.

---

## Relation to TDD

Once the area is covered, **new** work follows **`skills/tdd`**: test list, RED–GREEN–REFACTOR.
