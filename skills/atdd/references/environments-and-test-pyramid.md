# Environments and test pyramid (pragmatic layering)

Acceptance tests should prove **business outcomes** at the **highest layer that is still fast and trustworthy enough** for the team. Dave Farley’s CD framing: acceptance checks answer whether the change is **fit to release** for the agreed examples — not whether every brick was mortared twice.

---

## Pyramid (conceptual)

```text
        ┌─────────────┐
        │  Few, slow  │  Full E2E / browser / full stack
        │  acceptance │
        ├─────────────┤
        │  Some       │  API / in-process acceptance / contract
        ├─────────────┤
        │  Many, fast │  Unit / narrow integration (TDD skill)
        └─────────────┘
```

**Pragmatic:** prefer **more** fast tests and **fewer** full-stack tests; use acceptance to cover **gaps** the business cares about, not every branch.

---

## Layer guide

| Layer | Proves | Typical tooling | When to choose |
|-------|--------|-----------------|----------------|
| **Contract** | Published API/event promise to consumer | Pact, schema tests, OpenAPI examples | Microservice boundary **is** the story |
| **API / HTTP acceptance** | Application behavior without browser | REST client tests, supertest, httpx | Business rules live behind API |
| **In-process acceptance** | Module boundary in same deployable | acceptance test package, test server | Stable seam, no browser needed |
| **E2E / UI** | Full user journey | Playwright, Cypress, WebDriver | UI **is** the capability or no lower seam exists |

---

## Production-like environments (pragmatic)

- Run acceptance in **CI** on environment **close enough** to catch config and wiring issues.
- Do **not** block every inner TDD cycle on full docker-compose unless the team accepts the cost.
- **Smoke** subset (`@smoke`) for fast PR feedback; full acceptance on main/nightly if needed.

---

## Walking skeleton

First example through Distill should be the **thinnest vertical slice**:

- one API call, or
- one browser path with minimal pages, or
- one contract interaction.

Expand catalog after first green path — avoids a week of red E2E.

---

## Pipeline placement (not a CI tutorial)

| Check type | Typical stage |
|------------|----------------|
| Unit (TDD) | every commit, seconds |
| Contract / API acceptance | PR / merge queue, minutes |
| Full E2E | PR or post-merge, longer |

If acceptance is **always red** and ignored, it is not in the pipeline — it is decoration. Fix or delete.

---

## Wrong layer symptoms

- **Unit test pretending to be acceptance** — asserts business rule but never crosses a seam the business recognizes.
- **E2E for every branch** — suite > 15 minutes, flaky, skipped.
- **Contract missing** when teams integrate only via events/API — production surprises.

Use [checklists/pipeline-fit.md](../checklists/pipeline-fit.md) before Distill.
