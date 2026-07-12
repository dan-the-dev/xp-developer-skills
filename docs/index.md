# AMPD Documentation Index

Welcome to the internal documentation space of AMPD — Amplified XP & Product Development.

This directory contains the evolving context, vision, principles and architectural thinking behind the framework.

AMPD is an experimental AI-native approach to software product development inspired by:

* Extreme Programming (XP)
* Lean Software Development
* Agile Product Development
* DevOps
* Continuous Delivery
* AI-assisted engineering workflows

The goal is not to replace engineering discipline with AI.

The goal is to amplify proven engineering practices through AI systems.

⸻

## Reading Order

Suggested reading order for humans and AI agents:

1. vision.md
    Understand why AMPD exists and the problems it tries to solve.
2. principles.md
    Learn the values, principles and engineering philosophy behind the framework.
3. architecture.md
    Understand how the framework is structured conceptually.
4. roadmap.md
    Explore the current implementation roadmap and planned skills.
5. delivery-process.md
    Shared delivery rules — verification, roles, RED→GREEN, return payload.
6. project-verification.md
    Tests, lint, format, SonarQube, and all project gates after every code change.
7. test-strategy-selection.md
    Which test layers and techniques to adopt per slice (mutation, contract, property-based, integration, etc.).
8. technical-excellence-catalog.md
    Inventory of verifiable practices AMPD aims to enable and amplify (pipeline stages, test families, AMPD status).

⸻

## Repository Philosophy

This repository follows a simple rule:

docs/ explains the system
skills/ execute the system

The documentation should remain:

* lightweight
* practical
* modular
* evolving
* easy to maintain
* useful for both humans and AI agents

The goal is not perfect documentation.

The goal is shared operational context.

⸻

## Skill bibliography

Human-maintained citations for framework skills (for example the TDD skill) live in the docs folder, for example [tdd-skill-bibliography.md](tdd-skill-bibliography.md). Skill bodies under `skills/` avoid book titles; they may still name standard rules (e.g. the Three Laws) where those are part of the workflow.

⸻

## Current Status

Current implementation phase:

* Initial framework definition
* Skill system exploration
* AI-assisted engineering workflows validation
* Documentation architecture bootstrap

Implemented:

* Initial repository structure
* README
* Skills: `bugfix`, `tdd` (first draft under `skills/tdd/`)

Next priorities:

* Refactoring skill
* Evolve TDD skill from draft feedback
* Legacy testing skill
* AI DevLoop draft
* Manifesto website

⸻

## Important Notes

This documentation is intentionally incomplete.

AMPD is designed to evolve through:

* experimentation
* real projects
* iterative refinement
* validated practices
* operational learnings

Many concepts documented here are hypotheses under active validation.

The framework should always remain:

* practical
* adaptable
* implementation-driven
* grounded in real engineering workflows
