# Install AMPD

Use this after cloning the repository. Each script installs skills and subagents for **all projects** on that tool.

| Tool | Script | Bundle |
|------|--------|--------|
| **Cursor** | `./scripts/install-cursor.sh` | `~/.cursor/ampd/` |
| **Claude Code** | `./scripts/install-claude.sh` | `<claude-home>/ampd/` (default `~/.claude/ampd/`) |

Run one or both, depending on which tools you use.

## Quick start

```bash
git clone <repo-url> xp-developer-skills
cd xp-developer-skills

# Cursor
./scripts/install-cursor.sh

# Claude Code (default home: ~/.claude)
./scripts/install-claude.sh

# Claude Code — second / personal instance
./scripts/install-claude.sh --home ~/.claude-personal
```

Then restart the tool (or start a new Claude Code session) and invoke subagents (e.g. `/bugfix`, `/new-feature`, `/new-increment`, `/increment-review`, `/refactoring`, `/tweak`, `/pr-reviewer`).

For a non-default Claude home, the Claude Code process must use the **same** config directory (e.g. `CLAUDE_CONFIG_DIR=~/.claude-personal`), or it will keep loading `~/.claude` only.

## What gets installed

### Cursor

| Path | Purpose |
|------|---------|
| `~/.cursor/ampd/` | Full AMPD bundle (`skills/`, `docs/`, `agents/`, `AGENTS.md`) — update by re-running the script |
| `~/.cursor/skills/<name>/` | Symlink → `~/.cursor/ampd/skills/<name>/` (skill auto-discovery) |
| `~/.cursor/agents/<name>.md` | Symlink → `~/.cursor/ampd/agents/<name>.md` (subagents) |
| `~/.cursor/docs` | Symlink → `~/.cursor/ampd/docs` (bibliography links from skills) |

### Claude Code

Paths are under **`<claude-home>`** (default `~/.claude`; override with `--home` or `AMPD_CLAUDE_HOME`).

| Path | Purpose |
|------|---------|
| `<claude-home>/ampd/` | Full AMPD bundle (`skills/`, `docs/`, `agents/`, `AGENTS.md`) — update by re-running the script |
| `<claude-home>/skills/<name>/` | Symlink → `<claude-home>/ampd/skills/<name>/` (personal skill auto-discovery) |
| `<claude-home>/agents/<name>.md` | Symlink → `<claude-home>/ampd/agents/<name>.md` (user-level subagents) |
| `<claude-home>/docs` | Symlink → `<claude-home>/ampd/docs` (bibliography links from skills) |

New agents (e.g. **`refactoring`**) appear under the discovery folders only after you **re-run the install script** following `git pull`.

### Project-local Claude Code (this repo)

In **this** repository, **`.claude/agents/`** is already a symlink to **`agents/`**. That is enough for Claude Code when you work *inside* this clone. Global install (`<claude-home>/…`) is for using AMPD in **other** projects.

Project-local `.claude/agents/` / `.claude/skills/` take precedence over user-level agents/skills when names collide.

## Update

```bash
cd xp-developer-skills
git pull
./scripts/install-cursor.sh                              # if you use Cursor
./scripts/install-claude.sh                              # default ~/.claude
./scripts/install-claude.sh --home ~/.claude-personal    # if you also use a personal home
```

Always re-run after pull when agents or skills were added — otherwise the tool may lack types such as `refactoring` and orchestrators fall back to manual `/refactoring`.

## Options

```bash
./scripts/install-cursor.sh          # default: symlinks for discovery (recommended)
./scripts/install-cursor.sh --copy   # copy into discovery folders instead of symlinks

./scripts/install-claude.sh                        # ~/.claude (or $AMPD_CLAUDE_HOME)
./scripts/install-claude.sh --home ~/.claude-personal
./scripts/install-claude.sh --home ~/.claude-personal --copy
AMPD_CLAUDE_HOME=~/.claude-personal ./scripts/install-claude.sh
```

## Working inside this repository

If you open **this** repo without a global install, subagents resolve AMPD root to the **repository root** (`skills/` at workspace root).

Global install resolution (in agent bodies):

1. AMPD next to this agent file (`<dir>/ampd` when the agent lives under `<dir>/ampd/agents/`) — works for `~/.cursor`, `~/.claude`, `~/.claude-personal`, any `--home`
2. Else `$AMPD_ROOT` if set
3. Else `~/.cursor/ampd` if present
4. Else `~/.claude/ampd` if present
5. Else workspace `skills/`

## Do not install into

- `~/.cursor/skills-cursor/` — reserved for Cursor built-in skills

## Legacy cleanup

If you previously installed a skill as `~/.cursor/skills/bugfix-tdd/` (or the Claude equivalent under `<claude-home>/skills/`), remove that folder after install — the canonical folder is **`bugfix`**.
