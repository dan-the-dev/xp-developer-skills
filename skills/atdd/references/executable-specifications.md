# Executable specifications

An **executable specification** is an automated example that stays **readable** as a description of behavior while proving the system meets agreed outcomes.

---

## Properties of good executable specs

1. **Named for the business** — scenario title or test name states the rule, not the click path.
2. **Outcome-focused** — assert what changed in the world (balance, record, response body field), not internal call counts.
3. **Stable** — survives refactor if behavior is unchanged ([quality-and-flake-control.md](quality-and-flake-control.md)).
4. **Traceable** — links to catalog line and story/ticket.
5. **Minimal setup** — only data required for the example; factories over copy-paste giants.

---

## Readable automation (without ceremony)

**Gherkin** — good when:

- Steps are **domain language** (“user has balance €10”), reused across scenarios.
- Scenarios stay **short** (roughly < 10 steps).

**Code-first** — good when:

- Team already has fluent acceptance APIs.
- Examples in the catalog are the “spec”; test code stays thin.

Both are valid; pick per repo norms, not ideology.

---

## Given / When / Then semantics

| Part | Meaning |
|------|---------|
| **Given** | starting context the business cares about |
| **When** | the event or action under test |
| **Then** | observable outcomes (include “nothing happens” when relevant) |

**Then** must be verifiable without reading production source.

---

## Step definition hygiene (Gherkin)

- Steps express **domain**, not **UI mechanics** (“clicks checkout” → “checks out” unless UI *is* the capability).
- Reuse steps; avoid near-duplicate wording that diverges over time.
- Keep **assertions in Then**, not hidden in When steps.

---

## Contract as executable spec

For services, the “spec” may be:

- consumer expectations (Pact),
- OpenAPI examples + contract tests,
- schema snapshots with agreed fixtures.

The catalog line should still read in **business language**; the contract id/file is the automation reference.

---

## Living documentation

When green in CI, executable specs are **trustworthy docs**. When flaky or ignored, they are **noise**.

Maintain them like production code: delete obsolete scenarios, update examples when rules change, fix wording when the business renames concepts.
