# Delivery process (shared)

Language- and project-agnostic rules for AMPD delivery skills and subagents. Compose with skill-specific workflows; do not override skill scope with convenience.

---

## 1. Role boundaries

| Role | Delivers | Must stop before |
|------|----------|------------------|
| **Feature planning / orchestration** | Ordered backlog; optional empty tracking skeleton; **decides** whether to hand off the next increment or pause for feedback | Production code, tests, marking backlog lines complete (always delegated) |
| **One increment** | Exactly **one** open backlog line; commits when done; all verify steps green | Starting the next line — **always** (never continues the backlog) |
| **Post-increment review** | Explain the increment’s commits; small in-scope refactor / test suggestions (optional tiny mechanical applies) | Rewrites outside the increment change surface; new capability |
| **Harness (legacy)** | Trustworthy automated safety net for the change path | Large structural edits on unprotected code |
| **Refactor (structure)** | Behavior-preserving structure improvements | New capability or bug fixes in the same pass |
| **Capability / fix** | New behavior or corrected behavior | Silent mixing with refactor-only work |

**Delegation:** When a subagent exists for a role, invoke it for that role. Do not read its skill and perform the work in the parent thread.

### Orchestration modes (`new-feature`)

| Mode | How activated | After each `new-increment` + post-increment review |
|------|---------------|-----------------------------------------------------|
| **Step** (default) | Assumed unless the user explicitly opts in to automatic | **Full** review → **stop** for user feedback; do not start the next line |
| **Automatic** | Explicit user request only (e.g. “modalità automatica”, “automatic mode”, “implement the whole feature”, “run until the backlog is done”) | **Light** review by default → if no **blocking** gaps and open `[ ]` remain → hand off the **next** line; if all `[x]` → stop (feature complete) |

**Invariant:** `new-increment` **always** delivers one line, verifies green, commits, and **stops**. Only `new-feature` decides whether to continue or pause — and only continues in **automatic** mode when the review did not report **blocking** gaps.

**Review depth:** step → **full** (explain, suggest, optional tiny applies). Automatic → **light** (explain + suggest-only) unless the user opted into full review with applies.

**Anti-pattern:** Treating “continue” as implied; batching increments inside `new-increment`; skipping post-increment review when orchestrating; continuing automatic after blocking review findings.

---

## 2. Project verification (definition of done)

Full guide: [`project-verification.md`](project-verification.md).

### During work (every code change)

After **each meaningful edit** (RED/GREEN/REFACTOR step, bugfix change, refactor mechanical step, harness addition):

1. Re-run the **narrowest applicable checks** — at minimum **affected automated tests**.
2. If a step fails, **fix or revert** before continuing; do not stack edits on a broken baseline.

### Before claiming a slice complete

1. **Discover** what this project defines as verification for the **current language / module / track** you touched — scripts, Makefile targets, CI jobs, documented commands, or equivalent. Inspect README, contribution guides, CI config, Sonar/static-analysis config, and existing tooling; do not assume a single command.
2. **Run every applicable verify step** for that scope — not only the fastest or most familiar runner. This includes, when the project defines them: **tests** (unit, integration, contract, acceptance, **mutation**, property-based, …), **build/compile**, **typecheck**, **lint**, **format**, and **code quality platforms** (e.g. SonarQube, SonarCloud, CodeClimate).
3. **Fix violations you introduced** — leave lint, static analysis, and quality gates **without new warnings or errors** attributable to your change.
4. **Hard green gate:** do **not** mark the backlog line `[x]`, claim done, or hand off as complete while **any** applicable verify step is red. Fix first; then re-run the **full** applicable set.
5. **Report** each command run and pass or fail (verification table).

**Applicable vs out-of-scope:** **Applicable** = steps that cover the language/module/files you touched (or project gates that always run for that track). Pre-existing red on **debt outside your slice** must be documented with evidence — it does **not** block `[x]` once in-scope steps are green — but do **not** claim the whole project is clean. Failures in files you edited are in-scope: fix them.

**Principle:** One green signal (e.g. only the test runner) is not equivalent to “the project verifies” when the project defines additional steps (compile, typecheck, lint, integration, Sonar, packaging, etc.).

**AMPD commit rule:** For AMPD delivery agents (`new-increment`, post-increment review applies, dedicated refactor sessions), **commit is part of done**. Outside AMPD agent workflows, follow the user’s git policy (commit only when asked).

**Anti-pattern:** Declaring done after a subset of verify steps when the project defines more; stopping with failing **in-scope** tests “for the user to decide”; skipping re-verify after a refactor step; suppressing lint/sonar rules instead of fixing code.

---

## 3. Change-surface completeness

When a change alters how something is **constructed, imported, or named** (factory, type vs value, renamed API, moved module):

- **Search** the agreed scope (repo, package, or module) for obsolete usage patterns.
- Update **every** call site in scope — production, tests, examples, demos, entrypoints — not only files touched by the first verify step you ran.

**Anti-pattern:** Fixing tests while leaving entrypoints or sample code broken, or the reverse.

---

## 4. Test pyramid and strategy (one layer per concern)

Full guide: [`test-strategy-selection.md`](test-strategy-selection.md).

For a slice, use the **lowest sufficient** automated layer — but **do not default to unit TDD only** without evaluating other practices the project configures or the slice warrants (integration, contract, component, property-based, **mutation**, ATDD at outer seams, etc.).

**Before first RED:** complete a brief **test strategy decision** (adopt / skip with reason per relevant practice). Record in the return payload (§10).

Rules:

