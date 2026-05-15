# Gherkin and BDD tooling (optional layer)

Gherkin is a **structured plain-text** format for scenarios (`Feature`, `Scenario`, `Given`, `When`, `Then`, tables, tags). Cucumber and compatible runners compile Gherkin into executable tests.

**Pragmatic rule:** use Gherkin when it **improves communication** in your repo; otherwise keep examples in the **catalog** and automate in code.

Reference grammar: [Cucumber Gherkin reference](https://cucumber.io/docs/gherkin/reference).

---

## When to use Gherkin

- Product/BA reviewers read `*.feature` files in PRs.
- Team already pays down **step definition** maintenance.
- Scenarios are **stable** domain language, not one-off scripts.

## When to prefer code-first acceptance

- Strong Playwright / API test DSL already exists.
- Gherkin would duplicate the catalog verbatim with no extra audience.
- Step defs would be 1:1 wrappers around Playwright calls (smell).

---

## Ecosystem (illustrative)

| Stack | Common tools |
|-------|----------------|
| JVM | Cucumber JVM, Serenity |
| .NET | SpecFlow |
| JavaScript/TS | `@cucumber/cucumber`, Cypress + preprocessor (if adopted) |
| Ruby | cucumber-ruby, Turnip |
| Python | pytest-bdd, behave |
| Go | godog |
| API contracts | Pact, schema validators, Dredd (OpenAPI) |
| E2E (non-Gherkin) | Playwright, Cypress, WebDriver-based suites |
| Keyword-driven | Robot Framework |

Inspect the **project** first; never introduce a new runner without team alignment.

---

## Gherkin quality rules

- **One scenario, one rule** (or one example row).
- **3–7 steps** per scenario is a soft target; split if longer.
- **Background** only for shared **Given** that every scenario needs.
- **Scenario Outline** + **Examples** for tables the business supplied in Discuss.
- Tags (`@smoke`, `@billing`) for selective CI runs — align with pipeline-fit checklist.

---

## Good vs bad (sketch)

**Good** — domain language, clear outcome:

```gherkin
Scenario: Shipping applies above weight threshold
  Given a cart weighing 11 kg
  When the customer checks out
  Then the order total includes a shipping line
```

**Bad** — UI script, no business outcome:

```gherkin
Scenario: Checkout button
  Given I open "/cart"
  When I click "#checkout-btn"
  Then I see div.checkout-modal
```

More examples: [examples/gherkin-scenario-good-bad.md](../examples/gherkin-scenario-good-bad.md).

---

## Catalog + Gherkin relationship

Pick **one** primary human-readable home:

- **A:** catalog is canonical; Gherkin mirrors selected lines, or
- **B:** feature files are canonical; catalog links to `feature:line` with short summary.

Avoid two diverging sources without links.
