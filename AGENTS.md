# AMPD — agent orientation

**Source of truth:** `skills/*/SKILL.md`. Subagents are thin routers with isolated context.

## Subagents

Location: **`agents/`** (symlinked at **`.claude/agents/`** for Claude Code in this repo). After [install](INSTALL.md): Cursor → **`~/.cursor/agents/`**; Claude Code (global) → **`~/.claude/agents/`**. Invoke with `/name` or natural mention.

| Subagent | Skill(s) |
|----------|----------|
| `new-feature` | `skills/new-feature/` — slice epic into `increments/<stem>.md`; **plan + orchestrate**; hand off to `new-increment`; post-increment review via `refactoring`; **step** (default) or **automatic** (explicit) |
| `new-increment` | `skills/new-increment/` → `skills/tdd` per slice (ATDD only at outer seam); **one** increment per invocation; verify green; commit; stop |
| `refactoring` | `skills/refactoring/` — dedicated tidy-up **or** post-increment review after `new-increment` (not for untested code) |
| `bugfix` | `skills/bugfix/` |
| `legacy-refactor` | `skills/legacy-testing/` then `skills/refactoring/` — harness first on unprotected code, then structure |
| `spike` | `skills/spike/` (`spike/` branch, disposable) |
| `pr-reviewer` | `docs/manifesto.md` + applicable skills (`readonly`) |

## Skills (delivery)

`bugfix`, `tdd`, `atdd`, `refactoring`, `legacy-testing`, `spike`, `new-feature`, `new-increment` — under `skills/`.

## Docs

- [`docs/manifesto.md`](docs/manifesto.md)
- [`docs/delivery-process.md`](docs/delivery-process.md) — shared delivery rules (verification, roles, **feature branch §1a**, return payload)
- [`docs/project-verification.md`](docs/project-verification.md) — scoped checks during work; full gates after every code-touching slice
- [`docs/test-strategy-selection.md`](docs/test-strategy-selection.md) — which test layers and techniques to adopt per slice (mutation, contract, property-based, owned vendor clients §3a, etc.)
- [`docs/roadmap.md`](docs/roadmap.md)

## Install

See **[INSTALL.md](INSTALL.md)** for global setup — Cursor (`~/.cursor/ampd`) and/or Claude Code (`<claude-home>/ampd`, default `~/.claude`; use `--home` for e.g. `~/.claude-personal`) + auto-discovery.
