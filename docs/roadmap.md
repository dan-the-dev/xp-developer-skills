# Roadmap

This document tracks the current implementation roadmap of AMPD.

The roadmap is intentionally iterative and experimental.

The goal is not to design the perfect framework upfront.

The goal is to progressively validate:

* workflows
* practices
* tooling
* repository structures
* AI-assisted engineering patterns

through real-world experimentation.

⸻

## Current Development Strategy

The current strategy is:

1. Build practical reusable skills first
2. Validate workflows through real projects
3. Iterate on the framework continuously
4. Document only validated learnings
5. Evolve architecture progressively

The first focus area is:
AI-assisted engineering execution.

⸻

## Skill System Roadmap

Skills are reusable operational behaviors designed for AI coding agents such as:

* Cursor
* Claude Code
* Codex
* future AI-native engineering agents

Each skill should:

* be self-contained
* be language agnostic
* encode engineering discipline
* enforce best practices
* optimize for safety and clarity
* remain composable

Skills are not prompts.

They are operational engineering workflows.

⸻

## Product Discovery & Validation

* business-idea-validation
    Validate ideas, identify risks, define and explore hypotheses, identify market signals and propose experiments.
* product-discovery
    Support user research synthesis, JTBD analysis, pain point identification and opportunity mapping.
* experimentation
    Design and validate experiments, MVPs, fake-door tests, smoke tests and A/B testing strategies.

⸻

## Architecture & Documentation

* adr-management
    Create, organize and evolve Architecture Decision Records (ADR) with lifecycle and traceability support.
* architecture-review
    Analyze architectural consistency, modularity, boundaries, coupling/cohesion and fitness functions.
* documentation-context-sync
    Keep technical documentation, architecture notes and repository context aligned and updated.

⸻

## Development Core Skills

* bugfix
    Fix bugs through strict RED → GREEN workflows using failing tests first, minimal fixes and isolated commits.
* tdd
    Apply strict Test-Driven Development using micro-iterations, fast feedback and disciplined commit flows.
* atdd
    Transform acceptance criteria into executable acceptance tests using outside-in development.
* refactoring
    Perform safe incremental refactoring inspired by Martin Fowler’s refactoring methodology.
* add-tests-to-legacy-code (repo implementation: **`skills/legacy-testing/`**)
    Safely introduce characterization tests and protection tests into legacy systems before modifications.
* spike
    Time-boxed technical experiments with explicit promotion to delivery skills (ATDD/TDD/legacy); implementation: **`skills/spike/`** (planned).
* feature-development
    Orchestrate full feature implementation workflows across testing, validation and delivery systems.

⸻

## Delivery & DevOps

* deployments-delivery-automated-pipelines
    Configure and validate deployments and delivery automated pipelines with quality gates.
* ephemeral-environments
    Provision isolated preview environments dynamically for branches, experiments and feature validation.
* feature-flags
    Manage feature rollout strategies, dark launches, kill switches and progressive delivery.

⸻

## Metrics & Observability

* setup-observability
    Configure logs, tracing, metrics, alerting and operational visibility using modern observability practices.
* monitor-observability
    Continuously monitor system health, logs, traces and metrics to proactively detect issues and validate operational quality.
* setup-product-metrics
    Define business KPIs, adoption metrics, funnels and product impact indicators.
* monitor-product-metrics
    Continuously track, monitor and analyze product metrics to validate business impact and surface actionable insights.

⸻

## Agile Process & Team Practices

* agile-planning
    Support incremental planning, scope slicing, risk reduction and iterative delivery strategies.
* retrospective-analysis
    Analyze recurring problems, bottlenecks, regressions and process improvement opportunities.
* engineering-coach
    Act as an AI engineering mentor promoting simplicity, XP values, technical excellence and sustainable delivery.

⸻

## Current Priorities

### Done (skills & docs baseline)

