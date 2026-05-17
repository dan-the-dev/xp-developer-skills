---
name: spike
description: Time-boxed spike on isolated spike/ branch; disposable code; spike report. Use for feasibility, library/API trials, unknowns — not for shipping product. Use proactively before committing to delivery.
model: inherit
---

**Required:** Read and follow **`skills/spike/SKILL.md`**.

**Non-negotiables:**

- All experiment code on **`spike/<slug>`** branch only — **not** on `main` or `feat/…`.
- Code is **throwaway** by default; **do not merge** as finished product.
- **No** delivery test pyramid, test lists, or example catalogs unless a one-off check proves the charter faster.
- Produce a **spike report**: verdict, evidence, recommendation (**discard** | **promote** | follow-up spike).

**Promotion** means a **new** delivery workflow — **`skills/atdd`**, **`skills/tdd`**, **`skills/legacy-testing`** — not continuing on the spike branch as production.

Return the spike report structure from the skill to the parent.
