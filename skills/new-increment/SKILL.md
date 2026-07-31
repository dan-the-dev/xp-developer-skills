---
name: new-increment
description: Deliver one releasable increment from increments/<feature>.md — strict TDD by default (one test-lists/<feature>.md, unit tests). ATDD only when a real outer seam exists (API/UI/contract). One increment per invocation; RED before GREEN; all project verify steps green before done; commit then stop. Not for whole-feature planning (skills/new-feature).
allowed-tools: Read, Edit, MultiEdit, Bash, Grep, Glob
---

# New increment (one slice)

## Mission

Implement **exactly one** open line from `increments/<feature-stem>.md`.

**Default:** **`skills/tdd/SKILL.md`** only — unit (or narrow integration) tests, behaviors tracked in **one** `test-lists/<feature-stem>.md` (section per increment).

**When a real outer seam exists:** compose **`skills/atdd/SKILL.md`** at that boundary, then TDD inside. **Never** duplicate the same assertions in acceptance and unit layers.

**Always:** complete test strategy before first RED; during RGR run **scoped** tests only; apply **Simple Design** on REFACTOR ([`docs/simple-design.md`](../../docs/simple-design.md) — mandatory Object Calisthenics; patterns only toward evidenced smells); at the end run **all** applicable verify steps; leave the suite **green**; **commit on the feature branch**; mark the parent backlog line **`[x]`**; **stop**. Never start the next backlog line — even if the user asked for the whole feature (that is **`new-feature`** automatic mode).

---

## Workflow

Shared delivery rules: [`docs/delivery-process.md`](../../docs/delivery-process.md) and [`docs/project-verification.md`](../../docs/project-verification.md).

1. Lock scope to **one** `[ ]` backlog line. **Stay on the feature branch** `feat/<feature-stem>` (create it only if missing) — **never** a new branch per increment, and **never** merge to main between increments ([`delivery-process.md`](../../docs/delivery-process.md) §1a). Record the branch's current commit SHA (`git rev-parse HEAD`) as the **start point** — you will squash back to it in step 11.
2. **Test strategy** — [`test-strategy-selection.md`](../../docs/test-strategy-selection.md): discover configured jobs; complete adopt/skip table **before first RED** ([checklists/test-strategy.md](checklists/test-strategy.md)). On **greenfield**, introduce mutation (and other warranted practices) when characterization says adopt **and** the introduce-tooling threshold is met — do not wait to be asked; teaching/kata may skip with an explicit reason. For an **owned third-party API client**, follow §3a (prefer SDK; sandbox when feasible; else manual fake/stub).
3. **Discover project verification** for the language/module you will touch (§2; [`project-verification.md`](../../docs/project-verification.md)) — README, CI, scripts, Makefile, Sonar, **mutation** config; do not assume one command.
4. **Choose layer** — [references/scoped-atdd-tdd.md](references/scoped-atdd-tdd.md) (TDD-only vs ATDD+TDD; Gherkin only when Distill needs it).
5. **Artifacts** — [references/artifact-policy.md](references/artifact-policy.md): one feature test list; no per-increment markdown sprawl.
6. **RED → GREEN → REFACTOR** per behavior; **one failing check at a time**; after each edit run **only the narrowest tests** for what you touched (file/test id/package) — **not** the full suite mid-increment. REFACTOR must satisfy Simple Design + mandatory Object Calisthenics on touched OO ([`docs/design-quality.md`](../../docs/design-quality.md)).
7. If construction/import/API changed, **search and update all call sites** in scope (§3).
8. Update parent `increments/…` to `[x]` with link to test list section (and acceptance section if used) — **only after** verification is fully green.
9. **Cleanup** redundant slice-only markdown if created by mistake.
10. **At increment end only:** run **all** applicable project verify steps — full test suite **scoped to the module/package/app you touched** when the project is multi-module and defines a narrower command; the entire repo suite only when no such scoping exists — plus lint, format, typecheck, SonarQube, **mutation job if adopted** (§2). None may be skipped because another already passed. **If any step is red → fix; do not stop as done.**
11. **Commit — mandatory, squashed.** Ensure this increment's work is committed on the **same feature branch** (follow `skills/tdd` micro-commits during RGR). Before returning, squash every commit made since the step-1 start point into **one** commit for this line:
    ```
    git reset --soft <start-point-sha>
    git commit -m "<type>: <increment summary>"
    ```
    Confirm `git status` reports a clean working tree. **Never** return with uncommitted changes or more than one commit for this line. **AMPD agents:** commit is part of done. Outside AMPD delivery workflows, follow the user's git policy. Do **not** merge to main or open a per-increment PR unless the user asks.
