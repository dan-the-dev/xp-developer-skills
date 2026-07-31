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
| External vendor API / **owned client or adapter** | Test the **owned client** (see §3a) | Sandbox live when feasible; else manual fake/stub at owned seam |
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
| **Mutation testing** | Branchy/critical logic; weak tests suspected; **project already runs mutation**; after bugfix on complex rules; **greenfield domain** where rules have meaningful branches | Trivial CRUD; first walking-skeleton with no domain branches yet; brownfield with no tool and setup ≫ slice (follow-up) | Stryker, PIT, cargo-mutants |
| **Snapshot / approval** | Stable structured output (JSON, HTML fragment) | Behavior better expressed as explicit assertions | Jest snapshots, ApprovalTests |
| **Accessibility (automated)** | UI component or page in slice; a11y is acceptance criterion | No UI; project has no a11y tooling | axe-core, pa11y, Storybook a11y |
| **Smoke (deploy)** | Slice touches deploy path, health, or env wiring | No deployable change | curl health, `@smoke` tag |
| **E2E / browser journey** | Capability **only** visible through full stack + browser | API or component layer can prove it | Playwright, Cypress |
| **Vendor client — sandbox** | Owned third-party client/adapter; sandbox/test env is reachable and stable enough for the chosen suite | No credentials/test mode, cost/rate limits block, or flake budget exceeded — use §3a fallback | Vendor test mode, Stripe test keys, sandbox base URL |
| **Vendor client — manual fake/stub** | Sandbox not feasible; still need to prove owned client mapping/errors at the seam you own | Prefer sandbox when §3a “possible” criteria pass | Hand-written fake implementing your port; canned stub responses |
| **HTTP mocking / fixtures** | HTTP-only client **and** no owned fake yet; or recorded fixtures for replay | Prefer sandbox or manual fake/stub per §3a; do not default here | MSW, WireMock, VCR |
| **Visual regression** | Design-system or layout stability is the risk | Logic-only change | Chromatic, Playwright screenshots |
| **Load / benchmark** | Performance is the acceptance criterion | Normal feature slice; use spike first | k6, criterion |

### 3a. Owned third-party API clients (vendor adapters)

When the slice **introduces or changes** a client toward an external vendor (payment, quotes, identity, webhooks, etc.), the **system under test is that owned client / adapter** — not the domain with the vendor SDK mocked away.

**Implementation preference (production):**

1. Prefer the **official vendor SDK** when one exists and fits the stack.
2. Otherwise use **HTTP** (or the project’s standard HTTP client).
3. SDK vs raw HTTP does **not** change the testing rule below — both are implementation details of the **same** owned client.

**Testing preference (classical / state verification):**

Align with [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html) (Meszaros vocabulary via Fowler): prefer **real** collaborators when practical; otherwise a **fake** or **stub** with **state verification**. Reserve **mocks** (behavior verification / expected call sequences) for command-style contracts you actually specify — not for vendor SDK types.

| Order | Practice | When |
|-------|----------|------|
| **1** | **Real calls** to vendor **sandbox / test** environment | Feasible per criteria below |
| **2** | **Manual fake** at the **owned** seam, answering with **stub** (canned) responses | Sandbox not feasible |
| **Avoid as default** | Mocking vendor SDK types; HTTP mock servers/fixtures when a hand-written fake on your port would do | Use only as interim or when the project already standardizes on recorded fixtures |

**Sandbox is “possible” when all hold:**

- Non-production credentials / test mode exist (env or CI secrets — never production keys).
- Vendor documents a sandbox or test API.
- Cost and rate limits are acceptable for the suite (commit vs nightly/acceptance).
- Flake/timeout risk is within team budget (document if moved to interactive/nightly).

If any criterion fails → **manual fake + stubs**, and record the skip reason in the §6 strategy table.

**Seam rule:** domain and application services depend on **your** port/interface. Only the adapter talks to the SDK or HTTP. Tests of domain logic inject a fake; tests of the **adapter** exercise sandbox or the adapter’s own fake/stub path — do **not** mock third-party types directly.

**Pipeline note:** sandbox suites are often **interactive** (acceptance/nightly). A fast **manual fake** suite may stay in **commit** stage. Prefer one strong layer for the client contract; do not duplicate the same assertion in unit + sandbox without different boundaries.

**Do not confuse** with TDD’s GREEN-phase “fake it” (hard-coded production return). Here **fake/stub** means a **test double** for the collaborator.

### Mutation testing (explicit)

Mutation tests are **optional but must be considered** when:

- The project defines a mutation job or config (`stryker.conf`, `pitest`, `cargo-mutants`, CI `mutation` job).
- The slice adds or fixes **branch-heavy** logic (pricing, auth rules, validation matrices, state machines).
- A bugfix passed unit tests but confidence in **test strength** is low.
- **Greenfield / new system:** the first increment that introduces real domain branches — do **not** wait for the user to ask **when the threshold below is met**.

**Introduce-tooling threshold (greenfield / new module):** add minimal mutation config in this slice only when characterization says adopt **and** estimated setup (config + script + first scoped run) is **≤ ~25%** of the slice effort. If setup would dominate, adopt the *practice intent* in the strategy table, note **follow-up** for tooling, and strengthen unit tests this slice instead.

**Teaching / kata / demo slices:** skip with an explicit reason (e.g. “teaching slice — no mutation tooling”) is fine.

**Action when adopted:**

1. If tooling is missing and the threshold above is met, **add minimal project-native mutation config** in this increment (or the first branchy one), wire a script/CI-friendly command, then run it (prefer **scoped** to touched files).
2. Run the project’s mutation command (or scoped run); fix **surviving mutants** by strengthening tests or fixing code; report score or surviving count.
3. **Deferred survivors** are allowed if listed with reason (time budget / nightly) — do not mark mutation “adopt” and leave it unrun without that note.

