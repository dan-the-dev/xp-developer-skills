# Delivery process (shared)

Language- and project-agnostic rules for AMPD delivery skills and subagents. Compose with skill-specific workflows; do not override skill scope with convenience.

---

## 1. Role boundaries

| Role | Delivers | Must stop before |
|------|----------|------------------|
| **Feature planning / orchestration** | Ordered backlog; optional empty tracking skeleton; confirms the plan before executing; **decides** whether to hand off the next increment or pause for feedback; can open the feature PR when done | Production code, tests, marking backlog lines complete, reviewing an increment (always delegated) |
| **One increment** | Exactly **one** open backlog line; commits when done, squashed to one; all verify steps green; a mini-journal (recap + review-focus) | Starting the next line — **always** (never continues the backlog) |
| **Post-increment review** | Fast, single-pass verdict (`approved` \| `changes-requested` \| `bug-found`) from the increment's diff + mini-journal, per `docs/code-review.md`; a ready-to-paste fix brief when changes are requested (typically **`increment-review`**) | Rewrites outside the increment change surface; new capability; a second review round on the same increment |
| **Fix execution** | Applies a review's fix brief as behavior-preserving mechanical steps (typically **`refactoring`**) | Anything outside the brief; correctness bugs (route to `bugfix` instead) |
| **Small tweak** | One small, tested, committed change on the **current** branch — no backlog/branch/PR (typically **`tweak`**) | Anything that grows past a handful of files (escalate to feature planning) |
| **Harness (legacy)** | Trustworthy automated safety net for the change path | Large structural edits on unprotected code |
| **Refactor (structure)** | Behavior-preserving structure improvements | New capability or bug fixes in the same pass |
| **Capability / fix** | New behavior or corrected behavior | Silent mixing with refactor-only work |

**Delegation:** When a subagent exists for a role, invoke it for that role. Do not read its skill and perform the work in the parent thread.

### Orchestration modes (`new-feature`)

Before any increment starts, `new-feature` presents the backlog and runs a **plan confirmation gate**: step mode stops and waits for explicit confirmation; automatic mode announces and holds a ~2 minute pause (or the closest the host tool supports) before proceeding.

| Mode | How activated | After each `new-increment` + `increment-review` |
|------|---------------|---------------------------------------------------|
| **Step** (default) | Assumed unless the user explicitly opts in to automatic | `increment-review` runs **once** → **stop** for user feedback; present the verdict + next line; ask before dispatching a `changes-requested` fix |
| **Automatic** | Explicit user request only (e.g. “modalità automatica”, “automatic mode”, “implement the whole feature”, “run until the backlog is done”) | `increment-review` runs **once** → `approved`: hand off the **next** line; `changes-requested`: dispatch `refactoring` with the review's brief automatically, then continue; `bug-found`: **always stop** for the user. If all `[x]` → offer/open the **feature PR** from the increments' mini-journals. |

**Invariant:** `new-increment` **always** delivers one line, verifies green, commits (squashed to one), returns a mini-journal, and **stops**. `increment-review` runs **once** per increment — never a second pass after a fix is applied. Only `new-feature` decides whether to continue or pause — and only continues automatically on `approved` or a resolved `changes-requested`; a `bug-found` verdict stops in **both** modes.

**Anti-pattern:** Treating “continue” as implied; batching increments inside `new-increment`; skipping `increment-review` (or calling `refactoring` directly for the review) when orchestrating; continuing automatic after a `bug-found` verdict; dispatching `refactoring` to fix a correctness bug; a second review round on the same increment; cascading past the plan confirmation gate; **one git branch (or merge to main) per increment** instead of one feature branch (§1a).

---

## 1a. Feature branch (one branch for the whole feature)

AMPD expects **one long-lived feature branch** that can become **one PR for the feature**. Increments are **commits on that branch**, not separate branches or merges.

