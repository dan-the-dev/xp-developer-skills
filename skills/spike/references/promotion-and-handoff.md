# Promotion and handoff

## After the spike ends

Three outcomes:

| Outcome | Action |
|---------|--------|
| **Discard** | Delete or abandon `spike/<slug>` branch; keep report; no merge |
| **Follow-up spike** | Narrower hypothesis; **new** `spike/…` branch |
| **Promote** | Start **delivery** on a **new** branch with the right skill |

---

## Promotion decision tree

1. **Still don’t know if it’s possible?** → another spike (smaller question).
2. **Possible, but production area has no tests and you must edit it?** → **`skills/legacy-testing`** on a delivery branch.
3. **Need stakeholder-visible examples and acceptance checks?** → **`skills/atdd`** (example catalog, Distill→Develop).
4. **Clear programmer slice, examples already agreed?** → **`skills/tdd`** (test list, R–G–R).

You may sequence: e.g. promote to **ATDD** for examples, then **TDD** for implementation — always on **non-spike** branches with full discipline.

---

## Do not merge spike code as product

**Anti-pattern:** merging `spike/…` because “it already works.”

**Preferred:**

- **Rewrite** on `feature/…` or `feat/…` with proper tests and design.
- **Port ideas** (API shape, config keys) — not copy-paste of spike mess.
- If a **tiny** module is genuinely reusable, extract it **during** delivery with tests, not by merging the spike branch wholesale.

---

## Handoff to parent agent / team

Spike report must state:

- **Verdict** and **evidence**
- **Branch disposed:** yes / name if still open
- **Next skill:** `atdd` | `tdd` | `legacy-testing` | `none` | `spike` (follow-up)
- **One paragraph** for the delivery slice: what we now believe and what we will **not** assume without proof

---

## Refactoring and bugfix

- **Bug found during spike?** If it blocks the experiment, fix **minimally on spike branch** only to learn — or note “blocked by defect X” and switch to **`skills/bugfix`** on a proper branch if production must be fixed.
- **Refactoring urge on spike branch?** Defer — spike code is disposable; clean design belongs in **promotion**, not in the experiment.
