#!/usr/bin/env bash
# Install AMPD skills and subagents for Claude Code (all projects).
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
MODE="symlink"
# Default: ~/.claude — override with --home or AMPD_CLAUDE_HOME (e.g. ~/.claude-personal)
CLAUDE_HOME="${AMPD_CLAUDE_HOME:-${HOME}/.claude}"

usage() {
  cat <<'EOF'
Usage: install-claude.sh [--home <dir>] [--copy]

  Installs AMPD under <claude-home>/ampd and wires Claude Code auto-discovery paths.

  --home <dir>   Claude config home (default: ~/.claude, or $AMPD_CLAUDE_HOME).
                 Example: --home ~/.claude-personal
  --copy         Copy into <claude-home>/skills and <claude-home>/agents instead of symlinks

  The Claude Code instance must use the same config dir (e.g. CLAUDE_CONFIG_DIR=~/.claude-personal)
  or it will not load skills/agents from a custom --home.
EOF
}

expand_path() {
  local p="$1"
  if [[ "${p}" == ~* ]]; then
    p="${p/#\~/${HOME}}"
  fi
  # Resolve to absolute when the path exists or its parent does
  if [[ -d "${p}" ]]; then
    (cd "${p}" && pwd)
  elif [[ -d "$(dirname "${p}")" ]]; then
    echo "$(cd "$(dirname "${p}")" && pwd)/$(basename "${p}")"
  else
    echo "${p}"
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --home)
      if [[ $# -lt 2 ]]; then
        echo "Missing value for --home" >&2
        usage >&2
        exit 1
      fi
      CLAUDE_HOME="$(expand_path "$2")"
      shift 2
      ;;
    --copy) MODE="copy"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
  esac
done

CLAUDE_HOME="$(expand_path "${CLAUDE_HOME}")"
AMPD="${CLAUDE_HOME}/ampd"

for dir in skills docs agents; do
  if [[ ! -d "${REPO}/${dir}" ]]; then
    echo "Missing ${REPO}/${dir}" >&2
    exit 1
  fi
done

mkdir -p "${AMPD}" "${CLAUDE_HOME}/skills" "${CLAUDE_HOME}/agents"

echo "Installing bundle to ${AMPD} ..."
mkdir -p "${AMPD}/skills" "${AMPD}/docs" "${AMPD}/agents"
rsync -a --delete "${REPO}/skills/" "${AMPD}/skills/"
rsync -a --delete "${REPO}/docs/" "${AMPD}/docs/"
rsync -a --delete "${REPO}/agents/" "${AMPD}/agents/"
cp "${REPO}/AGENTS.md" "${AMPD}/AGENTS.md"

install_skill() {
  local name="$1"
  local target="${CLAUDE_HOME}/skills/${name}"
  if [[ "${MODE}" == "symlink" ]]; then
    ln -sfn "${AMPD}/skills/${name}" "${target}"
  else
    mkdir -p "${target}"
    rsync -a --delete "${AMPD}/skills/${name}/" "${target}/"
  fi
}

install_agent() {
  local file="$1"
  local base
  base="$(basename "${file}")"
  local target="${CLAUDE_HOME}/agents/${base}"
  if [[ "${MODE}" == "symlink" ]]; then
    ln -sfn "${file}" "${target}"
  else
    cp "${file}" "${target}"
  fi
}

for skill_dir in "${AMPD}/skills"/*/; do
  install_skill "$(basename "${skill_dir}")"
done

for agent_file in "${AMPD}/agents"/*.md; do
  [[ -f "${agent_file}" ]] || continue
  install_agent "${agent_file}"
done

if [[ "${MODE}" == "symlink" ]]; then
  ln -sfn "${AMPD}/docs" "${CLAUDE_HOME}/docs"
else
  mkdir -p "${CLAUDE_HOME}/docs"
  rsync -a --delete "${AMPD}/docs/" "${CLAUDE_HOME}/docs/"
fi

echo "Done (${MODE} mode)."
echo "  Claude home: ${CLAUDE_HOME}"
echo "  Bundle:      ${AMPD}"
echo "  Skills:      ${CLAUDE_HOME}/skills/"
echo "  Agents:      ${CLAUDE_HOME}/agents/"
echo "  Docs:        ${CLAUDE_HOME}/docs"
echo "Restart Claude Code (or start a new session) to pick up changes."
echo "If this is a non-default home, launch Claude with the same config dir"
echo "  (e.g. CLAUDE_CONFIG_DIR=${CLAUDE_HOME})."
echo "Note: project-local .claude/agents/ in a repo still takes precedence over user agents."
