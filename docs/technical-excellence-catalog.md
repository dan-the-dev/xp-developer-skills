# Technical excellence catalog

Inventory of **practical, verifiable** engineering practices AMPD aims to **enable and amplify** through skills, delivery rules, and project verify steps.

**Not in scope:** theory-only advice, ceremonies without artifacts, or practices that cannot be checked or automated (for example pairing sessions or alignment meetings).

**Related:** [manifesto.md](manifesto.md), [delivery-process.md](delivery-process.md), [principles.md](principles.md), [roadmap.md](roadmap.md).

---

## How to use this catalog

| Column | Meaning |
|--------|---------|
| **Practice** | What the team adopts (name is tool-agnostic). |
| **Family** | `Isolated` = no running deployable/environment; `Interactive` = needs deploy, browser, or external system; `—` = not a test suite. |
| **Verify / automate** | What “done” looks like in CI, repo, or pipeline. |
| **Examples** | Illustrative tools only — swap for your stack. |
| **AMPD** | **Covered** = skill or delivery rule today · **Partial** = referenced or composable · **Gap** = not yet first-class in AMPD |

### AMPD status

| Status | Meaning |
|--------|---------|
| **Covered** | Encoded in a skill, delivery rule, or agent workflow |
| **Partial** | Referenced or composable; no dedicated skill yet |
| **Gap** | Valuable for AMPD; not yet first-class |

### Explicit exclusions

| Excluded | Why |
|----------|-----|
| Pair / mob programming | Not automatable |
| Alignment meetings | Human-only; use **pilot charter in repo** instead |
| Showcase / management demos | Human-only |
| Abstract “clean code” | Use **formatter**, **linter**, **static analysis** gates |
| Code coverage thresholds | Excluded by policy (gaming risk) |
| Strategic-only workshops | Keep **executable** artifacts (catalog, charter, checks) |

---

## Test suite taxonomy

Two families drive **where** suites run in the pipeline:

| Family | Needs | Speed | Pipeline home |
|--------|--------|-------|----------------|
| **Isolated** | No running app, browser, or external system (in-process fakes OK) | Seconds | **Commit** stage |
| **Interactive** | Deployed environment, browser, or real/sandbox IO | Minutes | **Acceptance** stage (after deploy) |

**Rules**

1. Isolated suites run and pass **before** interactive suites start.
2. Interactive suites run **only after** deploy to the acceptance environment (or equivalent).
3. Do not put full browser or E2E jobs in the commit stage.
4. Cap interactive suites — pilot **3–5** critical acceptance scenarios; keep E2E **few**.
5. One concern per layer still applies ([delivery-process.md](delivery-process.md) §4) — family is *how* you run; pyramid is *what* you prove.

**Fast narrow integration:** If Testcontainers (or similar) stays within PR time budget, it may stay in commit stage; otherwise move to interactive.

---

## Pipeline reference (Commit → Acceptance → Release)

Same **deployment process** for acceptance, QA, and production — environments differ by parameters only.

```text
COMMIT STAGE (isolated + artifact)
  compile
  → unit tests
  → component tests (if any)
  → static analysis platform gate
  → build artifact → publish to registry

ACCEPTANCE STAGE (deploy, then interactive — sequential gates)
  deploy → ACCEPTANCE ENVIRONMENT
  → smoke tests (deploy)
  → acceptance tests (every acceptance criterion)
  → integration tests (service / stack)
  → external system contract tests
  → end-to-end tests (few)

RELEASE STAGE
  deploy → QA → production (same process)
  optional: smoke tests (synthetic / production), scheduled
```

**Prerequisites for ATDD pilot:** commit stage with build automation; release stage with automated deploy to QA and production.

---

## P. Pipeline & suite discipline

