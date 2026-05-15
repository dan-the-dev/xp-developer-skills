---
name: atdd
description: Pragmatic Acceptance Test-Driven Development — agree concrete examples with stakeholders (Discuss), capture them as executable acceptance checks (Distill), then implement with outside-in delivery (Develop). Supports Gherkin/Cucumber when it helps, code-first acceptance tests, and contract tests at service boundaries. Composes with the inner-loop TDD skill for programmer tests. Use when defining story done, writing acceptance or executable specifications, or aligning business examples with automation before feature code.
allowed-tools: Read, Edit, MultiEdit, Bash, Grep, Glob
---

# Pragmatic ATDD (outside-in)

## Mission

Turn **business intent** into **concrete, automated examples** before (or as) the team builds the feature — so programmers and stakeholders mean the **same thing** when they say “done.”

**First step of every capability slice:** agree **examples** (scenarios, tables, or outcomes) and record them in a **tracked artifact** in the repo (path rules in [references/example-catalog.md](references/example-catalog.md)).

**Distill step:** turn the highest-value examples into **at least one failing automated acceptance check** at the right layer (see [references/environments-and-test-pyramid.md](references/environments-and-test-pyramid.md)) — unless the slice is explicitly **example-only** (spike, UI mock) with a written deferral.

**Develop step:** make acceptance green using **outside-in** work; use **strict TDD** (`skills/tdd`) for inner-loop programmer tests.

Optimize for:

- **shared understanding** (examples beat abstract requirements)
- **executable definition of done** (automated where practical)
- **right layer** (contract or narrow acceptance over slow full-stack when that still proves the business outcome)
- **living documentation** readable by non-programmers when possible
- **composition** with inner TDD — not duplication at every layer

This skill covers the **outer** acceptance loop. It does **not** replace unit TDD, bugfix workflows, CI pipeline design, or product discovery — compose with other skills for those.

---

## Discuss → Distill → Develop (pragmatic)

### 1. Discuss — agree examples

**Who:** business representative, developer, and someone who thinks about quality (the “triad” / three amigos) — roles can be played by the same person on small teams.

**Output:** concrete **examples** with agreed **data**, **terminology**, and **boundaries** — not a long specification document.

Practices:

- Start from a **user story** or capability and ask: “How would we **manually** check this is right?”
- Capture **happy path**, **important edges**, and **failure** the business cares about now.
- Use **tables** or **Given / When / Then** language when it helps clarity; plain bullet examples are fine.
- Record outcomes in the **example catalog** file before coding (see reference).

See [references/collaboration-and-examples.md](references/collaboration-and-examples.md).

### 2. Distill — automate the agreement

Transform agreed examples into **executable** checks:

| Approach | When (pragmatic) |
|----------|------------------|
| **Gherkin + runner** (Cucumber, SpecFlow, pytest-bdd, etc.) | Stakeholders will read scenarios in PRs; team already uses BDD tooling |
| **Code-first acceptance** (Playwright, API tests, RSpec feature specs) | Faster for the team; examples stay in catalog + test names/assertions |
| **Contract tests** (Pact, schema/contract suites, consumer-driven contracts) | **Service boundary** is the capability; business outcome is “honors agreed contract” |
| **Narrow acceptance** (HTTP against app, in-process acceptance module) | Full E2E is slow/flaky but **business rule** can be proven at a stable seam |

Rules:

- Prefer **one** failing acceptance check that proves the **next** agreed example — not a suite of ten scenarios upfront.
- The check must **fail for the right reason** (missing behavior), not environment noise — see [references/quality-and-flake-control.md](references/quality-and-flake-control.md).
- **Do not** block Distill on perfect Gherkin if code-first is the repo norm — keep the **catalog** as the human-readable source of truth.

See [references/discuss-distill-develop.md](references/discuss-distill-develop.md) and [references/gherkin-and-bdd-tooling.md](references/gherkin-and-bdd-tooling.md).

### 3. Develop — outside-in, then inner TDD

1. **Acceptance RED:** failing automated check for the current example.
2. **Inner loop:** use `skills/tdd` — test list + R–G–R — to grow production code until acceptance can pass.
3. **Acceptance GREEN:** run the acceptance check; widen scope only when touching shared setup.
4. Repeat for the **next open example** in the catalog.

Refactor when **acceptance and programmer tests are green**; keep acceptance assertions at **outcomes**, not incidental UI structure.

See [references/executable-specifications.md](references/executable-specifications.md) and [references/acceptance-vs-programmer-tests.md](references/acceptance-vs-programmer-tests.md).

---

## Example catalog (mandatory)

The catalog is a **Markdown file** in the repo listing **business-visible examples** for the slice — the outer-loop counterpart to TDD’s test list.

Before **Distill** (automation) for a slice:

1. **Choose folder:** project convention, else `acceptance-examples/` at repo root (see [references/example-catalog.md](references/example-catalog.md)).
2. **Create** `<stem>.md` from branch and/or feature name (kebab-case).
3. List each example as `[ ]` with **Given / When / Then** or a short scenario + key data.
4. During work: flip to `[x]` when an **automated acceptance check** exists, passes, and is **referenced** on the line.
5. Slice **done** when agreed examples are `[x]` (or documented as deferred/removed) and relevant suites are green.

Refactor-only or internal tech tasks **do not** belong in the catalog — use a sibling `-follow-ups.md` or the closing reply (same pattern as TDD test list).

