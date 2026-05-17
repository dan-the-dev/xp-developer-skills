# Amplified XP & Product Development

**An AI-native framework for software product development.**

Bringing Extreme Programming, Product Thinking, DevOps, Lean and AI Agents together into a single development operating system.

Experimental framework • Open evolution — see **[docs/manifesto.md](docs/manifesto.md)** for a brief statement of intent.

---

## 🚀 About

> What happens when you take Extreme Programming seriously in the age of AI?

Amplified XP & Product Development (AMPD) is an experimental framework exploring how modern AI agents can amplify — not replace — the best practices of software engineering and product development.

This project is heavily inspired by:

- Extreme Programming (Kent Beck)
- Continuous Delivery (Dave Farley)
- Refactoring (Martin Fowler)
- Lean Product Development
- Team Topologies
- DevOps & Platform Engineering
- Modern AI-assisted software development

The core idea is simple:

> AI should amplify good engineering practices, not bypass them.

---

## 🧠 The Vision

Modern AI coding tools are incredibly powerful.

But most current workflows:

- ignore software engineering discipline
- bypass testing
- generate unmaintainable systems
- create fragile architectures
- optimize for speed instead of sustainability

AMPD explores a different direction.

Instead of:
> "AI writes code for humans"

we explore:
> "AI participates inside rigorous engineering systems."

---

## ⚡ Current Scope

This repository currently contains the first foundational building block of the framework:

## AI Development Skills

Structured AI-native engineering skills for tools like:

- Claude Code
- Cursor
- Codex
- OpenCode
- future AI coding agents

Implemented skills live under `skills/` (one package per skill) so each workflow can grow or be shared in isolation.

Implemented skills include:

```text
skills/bugfix/
skills/tdd/
skills/atdd/
skills/refactoring/
skills/legacy-testing/
skills/spike/
skills/new-feature/
skills/new-increment/
```

**Bugfix** — a strict bugfix workflow enforcing:

- RED → GREEN discipline
- minimal fixes
- isolated commits
- deterministic reproduction
- review-friendly git history
- no uncontrolled refactoring

**TDD** — strict RED → GREEN → REFACTOR with micro-commits (`test:` / `feat:` / `refactor:`), fast narrow test runs, and squash-to-one-commit before push (see `skills/tdd/SKILL.md`).

**ATDD** — pragmatic Discuss → Distill → Develop: agree examples in an example catalog, automate at the right layer (contract, API, or E2E; Gherkin optional), then implement outside-in while composing with inner TDD (see `skills/atdd/SKILL.md`).

**Refactoring** — Fowler-style behavior-preserving changes: two hats, baby steps, green between steps, revert on red, named refactorings and clear commits (see `skills/refactoring/SKILL.md`).

**Legacy testing** — Feathers-style work on code without tests: change algorithm (pinch points, seams, characterization, sprout/wrap), then compose with TDD, refactoring, or bugfix (see `skills/legacy-testing/SKILL.md`).

**Spike** — time-boxed experiments on an isolated `spike/` branch: disposable code, prove an idea or library fit, optional ad hoc checks only; explicit promotion to ATDD/TDD/legacy (see `skills/spike/SKILL.md`).

**New feature** — slice a whole capability into ordered increments (`increments/<stem>.md`); e.g. FizzBuzz as one feature with separate increments per rule (see `skills/new-feature/SKILL.md`).

**New increment** — deliver one increment with full ATDD + TDD for that slice only (see `skills/new-increment/SKILL.md`).

### Subagents

Goal-oriented agents in **`.claude/agents/`**: `new-feature`, `new-increment`, `bugfix`, `legacy-refactor`, `spike`, `pr-reviewer`. Each reads the matching **`skills/*/SKILL.md`**. See **`AGENTS.md`**.

---

## 🏗️ Repository Philosophy

AMPD treats AI skills as:
> executable engineering systems

not:
> prompt snippets.

Example structure:

```text
skills/
├── bugfix/
│   ├── SKILL.md
│   ├── references/
│   ├── examples/
│   └── checklists/
├── tdd/
│   ├── SKILL.md
│   ├── references/
│   ├── examples/
│   └── checklists/
├── atdd/
│   ├── SKILL.md
│   ├── references/
│   ├── examples/
│   └── checklists/
├── refactoring/
│   ├── SKILL.md
│   ├── references/
│   ├── examples/
│   └── checklists/
├── legacy-testing/
│   ├── SKILL.md
│   ├── references/
│   ├── examples/
│   └── checklists/
└── spike/
    ├── SKILL.md
    ├── references/
    ├── examples/
    └── checklists/
```

---

## 🔥 Core Principles

## 1. AI amplifies systems

AI does not replace engineering discipline.

Good systems become better.
Bad systems become chaos faster.

---

## 2. Code should explain HOW

Documentation should explain:

- WHY
- tradeoffs
- decisions
- constraints
- business intent

---

## 3. Every change must be verifiable

Every modification should be:

- testable
- reproducible
- reviewable
- incremental
- observable

---

## 4. AI agents need constraints

The future is:
> constrained AI systems operating inside engineering guardrails.

---

