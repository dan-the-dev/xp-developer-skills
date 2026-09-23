# API-only acceptance (no browser)

Use this reference when the slice's acceptance **mode** is **`api`** (see [SKILL.md § Acceptance mode](../SKILL.md#acceptance-mode-api-only-or-e2e)): the agreed example is provable through the application's public boundary — HTTP/GraphQL/gRPC endpoint, CLI, message/event, or an in-process application-service seam — without driving a UI.

This is the **default** mode: it is Fowler's [subcutaneous test](https://martinfowler.com/bliki/SubcutaneousTest.html) — just under the UI, covering most business behavior with far less cost and flake than a browser (see the [Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)). It also applies to backends and services with no UI at all, and to the **backend half of an `e2e` slice** (mode `mixed`): when a browser journey relies on new or changed backend behavior, the backend rules get their own API acceptance here.

---

## Structure (same four layers as E2E)

Dave Farley's four-layer acceptance architecture, with an HTTP (or CLI/queue) driver instead of a browser:

| Layer | API-mode shape | Rule |
|-------|----------------|------|
| **Test case** | `.feature` (if Gherkin is used) or a test whose name states the business rule | Domain language only — no URLs, status codes, JSON paths in the scenario text |
| **DSL** | Step definitions / helper functions (`placeOrder(cart)`, `balanceOf(account)`) | Translates domain intent to driver calls; hides auth, headers, serialization |
| **Protocol driver** | A thin **API client** for tests (the API's equivalent of a Page Object) | Owns endpoints, payload shapes, auth tokens; one place to change when the wire format changes |
| **SUT** | Running app (test server, container, or in-process host) | Real wiring, real persistence (isolated), fakes only for third parties |

Keep the layers even with code-first tests: a test calling `fetch('/api/v2/orders', {…})` inline, repeated in 20 tests, is the API version of raw selectors in step definitions.

---

## Choosing the seam

| Seam | Use when | Tooling (illustrative) |
|------|----------|------------------------|
| **HTTP against a running app** | Default for web backends; proves routing, serialization, auth, persistence | supertest, httpx/pytest, REST-assured, Karate, `fetch` + Vitest |
| **In-process application service** | One deployable, stable module boundary, HTTP adds nothing the business cares about | acceptance package calling use cases directly |
| **CLI** | The product is a CLI | spawn process, assert stdout/exit code/files |
| **Message / event** | Capability is "when X happens, Y is published" | test broker / in-memory bus, consumer assertions |
| **Contract** | The boundary is consumed by another team/service | [Consumer-driven contracts](https://martinfowler.com/articles/consumerDrivenContracts.html), [Pact](https://docs.pact.io/), OpenAPI/schema tests — see [ContractTest](https://martinfowler.com/bliki/ContractTest.html) |

Pick the **highest** seam that is still fast and trustworthy ([pipeline-fit](../checklists/pipeline-fit.md)).

---

## Practices

- **Assert business outcomes, not transport trivia.** "Order is accepted and total is €12" (status + body field) — not every header, not the exact JSON shape (that is a contract test's job).
- **Observe through the public boundary.** Verify with a follow-up read (`GET /orders/{id}`) rather than querying the DB, unless the DB state *is* the agreed outcome.
- **Given via the side door is fine** here too: seed with factories/[Test Data Builders](http://natpryce.com/articles/000714.html) or setup endpoints; keep only the **When** on the endpoint under test.
- **Auth:** obtain a token once per suite through a test helper; one dedicated scenario covers the auth rule itself (401/403) if it is in the catalog.
- **Isolation & determinism:** unique data per test, injected clock, seeded ids, no order dependence — [Test Desiderata](https://testdesiderata.com/), [Eradicating Non-Determinism](https://martinfowler.com/articles/nonDeterminism.html), [quality-and-flake-control.md](quality-and-flake-control.md).
- **Third parties:** sandbox or manual fake at the owned seam ([`test-strategy-selection.md`](../../../docs/test-strategy-selection.md) §3a); never live production services.
- **Credentials/base URL from env** (dedicated gitignored test env file; base URL overridable per run) — same rules as [e2e-acceptance.md § Test credentials](e2e-acceptance.md#test-credentials-and-secrets).
- **Error examples are first-class:** the catalog's failure cases (validation, conflict, not found) usually live best at this layer, not in E2E.

---

## Gherkin in API mode

Valid when stakeholders read the features. Scenarios must read the same as they would for a UI:

```gherkin
Scenario: Shipping applies above weight threshold
  Given a cart weighing 11 kg
  When the customer checks out
  Then the order total includes a shipping line
```

Step definitions call the test API client — never `Given I POST "/api/cart" with body …` (that is an HTTP script, the API version of a click script).

---

## API review checklist (add to Distill)

- [ ] No browser needed — business outcome observable at this boundary
- [ ] Scenario/test name is business language; no URLs or status codes in Gherkin text
- [ ] Endpoints, headers, payloads live in one test client / driver
- [ ] Outcome verified via public boundary (or DB only when that is the agreed outcome)
- [ ] Data isolated per test; clock/ids deterministic
- [ ] Third parties sandboxed or faked at an owned seam
