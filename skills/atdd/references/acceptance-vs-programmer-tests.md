# Acceptance tests vs programmer tests

Two loops, two questions. Confusing them creates slow suites, duplicated assertions, or false confidence.

---

## Questions each layer answers

| Layer | Primary question | Typical owner | Speed |
|-------|------------------|---------------|-------|
| **Acceptance** | Did we build the **right thing** for the business? | Whole team (examples) | Slower |
| **Programmer (unit)** | Is each piece **well built** and easy to change? | Developers | Fast |

Kent Beck’s framing: **customer tests** vs **programmer tests** — same idea, different granularity.

---

## What belongs in acceptance

- **Outcomes** the business can name (balances, emails sent, visible states).
- **Rules** that define story done.
- **Cross-cutting** paths that prove wiring (one thin path through UI/API/contract).

**Pragmatic:** a **contract test** *is* acceptance when the story is “consumer can rely on this API shape and behavior.”

---

## What belongs in programmer tests

- Algorithms, branches, and edge cases **cheaper** to run at unit level.
- Refactoring safety net **close** to the code changing.
- Cases that would make acceptance tests **slow or brittle** if duplicated.

---

## Composition rules (pragmatic)

1. **One business rule, one home** — assert the rule strongly at the **lowest trustworthy layer**, then don’t copy the same assertion everywhere.
2. **Acceptance proves the example** from the catalog; **unit tests** prove design and fine-grained edges.
3. If acceptance is **coarse** (full browser), units cover **logic**; acceptance covers **integration of value**.
4. If acceptance is a **contract**, units cover **provider internals**; contract covers **published promise**.

---

## Double counting

**Anti-pattern:** ten unit tests and one acceptance test all asserting “total = 12” with no additional signal.

**Better:** acceptance checks “checkout charges €12 for this scenario”; units check tax rounding, currency conversion, or empty-cart guard.

---

## When acceptance is “too low”

If acceptance only hits a **private helper** or a **mocked** stack with no business seam, it is a **slow unit test** — move down the pyramid or raise the seam ([environments-and-test-pyramid.md](environments-and-test-pyramid.md)).

---

## Skill boundaries

- **This skill** — catalog, Distill, Develop, layer choice.
- **`skills/tdd`** — Three Laws, test list, R–G–R micro-cycles.
- **`skills/bugfix`** — regression on broken behavior, not new capability.

Compose; do not merge into one undifferentiated “test everything” skill.