- [x] Initial repository structure
- [x] Initial README
- [x] Bugfix skill (`skills/bugfix/`)
- [x] TDD skill (`skills/tdd/`)
- [x] ATDD skill (`skills/atdd/`)
- [x] Refactoring skill (`skills/refactoring/`)
- [x] Legacy code testing skill (`skills/legacy-testing/`)
- [x] Manifesto (`docs/manifesto.md`)

### Next: Agent harness (ordering: skills → commands → subagents)

Canonical behavior stays in **`skills/*/SKILL.md`**. **Commands** are thin slash entry points that load the right skill. **Subagents** are goal-oriented delegation (isolated context) with short prompts that *route* to the same skills—no duplicate long procedures in agent files.

1. **Skills** — finish the missing workflow package:
   - [ ] **Spike** — add `skills/spike/` (charter, time box, spike report, explicit promotion to `skills/atdd` / `skills/tdd` / `skills/legacy-testing` as appropriate).

2. **Commands** (e.g. Cursor `.cursor/commands/`, mirrored for Claude Code in `.claude/commands/`). One-to-one with existing skills, plus two meta commands:
   - [ ] `/bugfix` → `skills/bugfix/SKILL.md`
   - [ ] `/tdd` → `skills/tdd/SKILL.md`
   - [ ] `/atdd` → `skills/atdd/SKILL.md`
   - [ ] `/refactor` → `skills/refactoring/SKILL.md`
   - [ ] `/legacy` → `skills/legacy-testing/SKILL.md`
   - [ ] `/spike` → `skills/spike/SKILL.md` (after spike skill exists)
   - [ ] `/verify` — skeptical “done” check using `docs/manifesto.md` + repo test commands (no separate skill)
   - [ ] `/plan` — plan-only sequencing: which skills to run next, no implementation unless requested

3. **Subagents** (e.g. `.cursor/agents/`, mirrored `.claude/agents/`). Five goal agents + behavior agreed:
   - [ ] **`new-feature`** — Deliver a production-bound feature: optional preparatory **`skills/refactoring`** if tests are green and structure blocks work; **`skills/legacy-testing`** first if the area is untested; then **`skills/atdd`** when acceptance/examples matter, **`skills/tdd`** for inner implementation; use **`skills/spike`** only for exploration, then **promote** to delivery skills.
   - [ ] **`bugfix`** — Follow **`skills/bugfix`** entirely; subagent value = **isolated context** for heavy repro logs and strict RED→GREEN separation from the parent thread, plus parallel use while parent plans/reviews.
   - [ ] **`legacy-refactor`** — **Phase 1:** `skills/legacy-testing` (harness, characterization). **Phase 2:** `skills/refactoring` (small, green steps). New feature behavior only after an explicit hat/skill switch (e.g. to `tdd` / `atdd`).
   - [ ] **`spike`** — Follow **`skills/spike`** after it exists.
   - [ ] **`pr-reviewer`** — Read-first review (e.g. `readonly: true` where supported): tests, hat discipline, alignment with manifesto and skills.

Optional: root **`AGENTS.md`** as a short index (skills → commands → subagents) once the harness files exist.

⸻

## Future Exploration Areas

Potential future exploration areas:

* AI-native pull request workflows
* autonomous AI DevLoops
* repository-native operational memory
* automated architecture fitness systems
* AI-assisted observability
* AI-assisted product operations
* multi-agent engineering systems
* self-improving engineering pipelines
* AI-assisted code review systems
* AI-assisted delivery governance

These topics remain experimental and intentionally undefined.

They should emerge from validated learnings instead of premature architecture.

⸻

## Important Philosophy

The roadmap itself is expected to evolve continuously.

AMPD follows the same principles it promotes:

* iterative development
* continuous feedback
* experimentation
* incremental improvement
* simplicity first
* validated learning over speculation

The framework should remain:

* lightweight
* adaptable
* practical
* implementation-driven
* deeply connected to real engineering workflows
