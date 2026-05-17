#!/usr/bin/env bash
# Install AMPD skills and subagents for Cursor (all projects).
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
AMPD="${HOME}/.cursor/ampd"
MODE="symlink"

usage() {
  cat <<'EOF'
Usage: install-cursor.sh [--copy]

  Installs AMPD to ~/.cursor/ampd and wires Cursor auto-discovery paths.

  --copy   Copy into ~/.cursor/skills and ~/.cursor/agents instead of symlinks
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --copy) MODE="copy"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
  esac
done

for dir in skills docs agents; do
  if [[ ! -d "${REPO}/${dir}" ]]; then
    echo "Missing ${REPO}/${dir}" >&2
    exit 1
  fi
done

mkdir -p "${AMPD}" "${HOME}/.cursor/skills" "${HOME}/.cursor/agents"

echo "Installing bundle to ${AMPD} ..."
mkdir -p "${AMPD}/skills" "${AMPD}/docs" "${AMPD}/agents"
rsync -a --delete "${REPO}/skills/" "${AMPD}/skills/"
rsync -a --delete "${REPO}/docs/" "${AMPD}/docs/"
rsync -a --delete "${REPO}/agents/" "${AMPD}/agents/"
cp "${REPO}/AGENTS.md" "${AMPD}/AGENTS.md"

install_skill() {
  local name="$1"
  local target="${HOME}/.cursor/skills/${name}"
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
  local target="${HOME}/.cursor/agents/${base}"
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
  ln -sfn "${AMPD}/docs" "${HOME}/.cursor/docs"
else
  mkdir -p "${HOME}/.cursor/docs"
  rsync -a --delete "${AMPD}/docs/" "${HOME}/.cursor/docs/"
fi

echo "Done (${MODE} mode)."
echo "  Bundle:    ${AMPD}"
echo "  Skills:    ${HOME}/.cursor/skills/"
echo "  Agents:    ${HOME}/.cursor/agents/"
echo "  Docs:      ${HOME}/.cursor/docs"
echo "Restart Cursor to pick up changes."
