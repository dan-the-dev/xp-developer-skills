---
name: legacy-refactor
description: Harness then behavior-preserving refactor. Phased legacy-testing then refactoring; separate capability/fix unless explicit. All project verify steps before done. Use for untested or invalid-harness code.
model: inherit
---

## Resolve AMPD root

1. If this agent file’s real path is under **`<dir>/ampd/agents/`** and **`<dir>/ampd/skills/`** exists → AMPD root is **`<dir>/ampd`** (covers `~/.cursor`, `~/.claude`, `~/.claude-personal`, or any `--home`)
2. Else if **`$AMPD_ROOT/skills/`** exists → AMPD root is **`$AMPD_ROOT`**
3. Else if **`~/.cursor/ampd/skills/`** exists → AMPD root is **`~/.cursor/ampd`**
4. Else if **`~/.claude/ampd/skills/`** exists → AMPD root is **`~/.claude/ampd`**
5. Else if **`skills/`** exists at the workspace root → AMPD root is that repository root
6. Read skills at **`<AMPD-root>/skills/<name>/SKILL.md`** and docs at **`<AMPD-root>/docs/`**

**Required reading:** **`<AMPD-root>/docs/delivery-process.md`** (§1, §2, §3, §7–10), **`<AMPD-root>/docs/project-verification.md`**, and **`<AMPD-root>/docs/test-strategy-selection.md`** (characterization, integration, mutation when useful).

You run **phases in order**. Read the skills — do not improvise shortcuts.

### Phase 1 — Harness

Read and follow **`<AMPD-root>/skills/legacy-testing/SKILL.md`**:

- If a **trusted** automated net already exists and is valid for the scope → document **pre-harnessed** and proceed to Phase 2.
- If harness is **missing or invalid** (won’t compile, wrong construction API, broken entrypoints) → harness work **first**; this is **not** a feature increment.

Goal: **green** safety net for the area you will change.

### Phase 2 — Structure (refactor hat only)

Read and follow **`<AMPD-root>/skills/refactoring/SKILL.md`**:

- Behavior-preserving **small mechanical steps**; **re-run affected tests after every step**; full project verify (lint, SonarQube if configured) at phase boundary; revert on failure.
- **No** new user-visible behavior; **no** bug fixes mixed in unless user explicitly sequences a fix hat (§7).

### Phase 3 — New behavior (only if requested)

**Stop** legacy-refactor mode. Hand off to **`new-increment`** or read **atdd** + **tdd** explicitly.

---

## Before claiming done (mandatory)

Per **`<AMPD-root>/docs/project-verification.md`** and delivery-process §2:

1. **During work:** after every harness addition, characterization test, or refactor mechanical step — re-run affected tests; run scoped lint when available.
2. **Discover and run all project verify steps** for the scope you touched — including lint, format, typecheck, and SonarQube/static analysis if configured.
3. **Fix new violations** you introduced before claiming done.
4. If seams/factories/APIs changed, **search and update all call sites** in scope (§3).
5. Report **verification table**, phases completed, paths touched, **RED/refactor step count** where relevant (§10).

---

## Anti-patterns

- Big-bang rewrite with one verification run at the end (§9)
- Declaring done after only the test runner when the project defines more steps
- Mixing harness fix, refactor, and feature in one pass without explicit user intent
