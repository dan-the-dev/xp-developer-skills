# E2E acceptance (browser, full stack)

Use this reference when the slice's acceptance **mode** is **`e2e`** (see [SKILL.md § Acceptance mode](../SKILL.md#acceptance-mode-api-only-or-e2e)): the agreed example is only provable by driving the real UI in a browser against a running app.

**Backend involved?** If the slice also adds or changes backend behavior, E2E is not enough on its own: add [API acceptance](api-acceptance.md) for the backend rules (mode `mixed`) — or, if it is unclear whether the backend is touched or an API test would add signal, **ask the user** before Distill. The browser test proves the journey and wiring; the API tests prove the backend rules and their failure cases fast and without flake.

E2E tests are Fowler's [broad-stack tests](https://martinfowler.com/bliki/BroadStackTest.html) — the most realistic and the most expensive layer of the [test pyramid](https://martinfowler.com/articles/practical-test-pyramid.html). Keep them **few, thin and outcome-focused**: one journey per capability, branches and field validation pushed down to API, component or unit tests.

---

## Reference stack (JS/TS web apps): Cypress + Gherkin

When the repo already uses it — or on greenfield JS/TS web apps where the team wants business-readable scenarios — follow this layout. On other stacks (Playwright, WebDriver, Capybara, …) keep the **same structure and rules**, swapping the tool.

### Tooling

