# Scoped delivery per increment

Pick **one** outer/inner strategy for this backlog line. Do not stack duplicate layers.

**Before choosing:** complete the test strategy decision in [`docs/test-strategy-selection.md`](../../../docs/test-strategy-selection.md) — unit TDD is the default **inner** loop, not the only practice to evaluate (mutation, property-based, integration, contract, component, etc.).

---

## Decision (pick one row)

| Backlog slice looks like… | Use | Artifacts |
|---------------------------|-----|-----------|
| Domain logic, class, kata, in-process module | **TDD only** (+ **mutation** when branchy — introduce on greenfield) | `test-lists/<feature-stem>.md` (§ this increment) + unit tests (+ mutation config/run if adopted) |
| Branchy/critical rules (pricing, auth, validation) | **TDD + mutation** (configure if greenfield) | Unit tests + mutation run on touched scope |
| Invariants / parsers / serializers | **TDD + property-based** when rules exceed fixed examples | Unit + property tests |
| DB/repository wiring | **TDD + narrow integration** | Unit at seam + integration if project uses Testcontainers/DB tests |
| **Owned third-party API client / adapter** | **TDD** on the client; **sandbox** when feasible else **manual fake/stub** ([`test-strategy-selection.md`](../../../docs/test-strategy-selection.md) §3a) | Prefer vendor SDK in production; test list behaviors for mapping/errors; strategy rows for sandbox + fake |
| API/HTTP/CLI user-visible contract | **ATDD + TDD** (Gherkin only if team reads features) | `acceptance-examples/<feature-stem>.md` (§ slice) + acceptance tests at boundary + TDD inside |
| UI journey | **ATDD + TDD** | Catalog + UI/contract tests + TDD |
| Feasibility unknown | **`skills/spike`** first | Promote, then return here |

**Rule:** If acceptance tests would import the same module and assert the same values as unit tests, use **TDD only**.

---

## TDD-only order (default)

1. Add `[ ]` behavior lines under this increment’s section in `test-lists/<feature-stem>.md`.
2. **RED:** add **one** test; run runner; confirm failure in transcript.
3. **GREEN:** minimal production; run; confirm pass.
4. **REFACTOR** (optional): small steps, tests green after each.
5. Mark the behavior `[x]` with test reference; repeat for next behavior in **this increment only**.
6. Run **all** applicable verify steps (including adopted mutation); **all green**.
7. Mark parent `increments/…` line `[x]`; **commit**; **stop** (never start the next backlog line).

See `skills/tdd/SKILL.md` for Three Laws, commits, and anti-patterns.

---

## ATDD + TDD order (outer seam only)

1. **Discuss** (lightweight if solo): agree **one** example for this slice; record under `acceptance-examples/<feature-stem>.md` (§ slice) as `[ ]`.
2. **Distill — RED:** one **failing** acceptance check at the boundary (HTTP, UI, contract — not duplicate unit layer).
3. **Inner TDD:** `test-lists/<feature-stem>.md` + R–G–R until acceptance can pass.
4. **GREEN:** acceptance check passes; mark catalog line `[x]`.
5. Parent backlog `[x]`; run full verify (green); **commit**; **stop**.

Do **not** add parallel unit tests that copy the same assertions as the acceptance test unless they test **finer** behavior worth fast feedback.

---

## RED gate (mandatory)

Before **any** production edit in this increment:

- Run tests and capture output showing **failure** for the behavior you just added.
- If the suite is already green, you did not RED — add or fix the test first.

Before marking any markdown line `[x]`:

- The linked automated test must exist and pass.

---

## Scope fence

- Only examples and behaviors for **this** backlog line.
- No production code or tests for **future** lines.
- No phrase “implementing increments 2–7” — one line per invocation.

See [artifact-policy.md](artifact-policy.md).
