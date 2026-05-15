# Example catalog (acceptance backlog)

The example catalog is a **Markdown file committed in the repository** so the capability slice stays inspectable in PRs and history. It lists **business-visible examples** that define **when the slice is done** for stakeholders — not internal refactors.

---

## Purpose

- Forces **concrete agreement** before or alongside automation (Discuss).
- **Done** for the slice: every in-scope line is `[x]` with an automation reference (or explicitly deferred/removed) **and** acceptance checks are green.
- Captures **new** examples as they appear; nothing ships “by the way” without a line.

---

## Where to put the file

1. **Prefer project convention**  
   Inspect: `AGENTS.md`, `README.md`, `docs/*`, `.cursor/rules`, `features/`, `spec/`, `e2e/`, BDD folders, and existing patterns.

2. **Default**  
   If nothing applies:

   `acceptance-examples/`  
   at the **repository root**.

---

## File naming

Same algorithm as TDD test lists (see `skills/tdd/references/test-list.md`):

1. Read branch: `git branch --show-current`.
2. Strip prefixes: `feature/`, `feat/`, `fix/`, `bugfix/`, `chore/`, `hotfix/`.
3. Replace `/` and `_` with `-`, collapse `-`, lowercase.
4. If branch is generic, use a slug from the **capability title**.
5. Filename: `<stem>.md`  
   Optional ticket prefix: `str-142-order-shipping.md`.

Sibling **follow-ups** (refactor / tech debt only): `<stem>-follow-ups.md`.

---

## What belongs (and what does not)

**Include** — one line per **business-visible example**:

- Scenario in plain language or Given / When / Then.
- Key data values the business cares about (amounts, roles, states).
- Optional: link to story/ticket id.

**Do not include**:

- Refactors, performance tuning, “extract service later.”
- Every unit-test case (those belong in the TDD **test list**).
- Implementation tasks (“add index on column X”) unless the business explicitly tracks them as acceptance.

---

## Format

```markdown
# Example catalog — <short capability title>

Story: <optional ticket / id>
Branch: <optional>
Updated: <optional ISO date>

## Examples

- [ ] Given a cart with items totaling €10, when checkout with €2 shipping, then total charged is €12
- [x] Given … — `features/checkout.feature::Checkout totals` **or** `tests/acceptance/checkout.spec.ts::charges shipping on checkout`

## Deferred examples (not in this slice)

- [ ] <example> — target: <ticket>; agreed <date>

## Removed / out of scope

- <example> — removed <date>; reason: …
```

---

## Traceability

When marking `[x]`:

- Add a pointer to the **automated** check: feature file + scenario, spec file + test name, or contract id.
- Do **not** mark `[x]` for “we discussed it” without automation — unless the slice is explicitly **Discuss-only** with a **Removed** or **Deferred** note and user agreement (spike).

---

## Lifecycle

1. **Create catalog in Discuss** — before Distill for the first example (can be bullets only).
2. **Pick one open `[ ]` line** — Distill to one failing check, then Develop.
3. After acceptance green, flip to `[x]` with reference.
4. **Append** new `[ ]` when the business discovers cases; use **Deferred** / **Removed** for scope changes.

**Slice complete** when in-scope **Examples** are `[x]` or documented, deferred rows are closed per agreement, and suites are green.

---

## Relationship to TDD test list

| File | Role |
|------|------|
| `acceptance-examples/<stem>.md` | What the **business** must see working |
| `test-lists/<stem>.md` | What **programmer tests** will prove during inner TDD |

Same stem is fine when one slice maps 1:1 to one branch. Different stems are fine when one story spans multiple inner lists.

---

## Anti-patterns

- No on-disk catalog (examples only in chat).
- Mixing refactor lines into **Examples**.
- `[x]` without automation reference.
- Silent deletion without **Removed** section.
- Duplicating the entire catalog verbatim inside Gherkin **and** the md file without a single source of truth — pick one primary human-readable home.
