# Post-increment review (legacy / manual mode)

Mode of **`skills/refactoring`**, previously invoked by `new-feature` after every increment. **`new-feature` now calls `skills/increment-review`** for that (fast, single-pass, ~60s) and dispatches this skill only to execute the resulting fix brief. Use **this** mode only when the **user** directly asks for a full/manual review of the last increment (or `increment-review`/its agent is missing after install).

Invoked after a **`new-increment`** has marked one backlog line `[x]`, verified green, and **committed**.

---

## Mission

Review **only** the commits (and files) from the just-finished increment:

1. **Explain** what changed (behavior + structure) in reviewer-friendly language.
2. **Suggest** small, targeted improvements: naming, extracts, **Simple Design / Object Calisthenics breaches**, unjustified pattern theater, test gaps, pyramid/strategy holes (e.g. missing mutation on branchy logic).
3. **Optionally apply** (full depth only) only **tiny** mechanical refactors clearly inside that change surface — baby steps, tests stay green, `refactor:` commits — including calisthenics fixes and inlining speculative single-implementation patterns.
4. **Stop** with a structured report. Do **not** implement the next backlog line.

This pass is an **external quality gate**, not a second stylistic REFACTOR. The increment’s TDD loop already includes REFACTOR — apply here only when **clear leftover debt** remains in the change surface (e.g. an obvious extract the slice left half-done, an `else` chain on owned OO, a misleading name in touched files). Do **not** re-tidy for taste by default.

Design compass: [`docs/simple-design.md`](../../../docs/simple-design.md), playbook [`docs/design-quality.md`](../../../docs/design-quality.md).

---

## Review depth

| Depth | Typical caller | Applies allowed? |
|-------|----------------|------------------|
| **Full** | `new-feature` **step** mode; or user asked for full review / applies | Yes — tiny in-surface only |
| **Light** | `new-feature` **automatic** mode (default) | **No** — explain + suggest-only |

Caller passes depth explicitly. If omitted: **full** when SHAs come from a step-mode handoff or interactive user review; **light** when continuing an automatic backlog.

---

## Scope fence (non-negotiable)

| In scope | Out of scope |
|----------|--------------|
| Diff / commits of this increment (plus your own tiny follow-up commits in full depth) | Future increment behavior |
| Local names, duplication, extract/inline in touched modules | Module-wide redesign, layering rewrite |
| **Object Calisthenics** breaches on OO introduced/edited this slice | Pre-existing debt far outside the change surface (suggest only) |
| Speculative pattern theater introduced this slice | Inventing large GoF hierarchies “properly” under review |
| Missing tests for branches **introduced in this increment** | New product capabilities |
| Flagging weak strategy vs [`test-strategy-selection.md`](../../../docs/test-strategy-selection.md) | Introducing unrelated tooling “while here” without clear increment need |

**Rule of thumb:** if a suggestion would touch files the increment did not touch (except trivial call-site updates from a rename you started), **suggest only** — do not apply.

---

## Blocking vs non-blocking findings

| Kind | Meaning | Effect on `new-feature` automatic |
|------|---------|-----------------------------------|
| **Blocking** | Tests or strategy holes that belong in **this** increment (e.g. untested branch just introduced; mutation adopted but never run); **Object Calisthenics** breach on OO introduced/edited this slice without boundary exception; duplicated type/state behavior switch left procedural; speculative pattern hierarchy introduced this slice | **Stop** — do not hand off the next backlog line |
| **Non-blocking** | Nice-to-have renames, future extracts, cross-cutting cleanups, pre-existing design debt outside surface | Continue automatic; record under deferred |

Mark blocking items clearly in the report (`blocking: yes`).

---

## Workflow

1. **Inputs** — feature stem, backlog line text, commit range or SHAs, **review depth** (full \| light).
2. **Baseline** — `git show` / `git diff` / `git log` for that range; confirm working tree clean or only review follow-ups.
3. **Read** production + tests in the diff; note RED/GREEN intent from commit messages when present.
4. **Explain** — short narrative: what the slice delivers; main seams; test layers used.
5. **Findings** — list suggestions ordered by impact; mark each as `apply-now` (tiny, in-surface, **full depth only**) or `suggest-only`; mark **blocking** when applicable.
6. **Apply** (full depth, optional) — only non-blocking `apply-now` items with clear leftover debt; one mechanical step at a time; re-run affected tests after each; full verify before final commit ([`project-verification.md`](../../../docs/project-verification.md)). Do not “fix” blocking gaps under the refactor hat — report them and stop.
7. **Return** — report below; hand back to **`new-feature`** (step vs automatic + blocking decides continue/stop).

---

## Output format

```markdown
## Post-increment review: <feature-stem> / <increment>

### Depth
full | light

### Commits reviewed
- <sha> <message>
- …

### What changed
- <2–5 bullets — behavior and structure>

### Test posture
- Layers seen: <unit | ATDD | mutation | …>
- Gaps / follow-ups: <bullets or none>
- Blocking gaps: <none | bullets>

### Design posture
- Simple Design / calisthenics: <ok | breaches…>
- Patterns: <none | toward/away Name | theater…>
- Blocking design gaps: <none | bullets>

### Suggestions
| Id | Kind | Scope | Action | Blocking | Note |
|----|------|-------|--------|----------|------|
| 1 | rename / extract / calisthenics / pattern / test | in-surface | apply-now \| suggest-only | yes \| no | … |

### Applied (if any — full depth only)
- `refactor: …` — <sha>
- Verification: <commands> — green

### Deferred for user / later
- <bullets or none>

### Orchestration signal
continue-ok | blocked | pending
```

**Orchestration signal:** `continue-ok` (no blocking gaps), `blocked` (automatic must stop), `pending` (review could not run — user must `/refactoring` or re-install agents).

---

## Anti-patterns

- Rewriting the increment “properly” under a refactor label
- Expanding review into the next backlog line
- Mixing feature/bugfix hats into the review pass
- Applying cross-module cleanups without listing them as suggest-only
- Skipping verification after applying tiny refactors
- Second stylistic REFACTOR pass when TDD already left the surface clean
- Applying in **light** depth
- Hiding **blocking** gaps so automatic mode continues
