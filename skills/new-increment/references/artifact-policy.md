# Artifact policy (avoid documentation theater)

Markdown artifacts must **drive** the next RED step, not **record** work already batched in code.

---

## Default: one test list per feature

| Artifact | Path | When |
|----------|------|------|
| Increment backlog | `increments/<feature-stem>.md` | Always (from **new-feature**) |
| Test list | `test-lists/<feature-stem>.md` | **One file per feature**, not per increment |

Structure the test list with a **section per increment** (heading = increment slug). Add `[ ]` behavior lines only for **this** increment’s scope while that slice is open.

**Do not** create `test-lists/plain-number.md`, `test-lists/fizz-for-three.md`, etc., unless the team already uses that convention in the repo.

Parent backlog lines link to the feature test list and section, e.g.:

```markdown
- [x] Plain number (1 → "1") — `test-lists/fizzbuzz.md` (§ plain-number)
```

---

## When to add acceptance artifacts

Use **`skills/atdd`** only when the increment has a **real outer seam** the business cares about separately from units:

- HTTP/API, browser/UI, message bus, or **contract** boundary
- A deployable walking skeleton (thin vertical through the boundary)

**Do not** add `acceptance-examples/` or `*.acceptance.test.ts` that call the same in-process class with the **same assertions** as unit tests — that duplicates the pyramid without value.

| Situation | Outer loop | Inner loop |
|-----------|------------|------------|
| Library, domain class, kata in one package | **TDD only** (`skills/tdd`) | Unit (or narrow integration) tests |
| Owned third-party API client / adapter | **TDD** on the client ([`test-strategy-selection` §3a](../../../docs/test-strategy-selection.md)) | Sandbox when feasible; else manual fake/stub — not a separate acceptance catalog unless business AC lives at that boundary |
| Service with HTTP contract | ATDD at API + example catalog | TDD below the controller |
| Full UI story | ATDD at UI or contract + catalog | TDD for domain |

If unsure: **start with TDD only**; add ATDD when a stable outer seam appears.

When ATDD applies, prefer **one** `acceptance-examples/<feature-stem>.md` with **sections per increment**, not one file per slice.

---

## Honest checklist lines

- Lines stay `[ ]` until a **failing** automated test exists for that behavior (RED observed).
- Flip to `[x]` only after GREEN, with a **test reference** on the line.
- **Forbidden:** creating a catalog or test list already full of `[x]` before tests exist.
- **Forbidden:** one assistant turn that marks multiple increment sections done without RED between behaviors.

---

## Cleanup (reduce file noise)

**After one increment is done**

- Do not add new markdown files “for completeness.”
- If you accidentally created per-increment `test-lists/<slice>.md` files, **merge** behaviors into `test-lists/<feature-stem>.md` and **delete** the slice-only files in the same change set.

**After the whole feature is done** (last increment or explicit user request)

- Keep `increments/<feature-stem>.md` (history of slices).
- Keep `test-lists/<feature-stem>.md` if it still helps reviewers; optional trim of empty sections.
- **Delete** redundant per-increment markdown that only duplicates what tests already express.
- **Delete** `acceptance-examples/` slice files if acceptance was never run at a distinct layer.
- **Do not** delete automated tests — only redundant **planning** markdown.

---

## Minimum viable tracking

For a trivial slice (one behavior, solo dev):

- Updating the **increment backlog line** and **one `[ ]` → `[x]`** in `test-lists/<feature-stem>.md` is enough.
- Skip separate “example catalog” prose when TDD alone proves the slice.
