# Bugfix Heuristics

These heuristics help guide safe bug fixing decisions.

They are not absolute rules, but preferred strategies.

---

## Prefer Narrow Scope

Always reduce:

- execution scope
- test scope
- change scope
- reasoning scope

Smaller scopes reduce regression risk.

---

## Prefer Existing Patterns

When fixing bugs:

- follow repository conventions
- reuse existing approaches
- preserve architectural consistency

Avoid introducing:

- new abstractions
- new paradigms
- new patterns

unless strictly required.

---

## Prefer Lowest Useful Test Level

Preferred order:

1. unit
2. integration
3. e2e

Choose the lowest level capable of reproducing the bug reliably.

---

## Prefer Deterministic Reproduction

Good reproduction:

- stable
- isolated
- repeatable

Bad reproduction:

- timing-dependent
- flaky
- environment-sensitive
- manually validated only

---

## Prefer Minimal Behavioral Changes

A bugfix should:

- solve one problem
- preserve unrelated behavior

Avoid:

- side-effect changes
- broad rewrites
- hidden improvements

---

## Prefer Observability Before Guessing

Before modifying code:

- inspect logs
- inspect traces
- inspect runtime state
- inspect failing paths

Do not guess blindly.

---

## Prefer Progressive Validation

Validation order:

1. focused test
2. nearby tests
3. broader tests

Avoid unnecessary full-suite execution early.

---

## Prefer Reversible Changes

Safe fixes should:

- be easy to revert
- be isolated
- minimize blast radius

Avoid:

- multi-system changes
- hidden coupling
- large commits

---

## Prefer Explicit Failure

A failing test is better than:

- silent assumptions
- partial validation
- manual confidence

The system must prove the failure exists.

---

## Prefer Stability Over Elegance

During bugfixing:

- correctness > beauty
- safety > optimization
- isolation > perfection