---

## Relationship to TDD (inner loop)

| Concern | ATDD (this skill) | TDD (`skills/tdd`) |
|---------|-------------------|---------------------|
| Question | “Did we build the **right thing** for the business?” | “Is each unit **well built**?” |
| Granularity | Story / capability / boundary | Class / module / function |
| Artifact | Example catalog + acceptance checks | Test list + unit tests |
| Audience | Business-readable examples | Programmers |

**Compose:** one acceptance example → inner TDD until green → next example. Do **not** re-assert every business rule in unit tests if acceptance already proves it at a stable seam — unit tests should cover **design pressure**, edges the acceptance layer is too coarse to catch, and **fast feedback** on logic.

---

## Language-agnostic execution

Adapt to the repository:

- detect existing acceptance, BDD, E2E, or contract tooling
- follow project layout for features, specs, and tags
- run the **smallest** acceptance command that covers the current example

Never assume Cucumber, Playwright, or a specific folder; inspect first.

Tooling orientation: [references/gherkin-and-bdd-tooling.md](references/gherkin-and-bdd-tooling.md).

---

## Pragmatic commit flow

Match team conventions when they exist. Default story for a **single acceptance example**:

| Step | Typical content | Suggested prefix |
|------|-----------------|------------------|
| Distill (RED) | acceptance spec / scenario / contract only | `test:` |
| Develop (GREEN) | production + any glue to pass acceptance | `feat:` |
| Refactor | structure, step defs, helpers — behavior unchanged | `refactor:` |

Squash per team policy (many teams squash per story; TDD skill squashes per **unit** cycle — do not mix the two rhythms in one commit message without intent).

Inner **unit** cycles still follow `skills/tdd` micro-commits when that skill is active.

---

## Anti-patterns (summary)

- Coding before **any** agreed example (surprise delivery).
- **UI click scripts** masquerading as business scenarios (see Gherkin reference).
- **One giant E2E** as the only acceptance test for a large story.
- **Duplicating** every acceptance assertion in dozens of unit tests.
- **Flaky** acceptance that the team ignores (definition of done erodes).
- Catalog lines marked `[x]` without a **test reference** or passing automation.
- Using acceptance tests for **all** regression (wrong layer — use unit/integration too).

Full list: [references/anti-patterns.md](references/anti-patterns.md).

---

## Definition of done

### One acceptance example

- Example agreed in **Discuss** and recorded in the catalog.
- **Distill:** failing automated check at chosen layer; failure is intentional.
- **Develop:** acceptance green; inner TDD test list items for this example are `[x]` or explicitly deferred.
- Catalog line `[x]` with **automation reference** (path, scenario name, or contract id).

### Capability slice

- Example catalog file exists and was maintained through the slice.
- All **in-scope** examples `[x]` or documented under **Deferred** / **Removed**.
- Acceptance suite (and unit suite, if composed) green.
- No undeclared business behavior shipped.

Checklists: [checklists/story-readiness.md](checklists/story-readiness.md), [checklists/scenario-and-test-quality.md](checklists/scenario-and-test-quality.md), [checklists/pipeline-fit.md](checklists/pipeline-fit.md).

---

## Output format

```markdown
## Capability: <name>

### Example catalog
- Path: `<e.g. acceptance-examples/order-shipping-threshold.md>`
- Branch / slug: <optional>

### Examples (excerpt; source of truth is the file)
- `[x]` lines must show automation back-reference

### Discuss → Distill → Develop (latest example)

#### Discuss
- Agreed example: <one line>
- Data / terms: <bullets>

#### Distill (acceptance RED)
- Check: <file::scenario or test name>
- Layer: <e2e | api | contract | in-process>
- Failure: <short message>

#### Develop
- Inner TDD: <test list path, cycles summary or "composed with tdd skill">
- Acceptance: <command scope> — green

### Commits (if applicable)
- test: … / feat: … / refactor: …

### Slice status
- Catalog: `<path>` — all `[x]` | N open
- Follow-ups: `<path or "in closing reply">`
```

---

## Additional resources

### References

- [references/example-catalog.md](references/example-catalog.md)
- [references/collaboration-and-examples.md](references/collaboration-and-examples.md)
- [references/discuss-distill-develop.md](references/discuss-distill-develop.md)
- [references/acceptance-vs-programmer-tests.md](references/acceptance-vs-programmer-tests.md)
- [references/executable-specifications.md](references/executable-specifications.md)
- [references/gherkin-and-bdd-tooling.md](references/gherkin-and-bdd-tooling.md)
- [references/environments-and-test-pyramid.md](references/environments-and-test-pyramid.md)
- [references/quality-and-flake-control.md](references/quality-and-flake-control.md)
- [references/anti-patterns.md](references/anti-patterns.md)

### Examples

- [examples/narrative-workflow.md](examples/narrative-workflow.md)
- [examples/gherkin-scenario-good-bad.md](examples/gherkin-scenario-good-bad.md)

### Checklists

- [checklists/story-readiness.md](checklists/story-readiness.md)
- [checklists/scenario-and-test-quality.md](checklists/scenario-and-test-quality.md)
- [checklists/pipeline-fit.md](checklists/pipeline-fit.md)

## Resource usage

Open reference files when layer choice, catalog format, Gherkin quality, or acceptance vs unit boundaries are unclear.