| Rule | Meaning |
|------|---------|
| **One branch per feature** | Name e.g. `feat/<feature-stem>` (or the repo’s equivalent). Create it when starting the feature (typically `new-feature` / first `new-increment`). |
| **All increments on that branch** | Every `new-increment` commit stays on the **same** feature branch. Do **not** create `feat/<feature>-<increment-slug>` (or similar) per backlog line. |
| **No merge between increments** | Do **not** merge the feature branch into `main`/`master`/`develop` after each increment in order to “start the next.” Leave commits stacked; open/update **one PR** when the feature (or an agreed release slice) is ready. |
| **Reuse if already checked out** | If already on `feat/<feature-stem>`, keep working there. Only create the branch when missing. |
| **Exceptions** | User explicitly asks for a different branch layout; or a true emergency hotfix branch unrelated to this feature backlog. Spikes stay on `spike/…` and do not replace this rule for delivery. |

**Why:** A PR per feature reviews the whole capability; per-increment branches + merges fragment history and force premature integration.

**Anti-pattern:** Branch → implement one increment → merge to main → new branch for the next increment; opening a PR per backlog line while orchestrating a multi-increment feature (unless the user explicitly wants that).

---

## 2. Project verification (definition of done)

Full guide: [`project-verification.md`](project-verification.md).

### During work (every code change)

After **each meaningful edit** (RED/GREEN/REFACTOR step, bugfix change, refactor mechanical step, harness addition):

1. Re-run **only the narrowest checks for what you just touched** — typically the **single failing/passing test**, file, or package under change. Do **not** run the full suite or the full lint/typecheck/Sonar inventory on every micro-step.
2. If that narrow check fails, **fix or revert** before continuing; do not stack edits on a broken baseline.

**Speed rule:** Mid-increment feedback stays **scoped**. Save the **full** project verify set for the slice boundary below.

### Before claiming a slice complete

1. **Discover** what this project defines as verification for the **current language / module / track** you touched — scripts, Makefile targets, CI jobs, documented commands, or equivalent. Inspect README, contribution guides, CI config, Sonar/static-analysis config, and existing tooling; do not assume a single command.
2. **Run every applicable verify step** for that scope — **now** include the **full** relevant test suite (not only the one test from the last RGR) plus build/compile, typecheck, lint, format, and code quality platforms when the project defines them (e.g. SonarQube, SonarCloud, CodeClimate), and adopted practices (mutation, contract, …). In a **monorepo / multi-module** project, "full relevant test suite" means the suite **scoped to the module/package/app you touched** when the project defines a narrower command for that — run the entire repository's suite only when no such scoping exists.
3. **Fix violations you introduced** — leave lint, static analysis, and quality gates **without new warnings or errors** attributable to your change.
4. **Hard green gate:** do **not** mark the backlog line `[x]`, claim done, or hand off as complete while **any** applicable verify step is red. Fix first; then re-run the **full** applicable set.
5. **Report** each command run and pass or fail (verification table).

**Applicable vs out-of-scope:** **Applicable** = steps that cover the language/module/files you touched (or project gates that always run for that track). Pre-existing red on **debt outside your slice** must be documented with evidence — it does **not** block `[x]` once in-scope steps are green — but do **not** claim the whole project is clean. Failures in files you edited are in-scope: fix them.

**Principle:** One green signal (e.g. only the test runner) is not equivalent to “the project verifies” when the project defines additional steps (compile, typecheck, lint, integration, Sonar, packaging, etc.). Scoped runs during RGR do **not** replace this boundary gate.

**AMPD commit rule:** For AMPD delivery agents (`new-increment`, post-increment review applies, dedicated refactor sessions), **commit is part of done**. Outside AMPD agent workflows, follow the user’s git policy (commit only when asked).

**Anti-pattern:** Running the **full** suite (or full CI inventory) after every tiny RGR edit; declaring done after a subset of verify steps when the project defines more; stopping with failing **in-scope** tests “for the user to decide”; skipping re-verify after a refactor step; suppressing lint/sonar rules instead of fixing code.

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
| **REFACTOR** | Structure-only steps; verification green after each meaningful step; revert on failure. Apply [`simple-design.md`](simple-design.md): Beck rules + **mandatory** Object Calisthenics on touched OO code; introduce GoF patterns only by refactoring toward them when smells persist ([`design-quality.md`](design-quality.md)). |

