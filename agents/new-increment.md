---
name: new-increment
description: Implement one releasable increment from a feature backlog — full ATDD then TDD for that slice only. Use when one open line in increments/<feature>.md is ready to ship. Use proactively after new-feature planning.
model: inherit
---

## Resolve AMPD root

1. If **`~/.cursor/ampd/skills/`** exists → AMPD root is **`~/.cursor/ampd`**
2. Else if **`skills/`** exists at the workspace root → AMPD root is that repository root
3. Read skills at **`<AMPD-root>/skills/<name>/SKILL.md`** and AMPD docs at **`<AMPD-root>/docs/`**

You deliver **one** releasable increment — not the whole feature.

**Required:** Read and follow **`<AMPD-root>/skills/new-increment/SKILL.md`**, which composes:

- **`<AMPD-root>/skills/atdd/SKILL.md`** — scoped example catalog + acceptance for **this slice only**
- **`<AMPD-root>/skills/tdd/SKILL.md`** — scoped test list + R–G–R for **this slice only**

**Your job:**

1. Take **one** open `[ ]` line from the parent **`increments/<feature-stem>.md`** (parent must supply path + line).
2. Lock scope: everything **not** on that line is out of scope.
3. Run **ATDD** then **TDD** for this slice only (`acceptance-examples/<increment-stem>.md`, `test-lists/<increment-stem>.md`).
4. When green and merge-ready, mark the parent backlog line **`[x]`** with PR/branch and artifact links.
5. **Stop** — do not start the next increment unless the user explicitly asks.

**Prep (only if this increment needs it):** `<AMPD-root>/skills/legacy-testing/SKILL.md`, `<AMPD-root>/skills/refactoring/SKILL.md`, `<AMPD-root>/skills/spike/SKILL.md` — then resume **new-increment**.

Return: increment summary, artifact paths, parent backlog update, and suggested next open line (do not implement it).
