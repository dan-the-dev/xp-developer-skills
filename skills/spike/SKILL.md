---
name: spike
description: XP-style spike — time-boxed experiment on an isolated branch; code is disposable. Answer one technical or design question (feasibility, library fit, performance bound, integration). Use automated checks only when they help prove the goal — no delivery test pyramid, no ATDD/TDD discipline on the spike branch. Explicit promotion to skills/atdd, skills/tdd, or skills/legacy-testing when learning is done. Use for unknowns before committing to product work, not for shipping features.
allowed-tools: Read, Edit, MultiEdit, Bash, Grep, Glob
---

# Spike (time-boxed experiment)

## Mission

A **spike** is a **small, time-boxed experiment** to **reduce uncertainty**: prove a point, test an idea, a feature approach, or a **library / API / integration** — not to deliver production-ready software.

**All spike code lives on an isolated branch** (see [references/charter-and-timebox.md](references/charter-and-timebox.md)). Treat that branch as **throwaway**: merge to main only after **explicit promotion** into normal delivery workflows; default outcome is **discard** the branch and keep the **spike report**.

Optimize for:

- **One clear question** (hypothesis) and **evidence** (yes / no / inconclusive)
- **Isolation** — experiment does not pollute main or production paths
- **Speed of learning** — ignore polish, pyramid, and “proper” architecture unless they are the question
- **Honest handoff** — promotion to **`skills/atdd`**, **`skills/tdd`**, or **`skills/legacy-testing`** when building for real

NOT for:

- shipping user-facing behavior from the spike branch as-is
- full **test pyramid**, example catalogs, or test lists on the spike branch
- **`skills/bugfix`**, **`skills/refactoring`** (delivery hats), or legacy harness **unless** the spike question is specifically “can we test this seam?”

---

## What a spike is (XP)

From Extreme Programming: a **very simple program** (or script) that explores a **tough technical or design problem**, addresses **only that problem**, and is **often thrown away**. Goal: **reduce risk** or **improve estimates** — “What is the simplest thing we can try that convinces us we are on the right track?” (Kent Beck / Ward Cunningham).

Use spikes when you are **knowledge-limited**, not merely **time-limited**. See [references/definition-and-when.md](references/definition-and-when.md).

---

## Isolated branch (mandatory)

Before writing spike code:

1. **Create a dedicated branch** — e.g. `spike/<short-question-slug>` off the agreed base (`main` / `develop`).
2. **Do all spike edits on that branch only** — no mixed commits on feature or main branches.
3. **Assume disposal** — do not depend on spike structure in production; do not ask reviewers to treat spike code as product.

When the spike ends:

- **Discard:** delete branch or abandon without merge; keep **spike report** (charter artifact).
- **Promote:** open a **new** branch / slice and re-implement (or carefully port **ideas**, not bulk paste) under **`skills/atdd`** / **`skills/tdd`** / **`skills/legacy-testing`**.

---

## Tests on a spike (pragmatic only)

Spikes are **not** governed by the delivery test pyramid ([references/spike-vs-other-skills.md](references/spike-vs-other-skills.md)).

| Use automated checks when… | Skip when… |
|----------------------------|------------|
| They **directly prove** the hypothesis (script assertion, one integration call, timing log) | You would be building a “proper” unit/integration suite for maintainability |
| A failing check would **invalidate** the approach quickly | ATDD example catalog or TDD test list is required |
| A one-off test is **faster** than manual clicking | Refactoring for testability is unrelated to the question |

**No requirement** for: layered pyramid, characterization of full modules, Gherkin, CI gates on the spike branch, or green-before-every-step TDD. Manual proof (logs, screenshots, measured latency) is valid when it answers the charter.

---

## Workflow

### 1. Charter (before code)

Record in chat or **`docs/spikes/<slug>.md`** (see [references/charter-and-timebox.md](references/charter-and-timebox.md)):

