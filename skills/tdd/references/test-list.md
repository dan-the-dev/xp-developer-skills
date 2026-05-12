# Test list (feature backlog of cases)

Before the **first** RED of a feature, maintain an explicit **test list**: every test case you can think of **up front** for that feature slice, written as short, checkable lines (not full test code yet).

---

## Purpose

- Forces **inventory** of behavior before coding.
- Gives a **done** criterion for the feature: the list is empty of open items (everything implemented) or, equivalently, every item is marked **done**.
- Captures **new** cases as they occur during development instead of forgetting them.

---

## Rules

1. **Create the list first** — before writing the first failing test for the feature.
2. **Pick one item** — translate the next open item into **one** minimal failing test (Law 2: only enough test to fail).
3. **Run R–G–R** for that test; when the increment is integrated per skill, mark that item **done** on the list.
4. **Add items** whenever a new edge case, error path, or example comes to mind; do not silently expand scope without listing it.
5. **Feature complete** when every item on the list is **done** and the suite is green — no hidden “just one more thing” without a listed case.

---

## Format (suggested)

Use a simple markdown checklist the agent updates in the **session summary** (and in a repo file only if the team wants it, e.g. `TEST_LIST.md` on the feature branch):

```markdown
## Test list — <feature name>

- [ ] case: …
- [x] case: … (implemented)
- [ ] case: …
```

Optional tags: `blocked`, `deferred` with a one-line reason — but **deferred** is not **done**; the job is not finished until deferred items are resolved or explicitly removed by agreement.

---

## Relationship to the Three Laws

The list is **planning**; each cycle still obeys: minimal test to fail → minimal code to pass → refactor. The list prevents speculative production code (Law 1) by tying every change to a named case you will turn into a test.

---

## Anti-patterns

- Starting RED without any list (unless the slice is truly trivial — then write a **two-line** list: main case + “nothing else”).
- Marking items done before the automated test exists and passes.
- Leaving the list stale (done markers or new cases not updated).
