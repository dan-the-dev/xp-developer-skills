# Post-increment review

- [ ] Inputs received: feature stem, backlog line, commit SHAs/range, **review depth** (full \| light)
- [ ] Diff limited to this increment (no drive-by files)
- [ ] Explanation written (what changed)
- [ ] Test posture noted (layers + gaps vs strategy)
- [ ] Suggestions tagged `apply-now` vs `suggest-only`; **blocking** marked when applicable
- [ ] Light depth: **no** applies
- [ ] Full depth: only in-surface tiny mechanical steps for **clear leftover debt** (not a second stylistic pass)
- [ ] Tests re-run after each applied step; full verify before done
- [ ] No new behavior; no next backlog line started
- [ ] Orchestration signal set: `continue-ok` \| `blocked` \| `pending`
- [ ] Return payload / report delivered to `new-feature`
