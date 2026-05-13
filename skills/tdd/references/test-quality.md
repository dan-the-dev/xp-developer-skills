# Test quality — structure, names, and clarity

These rules support the **Three Laws**: every failure should be **obvious** and **local**; tests should read as **executable specification**.

---

## Arrange–Act–Assert (or equivalent)

Structure each test so a reader can scan it in three phases:

1. **Arrange**: minimal context — data, system under test, collaborators (real or double).
2. **Act**: **one** call or operation that triggers the behavior under test.
3. **Assert**: outcomes and contracts that matter to callers — not internal steps.

If Arrange grows large, treat it as a **design signal** (see [behavior-and-tests.md](behavior-and-tests.md)) and extract **named helpers or builders** in test code only, still keeping one clear Act.

---

## Names as specification

- Test names (or nested `describe` / context labels) should state **expected behavior** under a **condition**: e.g. `rejects order when inventory is empty`, not `testOrder1`.
- Prefer language close to the domain and the test list line you are implementing.

---

## No “test logic”

Avoid non-trivial **conditionals, loops, and try/catch** in tests unless the framework forces a pattern.

- Do not branch assertions on runtime state to “maybe” assert — split into **two tests** or two list items.
- Avoid random data unless the behavior under test **is** randomness and you control the seed.

Complexity in tests hides **why** RED happened and breaks Law 2’s goal: always know the smallest failing increment.

---

## One primary behavior per test

One failing test should usually prove **one** rule or example (aligned with the test list line). Multiple unrelated assertions obscure the first failure; prefer another RED cycle for the next assertion.

---

## Links to other references

- **Determinism and environment**: [behavior-and-tests.md](behavior-and-tests.md) (determinism section).
- **Seam choice and doubles**: [behavior-and-tests.md](behavior-and-tests.md) (test shape and doubles).
- **Refactor test code too**: [refactor-discipline.md](refactor-discipline.md).
