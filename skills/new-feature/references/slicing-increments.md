# Slicing increments

- **Thin vertical slice** — demonstrable behavior for that slice (through the **lowest** seam that proves it — often unit tests for domain/kata)
- **Releasable** — product not worse after merge; for teaching katas, “releasable” means green suite + backlog line, not necessarily seven production deploys
- **Ordered** — later increments build on earlier ones
- **One rule or outcome per increment** when teaching (FizzBuzz: 3, then 5, then generalize 3, 5, 15)

**Pedagogical slices** (FizzBuzz: “3 → Fizz” then “multiples of 3”) are valid for learning but are **not** seven independent products — **new-increment** still runs one at a time with real RED→GREEN each time.

Split when you cannot describe **done** in one sentence or one TDD cycle would cover unrelated rules.

See `skills/new-increment/references/scoped-atdd-tdd.md` for when ATDD is worth adding on top.
