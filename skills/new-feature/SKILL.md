---
name: new-feature
description: Slice a whole capability into ordered releasable increments (increment backlog in increments/<stem>.md). Delegate each slice to skills/new-increment, review via skills/increment-review — do not implement slices or review them yourself. Confirms the plan before executing (wait in step mode, ~2min pause in automatic). Default step mode stops after each increment for feedback; automatic mode (explicit opt-in) continues until the backlog is done, then can open the feature PR from the increments' mini-journals. Use for an entire feature or epic (e.g. full FizzBuzz), not for implementing one increment.
allowed-tools: Read, Edit, MultiEdit, Bash, Grep, Glob
---

# New feature (increment planning + orchestration)

## Mission

Plan a **whole feature** as **ordered, releasable increments**. **Do not implement** slices in this skill — each open line is delivered by **`skills/new-increment`** (or the **`new-increment`** subagent) in a **separate** invocation.

**First step:** create **`increments/<feature-stem>.md`** (see [references/increment-backlog.md](references/increment-backlog.md)).

**Feature complete** when every in-scope increment is `[x]` on that backlog — each line completed via **`new-increment`**, not by implementing in this session.

---

## Orchestration modes

| Mode | Activation | After each increment |
|------|------------|----------------------|
| **Step** (default) | Assumed unless the user **explicitly** opts into automatic | **`increment-review`** runs once → **stop**, present the verdict + next open line, wait for the user (including whether to dispatch a `changes-requested` fix) |
| **Automatic** | Explicit only — e.g. “modalità automatica”, “automatic mode”, “implement the whole feature”, “run until the backlog is done” | **`increment-review`** runs once → `approved`: continue immediately, no user action. `changes-requested`: dispatch **`refactoring`** with the review's brief automatically, commit, continue. `bug-found`: **always stop** for the user regardless of mode — a correctness bug is not an automatic-refactor fix. If no open `[ ]` remain, go to the **PR** step. |

**Invariants (both modes):**

1. **`new-increment` always** implements **one** line, runs full verification (all green), **commits (squashed to one) on the feature branch**, returns a **mini-journal**, and **stops**. It never starts the next backlog line or merges to main between increments.
2. **This skill** decides whether to continue or pause — only continues in **automatic** mode, and only on an `approved` or resolved `changes-requested` verdict.
3. After every successful increment, run **`skills/increment-review`** (not `refactoring` directly) before stopping or continuing — it is a single fast pass, not a variable-depth review.
4. A **`bug-found`** verdict always stops, in both modes — it needs `bugfix`, not an automatic refactor.

Also confirm the **plan** itself before any increment starts (see below), and offer to open the **PR** once the backlog is done (see below).

If the user does **not** name automatic mode, stay in **step**.

---

## Workflow

Shared delivery rules: [`docs/delivery-process.md`](../../docs/delivery-process.md) (orchestration — §1, **§1a feature branch**, §10).

1. Clarify capability and whole-feature definition of done.
2. Resolve **orchestration mode** (step vs automatic) from the user request; state it in the return payload.
3. If feasibility unknown → **`skills/spike`** on `spike/…` branch; promote before slicing.
4. Write **ordered** increment lines in `increments/<stem>.md` (all `[ ]` initially). Optionally note **expected test layers** per line (see [`test-strategy-selection.md`](../../docs/test-strategy-selection.md) §2) — e.g. “mutation likely”, “ATDD at API”, “property-based”.
5. Ensure a **single feature branch** exists and is the working branch: `feat/<feature-stem>` (create from the default base if missing). Pass this branch name when handing off to **`new-increment`**. Do **not** ask for a new branch per increment or merge to main between increments (§1a) — goal is **one PR for the feature**.
6. **Confirm the plan** (see gate below) before handing off the first increment.
7. **Loop** (one open line at a time):
   1. Hand off the **next** open line to **`new-increment`** with a **minimal** prompt (template in [references/handoff-prompts.md](references/handoff-prompts.md): stem, exact line text, branch, backlog path — nothing it can already read itself). Do **not** implement it here.
   2. Wait for return payload: backlog `[x]`, **verification all green**, single squashed **commit**, and the **mini-journal** (recap + review-focus).
   3. Hand off to **`skills/increment-review`** with a minimal prompt: stem, increment slug, commit SHA, and the mini-journal verbatim (template in [references/handoff-prompts.md](references/handoff-prompts.md)).
   4. Record the increment's mini-journal (you need it for the PR later — see below).
   5. Act on the verdict per the **orchestration modes** table above.
   6. **If step mode** → **stop** after presenting the verdict + next open line; wait for the user.
   7. **If automatic mode** and open `[ ]` remain → go to step 7.1.
   8. **If automatic mode** and all `[x]` → go to the **PR** step below.

