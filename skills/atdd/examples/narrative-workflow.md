# Narrative example — pragmatic ATDD with inner TDD (language-agnostic)

Story, not live code. Replace paths and commands with project-native ones.

---

## Capability slice

**Checkout shipping:** orders above 10 kg include a shipping line in the total.

---

## Discuss — example catalog first

Create **`acceptance-examples/order-shipping-by-weight.md`** (unless the repo defines another folder).

```markdown
# Example catalog — shipping by weight

## Examples

- [ ] Given a cart weighing 11 kg, when the customer checks out, then the order total includes a shipping line
- [ ] Given a cart weighing 9 kg, when the customer checks out, then the order total has no shipping line
- [ ] Given a cart weighing exactly 10 kg, when the customer checks out, then (agree: shipping applies or not)
```

Agree with business: threshold is **strictly greater than** 10 kg for shipping.

---

## Distill — first example (acceptance RED)

**Pipeline fit:** business rule is calculable in the **order domain** — team chooses **API acceptance** (POST checkout) instead of full browser for speed.

Write the smallest failing check, e.g.:

- `tests/acceptance/checkout.spec.ts::includes shipping when weight above 10kg`
- or Gherkin scenario linked from catalog

Run → fails: total has no shipping line (or 404 if endpoint missing).

Optional commit: `test: acceptance for shipping over 10kg threshold`

---

## Develop — inner TDD + acceptance GREEN

Create **`test-lists/order-shipping-by-weight.md`** for programmer tests (see `skills/tdd`).

Inner cycles (abbreviated):

1. Unit: shipping line appears in total calculation for weight 11 → green.
2. Unit: no shipping for weight 9 → green.
3. Wire HTTP handler → acceptance re-run → **green**.

Update catalog:

```markdown
- [x] Given a cart weighing 11 kg, … — `tests/acceptance/checkout.spec.ts::includes shipping when weight above 10kg`
```

Refactor helpers when acceptance **and** units are green.

---

## Second example

Pick next open `[ ]` line (9 kg). Repeat Distill → Develop; do not start until first acceptance is green (unless scope explicitly changed).

---

## Pragmatic variant note

If this capability were **only** a published REST contract to another service, **Distill** might be a **Pact** or schema test instead of HTTP acceptance — catalog line still describes the business rule; reference points to contract id.

---

## Slice complete

- All in-scope catalog lines `[x]` with references.
- Acceptance smoke + unit suite green.
- Deferred boundary case (10 kg) either implemented, deferred with ticket, or in **Removed** with reason.
