# Squash micro-commits and push

After **RED → GREEN → REFACTOR**, collapse the **local** micro-commits into **one** commit before pushing.

---

## Goal

- Preserve **story** during development (`test:` → `feat:` or `fix:` → `refactor:`).
- Publish **one** cohesive commit per completed cycle, titled like the **GREEN** commit (`feat:` or `fix:`).

---

## Safe mechanics (typical)

When the cycle produced **exactly three** commits on top of the previous pushed tip:

```bash
# Example: squash last 3 commits into one
git reset --soft HEAD~3
git commit -m "feat: <same intent as green commit>" -m "Optional body: tests added; refactor notes."
# If GREEN used fix: (bug/regression), use that as the squashed title instead, e.g.:
# git commit -m "fix: <same intent as green commit>" -m "..."
git push
```

Adjust `HEAD~3` if the cycle legitimately had more micro-commits (e.g. amend fixes) — squash **all** commits belonging to that single R-G-R cycle.

---

## Message alignment

- **Primary title** mirrors the GREEN subject: **`feat:`** for new behavior, **`fix:`** when the failing test encodes a **bug** or **regression** in existing behavior (polish allowed, meaning must match).
- Do **not** lead with `test:` or `refactor:` in the squashed title; the squashed commit represents **delivered behavior** (or a corrective fix).

---

## Conflicts and collaboration

- If others may have pulled the branch **before** squash, coordinate: rewriting published history needs agreement. This skill assumes **local-only** micro-commits or a **private** branch segment.
- If squash is not possible (policy), stop and ask the user; do not violate repository rules.

---

## Verification after squash

Run the same test scope used at the end of REFACTOR (or broader if shared code changed).
