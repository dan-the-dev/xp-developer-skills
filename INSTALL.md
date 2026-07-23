# Install AMPD for Cursor

Use this after cloning the repository. One script installs skills and subagents for **all projects**.

## Quick start

```bash
git clone <repo-url> xp-developer-skills
cd xp-developer-skills
./scripts/install-cursor.sh
```

Restart Cursor, then invoke subagents (e.g. `/bugfix`, `/new-feature`, `/new-increment`, `/refactoring`, `/pr-reviewer`).

## What gets installed

| Path | Purpose |
|------|---------|
| `~/.cursor/ampd/` | Full AMPD bundle (`skills/`, `docs/`, `agents/`, `AGENTS.md`) — update by re-running the script |
| `~/.cursor/skills/<name>/` | Symlink → `~/.cursor/ampd/skills/<name>/` (Cursor skill auto-discovery) |
| `~/.cursor/agents/<name>.md` | Symlink → `~/.cursor/ampd/agents/<name>.md` (subagents) |
| `~/.cursor/docs` | Symlink → `~/.cursor/ampd/docs` (bibliography links from skills) |

New agents (e.g. **`refactoring`**) appear under `~/.cursor/agents/` only after you **re-run the install script** following `git pull`.

## Update

```bash
cd xp-developer-skills
git pull
./scripts/install-cursor.sh
```

Always re-run after pull when agents or skills were added — otherwise Cursor may lack types such as `refactoring` and orchestrators fall back to manual `/refactoring`.

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
