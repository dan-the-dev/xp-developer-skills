# Checklist — one mechanical step

Use **after every** single transformation.

- [ ] This step is **one** mechanical intent (rename / extract / move / inline / …)
- [ ] **Tests run** — narrow first
- [ ] **Green** — if red: **revert** step; shrink; retry (do not “fix forward” unless hat switch)
- [ ] If shared code touched: **widen** test scope once local green
- [ ] **Commit** (optional per team): chunk small enough for review if committing mid-session
