# AMPD — agent orientation

**Source of truth:** `skills/*/SKILL.md`. Subagents are thin routers with isolated context.

## Subagents

Location: **`agents/`** (symlinked at **`.claude/agents/`** for Claude Code). Cursor discovers them at **`~/.cursor/agents/`** after [install](INSTALL.md). Invoke with `/name` in Cursor or natural mention.

| Subagent | Skill(s) |
|----------|----------|
| `new-feature` | `skills/new-feature/` — slice epic into `increments/<stem>.md`; **plan only**, hand off to `new-increment` |
| `new-increment` | `skills/new-increment/` → `skills/tdd` per slice (ATDD only at outer seam); **one** increment per invocation |
| `bugfix` | `skills/bugfix/` |
| `legacy-refactor` | `skills/legacy-testing/` then `skills/refactoring/` |
| `spike` | `skills/spike/` (`spike/` branch, disposable) |
| `pr-reviewer` | `docs/manifesto.md` + applicable skills (`readonly`) |

## Skills (delivery)

`bugfix`, `tdd`, `atdd`, `refactoring`, `legacy-testing`, `spike`, `new-feature`, `new-increment` — under `skills/`.

## Docs

- [`docs/manifesto.md`](docs/manifesto.md)
- [`docs/delivery-process.md`](docs/delivery-process.md) — shared delivery rules (verification, roles, return payload)
- [`docs/roadmap.md`](docs/roadmap.md)

## Install

See **[INSTALL.md](INSTALL.md)** for global Cursor setup (`~/.cursor/ampd` + auto-discovery).