Optional: create **`test-lists/<feature-stem>.md`** with empty `## <increment-slug>` headings as a skeleton — **no** behavior lines or `[x]` until **new-increment** runs.

See [examples/fizzbuzz-increments.md](examples/fizzbuzz-increments.md).

---

## Plan confirmation gate (after the backlog, before the first increment)

Once `increments/<feature-stem>.md` is written, present it in full and ask "is this plan correct?" — never cascade straight from "here is the plan" into the first `new-increment` handoff in the same turn.

| Mode | Gate |
|------|------|
| **Step (manual)** | **Stop and wait.** Do not hand off the first increment until the user explicitly confirms the plan (or an edited version of it). |
| **Automatic** | State you will start the first increment in about **2 minutes** unless the user redirects, then actually hold that pause — use the host tool's timed-wait/schedule primitive if one is available; otherwise end your turn after presenting the plan so the user has a real chance to reply before you act. If ~2 minutes pass (or, absent a timer, the user's next message doesn't redirect you) with no objection, proceed automatically with the first `new-increment` handoff. Any user message that arrives first overrides the timer — address it before proceeding. |

This gate applies **once**, right after planning — not before every later increment (step mode already stops after each one; automatic mode's per-increment continuation is governed by the `increment-review` verdict, not a second timer).

---

## Post-increment review (mandatory when orchestrating)

After each committed increment, invoke **`skills/increment-review`** (prefer its subagent) — a fast, single-pass review, not `refactoring` directly.

- Scope: **only** the commits from that increment; the review reads the mini-journal, not a cold diff.
- Verdict handling: `approved` → continue (light nits noted, not applied); `changes-requested` → dispatch **`refactoring`** with the review's ready-made brief (automatic: right away; step: ask the user first) and, once it commits the fix, move on **without a second review round**; `bug-found` → **stop** for the user in both modes — point to `bugfix`, not `refactoring`.
- Forbidden: rewrite the feature, expand to future increments, large redesigns, re-reviewing after the fix commit, or dispatching `refactoring` for a `bug-found` verdict.

**Pending:** mark review **pending** only when the user must run `/increment-review` manually or the agent is missing until `./scripts/install-cursor.sh` and/or `./scripts/install-claude.sh` is re-run after pull.

Details: [`skills/increment-review/SKILL.md`](../increment-review/SKILL.md).

---

## Opening the feature PR

When every backlog line is `[x]` (or the user asks to ship a partial slice as its own PR):

1. Ensure the feature branch is pushed (`git push -u origin feat/<stem>` if not already tracking a remote).
2. Draft the **title** from the backlog's feature title, and the **description** as one bullet per increment built from that increment's mini-journal **recap** (not the raw commit list), plus a **Test plan** section assembled from each increment's verification table, plus a **Follow-ups** section for any non-blocking review nits that were deferred.
3. **Automatic mode:** push and open/update the PR (`gh pr create` / `gh pr edit`) without asking.
4. **Step mode:** show the drafted title + description and ask for confirmation before pushing or opening/updating the PR.
5. Never force-push or rewrite branch history "to clean up" for the PR — the stacked per-increment commits are the intended history.

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
| Post-increment review | **`skills/increment-review`** / **`increment-review`** — fast single pass |
| Execute a requested fix | **`skills/refactoring`** / **`refactoring`** with the review's brief |
| Small follow-up tweak after the feature ships | **`skills/tweak`** (not this skill — no branch/backlog ceremony) |
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
- Skipping **`increment-review`** between increments, or calling `refactoring` directly for the review
- Continuing **automatic** on a **`bug-found`** verdict instead of stopping for the user
- Dispatching `refactoring` to fix a `bug-found` verdict (wrong hat — that's `bugfix`)
- A second review round on the same increment after `refactoring` applies the brief
- Asking **`new-increment`** to “do the rest of the backlog”
- Cascading from "here is the plan" straight into the first `new-increment` handoff without the confirmation gate
- Padded handoff prompts that restate the subagent's own skill or the whole backlog instead of the minimal template
- Opening/pushing the PR in **step** mode without showing the draft and asking first
- No on-disk `increments/` file
- Creating many per-increment markdown files during planning
- **Per-increment branches / merges** — one branch (and ideally one PR) per **feature**, not per backlog line ([`delivery-process.md`](../../docs/delivery-process.md) §1a)

See [references/anti-patterns.md](references/anti-patterns.md).

---

## Additional resources

- [references/increment-backlog.md](references/increment-backlog.md)
- [references/slicing-increments.md](references/slicing-increments.md)
- [references/handoff-prompts.md](references/handoff-prompts.md)
- [references/anti-patterns.md](references/anti-patterns.md)
- [examples/fizzbuzz-increments.md](examples/fizzbuzz-increments.md)
