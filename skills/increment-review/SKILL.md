---
name: increment-review
description: Fast, single-pass review of one just-finished increment — target under 60 seconds of work. Reads the new-increment mini-journal and that increment's diff only, checks against docs/code-review.md, and returns approved / changes-requested / bug-found with a short targeted fix brief. This is the default reviewer new-feature invokes after new-increment — not skills/refactoring directly. Use immediately after a new-increment run returns, before starting or continuing the next backlog line.
allowed-tools: Read, Bash, Grep, Glob
---

# Increment review (fast, single-pass)

## Mission

Review **only** the commit(s) of the increment that just finished, using the **mini-journal** `new-increment` returned (recap + review-focus) as the map — do not re-derive intent from scratch. Decide once: **approved**, **changes-requested** (with a short, ready-to-paste fix brief), or **bug-found** (wrong behavior — out of scope for a refactor-only fix). Stop. There is no second review round on the same line: whatever `new-feature` does with the verdict, this skill runs **once** per increment.

Speed is the point: a full multi-minute audit defeats the purpose. Read the diff and the review-focus bullets first, run only the tests the review-focus points at (skip re-running what the mini-journal already reports green with a trivial diff), and write a compact report per [`docs/code-review.md`](../../docs/code-review.md).

This skill does **not** edit code. Fixes are delegated to **`skills/refactoring`** (structural/test-gap/design changes) via the brief this skill drafts, or to **`skills/bugfix`** (wrong behavior) — `new-feature` decides which to dispatch and whether to ask the user first.

---

## Workflow

1. **Inputs** (from `new-feature`): feature stem, backlog line / increment slug, commit SHA(s) for this increment, and the **mini-journal** (recap + review-focus) `new-increment` returned.
2. **Read** `git show <sha>` / `git diff` for that commit only. Start with the files the review-focus bullets name.
3. **Test posture** — trust the mini-journal's verification table by default; re-run a **scoped** test only when the diff touches something the review-focus flags as risky, or when no verification evidence was passed. Never run the full project suite here — that already happened in `new-increment`.
4. **Apply** [`docs/code-review.md`](../../docs/code-review.md): structure/architecture fit, new-file test coverage, tests updated for changed pre-existing files, error handling on critical paths, Object Calisthenics / Simple Design on touched OO ([`docs/design-quality.md`](../../docs/design-quality.md)). Skip nits a linter/formatter would already catch.
5. **Decide** (pick one):
   - **approved** — optionally with non-blocking nits.
   - **changes-requested** — quality/design/test-gap issue fixable under the refactor hat (no behavior change). Draft a **refactor brief**: 2–6 lines, ready to paste to `refactoring` verbatim.
   - **bug-found** — the code is **wrong**, not just untidy. Do not draft a refactor brief (refactoring must not change behavior) — name the bug and suggest `bugfix`.
6. **Return** the report below and stop. Never touch the next backlog line, never apply the fix yourself.

---

## Output format

```markdown
## Increment review: <feature-stem> / <increment-slug>

Verdict: approved | changes-requested | bug-found

Commit(s): <sha>

What it does: <1-2 bullets, from the mini-journal>

Findings (changes-requested only):
1. <file:area> — <issue> — fix: <one short line>
2. …

Bug (bug-found only): <what's wrong and why it's a behavior bug, not a tidy-up> — route to bugfix.

Nits (optional, approved-with-comments): <bullets, non-blocking>

Refactor brief (changes-requested only — paste verbatim to `refactoring`):
<2-6 lines: goal, files, the specific change(s), "tests stay green, refactor hat only">
```

Keep every section to the fewest words that stay clear — per [`docs/code-review.md`](../../docs/code-review.md)'s own rule: be direct, don't pad.

---

## Definition of done

- Reviewed **only** this increment's commit(s) — no drive-by scan of unrelated files
- Verdict is exactly one of `approved` / `changes-requested` / `bug-found`
- `changes-requested` always carries a **ready-to-paste** refactor brief; `bug-found` never does
- No file edited by this skill
- No full-suite run initiated here
- Report returned to `new-feature`; did not decide continue-vs-stop-vs-dispatch itself (that's `new-feature`'s call)

---

## Anti-patterns

- Re-reviewing files outside the increment's diff "while here"
- Running the full project test/lint suite to double-check what `new-increment` already verified
- A second review pass after `refactoring` applies the fix — one review per increment, full stop
- Drafting a refactor brief for a correctness bug (wrong hat — that's `bugfix`'s job)
- Vague findings ("could be cleaner") without a concrete file/fix
- Padding the report with a full restatement of `docs/code-review.md`'s checklist instead of applying it

---

## Additional resources

- [`docs/code-review.md`](../../docs/code-review.md) — review checklist and tone this skill applies
- [`docs/design-quality.md`](../../docs/design-quality.md) — Object Calisthenics / pattern-theater checks
- [`skills/new-increment/SKILL.md`](../new-increment/SKILL.md) — produces the mini-journal this skill consumes
- [`skills/refactoring/SKILL.md`](../refactoring/SKILL.md) — executes `changes-requested` fixes
- [`skills/bugfix/SKILL.md`](../bugfix/SKILL.md) — executes `bug-found` fixes
- [`skills/new-feature/SKILL.md`](../new-feature/SKILL.md) — the only caller; decides continue/dispatch/ask-user from the verdict