| Practice | Family | Verify / automate | Examples | AMPD |
|----------|--------|-------------------|----------|------|
| Isolated vs interactive suite classification | — | Suites documented; CI jobs tagged commit vs acceptance | Job names, README | Gap |
| Commit stage: isolated suites only | — | Pipeline: compile → unit → component → static → artifact; no deploy | GitHub Actions, GitLab CI | Gap |
| Acceptance stage: interactive suites only | — | Deploy job completes before smoke/acceptance/integration/E2E | Staged workflow | Gap |
| Sequential pipeline gates | — | Later stage skipped if earlier stage fails | `needs:` / stage dependencies | Gap |
| Integration tests in interactive stage | Interactive | Service-level tests after deploy, not in unit job | Post-deploy job | Gap |
| No interactive tests on failing commit | — | Acceptance stage triggers only if commit stage green | Branch protection | Gap |
| Disabled acceptance test (parallel delivery) | Interactive | Test committed skipped/ignored; enabled when green locally, then committed | `@Ignore`, `test.skip`, pending | Gap |
| ATDD progression: smoke → acceptance architecture → few E2E | — | Documented rollout order in repo | Pilot doc | Gap |

---

## A. Specification & outside-in

| Practice | Family | Verify / automate | Examples | AMPD |
|----------|--------|-------------------|----------|------|
| Example catalog in repo | — | Catalog file; lines open until linked check is green | `examples/`, catalog markdown | Partial |
| ATDD (Discuss → Distill → Develop) | — | Failing acceptance before implement; green in CI | `skills/atdd` | Covered |
| ATDD per user story or bug | — | Story/bug maps to catalog line + automated check | Increment + bugfix | Partial |
| Outside-in delivery | — | Outer check drives inner TDD | ATDD + TDD compose | Covered |
| Pilot scope cap (3–5 scenarios) | — | Pilot charter lists ≤5 critical scenarios | Charter file | Gap |
| Pilot charter in repo | — | Product, teams, scenarios, target pipeline stage | `pilot/` doc | Gap |
| Legacy ATDD (retroactive) | — | Harness + thin acceptance on legacy before widen | `legacy-testing` | Partial |
| Greenfield ATDD setup | — | Walking skeleton + acceptance stage from day one | — | Partial |
| AI-assisted ATDD with reviewed DSL | — | Human reviews DSL/channel text before merge of acceptance layer | PR review | Partial |
| Gherkin / BDD runner | Interactive | Feature files execute in acceptance (or commit if in-process only) | Cucumber, SpecFlow | Partial |
| Code-first acceptance | Interactive | Acceptance code runs in acceptance stage | Playwright, httpx | Partial |
| Walking skeleton | Interactive | Thinnest vertical path green in pipeline | One API or UI path | Partial |
| OpenAPI / AsyncAPI contract | Interactive | Spec lint, breaking-change diff, example tests | Spectral, oasdiff | Gap |
| Consumer-driven contracts | Interactive | Consumer publishes; provider verify job | Pact | Partial |
| Provider/schema contract tests | Interactive | Schema compatibility in CI | JSON Schema, buf | Gap |
| Contract tests for third-party APIs | Interactive | Recorded fixtures; sandbox; upgrade gate; owned client under test | VCR, sandbox job, manual fake/stub | Partial |
| API backward-compat gate | Interactive | Breaking change fails build | buf breaking, GraphQL inspector | Gap |
| Feature-flag behavior in tests | Interactive | Flag matrix or test mode in CI/stage | LaunchDarkly test hooks | Gap |

---

## B. Test layers & pyramid