12. **Mini-journal — mandatory.** Write a short recap (2–4 bullets: what shipped, key files/seams) and a review-focus note (1–3 bullets: the trickiest or riskiest part of this diff) — see Return payload. This is what `increment-review` and `new-feature` read instead of re-deriving intent from the diff.
13. **Return payload** (§10) including **test strategy table**, **Design** note ([`docs/design-quality.md`](../../docs/design-quality.md)), verification table, single commit SHA, **feature branch name**, and the **mini-journal**; **stop** — do not start the next increment.

Prep if needed: **`skills/legacy-testing`** (invalid harness), **`skills/refactoring`**, **`skills/spike`** — then resume.

---

## Definition of done

- One backlog line only; **test strategy table** completed before first RED ([`test-strategy-selection.md`](../../docs/test-strategy-selection.md))
- **All project verify steps** for this scope **passed** (§2; [`project-verification.md`](../../docs/project-verification.md)) — including adopted practices (mutation, contract, integration, etc.)
- **Hard green gate:** no applicable verify step left red
- Work **committed** and **squashed to one commit** for this line; `git status` clean — no uncommitted slice leftovers presented as done
- RED observed before each production change (see scoped reference)
- **Mini-journal** delivered (recap + review-focus bullets) for `increment-review` / `new-feature`
- Touched owned OO complies with **Object Calisthenics** / Simple Design (or stated boundary exception); no speculative pattern theater ([`docs/design-quality.md`](../../docs/design-quality.md))
- Test list lines `[x]` only with passing checks referenced
- No duplicate acceptance + unit tests for the same behavior
- Change-surface complete if APIs/seams changed (§3)
- Parent increment line `[x]`
- No behavior from **future** increments
- Return payload delivered (§10) including **Design** note when OO production was touched; **stopped** (next line is `new-feature`’s decision)

Checklist: [checklists/increment-done.md](checklists/increment-done.md), [checklists/test-strategy.md](checklists/test-strategy.md).

---

## Anti-patterns

- Implementing multiple backlog lines in one session (even under “automatic” feature mode)
- Stopping with failing tests or unverified adopted practices
- Leaving the increment uncommitted, or leaving its RGR micro-commits unsquashed, when claiming done
- Returning without a mini-journal (recap + review-focus)
- `acceptance-examples/` + unit tests with identical assertions (documentation theater)
- Per-increment `test-lists/<slice>.md` files (use one feature file)
- Marking `[x]` on markdown before tests exist or fail
- Writing full test files and full production in one step
- Skipping mutation on greenfield branchy domain with only “not configured” **when the introduce-tooling threshold is met**
- Forcing mutation tooling into teaching/kata slices or when setup clearly dominates the slice
- Batch message: “implementing increments 2–7”
- **Per-increment git branch** (`feat/<feature>-<increment-slug>`) or merge-to-main between increments — keep **one feature branch** (§1a)
- **Full suite on every RGR step** — scoped tests mid-increment; full verify only at step 10
- Leaving procedural multi-case `if`/`else` on owned OO (calisthenics breach) or introducing speculative GoF hierarchies

See [references/anti-patterns.md](references/anti-patterns.md).

---

## Additional resources

- [`docs/delivery-process.md`](../../docs/delivery-process.md)
- [`docs/test-strategy-selection.md`](../../docs/test-strategy-selection.md)
- [`docs/simple-design.md`](../../docs/simple-design.md)
- [`docs/design-quality.md`](../../docs/design-quality.md)
- [references/scoped-atdd-tdd.md](references/scoped-atdd-tdd.md)
- [references/artifact-policy.md](references/artifact-policy.md)
- [references/anti-patterns.md](references/anti-patterns.md)