- **Hypothesis / question** (one sentence)
- **Success signal** / **failure signal**
- **Time box**
- **Out of scope** (including: “no production design”, “no full test suite”)
- **Branch name** (`spike/…`)

### 2. Explore (on spike branch only)

- Smallest code, script, or config to learn
- Stop when the question is answered or the time box expires
- Prefer **prove the point** over **clean code**

### 3. Stop and report

Produce a **spike report** (template in [Output format](#output-format)):

- Verdict: **yes** / **no** / **inconclusive**
- Evidence
- **Recommendation:** **discard branch** | **promote** (which skill next) | **follow-up spike** (narrower question)

### 4. Promotion (explicit only)

If building product:

| Situation | Next skill |
|-----------|------------|
| Need agreed business examples + acceptance | **`skills/atdd`** |
| Clear slice, programmer tests | **`skills/tdd`** |
| Untested production area must change | **`skills/legacy-testing`** first |
| Still unknown | Another **spike** with a smaller question |

Do **not** merge spike branch as “done feature.”

Detail: [references/promotion-and-handoff.md](references/promotion-and-handoff.md).

---

## Composition with other skills

| Skill | Relationship |
|-------|----------------|
| **`skills/atdd`** | After spike: agree examples and automate acceptance on a **delivery** branch |
| **`skills/tdd`** | After spike: test list + R–G–R for real behavior |
| **`skills/legacy-testing`** | After spike: harness when you must change untested code |
| **`skills/refactoring`** | Not on spike branch for cleanup; optional on **delivery** branch if tests green |
| **`skills/bugfix`** | Wrong tool — known defect needs bugfix, not exploration |

---

## Anti-patterns (summary)

- Spike code on **main** or a **feature** branch without isolation
- Merging spike branch without **promotion** plan
- Building **full** test pyramid “while we’re here”
- **Eternal spike** — no time box, no report
- **Spike-as-feature** — shipping spike code without ATDD/TDD

Full list: [references/anti-patterns.md](references/anti-patterns.md).

---

## Definition of done (spike slice)

- Charter recorded; work on **`spike/…`** branch only
- Time box honored or explicitly extended with reason
- **Spike report** complete (verdict + evidence + recommendation)
- Branch **discarded** or **promotion** named with target skill — not ambiguous “we’ll clean later”

Checklists: [checklists/before-spike.md](checklists/before-spike.md), [checklists/spike-done.md](checklists/spike-done.md).

---

## Output format

```markdown
## Spike: <short title>

### Charter
- Branch: `spike/<slug>` (isolated; disposable)
- Hypothesis: …
- Success / failure: …
- Time box: …
- Out of scope: …

### What we tried (on spike branch only)
- …

### Evidence
- …

### Verdict
- yes | no | inconclusive

### Recommendation
- discard branch | promote to <atdd | tdd | legacy-testing | follow-up spike>
- If promote: what to re-build cleanly on a new branch (do not assume spike code merges as-is)

### Tests used (if any)
- Purpose-built checks only: … — or “none; manual / script evidence”
```

---

## Additional resources

### References

- [references/definition-and-when.md](references/definition-and-when.md)
- [references/charter-and-timebox.md](references/charter-and-timebox.md)
- [references/promotion-and-handoff.md](references/promotion-and-handoff.md)
- [references/spike-vs-other-skills.md](references/spike-vs-other-skills.md)
- [references/anti-patterns.md](references/anti-patterns.md)

### Examples

- [examples/narrative-api-feasibility.md](examples/narrative-api-feasibility.md)

### Checklists

- [checklists/before-spike.md](checklists/before-spike.md)
- [checklists/spike-done.md](checklists/spike-done.md)

### Bibliography

- [docs/spike-skill-bibliography.md](../../docs/spike-skill-bibliography.md)

## Resource usage

Open references when branch isolation, test scope, or promotion vs discard is unclear.