| Practice | Family | Verify / automate | Examples | AMPD |
|----------|--------|-------------------|----------|------|
| Unit tests (TDD) | Isolated | Fast suite every commit | JUnit, pytest, Vitest | Covered |
| Component tests (UI) | Isolated | Isolated render + behavior; commit stage | Testing Library, Vitest | Partial |
| Narrow in-process integration | Isolated | Real DB/broker in-process or Testcontainers within PR budget | Testcontainers | Partial |
| Storybook catalog build | Isolated | Stories compile in CI | Storybook, Ladle | Gap |
| Storybook interaction tests | Isolated | Interaction runner in CI | Storybook Test Runner | Gap |
| Design-system visual regression | Isolated | Component snapshots in CI | Chromatic, Loki | Gap |
| Accessibility automated checks | Isolated / Interactive | axe in stories or post-deploy UI job | axe-core, pa11y | Partial |
| API / HTTP acceptance | Interactive | REST/GraphQL against deployed acceptance env | supertest, httpx | Partial |
| In-process acceptance | Isolated / Interactive | Module boundary; stage per seam | Acceptance package | Partial |
| Service integration tests | Interactive | Post-deploy; real wiring | Integration job | Gap |
| Acceptance tests (per AC) | Interactive | Each criterion has automated check in acceptance stage | ATDD catalog | Partial |
| End-to-end / UI journey | Interactive | Few flows; last in acceptance stage | Playwright, Cypress | Partial |
| Smoke tests (deploy) | Interactive | Minimal path after deploy to acceptance env | curl + critical API/UI | Gap |
| Smoke tests (suite tag) | Isolated or Interactive | `@smoke` subset; document if pre-deploy API or post-deploy | Tag filter in CI | Partial |
| Smoke tests (synthetic / production) | Interactive | Scheduled probes on stage/prod | Checkly, Pingdom | Gap |
| Full vs smoke split | — | PR runs smoke; main/nightly runs full interactive | CI workflow branches | Partial |
| External system contract tests | Interactive | Third-party sandbox suite in acceptance stage; else manual fake/stub at owned seam | Vendor sandbox | Partial |
| Characterization / approval tests | Isolated | Golden output; legacy harness | ApprovalTests | Covered |
| Property-based tests | Isolated | Generative tests in commit stage | fast-check, Hypothesis | Partial |
| Mutation testing | Isolated | Mutation score gate (optional) | Stryker, PIT | Partial |
| Snapshot tests | Isolated | Reviewed snapshots in CI | Jest snapshots | Gap |
| Application visual regression | Interactive | Screenshot compare on key pages post-deploy | Playwright screenshots | Gap |
| HTTP mocking | Isolated | Stable tests without live vendor in commit — prefer after sandbox ruled out; prefer owned fake/stub when possible | MSW, WireMock | Partial |
| Parallel test sharding | — | CI splits by timing | Matrix jobs | Gap |
| Flake control / quarantine | — | Retry limits; tracked quarantined tests | CI retry policy | Partial |

---

## C. Legacy & change safety

| Practice | Family | Verify / automate | Examples | AMPD |
|----------|--------|-------------------|----------|------|
| Characterization before change | Isolated | New tests fail then pass on intended change | — | Covered |
| Invalid harness fix-first | Isolated | CI red until harness compiles and runs | — | Covered |
| Seam-based dependency breaking | Isolated | Green after each mechanical step | Feathers seams | Covered |
| Sprout / wrap | Isolated | New path covered by new tests | — | Covered |
| Strangler routing tests | Interactive | Old vs new path behavior asserted | Feature flag routes | Gap |
| Anti-corruption adapter tests | Isolated | External DTO mapping verified | Adapter tests | Gap |
| Expand–contract database migrations | Interactive | Up/down migration on fresh DB in CI | Flyway, Liquibase | Gap |

---

## D. Code quality & static gates

| Practice | Family | Verify / automate | Examples | AMPD |
|----------|--------|-------------------|----------|------|
| Strict TDD (RED observed) | Isolated | Failing test run before production change | — | Covered |
| Test-first bugfix | Isolated | Failing repro before fix merge | `skills/bugfix` | Covered |
| Refactor with green suite | Isolated | Verify after each mechanical step | `skills/refactoring` | Covered |
| Two hats (behavior vs structure) | — | Separate commits/PRs; skill boundary | delivery-process §7 | Covered |
| Formatter enforced | — | Format check in commit stage | Prettier, rustfmt | Partial |
| Linter enforced | — | Lint fails commit stage | ESLint, Ruff, clippy | Covered |
| Static analysis platform gate | — | Quality gate in commit stage | SonarQube, CodeClimate | Covered |
| Typechecker gate | — | Types fail commit stage | tsc, mypy, pyright | Covered |
| Import / architecture rules | — | Forbidden import fails build | deptrac, ArchUnit | Gap |
| Complexity limits | — | Cognitive complexity over threshold fails | Sonar rule, ESLint | Gap |
| Duplicate detection | — | Duplication over threshold fails | jscpd | Gap |
| Dead code detection | — | Unused export fails | knip, ts-prune | Gap |
| License / SBOM scan | — | Policy violation fails | syft, FOSSA | Gap |
| Conventional commits | — | Commit message lint in CI | commitlint | Gap |
| Required pull request status checks | — | Branch protection enforces green stages | GitHub rulesets | Gap |

