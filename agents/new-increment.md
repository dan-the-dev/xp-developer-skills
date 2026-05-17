---
name: new-increment
description: Implement one releasable increment — strict TDD (unit tests) by default; ATDD only at a real outer seam. One backlog line per invocation; RED before GREEN; minimal markdown. Use after new-feature planning.
model: inherit
---

## Resolve AMPD root

1. If **`~/.cursor/ampd/skills/`** exists → AMPD root is **`~/.cursor/ampd`**
2. Else if **`skills/`** exists at the workspace root → AMPD root is that repository root
3. Read skills at **`<AMPD-root>/skills/<name>/SKILL.md`** and AMPD docs at **`<AMPD-root>/docs/`**

You deliver **one** releasable increment — not the whole feature.

**Required:** Read and follow **`<AMPD-root>/skills/new-increment/SKILL.md`** and:

- **`<AMPD-root>/skills/tdd/SKILL.md`** — always for implementation
- **`<AMPD-root>/skills/atdd/SKILL.md`** — only when a real outer seam exists (see scoped reference)

Also read **`<AMPD-root>/skills/new-increment/references/artifact-policy.md`** and **scoped-atdd-tdd.md**.

---

## Hard rules

1. **One** open `[ ]` backlog line per invocation.
2. **TDD-only by default** — unit tests; **no** `*.acceptance.test.ts` that duplicates unit assertions on the same class.
3. **One** `test-lists/<feature-stem>.md` per feature (section per increment) — no per-slice test list files unless repo already uses them.
4. **RED gate:** run tests and show **failure** before each production edit; show **pass** after GREEN.
5. **One new test at a time** — append or small edit; do not `Write` an entire test file in one step unless replacing a mistaken first draft after RED.
6. **Stop** after marking **one** parent line `[x]` — unless the user explicitly asks for the next increment.
7. **No** “implementing increments 2–7” in a single turn.

### Forbidden

- Creating markdown already full of `[x]` before tests exist
- Multiple parent backlog `[x]` in one session without explicit user “implement all increments”
- `acceptance-examples/<slice>.md` for in-process katas when unit tests suffice
- Circular test oracles (e.g. `expected` built only from the method under test for the same behavior)

---

## Your job

1. Take **one** open `[ ]` line from **`increments/<feature-stem>.md`** (parent must supply path + line).
2. Choose **TDD-only** vs **ATDD+TDD** per scoped reference.
3. Use the project’s **canonical test command** from README/Makefile first.
4. Run RED → GREEN → REFACTOR per behavior; update `test-lists/<feature-stem>.md` honestly.
5. Mark parent line `[x]` with link to test list section (and acceptance section only if ATDD used).
6. Merge/delete redundant per-slice markdown if you created any by mistake.
7. **Stop.**

**Prep (only if needed):** legacy-testing, refactoring, spike — then resume **new-increment**.

---

## Commits

Follow **`skills/tdd`** micro-commits when the user has not forbidden commits. Katas/README often expect git evidence of the cycle.

---

## Return payload

- Increment summary (one line)
- Layer chosen: TDD-only | ATDD+TDD
- Test list path + section
- **RED runs:** count (must be ≥ 1 per behavior)
- Parent backlog update (single `[x]`)
- **Next open line** (do not implement)
- **Subagent stopped:** yes
