# Increment done

- [ ] Exactly **one** backlog line in scope this invocation
- [ ] **Test strategy table** completed before first RED ([`test-strategy-selection.md`](../../../docs/test-strategy-selection.md)) — mutation/ATDD evaluated; greenfield tooling introduced when adopted **and** threshold met (teaching/kata may skip with reason)
- [ ] Layer chosen: TDD-only (default) or ATDD+TDD with real outer seam; specialized techniques adopted if warranted (mutation, property-based, integration)
- [ ] `test-lists/<feature-stem>.md` — this increment’s section updated; lines `[x]` only with passing test refs
- [ ] **RED observed** before each production change
- [ ] **No** duplicate acceptance + unit tests for same behavior
- [ ] **All project verify steps** for this scope run and **passed** ([`docs/delivery-process.md`](../../../docs/delivery-process.md) §2; [`docs/project-verification.md`](../../../docs/project-verification.md)) — tests, lint, format, SonarQube, adopted mutation/contract/etc.
- [ ] **Hard green gate** — no applicable verify step left red
- [ ] Re-ran affected tests after every meaningful edit during the increment
- [ ] **Change-surface search** done if construction/import/API changed (§3)
- [ ] Parent `increments/…` **one** line `[x]` with links
- [ ] Work **committed**; SHAs in return payload
- [ ] Redundant per-slice markdown merged/deleted if created
- [ ] **Return payload** includes verification results, **test strategy table**, commits, and RED count ([`docs/delivery-process.md`](../../../docs/delivery-process.md) §10)
- [ ] **Stopped** — did not start the next backlog line
