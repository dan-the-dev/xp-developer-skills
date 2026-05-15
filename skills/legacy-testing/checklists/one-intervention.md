# Checklist — one legacy intervention

Use per **dependency break**, **new characterization**, or **small production change**.

- [ ] **Single** goal this step (one seam, one test class, one sprout)
- [ ] Production compiles / tests run after change
- [ ] If characterization: baseline **green** on **unchanged** behavior (or **RED** only for known bug slice per bugfix flow)
- [ ] If seam only: **no** intended behavior change — spot-check one scenario
- [ ] Avoid stacking: **no** “also fix typo across repo” in same commit
- [ ] Commit message reflects hat: `test:`, `refactor:`, `feat:`, `fix:`
