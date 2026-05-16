# Spike vs other AMPD skills

| Dimension | **Spike** | **TDD** | **ATDD** | **Legacy testing** | **Refactoring** | **Bugfix** |
|-----------|-----------|---------|----------|-------------------|-----------------|------------|
| **Goal** | Learn; prove/disprove | Build behavior well | Build the *right* behavior | Safe change without tests | Improve structure, same behavior | Fix wrong behavior |
| **Branch** | **`spike/…` only** | Delivery branch | Delivery branch | Delivery branch | Delivery branch | `bugfix/…` |
| **Code fate** | **Throwaway** default | Keep | Keep | Keep | Keep | Keep |
| **Test pyramid** | **No** — ad hoc checks only | Full inner loop | Acceptance + compose TDD | Characterization harness | Green suite required | Failing repro test |
| **Test list / catalog** | **No** | **Yes** (`test-lists/`) | **Yes** (`acceptance-examples/`) | N/A (characterization) | N/A | N/A |
| **Design quality** | **Not required** | Emerges via tests | Outside-in | Seams for harness | Fowler steps | Minimal fix |
| **Definition of done** | Report + verdict | List `[x]`, green | Catalog `[x]`, green | Harness + change | Goal + green | Bug test green |

---

## Routing cheat sheet

- **“Will library X work?”** → **spike** on `spike/…`
- **“Ship checkout with rules Y”** → **atdd** + **tdd** (not spike)
- **“Change untested module Z”** → **legacy-testing** (not spike unless feasibility unknown first)
- **“Rename for clarity, same behavior”** → **refactoring**
- **“Login broken for user U”** → **bugfix**

---

## Tests: spike vs delivery

**Spike:** automated test **only if** it is the fastest way to show success/failure for the **charter question**. A single script, one HTTP call, one timing assertion — enough.

**Delivery:** follow skill-specific discipline (Three Laws, example catalog, Feathers algorithm, two hats, etc.).

Do not use “we’ll add proper tests on the spike branch” as a substitute for promotion.