- [Cypress](https://docs.cypress.io/) +
  [`@badeball/cypress-cucumber-preprocessor`](https://github.com/badeball/cypress-cucumber-preprocessor)
  for [Gherkin](https://cucumber.io/docs/gherkin/reference/)/BDD-style scenarios, bundled with
  [`@bahmutov/cypress-esbuild-preprocessor`](https://github.com/bahmutov/cypress-esbuild-preprocessor).
- Inspect first: never introduce Cypress if the repo already has Playwright (or vice versa) — add Gherkin only if someone reads the features ([gherkin-and-bdd-tooling.md](gherkin-and-bdd-tooling.md)).

### Layout (three layers, one responsibility each)

| Path | Contains | Must not contain |
|------|----------|------------------|
| `cypress/e2e/*.feature` | Scenarios in plain-language Given / When / Then ([Cucumber's BDD guide](https://cucumber.io/docs/bdd/)) | Selectors, URLs of internal routes, CSS, waits |
| `cypress/support/step_definitions/` | Step implementations: translate domain language into Page Object calls | Raw selectors (`cy.get('[data-testid=…]')`) |
| `cypress/support/pages/` | One [Page Object](https://martinfowler.com/bliki/PageObject.html) class per page/screen, exposing **actions** (`fillEmail`, `submit`, …) and **queries** about state | Assertions about business rules (keep those in **Then** steps) |

Steps **never** touch selectors directly — only Page Objects do. When the UI changes, exactly one Page Object changes; scenarios and steps stay put.

This is Dave Farley's **four-layer acceptance test architecture** applied to a browser suite: **test case** (`.feature`) → **domain-specific language** (step definitions) → **protocol driver** (Page Objects) → **system under test**. The scenario must still make sense if the protocol driver were swapped for an HTTP client — that is the test of good layering.

### Language

- Scenarios and steps are written in **English** — Gherkin keywords included — even when the product UI and its own docs are in another language: feature files are read by the whole team, not only by whoever wrote the product copy they exercise.
- Product copy asserted in **Then** steps stays in the UI's language, ideally referenced through a constant/i18n key in the Page Object rather than inlined in the step.

### Selectors

- Prefer a **`data-testid`** attribute over CSS id, class or visible text — see Cypress's
  [Selecting Elements best practice](https://docs.cypress.io/app/core-concepts/best-practices#Selecting-Elements).
- **Add** a `data-testid` to the component **before** writing a Page Object against it, rather than reusing whatever `id`/label happens to exist.
- Accessible role/label queries ([Testing Library priority](https://testing-library.com/docs/queries/about/#priority), [Playwright locators](https://playwright.dev/docs/best-practices#use-locators)) are equally acceptable when the project already uses them — they double as an a11y check. Pick **one** convention per repo.
- Never: generated class names, nth-child paths, XPath on layout.

### Test credentials and secrets

- Test user credentials (e.g. `E2E_TEST_USER_EMAIL` / `E2E_TEST_USER_PASSWORD`) live in a **dedicated, gitignored** env file such as **`.env.test.local`** — deliberately **not** the app's own `.env.local` — loaded by a support module (e.g. `cypress/support/load-env.ts`) with the **same fallback chain** as the unit-test env setup (e.g. `test/setup-env.ts` for Vitest).
- Read them **on demand** via a Node-side task (`cy.task('getE2ETestUser')`, defined in `cypress.config.ts`), **not** through `Cypress.env()` / `config.env`, so they never land in Cypress's debug/run output, screenshots or videos.
- Never commit real or production credentials; document the **canonical** test user in the repo.

### Target environment

- `baseUrl` defaults to `http://localhost:3000` (or the app's dev port) and is **overridden per run** via `CYPRESS_BASE_URL` — Cypress maps any `CYPRESS_<CONFIG_KEY>` env var onto that config key. This is the mechanism a CI job uses to point the **same** suite at staging.
- No environment-specific branches inside tests.

### Run

- `npm run cypress:open` (interactive) / `npm run cypress:run` (headless), against an **already-running** app (`npm run dev`) — or a `start-server-and-test` style script in CI.
- During Develop run the **single** feature file (`--spec cypress/e2e/<feature>.feature`), not the whole suite.

---

## Patterns and practices

### Page Object — and when to outgrow it

- [Page Object](https://martinfowler.com/bliki/PageObject.html) (Fowler): model the **page's services**, not its HTML. Methods return other Page Objects or domain values; they read like what a user *does* (`loginAs(user)`), not what the DOM *is*.
- Page Objects may also be **fragments** (header, cart widget) — "page" means a significant UI area, not necessarily a URL.
- Keep business assertions out of Page Objects; they expose state, **Then** steps judge it.
- When Page Objects grow into god classes or journeys span many actors, consider the [**Screenplay pattern**](https://serenity-js.org/handbook/design/screenplay-pattern/) (actors, abilities, tasks, questions) — composition over inheritance for large suites. Do not start there (YAGNI).

### Set up through the side door, assert through the front door

- **Given** steps create state via **API calls, DB seeding or factories**, not by clicking through the UI — only the **When** under test goes through the browser.
- Log in programmatically and cache it ([`cy.session`](https://docs.cypress.io/api/commands/session), Playwright [storage state](https://playwright.dev/docs/auth)); exercise the real login form in **one** scenario whose subject *is* login.
- Build data with [Test Data Builders](http://natpryce.com/articles/000714.html) (Nat Pryce) or an [Object Mother](https://martinfowler.com/bliki/ObjectMother.html) — minimal, named, per-scenario.

### Independence and isolation

- Each scenario creates what it needs and can run **alone and in any order** — Kent Beck's [Test Desiderata](https://testdesiderata.com/): *isolated, deterministic, fast, behavioral, structure-insensitive, specific, readable, predictive*. E2E trades *fast* for *predictive*; do not also give up *isolated* and *deterministic*.
- Unique data per run (suffix ids/emails) instead of shared fixtures that scenarios mutate.
- Clean state **before** a test, not after — a crashed run must not poison the next one.

### Determinism (no flake)

- Never `cy.wait(ms)` / `sleep`: wait on **conditions** — an element state, a route alias (`cy.intercept` + `cy.wait('@alias')`), a URL. Rely on the tool's built-in retry-ability.
- No [conditional testing](https://docs.cypress.io/app/guides/conditional-testing) (`if element exists then…`): the test must know the state it created.
- Control time, randomness and third parties — see Fowler's [Eradicating Non-Determinism in Tests](https://martinfowler.com/articles/nonDeterminism.html) and [quality-and-flake-control.md](quality-and-flake-control.md).

### Network stubbing — pick deliberately

| Choice | Proves | Use when |
|--------|--------|----------|
| Real backend (default for acceptance) | Full wiring, the business outcome | The catalog example is a **journey** |
| Stubbed API ([`cy.intercept`](https://docs.cypress.io/api/commands/intercept) fixtures) | UI behavior for a backend state hard to reproduce (errors, timeouts, empty lists) | Edge cases — and then it is a **UI/component** test, not end-to-end; keep API honesty with a [contract test](https://martinfowler.com/bliki/ContractTest.html) |
| Owned third-party (payments, email) | — | Vendor sandbox or fake at the owned seam ([`test-strategy-selection.md`](../../../docs/test-strategy-selection.md) §3a) |

### Scenarios that stay readable

- Declarative, not imperative: "When the customer checks out", not "When I click `#checkout-btn`" — Cucumber's [Writing better Gherkin](https://cucumber.io/docs/bdd/better-gherkin/) and Fowler's [GivenWhenThen](https://martinfowler.com/bliki/GivenWhenThen.html).
- One rule per scenario, 3–7 steps; **Then** asserts an outcome a user would notice (message, total, new page state), not a DOM detail.
- Step reuse comes from shared **domain vocabulary**, not from generic "I click {string}" steps.

### Keep the E2E layer thin

- One **walking skeleton** journey first ([environments-and-test-pyramid.md](environments-and-test-pyramid.md#walking-skeleton)), then only the journeys the business would call broken if they failed.
- Anything provable below the UI goes to an [API-level / subcutaneous test](api-acceptance.md) ([SubcutaneousTest](https://martinfowler.com/bliki/SubcutaneousTest.html)) or a component test — see Fowler's [On the Diverse and Fantastical Shapes of Testing](https://martinfowler.com/articles/2021-test-shapes.html) for why the exact shape matters less than fast, reliable, meaningful tests.
- Tag a `@smoke` subset for PR feedback; run the full E2E set in the acceptance stage.

---

## Cypress / Playwright specifics worth knowing

- Cypress [best practices](https://docs.cypress.io/app/core-concepts/best-practices): data-testid selectors, don't visit external sites, don't couple tests, set state programmatically, set `baseUrl`, no arbitrary waits.
- Playwright [best practices](https://playwright.dev/docs/best-practices) and its [Page Object guide](https://playwright.dev/docs/pom): user-facing locators, web-first assertions, test isolation per browser context.
- Artifacts (screenshots/videos/traces) on failure only; make sure they cannot capture secrets (hence the `cy.task` rule above).

---

## E2E review checklist (add to Distill)

- [ ] Mode is really `e2e` — no API/component seam could prove this example
- [ ] Backend changed in this slice → matching `api` acceptance exists (mode `mixed`), or the user explicitly declined it
- [ ] `.feature` has domain language only; no selectors, waits or internal URLs
- [ ] Steps call Page Objects only; Page Objects own every selector
- [ ] New selectors use the repo's convention (`data-testid` by default), added to the component first
- [ ] Given state built via API/seed/`cy.session`, not UI clicks
- [ ] No fixed waits, no conditional testing, no order dependence
- [ ] Credentials read via task from a gitignored test env file — not `Cypress.env()`
- [ ] Suite runs against `baseUrl` from env; same suite can target staging
