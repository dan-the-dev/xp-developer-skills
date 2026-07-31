---
name: tweak
description: Small, targeted change to the feature already on the current branch — copy/text, a color or style, a small logic change, or a small new file. Scoped edit, scoped tests, scoped lint, one commit on the current branch. No increments file, no feature branch, no PR. Use for a quick follow-up tweak right after new-feature/new-increment finished, not for a new capability or a multi-file feature (use skills/new-feature for that).
allowed-tools: Read, Edit, MultiEdit, Bash, Grep, Glob
---

# Tweak (small, direct follow-up change)

## Mission

Deliver **one small, well-tested tweak** directly on the branch you're already on — no planning ceremony, no new branch, no PR. This is the lightweight escape hatch for the case that otherwise tempts a direct, untested edit: "just change this text / color / small rule."

**Not this skill:** anything that needs more than a handful of files, a new capability, or its own backlog — hand that to **`skills/new-feature`** instead.

---

## Workflow

1. **State the tweak** in one sentence — what should look or behave differently. If it turns out to need multiple independent behaviors or a new component, stop and suggest `skills/new-feature` instead.
2. **Find the minimal file set.** Grep/search for the exact text, color token, or logic you're changing. Resist touching anything not strictly required.
3. **If changing existing tested logic:** extend or write the test for the new behavior first (RED), then make the change (GREEN) — one scoped test command for that file/module.
4. **If purely cosmetic** (copy/color/style with no test asserting the old value): make the change directly. If a snapshot/visual test breaks, update it deliberately — never blind-approve a snapshot without checking the new output is correct.
5. **If the tweak needs a new file:** it ships with its own test(s) covering its behavior — no exception for "it's small." Update every existing test that exercises a caller of that new file to match.
6. **Verify — scoped only:** run the test(s) for the file(s) touched (plus anything that imports/calls them), and the project's lint/format for those files. Do not run the full project suite unless the project has no way to scope it.
7. **Fix until scoped checks are green**, then **commit** — one commit, conventional message, on the **current branch**. Do not create `increments/`, a feature branch, or a PR.
8. **Report**: files changed, tests added/updated, verification run, commit SHA.

---

## Definition of done

- The tweak matches the one-sentence statement from step 1 — nothing broader
- Any behavior change has a test for it; any new file has its own tests and updated callers' tests
- Scoped tests + scoped lint green for every touched file
- Exactly **one** commit, on the current branch
- No `increments/`, feature branch, or PR created

---

## Anti-patterns

- Scope creep into a mini-feature — escalate to `skills/new-feature` instead of stretching this skill
- Skipping tests for a new file "because it's small"
- Running the whole project suite for a one-line tweak when a scoped command exists
- Leaving lint red on touched files
- Blind-approving a broken snapshot instead of checking the new output
- Batching several unrelated tweaks into one invocation — one tweak, one commit
- Creating a feature branch or opening a PR for a tweak

---

## Additional resources

- [`docs/project-verification.md`](../../docs/project-verification.md) — how to discover the project's scoped test/lint commands
- [`skills/new-feature/SKILL.md`](../new-feature/SKILL.md) — escalate here when the "tweak" turns out to be a feature
- [`skills/tdd/SKILL.md`](../tdd/SKILL.md) — RED/GREEN discipline for the logic-change case