## 🧪 Long-Term Direction

Future iterations of the framework will include:

- AI-native product discovery
- AI-assisted experimentation
- autonomous development loops
- ephemeral preview environments
- architecture governance
- AI-assisted observability
- metrics-driven validation

---

## 📚 Planned Framework Sections

- Product Discovery
- Idea Validation
- Experimentation
- Product Strategy
- User Story Design
- AI Development Loops
- TDD & ATDD
- Refactoring Systems
- CI/CD
- Ephemeral Environments
- Feature Flags
- Architecture Governance
- Observability
- Metrics & Product Analytics

---

## 👋 Who Created This?

AMPD is created by a software product builder exploring how AI can evolve modern software engineering without abandoning the principles that made great software possible in the first place.

The goal is not to present a finished methodology, but to:

- experiment
- validate
- refine
- challenge assumptions
- share learnings openly

My name is Daniele Scillia, also known as “Dan the Dev”, and I'm an Agile Software Developer, Technical Leader and Coach focused on helping teams achieve Technical Excellence through modern software engineering practices. I actively advocates every day for Agile, Extreme Programming (XP), Lean and DevOps as practical systems for building better products and healthier engineering organizations. AMPD is part of his ongoing exploration of how AI can amplify—not replace—the principles behind sustainable software development.

[Learn more about Daniele Scillia (“Dan the Dev”)](https://danthedev.carrd.co/)

---

## 🛠️ Current Status

Current focus:

1. defining skill architecture
2. implementing foundational engineering skills
3. validating workflows on real projects
4. iterating toward a complete AI-native product development framework

---

## 🤝 Contributing

Contributions, critiques, ideas and discussions are welcome.

Especially around:

- XP
- TDD
- ATDD
- DevOps
- AI-assisted engineering
- architecture governance
- product development systems

---

## 🧭 Complete Roadmap

### 🧠 Product Discovery & Validation

- [ ] `business-idea-validation`  
  Validate ideas, identify risks, define and explore hypotheses, identify market signals and propose experiments.

- [ ] `product-discovery`  
  Support user research synthesis, JTBD analysis, pain point identification and opportunity mapping.

- [ ] `experimentation`  
  Design and validate experiments, MVPs, fake-door tests, smoke tests and A/B testing strategies.

---

### 🏗️ Architecture & Documentation

- [ ] `adr-management`  
  Create, organize and evolve Architecture Decision Records (ADR) with lifecycle and traceability support.

- [ ] `architecture-review`  
  Analyze architectural consistency, modularity, boundaries, coupling/cohesion and fitness functions.

- [ ] `documentation-context-sync`  
  Keep technical documentation, architecture notes and repository context aligned and updated.

---

### 🧪 Development Core Skills

- [x] `bugfix`  
  Fix bugs through strict RED → GREEN workflows using failing tests first, minimal fixes and isolated commits.

- [x] `tdd` (first draft)  
  Apply strict Test-Driven Development using micro-iterations, fast feedback and disciplined commit flows.

- [ ] `atdd`  
  Transform acceptance criteria into executable acceptance tests using outside-in development.

- [ ] `refactoring`  
  Perform safe incremental refactoring inspired by Martin Fowler’s refactoring methodology.

- [ ] `add-tests-to-legacy-code`  
  Safely introduce characterization tests, protection tests and others "outside" tests into legacy systems before modifications.

- [ ] `feature-development`  
  Orchestrate full feature implementation workflows across testing, validation and delivery systems.

---

### 🚀 Delivery & DevOps

- [ ] `deployments-delivery-automated-pipelines`  
  Configure and validate deployments and delivery automated pipelines with quality gates.

- [ ] `ephemeral-environments`  
  Provision isolated preview environments dynamically for branches, experiments and feature validation.

- [ ] `feature-flags`  
  Manage feature rollout strategies, dark launches, kill switches and progressive delivery.

---

### 📊 Metrics & Observability

- [ ] `setup-observability`  
  Configure logs, tracing, metrics, alerting and operational visibility using modern observability practices.

- [ ] `monitor-observability`  
  Continuously monitor system health, logs, traces, and metrics to proactively detect issues and validate operational quality.

- [ ] `setup-product-metrics`  
  Define business KPIs, adoption metrics, funnels and product impact indicators.

- [ ] `monitor-product-metrics`  
  Continuously track, monitor, and analyze product metrics to ensure ongoing business impact and surface actionable insights.

---

### 🧭 Agile Process & Team Practices

- [ ] `agile-planning`  
  Support incremental planning, scope slicing, risk reduction and iterative delivery strategies.

- [ ] `retrospective-analysis`  
  Analyze recurring problems, bottlenecks, regressions and team/process improvement opportunities.

- [ ] `engineering-coach`  
  Act as an AI engineering mentor promoting simplicity, XP values, technical excellence and sustainable delivery.

---

## 🧭 Next Priorities

- [x] Initial skill architecture
- [x] Bugfix skill
- [ ] Refactoring skill
- [ ] TDD skill
- [ ] Legacy code testing skill
- [ ] AI DevLoop draft
- [ ] Manifesto website

---

## 📜 License

TBD