**Anti-pattern:** Replacing entire test or production files in one edit with no failing run in between; leaving procedural multi-case `if`/`else` on owned OO as “done”; introducing speculative pattern hierarchies in GREEN.

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
| **Role completed** | planning \| one increment \| post-increment review \| fix execution \| tweak \| harness \| refactor \| fix |
| **Orchestration mode** | step \| automatic (planning / `new-feature` only); plan-confirmation outcome |
| **Backlog** | Which line marked complete (if increment) — **at most one** |
| **Commits** | SHA(s) / messages for this slice (increment: squashed to **one**; review/fix/tweak must leave work committed) |
| **Mini-journal** | Recap + review-focus bullets (increment only) — feeds `increment-review` and the feature PR description |
| **Verdict** | approved \| changes-requested \| bug-found (post-increment review only) |
| **Branch** | Feature branch name (e.g. `feat/<stem>`) — same branch for all increments of the feature (§1a) |
| **Verification** | Each project verify step run → pass/fail — **all must be pass** to claim done |
| **Test strategy** | Practices evaluated → adopt or skip with reason ([`test-strategy-selection.md`](test-strategy-selection.md) §6) |
| **Design** | Simple Design / Object Calisthenics / patterns note ([`design-quality.md`](design-quality.md); required when OO production code was touched) |
| **RED cycles** | Count per behavior, or batch mode noted |
| **Layers** | e.g. unit + mutation \| API acceptance + inner TDD \| characterization only |
| **Change-surface** | Search performed yes/no; what was updated |
| **Post-increment review** | Verdict (see above) / pending (`new-feature` orchestration) |
| **Handoff** | Next open backlog line — **do not implement** (`new-increment`); or continue/stop decision (`new-feature`) |
| **PR** | Not yet / drafted awaiting confirmation / opened at `<url>` (`new-feature`, once the backlog is fully `[x]`) |

---

## Composition map

| Skill / agent | Uses especially |
|---------------|-----------------|
| `new-feature` | §1 orchestration modes + plan confirmation gate, **§1a feature branch**, §10 handoff, PR from mini-journals |
| `new-increment` | §1–3, **§1a** (stay on feature branch), §5–6, §10; always one line + squashed commit + mini-journal + green gate; [`project-verification.md`](project-verification.md); [`test-strategy-selection.md`](test-strategy-selection.md); [`simple-design.md`](simple-design.md) / [`design-quality.md`](design-quality.md) |
| `increment-review` (skill) / `increment-review` (agent) | §1 post-increment review — fast single pass driven by the mini-journal; [`code-review.md`](code-review.md); [`design-quality.md`](design-quality.md) |
| `legacy-testing` | §8; [`project-verification.md`](project-verification.md); [`test-strategy-selection.md`](test-strategy-selection.md) |
| `refactoring` (skill) / `refactoring` (agent) | Executes an `increment-review` fix brief, dedicated structure pass (§7, §9, §2), **or** legacy manual post-increment review (full/light) on direct request; [`project-verification.md`](project-verification.md); [`simple-design.md`](simple-design.md) / [`design-quality.md`](design-quality.md) |
| `legacy-refactor` (agent) | §1, §7–9, §2 — harness then structure (distinct from `refactoring` alone) |
| `tweak` (skill) / `tweak` (agent) | §2 scoped verify, §10 minimal payload — small edit on the current branch, no §1/§1a ceremony |
| `tdd` | §6; [`project-verification.md`](project-verification.md); [`test-strategy-selection.md`](test-strategy-selection.md); [`simple-design.md`](simple-design.md) |
| `atdd` | §4; [`project-verification.md`](project-verification.md); [`test-strategy-selection.md`](test-strategy-selection.md) |
| `bugfix` | §2, §3, §7; [`project-verification.md`](project-verification.md); [`test-strategy-selection.md`](test-strategy-selection.md) |
