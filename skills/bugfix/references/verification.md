# Verification Strategy

Verification must be incremental, deterministic, and risk-aware.

Shared rules: [`docs/delivery-process.md`](../../../docs/delivery-process.md) §2 and [`docs/project-verification.md`](../../../docs/project-verification.md).

---

## During the fix (every edit)

After **each** meaningful change (repro test, production fix, assertion tweak):

1. Re-run the **narrowest applicable tests** — at minimum the failing repro test.
2. Do not stack edits on a broken baseline.

---

## Validation Pyramid

Preferred validation order:

1. focused failing test
2. nearby tests
3. module/package tests
4. service/application tests
5. full suite only if justified

At **bugfix boundary**, run the **full applicable project verify set** — not only tests.

---

## Focused Validation First

Always begin with:

- the failing test
- the smallest useful scope

Goal:

- fast feedback
- fast iteration
- reduced noise

---

## Related Regression Validation

After GREEN:

- identify nearby behaviors
- validate likely regression zones

Examples:

- adjacent condition branches
- related serializers
- similar API endpoints

---

## Lint, format, typecheck, and code quality

When the project defines these gates:

- run them as part of the applicable verify set **before claiming done**
- fix **new** violations you introduced
- if **SonarQube**, **SonarCloud**, or similar is configured, ensure your change introduces **no new** issues at or above the project quality gate

Do not suppress rules to force green unless the user explicitly approves.

---

## Full Suite Execution

Run broader suites when:

- shared infrastructure changed
- cross-module behavior affected
- repository conventions require it at bugfix boundary

Avoid unnecessary expensive runs **during** micro-edits; run the **full applicable set** at the bugfix boundary.

---

## Deterministic Validation

Validation must be:

- repeatable
- stable
- environment-independent

Avoid relying on:

- timing
- randomness
- external unstable systems

---

## Flaky Tests

If tests are flaky:

- STOP
- document instability
- isolate failure source

Never trust unstable validation.

---

## Runtime Validation

When relevant:

- inspect logs
- inspect telemetry
- inspect traces
- inspect metrics

Validation is not limited to tests.

---

## Validation Completion Criteria

Verification is complete only when:

- failing behavior reproduced
- failing behavior resolved
- related regressions checked
- **all applicable project verify steps** passed (tests, lint, format, typecheck, Sonar/static analysis when configured)
- no **new** lint/sonar/quality violations attributable to your change
- no unexpected failures remain