---

## E. Continuous integration & delivery

| Practice | Family | Verify / automate | Examples | AMPD |
|----------|--------|-------------------|----------|------|
| Continuous integration | — | Every PR runs applicable verify steps | CI on PR | Covered |
| Full project verify | — | All project-defined steps, not tests-only | delivery-process §2, project-verification.md | Covered |
| Commit stage pipeline | — | Isolated gates + artifact publish | See pipeline reference | Gap |
| Acceptance stage pipeline | — | Deploy acceptance env → interactive gates → promote | Staged workflow | Gap |
| Release stage pipeline | — | Deploy QA → production | Release workflow | Gap |
| Dedicated acceptance environment | — | Env for interactive suites; same deploy as QA/prod | Acceptance URL | Gap |
| Same deployment process all environments | — | One template; env = parameters | Helm, Terraform | Gap |
| Acceptance stage test order | Interactive | smoke → acceptance → integration → external contracts → E2E | Job `needs:` order | Gap |
| Deploy-then-test on acceptance environment | Interactive | Tests hit freshly deployed build | Deploy job first | Gap |
| Automated deploy prerequisite (QA and production) | — | Release stage exists before ATDD pilot | CD pipeline | Gap |
| Artifact publish to registry | — | Immutable versioned artifact after commit stage | Docker registry, Maven | Gap |
| Ephemeral / preview environments | — | Per-PR URL; smoke optional | Preview deploy | Gap |
| Easy spinnable demo environments | — | One-command local or shared demo | `make demo`, Compose | Gap |
| Reproducible dev environments | — | Dev container or documented image matches CI | Dev Containers | Gap |
| Database migrations in CI | Interactive | Migrate test DB in pipeline | Flyway, Atlas | Gap |
| Seed data as code | — | Versioned seeds loaded in test job | SQL seeds, factories | Gap |
| Semantic release | — | Tag/changelog from conventional commits | semantic-release | Gap |
| Automated rollback (deploy) | — | Revert to previous artifact on failed health | Rollback job | Gap |
| Feature flags in delivery | Interactive | Flag state testable; kill switch | Unleash, LaunchDarkly | Gap |
| Canary / progressive rollout | Interactive | Promote or halt on metric gate | Flagger, Argo Rollouts | Gap |
| Blue-green deployment | Interactive | Traffic switch after health smoke | Load balancer swap | Gap |

---

## F. Infrastructure & platforms

| Practice | Family | Verify / automate | Examples | AMPD |
|----------|--------|-------------------|----------|------|
| Infrastructure as code | — | Plan/apply reviewed; plan in PR | Terraform, Pulumi | Gap |
| Infrastructure policy as code | — | Policy violation fails plan | Checkov, OPA | Gap |
| Container image build and scan | — | Build in CI; CVE policy gate | Trivy, Grype | Gap |
| Kubernetes manifest validation | — | Invalid manifest fails CI | kubeconform, helm lint | Gap |
| Helm/Kustomize render diff in PR | — | Rendered manifest diff commented or gated | helm diff | Gap |
| Secrets scanning (repository) | — | Leak fails push or PR | gitleaks, trufflehog | Gap |
| Environment parity | — | Same IaC/compose locally and in CI | Compose, IaC | Gap |
| Health / readiness / liveness probes | Interactive | Probes defined; smoke hits health endpoint | Kubernetes probes | Gap |
| Local stack via compose | — | `compose up` + smoke script documented | Docker Compose | Gap |

---

## G. Architecture & boundaries (encoded)

