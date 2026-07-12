# Test strategy selection (shared)

Pragmatic rules for choosing **which automated practices** to use on a slice — from the [technical excellence catalog](technical-excellence-catalog.md) — without defaulting to **unit TDD only** when another layer or technique proves the risk better.

Compose with [delivery-process.md](delivery-process.md) §4 (one layer per concern) and §10 (return payload).

**Principle:** Use the **lowest sufficient** layer, but **actively consider** higher layers and specialized techniques when they add evidence unit tests cannot. **Do not** adopt a practice because it is in the catalog — adopt it when the slice warrants it.

---

## 1. Mandatory decision (before first RED)

Before the first failing check for a slice (increment, bugfix, harness, or refactor session with new tests):

1. **Discover** what the project already configures — CI jobs, scripts, config files (see [project-verification.md](project-verification.md) §2).
2. **Characterize the slice** — what are you changing and what could break silently?
3. **Select practices** using §3 below — mark each as **adopt**, **already covered by project gate**, or **skip** with a one-line reason.
4. **Record** the decision in the session (chat) and in the **return payload** §6.

If you default to unit TDD only, you must **explicitly state** which catalog practices you considered and why they were skipped.

---

## 2. Slice characterization (quick)

| Slice looks like… | Usually start with | Also consider |
|-----------------|-------------------|---------------|
| Pure domain logic, kata, in-process module | Unit TDD | Property-based (invariants); mutation (branchy/critical) |
| Algorithm, parser, serializer, pricing rules | Unit TDD | Property-based; table-driven examples |
| HTTP/API/CLI contract | ATDD + TDD at boundary | Contract/schema; API acceptance; not duplicate unit |
| Service boundary with consumers | Contract tests | Provider verify job; inner TDD |
| DB, broker, or ORM wiring | Narrow integration | Testcontainers if project uses it; not mock-only if SQL is the risk |
| UI component behavior | Component tests | a11y (axe); avoid full E2E per field |
| User journey / only visible in browser | One thin E2E | Component tests for branches; smoke after deploy |
| Legacy, untested | Characterization | Harness first (`skills/legacy-testing`); then bugfix/TDD |
| Bug in branchy/critical logic | Repro test (bugfix) | Mutation if project has it — validates test strength |
| External vendor API | Contract/fixture tests | HTTP mocking (MSW, VCR); sandbox job if configured |
| Deploy / wiring / env config | Smoke after deploy | Integration in acceptance stage |
| Performance or feasibility unknown | **`skills/spike`** first | Load/benchmark only after spike promotes |

---

## 3. Practice selection reference

**Family:** `Isolated` = commit-stage friendly; `Interactive` = needs deploy/browser/external (acceptance stage).

| Practice | Use when | Skip when | Examples |
|----------|----------|-----------|----------|
| **Unit TDD** | Default inner loop; fast feedback on behavior | Same assertion duplicated at acceptance layer | JUnit, pytest, Vitest |
| **Narrow in-process integration** | Real SQL, migrations, repository, or module wiring is the risk | Logic is pure; DB is fully faked and stable | Testcontainers, `@DataJpaTest`, test DB |
| **Component / UI (isolated)** | Component renders/interacts; no full app deploy needed | No UI in slice; E2E already covers journey | Testing Library, Vitest + RTL |
| **API / HTTP acceptance** | Business outcome provable via HTTP without browser | In-process module seam is cheaper and sufficient | supertest, httpx, REST-assured |
| **In-process acceptance** | Clear module boundary inside one deployable | Would duplicate unit assertions | Acceptance test package |
| **Contract / schema** | Published API or event promise to another team/system | Single deployable, no consumer | Pact, OpenAPI examples, buf, JSON Schema |
| **Characterization** | Legacy behavior must be pinned before change | Greenfield with agreed examples | ApprovalTests, golden files |
| **Property-based** | Invariants over many inputs; round-trip; algebraic laws | Few fixed examples fully specify behavior | fast-check, Hypothesis, jqwik |
| **Mutation testing** | Branchy/critical logic; weak tests suspected; **project already runs mutation**; after bugfix on complex rules | Trivial CRUD; first slice before tests stabilize; not configured and setup > slice value | Stryker, PIT, cargo-mutants |
| **Snapshot / approval** | Stable structured output (JSON, HTML fragment) | Behavior better expressed as explicit assertions | Jest snapshots, ApprovalTests |
| **Accessibility (automated)** | UI component or page in slice; a11y is acceptance criterion | No UI; project has no a11y tooling | axe-core, pa11y, Storybook a11y |
| **Smoke (deploy)** | Slice touches deploy path, health, or env wiring | No deployable change | curl health, `@smoke` tag |
| **E2E / browser journey** | Capability **only** visible through full stack + browser | API or component layer can prove it | Playwright, Cypress |
| **HTTP mocking / fixtures** | External API must not be live in commit stage | Real sandbox is project standard and fast enough | MSW, WireMock, VCR |
| **Visual regression** | Design-system or layout stability is the risk | Logic-only change | Chromatic, Playwright screenshots |
| **Load / benchmark** | Performance is the acceptance criterion | Normal feature slice; use spike first | k6, criterion |

