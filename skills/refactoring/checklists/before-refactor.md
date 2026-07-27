# Checklist — before a refactoring session

- [ ] **Goal** — one sentence: what will be easier after this?
- [ ] **Hat** — this session is **refactor-only** (no new behavior) unless explicitly split
- [ ] **Baseline** — branch clean; relevant tests **green** (`<command>` noted)
- [ ] **Scope** — files/modules in scope listed; out of scope noted
- [ ] **Safety net** — coverage adequate for scope, or scope **shrunk** to match net
- [ ] **Catalog** — 1–3 named refactorings you expect to compose (optional but helpful); if aiming at a GoF destination, note evidence ([`docs/design-quality.md`](../../../docs/design-quality.md))
- [ ] **Simple Design** — plan to enforce Object Calisthenics on touched OO ([`docs/object-calisthenics.md`](../../../docs/object-calisthenics.md))
- [ ] **Integrate plan** — small commits; how you will run CI / wider tests