| Practice | Family | Verify / automate | Examples | AMPD |
|----------|--------|-------------------|----------|------|
| Architectural fitness functions | — | Cycles, forbidden imports, metrics fail build | ArchUnit, deptrac | Gap |
| Architecture decision records | — | ADR template and status in repo | MADR, adr-tools | Gap |
| Module boundary tests | Isolated | Forbidden import fails compile | custom lint | Gap |
| Hexagonal ports (tested) | Isolated | Adapters behind interfaces; sandbox or fakes for vendor adapters; fakes in unit layer | ports/adapters layout | Partial |
| Event schema registry compatibility | Interactive | Schema evolution check in CI | Confluent schema registry | Gap |
| Idempotency / outbox tests | Interactive | Duplicate delivery simulated | outbox pattern tests | Gap |

---

## H. Frontend, design systems & design–code sync

| Practice | Family | Verify / automate | Examples | AMPD |
|----------|--------|-------------------|----------|------|
| Component tests | Isolated | UI behavior without full app deploy | Testing Library | Gap |
| Storybook catalog in CI | Isolated | `build-storybook` in commit stage | Storybook | Gap |
| Storybook accessibility addon | Isolated | axe per story in CI | @storybook/addon-a11y | Gap |
| Design tokens as code | Isolated | Token build fails on invalid tokens | Style Dictionary | Gap |
| Design tool → code token sync | — | Export diff fails PR on drift | Figma Variables, Tokens Studio | Gap |
| Design tool component mapping | — | Component mapping checked in CI | Figma Code Connect | Gap |
| Design tool design lint | — | Lint rules on design export | Figma design lint | Gap |
| Visual regression (components) | Isolated | Story snapshots in CI | Chromatic, Loki | Gap |
| Cross-browser end-to-end matrix | Interactive | Multiple browsers in acceptance stage | Playwright projects | Gap |
| Web performance budgets | Interactive / — | Lighthouse or bundle size gate | Lighthouse CI, size-limit | Gap |
| Internationalization key coverage | Isolated | Missing translation fails build | i18n lint | Gap |

---

## I. Performance, resilience & security

| Practice | Family | Verify / automate | Examples | AMPD |
|----------|--------|-------------------|----------|------|
| Load / stress tests | Interactive | Thresholds in acceptance or scheduled job | k6, Gatling | Gap |
| Benchmark regression | Isolated | Regression fails commit or nightly | criterion, benchstat | Gap |
| Timeout / retry contract tests | Interactive | Simulated slow or failing dependency | toxiproxy | Gap |
| Chaos tests (non-production) | Interactive | Fault injection in non-prod pipeline | Litmus | Gap |
| Static application security testing | — | SAST job in commit or acceptance stage | CodeQL, Semgrep | Gap |
| Dependency vulnerability scan | — | CVE over policy fails | OSV, Dependabot | Gap |
| Dynamic application security testing | Interactive | DAST against preview/acceptance URL | OWASP ZAP | Gap |
| Container image CVE gate | — | Critical CVE fails publish | Trivy policy | Gap |
| Signed artifacts / provenance | — | Signature verified on promote | SLSA, sigstore | Gap |

---

## J. Observability & operational verification

| Practice | Family | Verify / automate | Examples | AMPD |
|----------|--------|-------------------|----------|------|
| Structured logging contract | — | Log field schema lint or test | JSON schema | Gap |
| Distributed tracing in integration tests | Interactive | Spans exported in test run | OpenTelemetry | Gap |
| Synthetic monitoring | Interactive | Scheduled URL/service checks | Checkly | Gap |
| Service level objective alerts | — | Alert rules in IaC; test firing | Prometheus rules | Gap |
| Error tracking release mapping | — | Release version tied to deploy | Sentry releases | Gap |
| Metrics alert rule tests | — | PromQL/rule unit tests | prometheus-rules tests | Gap |

---

## K. Data & integration

