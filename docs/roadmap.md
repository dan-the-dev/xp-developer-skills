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
    Time-boxed experiments on isolated `spike/` branches; disposable code; promotion to ATDD/TDD/legacy. Implementation: **`skills/spike/`**.
* new-feature (implemented — **`skills/new-feature/`**)
    Slice a **whole capability** into ordered, **releasable increments** (e.g. increment backlog in repo); delegate each slice to **new-increment**. Does not implement every increment in one pass.
* new-increment (implemented — **`skills/new-increment/`**)
    Deliver **one** increment per invocation: **`skills/tdd`** by default (one feature test list); **`skills/atdd`** only at a real outer seam; RED gates; minimal markdown.
* feature-development
    Umbrella for delivery orchestration; in practice **new-feature** + **new-increment** (when implemented).

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

* [x] Initial repository structure
* [x] Initial README
* [x] Bugfix skill (`skills/bugfix/`)
* [x] TDD skill (`skills/tdd/`)
* [x] ATDD skill (`skills/atdd/`)
* [x] Refactoring skill (`skills/refactoring/`)
* [x] Legacy code testing skill (`skills/legacy-testing/`)
* [x] Spike skill (`skills/spike/`)
* [x] New feature skill (`skills/new-feature/`)
* [x] New increment skill (`skills/new-increment/`)
* [x] Manifesto (`docs/manifesto.md`)

### Agent harness (skills → subagents)

Canonical behavior stays in **`skills/*/SKILL.md`**. **Slash commands are out of scope** for now—skills are sufficient for agents to load the right workflow. **Subagents** are goal-oriented delegation (isolated context) with short prompts that **read and follow** the relevant `SKILL.md` files—no duplicate long procedures in agent files.

1. **Skills** — core delivery, spike, and increment orchestration in place; see [Development Core Skills](#development-core-skills) for further backlog.

2. **Subagents** — implemented in **`agents/`** (symlinked at **`.claude/agents/`**; Cursor global install via **`INSTALL.md`**). Index: **`AGENTS.md`**.

   * [x] **`new-feature`** — `new-feature.md` → **`skills/new-feature`** (step default; automatic mode explicit; post-increment review via `refactoring`)
   * [x] **`new-increment`** — `new-increment.md` → **`skills/new-increment`** (TDD default; ATDD at outer seam only; green gate + commit + stop)
   * [x] **`refactoring`** — `refactoring.md` → **`skills/refactoring`** (dedicated tidy-up or post-increment review)
   * [x] **`bugfix`** — `bugfix.md` → **`skills/bugfix`**
   * [x] **`legacy-refactor`** — `legacy-refactor.md` → legacy-testing, then refactoring
   * [x] **`spike`** — `spike.md` → **`skills/spike`**
   * [x] **`pr-reviewer`** — `pr-reviewer.md` (`readonly: true`) → manifesto + skills

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
