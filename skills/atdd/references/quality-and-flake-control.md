# Quality and flake control (acceptance)

Acceptance tests that lie or flake destroy the **definition of done**. Pragmatic ATDD treats trustworthiness as non-negotiable.

---

## Determinism

| Risk | Mitigation |
|------|------------|
| **Time** | inject clock; freeze time in test; avoid `sleep` — wait on conditions |
| **Randomness** | seed RNG; stub id generators in test env |
| **Async** | explicit waits on outcomes, not fixed delays |
| **Shared data** | isolated tenants/users per run; cleanup or transactions |
| **Order** | tests must not depend on execution order |
| **External services** | Prefer vendor **sandbox/test** when feasible; else **manual fake/stub** at an owned seam; HTTP mock/fixtures only as interim — document which ([`test-strategy-selection.md`](../../../docs/test-strategy-selection.md) §3a; [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)) |

---

## RED must be trustworthy

Before calling Distill done:

- Failure is **missing behavior**, not 404 from wrong URL, wrong env var, or expired token.
- Re-run once if suspicious; if flaky on empty code, **fix setup** before Develop.

---

## Data setup

- Prefer **builders/factories** over copy-pasted 200-line fixtures.
- Keep **Given** data minimal — only what the example needs.
- Document **canonical** test users/accounts in repo (not production credentials).

---

## Retries policy (pragmatic)

- **Default:** no automatic retries in local development — fix the test.
- **CI:** if retries exist, cap them and **fail the build** on repeated flake; do not normalize retry-to-green without investigation.

---

## Selectors and coupling (UI)

- Prefer **roles, labels, test ids** agreed with accessibility in mind.
- Avoid CSS paths that change with every redesign.
- Assert **outcomes** (text, URL, state), not animation frames.

---

## When to quarantine

If a scenario is flaky and blocks the team:

1. Tag `@quarantine` or move to separate job **with owner and date**.
2. Do **not** mark catalog `[x]` until restored.
3. Replace with a **lower-layer** acceptance if E2E cannot be stabilized in slice time.

---

## Performance budget

- PR acceptance target: team-defined (e.g. < 5–10 minutes for smoke).
- Split scenarios; parallelize by file where runner supports it.
- Do not add scenarios that duplicate unit coverage **and** slow CI without business value.
