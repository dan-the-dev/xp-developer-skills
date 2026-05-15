# ATDD anti-patterns

Symptoms to avoid when applying pragmatic ATDD.

---

## Discuss

- **No examples** — coding from a one-line story (“build checkout”).
- **Abstract acceptance criteria** — “must be secure” without instances.
- **Catalog only in chat** — not versioned in repo.
- **Analysis paralysis** — dozens of examples before first Distill.

---

## Distill

- **Automation before agreement** — green test for the wrong rule.
- **Wrong layer** — full browser for pure calculation; unit test labeled “acceptance.”
- **Big-bang suite** — ten failing scenarios before any green path.
- **False RED** — failure from env, typo, or flake mistaken for missing feature.
- **Gherkin theater** — steps that only wrap Playwright one-liners with no domain language.

---

## Develop

- **Skipping inner TDD** — all logic stuffed into slow acceptance setup.
- **Duplicated assertions** — same business rule asserted in acceptance + many unit tests with no new signal.
- **Production before acceptance RED** (pragmatic default) — shipping code without any failing check for the agreed example when automation was feasible.
- **Ignoring red acceptance** — merging while outer loop is red “we’ll fix later.”

---

## Gherkin / specs

- **UI scripts** as scenarios (clicks and div ids, no outcome).
- **Implementation in steps** — Then step that asserts internal DB column the business never named.
- **Long scenarios** — 20 steps; split or raise abstraction.
- **Duplicate sources** — catalog and feature files diverge with no links.

---

## Catalog hygiene

- `[x]` without automation reference.
- Refactor lines in **Examples**.
- Silent removal without **Removed** section.
- **Deferred** rows with no owner/date at slice end.

---

## Organizational

- **Acceptance as only regression** — no unit tests; slow death.
- **Manual regression** replacing automated acceptance for releases (pragmatic teams automate repeatable checks).
- **Flaky suite ignored** — team disables job or retries until green without fixing root cause.

---

## Composition

- Using **bugfix** skill for new features (wrong workflow).
- Using **TDD test list** for business examples (wrong audience) — use example catalog + compose TDD for units.
