# ATDD checklist — story readiness (before Distill)

Use after **Discuss**, before automating the first example.

---

## Agreement

- [ ] Capability or story id recorded (ticket, title)
- [ ] Triad perspectives considered (business / dev / quality) — or explicit single-owner decision
- [ ] At least **one** concrete example the business would accept as “this works”
- [ ] Key **data values** named (amounts, roles, states)
- [ ] **Glossary** terms aligned (user vs customer, etc.)
- [ ] **Boundaries** noted (e.g. exactly 10 kg — inclusive or not?)

---

## Example catalog

- [ ] File created at resolved path (project convention **or** `acceptance-examples/<slug>.md`)
- [ ] Filename stem matches branch/feature (kebab-case; see [example-catalog.md](../references/example-catalog.md))
- [ ] File is **tracked** in git
- [ ] **Examples** section lists business-visible cases as `[ ]`
- [ ] **Deferred** / **Removed** sections used when scope is split or dropped
- [ ] No refactor-only lines in **Examples**

---

## Layer choice (pragmatic)

- [ ] Chosen layer for **first** example documented (contract / API / in-process / E2E)
- [ ] Rationale fits [pipeline-fit.md](pipeline-fit.md) and [environments-and-test-pyramid.md](../references/environments-and-test-pyramid.md)
- [ ] Team agrees Gherkin vs code-first vs contract for this repo

---

## Composition

- [ ] Inner TDD test list path planned or created when unit work will start in same slice
- [ ] No overlap: business examples in catalog, programmer cases in test list

---

## Explicit exceptions (if any)

- [ ] Spike / Discuss-only labeled with defer date and owner — **or** N/A
- [ ] Partner contract pending — **or** N/A
