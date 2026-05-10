# Verification Strategy

Verification must be incremental, deterministic, and risk-aware.

---

## Validation Pyramid

Preferred validation order:

1. focused failing test
2. nearby tests
3. module/package tests
4. service/application tests
5. full suite only if justified

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

## Full Suite Execution

Run broader suites only when:

- shared infrastructure changed
- cross-module behavior affected
- repository conventions require it

Avoid unnecessary expensive runs.

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
- no unexpected failures remain
