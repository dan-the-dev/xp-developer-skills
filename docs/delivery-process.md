# Delivery process (shared)

Language- and project-agnostic rules for AMPD delivery skills and subagents. Compose with skill-specific workflows; do not override skill scope with convenience.

---

## 1. Role boundaries

| Role | Delivers | Must stop before |
|------|----------|------------------|
| **Feature planning** | Ordered backlog; optional empty tracking skeleton | Production code, tests, marking backlog lines complete |
| **One increment** | Exactly **one** open backlog line | Starting the next line without explicit user opt-in |
| **Harness (legacy)** | Trustworthy automated safety net for the change path | Large structural edits on unprotected code |
| **Refactor (structure)** | Behavior-preserving structure improvements | New capability or bug fixes in the same pass |
| **Capability / fix** | New behavior or corrected behavior | Silent mixing with refactor-only work |

**Delegation:** When a subagent exists for a role, invoke it for that role. Do not read its skill and perform the work in the parent thread.

**Batch mode:** Completing multiple backlog lines in one invocation requires **explicit** user request (e.g. “implement the whole feature”). Default is **one line per invocation**.

---

## 2. Project verification (definition of done)

Before claiming a slice is **complete**:

1. **Discover** what this project defines as verification for the **current language / module / track** you touched — scripts, Makefile targets, CI jobs, documented commands, or equivalent. Inspect README, contribution guides, CI config, and existing tooling; do not assume a single command.
2. **Run every applicable verify step** for that scope — not only the fastest or most familiar runner.
3. **Report** each command run and pass or fail.

**Principle:** One green signal (e.g. only the test runner) is not equivalent to “the project verifies” when the project defines additional steps (compile, typecheck, lint, integration, packaging, etc.).

**Pre-existing failures:** If verification fails on debt **outside** your slice, state that explicitly with evidence. Do not imply the slice is done.

**Anti-pattern:** Declaring done after a subset of verify steps when the project defines more.

---

## 3. Change-surface completeness

When a change alters how something is **constructed, imported, or named** (factory, type vs value, renamed API, moved module):

- **Search** the agreed scope (repo, package, or module) for obsolete usage patterns.
- Update **every** call site in scope — production, tests, examples, demos, entrypoints — not only files touched by the first verify step you ran.

**Anti-pattern:** Fixing tests while leaving entrypoints or sample code broken, or the reverse.

---

## 4. Test pyramid (one layer per concern)

For a slice, use the **lowest sufficient** automated layer:

- If the same behavior would be asserted twice at the **same** boundary, use **one** layer.
- Add a higher layer only when it proves something the lower layer cannot (real outer seam: UI, HTTP API, contract, deployable path).

**Anti-pattern:** Duplicate checks at the same layer plus markdown that only restates them.

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
| **Role completed** | planning \| one increment \| harness \| refactor \| fix |
| **Backlog** | Which line marked complete (if increment) — **at most one** |
| **Verification** | Each project verify step run → pass/fail |
| **RED cycles** | Count per behavior, or batch mode noted |
| **Layers** | e.g. inner tests only \| outer + inner |
| **Change-surface** | Search performed yes/no; what was updated |
| **Handoff** | Next open backlog line — **do not implement** |

---

## Composition map

| Skill | Uses especially |
|-------|-----------------|
| `new-feature` | §1 planning stop, §10 handoff |
| `new-increment` | §1–3, §5–6, §10 |
| `legacy-testing` | §8 |
| `refactoring` | §7, §9, §2 at session end |
| `tdd` | §6 |
| `atdd` | §4 |
| `legacy-refactor` (agent) | §1, §7–9, §2 |
