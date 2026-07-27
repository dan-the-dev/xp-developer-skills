---
name: new-feature
description: Slice a whole capability into ordered releasable increments (increment backlog in increments/<stem>.md). Delegate each slice to skills/new-increment — do not implement slices yourself. Default step mode stops after each increment for feedback; automatic mode (explicit opt-in) continues until the backlog is done. Use for an entire feature or epic (e.g. full FizzBuzz), not for implementing one increment.
allowed-tools: Read, Edit, MultiEdit, Bash, Grep, Glob
---

# New feature (increment planning + orchestration)

## Mission

Plan a **whole feature** as **ordered, releasable increments**. **Do not implement** slices in this skill — each open line is delivered by **`skills/new-increment`** (or the **`new-increment`** subagent) in a **separate** invocation.

**First step:** create **`increments/<feature-stem>.md`** (see [references/increment-backlog.md](references/increment-backlog.md)).

**Feature complete** when every in-scope increment is `[x]` on that backlog — each line completed via **`new-increment`**, not by implementing in this session.

---

## Orchestration modes

| Mode | Activation | Behavior |
|------|------------|----------|
| **Step** (default) | Assumed unless the user **explicitly** opts into automatic | After each increment → **full** post-increment review → **stop** for user feedback |
| **Automatic** | Explicit only — e.g. “modalità automatica”, “automatic mode”, “implement the whole feature”, “run until the backlog is done” | After each increment → **light** review (default) → if no **blocking** gaps and open `[ ]` remain, hand off the **next** line; if all `[x]`, stop (feature complete) |

**Invariants (both modes):**

1. **`new-increment` always** implements **one** line, runs full verification (all green), **commits on the feature branch**, and **stops**. It never starts the next backlog line or merges to main between increments.
2. **This skill** decides whether to continue or pause — only continues in **automatic** mode, and only when the review did not report **blocking** gaps.
3. After every successful increment, run a **post-increment review** via **`skills/refactoring`** / **`refactoring`** subagent before stopping or continuing.

**Review depth:**

| Depth | When | What |
|-------|------|------|
| **Full** | Step mode (default); or user asked for “full post-increment review” / “review with applies” | Explain, suggest, optional tiny in-surface applies |
| **Light** | Automatic mode default | Explain + suggest-only — **no** applies (keeps long backlogs affordable) |

If the user does **not** name automatic mode, stay in **step**.

---

## Workflow

Shared delivery rules: [`docs/delivery-process.md`](../../docs/delivery-process.md) (orchestration — §1, **§1a feature branch**, §10).

1. Clarify capability and whole-feature definition of done.
2. Resolve **orchestration mode** (step vs automatic) from the user request; state it in the return payload.
3. If feasibility unknown → **`skills/spike`** on `spike/…` branch; promote before slicing.
4. Write **ordered** increment lines in `increments/<stem>.md` (all `[ ]` initially). Optionally note **expected test layers** per line (see [`test-strategy-selection.md`](../../docs/test-strategy-selection.md) §2) — e.g. “mutation likely”, “ATDD at API”, “property-based”.
5. Ensure a **single feature branch** exists and is the working branch: `feat/<feature-stem>` (create from the default base if missing). Pass this branch name when handing off to **`new-increment`**. Do **not** ask for a new branch per increment or merge to main between increments (§1a) — goal is **one PR for the feature**.
6. **Loop** (one open line at a time):
   1. Hand off the **next** open line to **`new-increment`** (subagent or new chat) **on the same feature branch**. Do **not** implement it here.
   2. Wait for return payload: backlog `[x]`, **verification all green**, **commits** (still on `feat/<feature-stem>`).
   3. Hand off **post-increment review** to **`refactoring`** with feature stem, backlog line, commit SHAs, and **review depth** (full vs light).
   4. Incorporate review summary (full mode: applied tiny refactors stay committed; light mode: suggestions only).
   5. If review reports **blocking** gaps (missing tests / strategy holes for **this** slice) → **stop**; do not continue automatic — present gaps to the user.
   6. **If step mode** → **stop**; present review + next open line; wait for user.
   7. **If automatic mode** and open `[ ]` remain → go to step 6.1.
   8. **If automatic mode** and all `[x]` → **stop** (feature complete; branch ready for a **feature PR** if desired).

Optional: create **`test-lists/<feature-stem>.md`** with empty `## <increment-slug>` headings as a skeleton — **no** behavior lines or `[x]` until **new-increment** runs.

See [examples/fizzbuzz-increments.md](examples/fizzbuzz-increments.md).

---

## Post-increment review (mandatory when orchestrating)

After each committed increment, invoke **`skills/refactoring`** in **post-increment review** mode (prefer **`refactoring`** subagent). Pass **review depth** (full vs light).

- Scope: **only** the commits / files from that increment (plus any tiny follow-up the review itself applies in **full** depth).
- Goals: explain what changed; flag test/strategy gaps; suggest **small, targeted** improvements. **Full** depth may apply **tiny** mechanical refactors only when clear leftover debt remains after the increment’s own TDD REFACTOR — not a second stylistic pass by default.
- Forbidden: rewrite the feature, expand to future increments, large redesigns, or continuing automatic when gaps are **blocking**.

**Pending:** mark review **pending** only when the user must run `/refactoring` manually or the `refactoring` agent is missing until `./scripts/install-cursor.sh` and/or `./scripts/install-claude.sh` is re-run after pull.

Details: [`skills/refactoring/references/post-increment-review.md`](../refactoring/references/post-increment-review.md).

---

## What this skill may edit

| Allowed | Forbidden |
|---------|-----------|
| `increments/<stem>.md` | `src/`, `test/`, `tests/` |
| Optional skeleton `test-lists/<feature-stem>.md` (headings only) | `acceptance-examples/` (created per increment in **new-increment**) |
| Docs clarifying scope | Production or test code |

Orchestration may **invoke** subagents that edit code; this skill’s own edits stay planning-only.

---

## Composition

| Need | Skill / agent |
|------|----------------|
| One slice delivery | **`skills/new-increment`** / **`new-increment`** |
| Post-increment review | **`skills/refactoring`** / **`refactoring`** (post-increment review mode) |
| Untested area | **`skills/legacy-testing`** (before or per increment) |
| Green prep | **`skills/refactoring`** (dedicated session) |
| Unknown tech | **`skills/spike`** |

This skill does **not** run ATDD/TDD or mark increments `[x]` from implementation work.

---

## Anti-patterns

- One backlog line for the entire feature
- Implementing code or tests in the **new-feature** session
- Marking multiple `[ ]` → `[x]` without a **new-increment** pass each
- Skipping **`new-increment`** (no scoped TDD per slice)
- Assuming **automatic** mode without explicit user opt-in
- Continuing to the next increment in **step** mode without user go-ahead
- Skipping **post-increment review** between increments
- Continuing **automatic** after a review that reported **blocking** gaps
- Asking **`new-increment`** to “do the rest of the backlog”
- Running **full** apply-capable review on every automatic increment when light depth would suffice (cost blow-up)
- No on-disk `increments/` file
- Creating many per-increment markdown files during planning
- **Per-increment branches / merges** — one branch (and ideally one PR) per **feature**, not per backlog line ([`delivery-process.md`](../../docs/delivery-process.md) §1a)

See [references/anti-patterns.md](references/anti-patterns.md).

---

## Additional resources

- [references/increment-backlog.md](references/increment-backlog.md)
- [references/slicing-increments.md](references/slicing-increments.md)
- [references/anti-patterns.md](references/anti-patterns.md)
- [examples/fizzbuzz-increments.md](examples/fizzbuzz-increments.md)
