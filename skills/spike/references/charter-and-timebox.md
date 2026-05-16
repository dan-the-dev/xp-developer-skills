# Charter, branch isolation, and time box

## Isolated branch (non-negotiable)

All spike **code** belongs on a **dedicated branch**, never mixed into ongoing feature or mainline delivery:

1. Create branch: **`spike/<slug>`**  
   - Slug from the question: `spike/vendor-x-latency`, `spike/redis-stream-consumer`
2. **Every commit** for the experiment stays on that branch until the spike ends.
3. **Default end state:** branch **not merged** — deleted or abandoned after the report is saved.
4. **Promotion** = new work on a **new** branch using **`skills/atdd`** / **`skills/tdd`** / **`skills/legacy-testing`** — treat spike code as **notes**, not as the implementation to merge.

**Why:** spikes are **throwaway experiments**. Isolation prevents accidental coupling, review fatigue, and “temporary” code becoming permanent.

---

## Charter (before any spike code)

Record in **`docs/spikes/<slug>.md`** (create folder if the repo has no convention) or in the task / PR description:

```markdown
# Spike charter — <title>

Branch: spike/<slug>
Time box: <e.g. 4 hours / end of day>
Hypothesis: <one sentence>
Success: <observable signal>
Failure: <observable signal>
Out of scope: <bullets — include "production architecture", "full test pyramid" unless those ARE the question>
```

---

## Time box

- Set a **wall-clock** or **maximum effort** before coding.
- When it expires: **write the report** even if inconclusive — extend only with an **explicit** new charter.
- Spikes should be **short** (often hours to a couple of days for a pair); long open-ended branches are a smell.

---

## What to ignore during explore (unless they are the question)

On the spike branch you **do not** owe:

- Clean layered architecture
- Full unit / integration / E2E pyramid
- Example catalogs or TDD test lists
- Fowler refactorings for style
- Production-ready error handling or observability

You **may** use a quick script test or one assertion if it **proves the hypothesis faster** than manual work.

---

## Durable artifacts

What survives after discard:

- **Spike report** (verdict, evidence, recommendation)
- **Charter file** (optional but useful in `docs/spikes/`)
- Links, numbers, screenshots — not necessarily the branch history