### Mutation testing (explicit)

Mutation tests are **optional but must be considered** when:

- The project defines a mutation job or config (`stryker.conf`, `pitest`, `cargo-mutants`, CI `mutation` job).
- The slice adds or fixes **branch-heavy** logic (pricing, auth rules, validation matrices, state machines).
- A bugfix passed unit tests but confidence in **test strength** is low.

**Action when adopted:** run the project’s mutation command (or scoped run on touched files); fix **surviving mutants** by strengthening tests or fixing code; report score or surviving count.

**Skip reason examples:** “no mutation tooling in repo”; “CRUD mapping only”; “first walking-skeleton increment”; “mutation job > PR time budget — deferred to nightly.”

### Property-based (explicit)

**Adopt** when examples are incomplete but **rules** are clear (e.g. “sort is stable”, “encode/decode round-trip”, “total is non-negative”).

**Skip** when three concrete examples from Discuss/ATDD fully specify behavior.

---

## 4. One layer per concern

Still obey [delivery-process.md](delivery-process.md) §4:

- Do **not** duplicate the same assertion at unit and acceptance unless they prove **different** boundaries.
- Prefer **one** specialized technique per concern (e.g. property-based **or** table-driven, not both for the same invariant unless complementary).

**Order (pipeline-aware):**

1. Isolated suites first (unit → component → narrow integration → mutation/property if commit-stage).
2. Interactive suites after deploy (smoke → acceptance → integration → contract external → few E2E).

---

## 5. Project-first rule

| Situation | Rule |
|-----------|------|
| Practice **configured** in repo/CI | **Strong bias to adopt** when slice characterization matches §2 |
| Practice **not configured** | Do **not** introduce heavy new tooling mid-slice unless user opts in; note as **follow-up** in handoff |
| Practice configured but **slow** | Scoped run (changed files only) or document deferral to nightly with reason |

---

## 6. Return payload — test strategy field

Add to every delivery return payload (with §10):

```markdown
### Test strategy
| Practice | Decision | Reason |
|----------|----------|--------|
| Unit TDD | adopt | inner loop for domain rules |
| Mutation (Stryker) | adopt | project CI job; branchy pricing logic |
| Property-based | skip | fixed examples agreed in catalog |
| Contract (Pact) | skip | no service boundary in this slice |
| E2E | skip | API acceptance proves AC |
```

List **every practice from §3 you evaluated** (at least 5 for non-trivial slices). **Adopt** rows must link to the automated check added or run.

---

## 7. Anti-patterns

- **Unit-only default** without documenting considered alternatives
- **Mutation everywhere** on CRUD or config-only slices
- **E2E for every story** when API or component layer suffices
- **Ignoring configured CI jobs** (mutation, contract verify, component, a11y) that match the slice
- **Adding new tooling** (Stryker, Pact) without user opt-in when repo has none
- **Duplicate pyramid layers** — same assertion in unit and E2E
- **Skipping characterization** on legacy when changing behavior without a harness

---

## Composition

| Consumer | Uses especially |
|----------|-----------------|
| `new-increment` | §1 before first RED; §6 in payload |
| `new-feature` | §2 when writing increment lines (note expected layers per slice) |
| `skills/tdd` | §3 unit + mutation/property when inner loop insufficient |
| `skills/atdd` | §3 outer layers; compose with [pipeline-fit checklist](../skills/atdd/checklists/pipeline-fit.md) |
| `skills/bugfix` | §3 mutation after repro on critical logic |
| `skills/legacy-testing` | characterization + narrow integration |
| `pr-reviewer` | §6 — flag missing strategy table or ignored configured gates |

See [technical-excellence-catalog.md](technical-excellence-catalog.md) §B for the full practice inventory.
