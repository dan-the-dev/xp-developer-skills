# Slicing increments

- **Thin vertical slice** — demonstrable behavior end-to-end for that slice
- **Releasable** — product not worse after merge
- **Ordered** — later increments build on earlier ones
- **One rule or outcome per increment** when possible (FizzBuzz: 3, then 5, then Fizz, Buzz, FizzBuzz)

Split when you cannot describe **done** in one sentence or one ATDD+TDD cycle would cover unrelated rules.
