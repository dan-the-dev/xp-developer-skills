# Collaboration and examples (Discuss)

ATDD succeeds when **examples** replace ambiguous requirements. The Discuss phase is facilitation, not a meeting template.

---

## Triad (three amigos)

Typical perspectives:

- **Business** — value, rules, priorities, what “wrong” looks like.
- **Development** — feasibility, seams, data, incremental delivery.
- **Testing / quality** — edge cases, failure modes, observability, what could break silently.

On small teams one person may wear multiple hats; the skill still requires **explicit** example agreement, not assumed alignment.

---

## Questions that produce good examples

- “Show me the **simplest** case that would make you say this works.”
- “What **data** would you use in a demo?”
- “What should happen if …?” (only for rules the business cares about **now**).
- “How would you **manually** verify this on day one?”
- “What would make you **reject** the release?”

Avoid:

- “Write all requirements upfront.”
- Abstract nouns without instances (“handle errors properly”).

---

## Example shapes

### Given / When / Then (informal)

Fine in the catalog before Gherkin:

```text
Given a registered user with balance €10
When they buy coffee for €2
Then balance is €8
```

### Tables (decision or examples)

| weight (kg) | shipping included? |
|-------------|-------------------|
| 9           | no                |
| 10          | (agree boundary)  |
| 11          | yes               |

### Plain scenario

“Order over €50 gets free shipping; under €50 pays €5.”

---

## Narrowing scope (pragmatic)

- Ship **one example** through Distill → Develop before expanding the catalog.
- Move “nice to have” examples to **Deferred examples** with a ticket target.
- Record disagreements in **Removed** with reason — do not leave silent ambiguity.

---

## Glossary and data

Agree on:

- **Terms** (customer vs user vs account).
- **Identifiers** (currency, timezone, locale).
- **Starting state** (empty cart vs seeded cart).

Mismatch here causes green tests that still disappoint the business.

---

## When Discuss-only is acceptable

Explicitly label the slice (in catalog or PR):

- **Spike** — learning; automation deferred with date/owner.
- **UI prototype** — no business rules yet.
- **Contract negotiation** — examples exist but automation waits on partner.

Do not use Discuss-only to skip automation on production-bound features without agreement.
