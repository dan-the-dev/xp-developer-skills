# Language-Agnostic Testing

This skill must adapt to repository-native tooling.

Never assume:

- language
- framework
- package manager
- test runner

Always inspect the repository first.

---

## Repository Discovery

Before executing commands:

- inspect package/configuration files
- inspect CI pipelines
- inspect existing tests
- inspect repository scripts

Examples:

- package.json
- pyproject.toml
- Cargo.toml
- pom.xml
- go.mod
- Makefile

---

## Preferred Strategy

Reuse:

- existing test commands
- repository conventions
- repository tooling

Do not invent new workflows.

---

## Common Ecosystem Examples

### JavaScript / TypeScript

Potential tools:

- npm
- pnpm
- yarn
- jest
- vitest
- playwright
- cypress

---

### Python

Potential tools:

- pytest
- unittest
- tox
- poetry

---

### Go

Potential tools:

- go test

---

### Java

Potential tools:

- junit
- maven
- gradle

---

### Ruby

Potential tools:

- rspec
- minitest

---

### Rust

Potential tools:

- cargo test

---

## Test Placement

Prefer existing conventions.

Examples:

- colocated tests
- dedicated tests directories
- package-level structures

Follow repository patterns.

---

## Command Discovery

Preferred order:

1. repository scripts
2. CI configuration
3. existing documentation
4. framework defaults

---

## Unknown Tooling

If tooling is unclear:

- inspect existing commands
- inspect CI pipelines
- inspect developer docs

Do not guess blindly.

---

## Goal

The skill must behave consistently across ecosystems while respecting local repository conventions.
