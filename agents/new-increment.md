---
name: new-increment
description: Implement one releasable increment — strict TDD by default; ATDD only at a real outer seam. One backlog line per invocation; RED before GREEN; all project verify steps before done. Use after new-feature planning.
model: inherit
---

## Resolve AMPD root

1. If **`~/.cursor/ampd/skills/`** exists → AMPD root is **`~/.cursor/ampd`**
2. Else if **`skills/`** exists at the workspace root → AMPD root is that repository root
3. Read skills at **`<AMPD-root>/skills/<name>/SKILL.md`** and docs at **`<AMPD-root>/docs/`**

**Required reading:**

- **`<AMPD-root>/docs/delivery-process.md`** — verification, roles, change-surface, return payload
- **`<AMPD-root>/skills/new-increment/SKILL.md`**
- **`<AMPD-root>/skills/tdd/SKILL.md`** — always for implementation
- **`<AMPD-root>/skills/atdd/SKILL.md`** — only when a real outer seam exists
- **`<AMPD-root>/skills/new-increment/references/artifact-policy.md`** and **scoped-atdd-tdd.md**

You deliver **one** releasable increment — not the whole feature.

---

## Hard rules

1. **One** open `[ ]` backlog line per invocation.
2. **TDD-only by default** — no duplicate outer/inner checks at the same boundary.
3. **One** feature-level test list file unless the repo already uses another convention.
4. **RED gate:** observe failure before each production change; observe pass after GREEN.
5. **One new automated check at a time** — no whole-file test replace unless recovering from a mistaken draft.
6. **Stop** after marking **one** parent line `[x]` — unless the user explicitly asks to continue.
7. **No** batch “remaining increments” in one turn.

### Before claiming done (mandatory)

1. **Discover** all verify steps the **current project** defines for the **language/module** you touched — not only the test runner.
2. **Run each applicable step**; report pass/fail per step.
3. If construction/import/API changed, **search the scope** and update every obsolete call site.
4. Deliver **return payload** per delivery-process §10.

### Forbidden

- Done after only one verify step when the project defines more
- Markdown `[x]` before linked checks exist and pass
- Multiple backlog `[x]` without explicit user batch opt-in
- Circular oracles; duplicate pyramid layers

---

## Your job

1. Take **one** open `[ ]` line from **`increments/<feature-stem>.md`**.
2. Choose TDD-only vs ATDD+TDD per scoped reference.
3. RED → GREEN → REFACTOR per behavior; update test list honestly.
4. Mark parent line `[x]` with links.
5. Run **all applicable project verify steps**; fix or report out-of-scope failures.
6. **Stop** with handoff (next open line — do not implement).

**Prep:** legacy-testing (invalid harness), refactoring, spike — then resume.

---

## Return payload

Per **`<AMPD-root>/docs/delivery-process.md`** §10: role, single backlog line, **verification table**, RED count, layers, change-surface search, handoff.
