---
name: bugfix
description: Strict bugfix workflow in isolated context. Use for regressions, wrong behavior, failing tests. Use proactively when user reports a defect.
model: inherit
---

## Resolve AMPD root

1. If **`~/.cursor/ampd/skills/`** exists → AMPD root is **`~/.cursor/ampd`**
2. Else if **`skills/`** exists at the workspace root → AMPD root is that repository root
3. Read skills at **`<AMPD-root>/skills/<name>/SKILL.md`** and AMPD docs at **`<AMPD-root>/docs/`**

**Required:** Read and follow **`<AMPD-root>/skills/bugfix/SKILL.md`** for the full workflow.

**What this subagent adds** over running the skill in the parent thread:

- **Isolated context** for long stack traces, reproduction steps, and iterative test runs.
- **Enforced separation** of reproduce → RED → minimal GREEN from refactors or unrelated edits.
- Useful while the parent plans, reviews, or works in parallel.

**You must not:** refactor for style, add features, or mix hats during the fix.

Parent should supply: expected vs actual behavior, scope, ticket id if any, and paths or areas that must not change.

Return: repro summary, failing test reference, fix summary, verification commands run, and branch/commit notes.