| Practice | Family | Verify / automate | Examples | AMPD |
|----------|--------|-------------------|----------|------|
| Migration up/down in CI | Interactive | Fresh DB + migrate + test | Flyway, Liquibase | Gap |
| Test data builders | Isolated | Repeatable factories in tests | Factory Boy | Partial |
| Anonymized fixture datasets | — | Seed from sanitized dump | seed scripts | Gap |
| Change data capture schema compatibility | Interactive | Event schema evolution in CI | Avro compatibility | Gap |
| Webhook replay tests | Interactive | Recorded payloads verified | VCR, custom replay | Gap |
| Vendor sandbox suite | Interactive | Nightly/acceptance external contract job; policy in `test-strategy-selection` §3a | Stripe test mode | Partial |

---

## L. Product metrics & release safety

| Practice | Family | Verify / automate | Examples | AMPD |
|----------|--------|-------------------|----------|------|
| Product metrics instrumentation | — | Events emitted; schema or contract tested | analytics schema tests | Gap |
| Experiment / A-B flag wiring | Interactive | Variant assignment testable in stage | experiment SDK | Gap |
| Release metric gate (canary) | Interactive | Promote only if KPIs within bounds | canary analysis | Gap |
| Automated rollback on goal miss | Interactive | Halt or revert when metric breaches threshold | auto-rollback | Gap |
| Guardrail metrics | Interactive | Auto-stop on error rate or latency SLO | rollout guardrails | Gap |
| Dashboard as code | — | Dashboard config reviewed in PR | Grafana Terraform | Gap |
| Funnel / outcome smoke (product) | Interactive | Key product event fires in stage after deploy | event assertion | Gap |

---

## M. AMPD agent & delivery discipline

| Practice | Family | Verify / automate | Examples | AMPD |
|----------|--------|-------------------|----------|------|
| Skills as operational workflows | — | Agent follows `SKILL.md`; return payload | `skills/*` | Covered |
| Honest increment backlog | — | Line open until linked check green | `new-increment` | Covered |
| One increment per invocation | — | Single backlog line + verify report | delivery-process §1 | Covered |
| RED cycle evidence | — | Failing run logged before green | delivery-process §6 | Covered |
| Change-surface completeness | — | All call sites in scope updated | delivery-process §3 | Covered |
| Spike isolation and promotion | — | Work on `spike/` branch; promotion checklist | `skills/spike` | Covered |
| Pull request reviewer agent | — | Review against manifesto + skills | `agents/pr-reviewer` | Covered |
| Test list linked to automated tests | — | `test-lists/` entries map to real checks | `skills/tdd` | Covered |

---

## O. Acceptance test architecture

Separate **drivers**, **channels**, and **DSL** so acceptance code stays maintainable and AI-generated layers are reviewable.

| Practice | Family | Verify / automate | Examples | AMPD |
|----------|--------|-------------------|----------|------|
| Driver layer | — | Technical adapters isolated from scenarios | Playwright, HTTP client wrappers | Gap |
| Channel layer | — | API vs UI vs message behind stable interface | channel abstractions | Gap |
| DSL layer | — | Human-readable steps; reviewed when AI-written | step definitions, fluent API | Gap |
| Acceptance stack decoupled from application language | — | Acceptance project in stack suited for speed | TypeScript Playwright vs Java app | Gap |
| Layered layout in repository | — | `drivers/`, `channels/`, `dsl/` or equivalent enforced | folder convention | Gap |

---

## Appendix: practice → AMPD artifacts

| Catalog area | Today | Roadmap / gap |
|--------------|--------|----------------|
| A, B (partial), C, D (partial), M | `skills/atdd`, `tdd`, `bugfix`, `legacy-testing`, `refactoring`, `new-increment`, `delivery-process.md`, `test-strategy-selection.md` | Disabled acceptance test, pilot charter, pipeline stages |
| P, E (stages) | — | Commit / acceptance / release modeling; `ephemeral-environments` |
| H (design–code) | — | Token sync, Code Connect |
| J, L | — | `setup-observability`, product metrics, feature flags |
| O | — | Driver/channel/DSL skill guidance |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-07-12 | Test strategy selection guide; mutation/property-based/component selection rules |
| 2026-05-28 | Initial catalog: isolated vs interactive taxonomy, pipeline stages, workshop ATDD practices, full practice tables |