**Skip reason examples:** “CRUD mapping only”; “walking-skeleton / no domain branches yet”; “brownfield, no mutation tooling, setup ≫ slice — follow-up noted”; “setup > ~25% of slice — follow-up noted”; “teaching/kata slice — no mutation tooling”; “mutation job > PR time budget — deferred to nightly.”

**Do not skip** with only “not configured” on a **new** system that already has branchy domain logic **and** meets the introduce-tooling threshold.

### ATDD and Gherkin (explicit)

| Situation | Prefer |
|-----------|--------|
| Real outer seam (HTTP, CLI, UI contract) in this slice | **ATDD** at that boundary + inner TDD ([`skills/atdd`](../skills/atdd/SKILL.md)) |
| Same assertions would duplicate unit tests with no extra boundary | **TDD only** — skip ATDD |
| Team/product already reviews `*.feature` / Cucumber | Gherkin as Distill format |
| Solo / code-first team, no BA reading features | **Code-first** acceptance tests — do not invent Gherkin theater |

Gherkin is a **format choice**, not a required layer. Record adopt/skip for “API/HTTP acceptance” and “In-process acceptance”; mention Gherkin only when Distill uses it.

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
| Practice **not configured**, **greenfield** / new system / new module you scaffold | **Bias to introduce** minimal tooling when §2–3 say adopt **and** the introduce-tooling threshold is met (especially mutation for branchy domain, property-based for invariants). Add config + script in the adopting increment; run before marking done. If setup ≫ slice, note follow-up and strengthen lower layers this slice. |
| Practice **not configured**, **brownfield** | Do **not** introduce heavy tooling mid-slice unless user opts in; note as **follow-up** in handoff |
| Practice configured but **slow** | Scoped run (changed files only) or document deferral to nightly with reason |

---

## 6. Return payload — test strategy field

Add to every delivery return payload (with §10):

```markdown
### Test strategy
| Practice | Decision | Reason |
|----------|----------|--------|
| Unit TDD | adopt | inner loop for domain rules |
| Mutation (Stryker) | adopt | greenfield branchy pricing; config added this slice |
| Property-based | skip | fixed examples agreed in catalog |
| API acceptance / ATDD | skip | no outer seam this slice |
| Gherkin | skip | code-first acceptance if ATDD later |
| Contract (Pact) | skip | no service boundary in this slice |
| Vendor client (sandbox) | skip | no test-mode credentials in CI — see fake row |
| Vendor client (manual fake/stub) | adopt | owned PaymentsPort fake; stub decline/success bodies |
| E2E | skip | API acceptance proves AC |
```

List **every practice from §3 you evaluated** (at least 5 for non-trivial slices; include **Mutation** and an **ATDD/acceptance** row). When the slice touches a **vendor client/adapter**, include **Vendor client (sandbox)** and **Vendor client (manual fake/stub)** rows. **Adopt** rows must link to the automated check added or run.

---

## 7. Anti-patterns

- **Unit-only default** without documenting considered alternatives
- **Skipping mutation on greenfield** branchy domain until the user asks **when the introduce-tooling threshold is met**
- **Mutation everywhere** on CRUD or config-only slices
- **Forcing mutation tooling** into teaching/kata slices or when setup clearly dominates the slice
- **E2E for every story** when API or component layer suffices
- **Ignoring configured CI jobs** (mutation, contract verify, component, a11y) that match the slice
- **Gherkin theater** — adding `*.feature` files no stakeholder reads while duplicating unit assertions
- **Adding heavy brownfield tooling** without user opt-in when repo has none and setup ≫ slice
- **Duplicate pyramid layers** — same assertion in unit and E2E
- **Skipping characterization** on legacy when changing behavior without a harness
- **Marking done with red tests** or unrun adopted practices (mutation adopted but never executed)
- **Vendor client untested** — adding an SDK/HTTP adapter without sandbox or manual fake/stub proof
- **Mocking vendor SDK types** instead of an owned seam (see §3a and [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html))
- **Defaulting to HTTP mocks/fixtures** when sandbox is possible, or when a hand-written fake on your port would suffice
- **Hand-rolling HTTP** when an official vendor SDK exists and fits the stack without a documented reason

---

## Composition

| Consumer | Uses especially |
|----------|-----------------|
| `new-increment` | §1 before first RED; §3a vendor clients; §5 greenfield introduce; §6 in payload; hard green gate |
| `new-feature` | §2 when writing increment lines (note expected layers per slice, e.g. “mutation”, “ATDD at API”, “vendor sandbox”) |
| `skills/tdd` | §3 unit + mutation/property when inner loop insufficient; §3a when SUT is vendor adapter |
| `skills/atdd` | §3 outer layers + Gherkin choice; compose with [pipeline-fit checklist](../skills/atdd/checklists/pipeline-fit.md); external services per §3a |
| `skills/bugfix` | §3 mutation after repro on critical logic |
| `skills/legacy-testing` | characterization + narrow integration; vendor wrappers per §3a |
| `skills/increment-review` | flag missing layers / weak tests in the increment's commit, using the mini-journal's review-focus as the starting point |
| `skills/refactoring` (fix brief) | apply the strategy fix `increment-review` names, scoped to its brief |
| `pr-reviewer` | §6 — flag missing strategy table, ignored configured gates, or vendor client without sandbox/fake row |

See [technical-excellence-catalog.md](technical-excellence-catalog.md) §B for the full practice inventory.
