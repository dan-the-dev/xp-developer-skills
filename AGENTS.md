# AMPD — agent orientation

**Source of truth:** `skills/*/SKILL.md`. Subagents are thin routers with isolated context.

## Subagents

Location: **`.claude/agents/`** (Cursor and Claude Code; invoke with `/name` in Cursor or natural mention).

| Subagent | Skill(s) |
|----------|----------|
| `new-feature` | `skills/new-feature/` — slice epic into `increments/<stem>.md` |
| `new-increment` | `skills/new-increment/` → `skills/atdd` + `skills/tdd` per slice |
| `bugfix` | `skills/bugfix/` |
| `legacy-refactor` | `skills/legacy-testing/` then `skills/refactoring/` |
| `spike` | `skills/spike/` (`spike/` branch, disposable) |
| `pr-reviewer` | `docs/manifesto.md` + applicable skills (`readonly`) |

## Skills (delivery)

`bugfix`, `tdd`, `atdd`, `refactoring`, `legacy-testing`, `spike`, `new-feature`, `new-increment` — under `skills/`.

## Docs

- [`docs/manifesto.md`](docs/manifesto.md)
- [`docs/roadmap.md`](docs/roadmap.md)
