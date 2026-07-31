# Minimal handoff prompts

Every subagent already reads its own `SKILL.md` and the shared `docs/`. Pass only the facts it **cannot** derive itself — stem, exact line, branch, SHA, the other agent's own report. Do not restate the subagent's skill, the whole backlog, or prior conversation history: that burns tokens without changing the outcome.

---

## To `new-increment`

```
Implement this increment.
Feature: <feature-stem>. Branch: feat/<feature-stem>.
Backlog: increments/<feature-stem>.md — line: "<exact [ ] line text>".
```

Nothing else — it reads the test strategy, project verification, and design docs itself.

---

## To `increment-review`

```
Review this increment.
Feature: <feature-stem> / increment: <slug>. Commit(s): <sha or range>.

Mini-journal from new-increment:
Recap: <paste recap bullets verbatim>
Review focus: <paste review-focus bullets verbatim>
```

Paste the mini-journal **verbatim** — that is the point of collecting it: the reviewer should not have to re-read the whole diff cold.

---

## To `refactoring` (fix brief — only on a `changes-requested` verdict)

```
Apply this fix — refactor hat only, no new behavior, tests stay green.
Feature: <feature-stem> / increment: <slug>.

<paste the "Refactor brief" from increment-review's report, verbatim>
```

Never expand this into a general "clean up this increment" request — the brief is already scoped and minimal; forward it as-is.