- If the same behavior would be asserted twice at the **same** boundary, use **one** layer.
- Add a higher layer or specialized technique only when it proves something the lower layer cannot (real outer seam, silent wiring failure, weak test confidence, invariant over many inputs).
- If the project **already runs** mutation, contract, component, or a11y jobs in CI, **strong bias to use them** when the slice matches — do not ignore configured gates.
- **Greenfield / new system:** when §2–3 say adopt (especially **mutation** for branchy domain, property-based for invariants, ATDD when the first outer seam appears), **bias to introduce** minimal tooling in-repo — do not wait for the user to ask — **unless** setup cost clearly dominates the slice (see [`test-strategy-selection.md`](test-strategy-selection.md) §3 mutation thresholds). Brownfield without the tool: note follow-up unless the user opts in.
- Prefer **code-first** acceptance tests unless the team already uses Gherkin or product/BA reviews `*.feature` files.

**Anti-pattern:** Unit tests only with no documented consideration of catalog alternatives; mutation warranted on greenfield but deferred until asked; mutation/contract/component configured but never run; duplicate checks at the same layer plus markdown that only restates them.

---

## 5. Tracking artifacts (honest, minimal)

| Rule | Meaning |
|------|---------|
| **Minimal** | Prefer one tracking artifact per feature unless the project already defines another convention. |
| **Honest** | Lines stay open until the linked automated check exists and has been exercised. |
| **Linked** | Done lines reference the actual automated check (as the project names it). |
| **Cleanup** | Remove or merge redundant tracking files that only duplicate what checks already express. |

**Anti-pattern:** Many small tracking files pre-marked complete before checks exist, or filled in after a big-bang edit.

---

## 6. RED → GREEN → REFACTOR (kinetic)

| Step | Rule |
|------|------|
| **RED** | Add or extend **one** failing automated check; run verification; **observe** failure before production changes. |
| **GREEN** | Minimal production change to pass; run verification again. |
| **REFACTOR** | Structure-only steps; verification green after each meaningful step; revert on failure. |

**Anti-pattern:** Replacing entire test or production files in one edit with no failing run in between.

**Evidence:** Report count of RED cycles observed, or state **batch mode** if the user explicitly opted in.

---

## 7. Two hats

In one invocation, wear **one** hat unless the user explicitly sequences both:

- **Structure hat** — observable behavior unchanged; verification stays green throughout.
- **Capability / fix hat** — behavior changes; use test-first or characterization as appropriate.

**Sequence when both are needed:** harness or structure first when code is unsafe; then capability in a separate pass or invocation.

**Anti-pattern:** “Refactor” that also fixes bugs, adds features, or changes outputs without an explicit separate step.

---

## 8. Harness when code is unprotected

**Unprotected** = behavior you need to change is not guarded by automated checks you trust.

| Situation | Process |
|-----------|---------|
| No harness | Pin behavior at stable seams **before** large edits ([`skills/legacy-testing`](../skills/legacy-testing/SKILL.md)). |
| Harness exists but **invalid** (won’t compile, wrong construction API, broken entrypoints) | **Harness work first** — not a feature increment. |
| Harness exists and green | Proceed to increment or refactor; still run **full project verification** at boundaries (§2). |

---

## 9. Refactoring step size

Structure changes use **small mechanical steps** with verification after each step.

**Anti-pattern:** One-shot rewrite of a whole module with a single verification run at the end.

---

## 10. Return payload (accountability)

End every delivery invocation with a short factual report:

| Field | Content |
|-------|---------|
| **Role completed** | planning \| one increment \| post-increment review \| harness \| refactor \| fix |
| **Orchestration mode** | step \| automatic (planning / `new-feature` only) |
| **Backlog** | Which line marked complete (if increment) — **at most one** |
| **Commits** | SHAs / messages for this slice (increment and review must leave work committed) |
| **Verification** | Each project verify step run → pass/fail — **all must be pass** to claim done |
| **Test strategy** | Practices evaluated → adopt or skip with reason ([`test-strategy-selection.md`](test-strategy-selection.md) §6) |
| **RED cycles** | Count per behavior, or batch mode noted |
| **Layers** | e.g. unit + mutation \| API acceptance + inner TDD \| characterization only |
| **Change-surface** | Search performed yes/no; what was updated |
| **Post-increment review** | Summary / depth (full\|light) / pending / blocked (`new-feature` orchestration) |
| **Handoff** | Next open backlog line — **do not implement** (`new-increment`); or continue/stop decision (`new-feature`) |

---

## Composition map

| Skill / agent | Uses especially |
|---------------|-----------------|
| `new-feature` | §1 orchestration modes + review depth + blocking gaps, §10 handoff |
| `new-increment` | §1–3, §5–6, §10; always one line + commit + green gate; [`project-verification.md`](project-verification.md); [`test-strategy-selection.md`](test-strategy-selection.md) |
| `legacy-testing` | §8; [`project-verification.md`](project-verification.md); [`test-strategy-selection.md`](test-strategy-selection.md) |
| `refactoring` (skill) / `refactoring` (agent) | §1 post-increment review (full/light) **or** dedicated structure pass (§7, §9, §2); [`project-verification.md`](project-verification.md) |
| `legacy-refactor` (agent) | §1, §7–9, §2 — harness then structure (distinct from `refactoring` alone) |
| `tdd` | §6; [`project-verification.md`](project-verification.md); [`test-strategy-selection.md`](test-strategy-selection.md) |
| `atdd` | §4; [`project-verification.md`](project-verification.md); [`test-strategy-selection.md`](test-strategy-selection.md) |
| `bugfix` | §2, §3, §7; [`project-verification.md`](project-verification.md); [`test-strategy-selection.md`](test-strategy-selection.md) |
