---
name: spike
description: Time-boxed spike on isolated spike/ branch; disposable code; spike report. Use for feasibility, library/API trials, unknowns — not for shipping product. Use proactively before committing to delivery.
model: inherit
---

## Resolve AMPD root

1. If **`~/.cursor/ampd/skills/`** exists → AMPD root is **`~/.cursor/ampd`**
2. Else if **`skills/`** exists at the workspace root → AMPD root is that repository root
3. Read skills at **`<AMPD-root>/skills/<name>/SKILL.md`** and AMPD docs at **`<AMPD-root>/docs/`**

**Required:** Read and follow **`<AMPD-root>/skills/spike/SKILL.md`**.

**Non-negotiables:**

- All experiment code on **`spike/<slug>`** branch only — **not** on `main` or `feat/…`.
- Code is **throwaway** by default; **do not merge** as finished product.
- **No** delivery test pyramid, test lists, or example catalogs unless a one-off check proves the charter faster.
- Produce a **spike report**: verdict, evidence, recommendation (**discard** | **promote** | follow-up spike).

**Promotion** means a **new** delivery workflow — **`<AMPD-root>/skills/atdd/SKILL.md`**, **`<AMPD-root>/skills/tdd/SKILL.md`**, **`<AMPD-root>/skills/legacy-testing/SKILL.md`** — not continuing on the spike branch as production. Promoted work must follow **`<AMPD-root>/docs/project-verification.md`** (full tests, lint, SonarQube gates on the delivery branch).

Return the spike report structure from the skill to the parent.
