# ATDD checklist — pipeline fit (choose layer)

Answer **before** Distill. Pick the **highest** layer that still meets trust and speed needs — not always E2E.

---

## Questions

| Question | If yes → consider |
|----------|-------------------|
| Is the deliverable an **API/event contract** to another team? | **Contract** tests |
| Can the business rule be verified via **HTTP/API** without a browser? | **API acceptance** |
| Is logic inside one deployable with a clear **module seam**? | **In-process acceptance** |
| Is the capability **only** visible through UI with no lower seam? | **E2E / browser** |
| Is feasibility still unknown (library, integration, performance)? | **`skills/spike`** on `spike/` branch first, then ATDD after promotion |

---

## Decision record (fill in)

- [ ] Story/capability: ___
- [ ] Chosen layer: contract | API | in-process | E2E | discuss-only (defer)
- [ ] Why this layer: ___
- [ ] What we are **not** automating in this slice: ___

---

## Red flags (reconsider layer)

- [ ] E2E chosen but **no** UI change in story
- [ ] Contract absent for **only** integration point between services
- [ ] Acceptance test imports **production DB** without isolation
- [ ] Expected runtime > team PR budget without `@smoke` split
- [ ] Same assertion already in **fast** unit test — acceptance adds no seam crossing

---

## Pragmatic defaults

1. **Contract** at service boundaries when consumers exist.
2. **API acceptance** for backend-heavy stories.
3. **One thin E2E** per capability when UI matters — not per field validation.
4. **Unit TDD** for algorithms and branches — compose with `skills/tdd`.
5. **Mutation / property-based** when configured and slice warrants it — see [`test-strategy-selection.md`](../../../docs/test-strategy-selection.md); not a substitute for outer layer choice above.
