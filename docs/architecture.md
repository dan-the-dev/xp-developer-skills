# Architecture

This document describes the conceptual architecture of AMPD.

It does NOT describe the architecture of a software product.

It describes:

* how the framework is structured
* how operational context is organized
* how skills interact with documentation
* how AI-assisted workflows are expected to operate

The architecture is intentionally lightweight and iterative.

It is expected to evolve continuously through experimentation.

⸻

## High-Level Structure

AMPD is built around two core concepts:

1. Shared operational context
2. Executable engineering workflows

This is reflected directly in the repository structure:

docs/ explains the system
skills/ execute the system

The documentation layer provides:

* philosophy
* architecture
* workflows
* principles
* roadmap
* operational understanding

The skill layer provides:

* executable engineering behaviors
* structured workflows
* operational constraints
* repeatable AI execution patterns

Together, they form a repository-native AI engineering system.

⸻

## Repository-Native Context

AMPD treats the repository itself as the primary operational context for AI agents.

The repository is not only source code.

It also contains:

* architectural knowledge
* workflow definitions
* engineering principles
* operational standards
* implementation guidance
* historical decisions

This approach follows a simple principle:

AI systems perform better when context lives close to execution.

⸻

## Documentation Architecture

The documentation layer is intentionally lightweight.

AMPD avoids:

* massive centralized documentation
* process-heavy documentation systems
* duplicated implementation details
* documentation disconnected from execution

The framework instead favors:

* small focused documents
* layered context
* modular knowledge
* progressive refinement
* operational clarity

Each document should have:

* a single responsibility
* high signal density
* low maintenance overhead

⸻

## Skill Architecture

Skills are the operational core of AMPD.

A skill is:
a reusable executable engineering workflow for AI agents.

Skills are designed to:

* standardize behavior
* encode engineering discipline
* reduce unsafe execution
* improve consistency
* create repeatable workflows

Skills are intentionally:

* language agnostic
* implementation-oriented
* composable
* repository-native

Each skill should remain self-contained.

A skill owns:

* its workflow
* its constraints
* its examples
* its references
* its operational philosophy

The documentation layer may reference skills conceptually, but should not duplicate them.

⸻

## Skill Structure

Current skill structure:

skills/
└── skill-name/
├── skill.md
├── examples/
├── references/
└── checklists/

The goal is to separate:

* operational instructions
* practical examples
* conceptual references
* execution validation

This improves:

* maintainability
* readability
* AI context loading
* progressive learning

⸻

## AI Operational Model

AMPD assumes AI agents operate through constrained workflows.

The framework favors:

* explicit instructions
* small iterations
* continuous validation
* deterministic workflows
* test-driven execution

The architecture intentionally discourages:

* uncontrolled generation
* large unsafe modifications
* architecture drift
* context-free execution

AI systems should work inside engineered feedback loops.

⸻

## The AI DevLoop

One of the central concepts of AMPD is the AI DevLoop.

The long-term vision is a development loop where an AI agent can:

1. Receive a story, task or experiment
2. Load repository context
3. Understand architecture and constraints
4. Generate acceptance tests
5. Execute ATDD and TDD workflows
6. Develop incrementally
7. Continuously validate through tests
8. Refactor safely
9. Deploy to ephemeral environments
10. Configure feature flags
11. Expose observability and metrics
12. Prepare delivery artifacts
13. Generate product feedback loops

The framework does not assume this is fully autonomous today.

AMPD currently focuses on:
semi-autonomous operational workflows.

⸻

## Feedback-Driven Architecture

AMPD is heavily feedback-oriented.

The architecture revolves around continuous feedback loops:

* testing feedback
* product feedback
* observability feedback
* delivery feedback
* experimentation feedback
* architectural feedback

The framework assumes:
fast feedback reduces risk.

AI systems amplify the speed of these loops.

⸻

## Evolutionary Architecture

AMPD intentionally avoids rigid upfront architecture.

The framework itself should evolve through:

* experimentation
* iterative implementation
* validated learnings
* operational experience
* tooling discoveries

The architecture is expected to change continuously.

Stability should emerge from:

* strong principles
* repeatable workflows
* feedback systems

not from rigid documentation.

⸻

## Long-Term Direction

Future evolutions may include:

* autonomous AI execution loops
* repository-native memory systems
* architecture fitness automation
* AI-assisted observability
* multi-agent workflows
* AI-native CI/CD systems
* persistent operational context systems
* product analytics integration
* automated delivery orchestration

These concepts remain exploratory.

AMPD strongly prefers:
validated evolution over speculative architecture.

⸻

## Architectural Philosophy

The framework optimizes for:

* simplicity
* adaptability
* operational clarity
* safe iteration
* engineering discipline
* continuous learning

AMPD is not trying to automate software engineering away.

It is trying to build systems where AI amplifies the best engineering and product development practices we already know.
