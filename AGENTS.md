# AMPD — agent orientation

**Source of truth:** `skills/*/SKILL.md`. Subagents are thin routers with isolated context.

## Subagents

Location: **`agents/`** (symlinked at **`.claude/agents/`** for Claude Code in this repo). After [install](INSTALL.md): Cursor → **`~/.cursor/agents/`**; Claude Code (global) → **`~/.claude/agents/`**. Invoke with `/name` or natural mention.

| Subagent | Skill(s) |
|----------|----------|
| `new-feature` | `skills/new-feature/` — slice epic into `increments/<stem>.md`; **plan + orchestrate**; confirms the plan before executing; hand off to `new-increment`, then `increment-review`; **step** (default) or **automatic** (explicit); can open the feature PR from the increments' mini-journals |
| `new-increment` | `skills/new-increment/` → `skills/tdd` per slice (ATDD only at outer seam); **one** increment per invocation; verify green; commit **squashed to one**; return a mini-journal; stop |
| `increment-review` | `skills/increment-review/` — fast, single-pass review (target <60s) of one increment, per `docs/code-review.md`; default reviewer `new-feature` calls, not `refactoring` |
| `refactoring` | `skills/refactoring/` — dedicated tidy-up, or executing an `increment-review` fix brief (not for untested code); legacy manual post-increment review on direct request |
| `tweak` | `skills/tweak/` — small, direct follow-up edit on the current branch; no branch/backlog/PR ceremony |
| `bugfix` | `skills/bugfix/` |
| `legacy-refactor` | `skills/legacy-testing/` then `skills/refactoring/` — harness first on unprotected code, then structure |
| `spike` | `skills/spike/` (`spike/` branch, disposable) |
| `pr-reviewer` | `docs/manifesto.md` + applicable skills (`readonly`) |
| `montecarlo-simulator` | routes to `skills/montecarlo-single-item/`, `skills/montecarlo-epic/` or `skills/montecarlo-epics/` — flow-based probabilistic forecasting; never computes by itself |

## Skills (delivery)

`bugfix`, `tdd`, `atdd`, `refactoring`, `legacy-testing`, `spike`, `new-feature`, `new-increment`, `increment-review`, `tweak` — under `skills/`.

## Skills (forecasting)

`montecarlo-single-item`, `montecarlo-epic`, `montecarlo-epics` — under `skills/`; shared script **`tools/montecarlo/montecarlo.py`** (no network, normalized CSV/JSON only), shared rules in [`docs/montecarlo-forecasting.md`](docs/montecarlo-forecasting.md). See [`tools/montecarlo/README.md`](tools/montecarlo/README.md).

## Docs

- [`docs/manifesto.md`](docs/manifesto.md)
- [`docs/code-review.md`](docs/code-review.md) — checklist `increment-review` (and `pr-reviewer`) apply
- [`docs/delivery-process.md`](docs/delivery-process.md) — shared delivery rules (verification, roles, **feature branch §1a**, return payload)
- [`docs/project-verification.md`](docs/project-verification.md) — scoped checks during work; full gates after every code-touching slice
- [`docs/test-strategy-selection.md`](docs/test-strategy-selection.md) — which test layers and techniques to adopt per slice (mutation, contract, property-based, owned vendor clients §3a, etc.)
- [`docs/simple-design.md`](docs/simple-design.md) — Simple Design + YAGNI; **mandatory** Object Calisthenics; patterns as emerged destinations
- [`docs/design-quality.md`](docs/design-quality.md) — agent playbook (smell → move → pattern)
- [`docs/roadmap.md`](docs/roadmap.md)
- [`docs/montecarlo-forecasting.md`](docs/montecarlo-forecasting.md) — data collection and communication rules for the Monte Carlo forecasting skills

## Install

See **[INSTALL.md](INSTALL.md)** for global setup — Cursor (`~/.cursor/ampd`) and/or Claude Code (`<claude-home>/ampd`, default `~/.claude`; use `--home` for e.g. `~/.claude-personal`) + auto-discovery.
