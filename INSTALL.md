# Install AMPD for Cursor

Use this after cloning the repository. One script installs skills and subagents for **all projects**.

## Quick start

```bash
git clone <repo-url> xp-developer-skills
cd xp-developer-skills
./scripts/install-cursor.sh
```

Restart Cursor, then invoke subagents (e.g. `/bugfix`, `/new-feature`, `/pr-reviewer`).

## What gets installed

| Path | Purpose |
|------|---------|
| `~/.cursor/ampd/` | Full AMPD bundle (`skills/`, `docs/`, `agents/`, `AGENTS.md`) — update by re-running the script |
| `~/.cursor/skills/<name>/` | Symlink → `~/.cursor/ampd/skills/<name>/` (Cursor skill auto-discovery) |
| `~/.cursor/agents/<name>.md` | Symlink → `~/.cursor/ampd/agents/<name>.md` (subagents) |
| `~/.cursor/docs` | Symlink → `~/.cursor/ampd/docs` (bibliography links from skills) |

## Update

```bash
cd xp-developer-skills
git pull
./scripts/install-cursor.sh
```

## Options

```bash
./scripts/install-cursor.sh          # default: symlinks for discovery (recommended)
./scripts/install-cursor.sh --copy   # copy files into discovery folders instead of symlinks
```

## Working inside this repository

If you open **this** repo in Cursor without global install, subagents resolve AMPD root to the **repository root** (`skills/` at workspace root). Global install uses `~/.cursor/ampd` when present.

## Claude Code

Subagents are also available at **`.claude/agents/`** (symlink to `agents/`).

## Do not install into

- `~/.cursor/skills-cursor/` — reserved for Cursor built-in skills

## Legacy cleanup

If you previously installed a skill as `~/.cursor/skills/bugfix-tdd/`, remove that folder after install — the canonical folder is **`bugfix`**.
