# Anti-patterns

- Two or more parent backlog `[x]` in one invocation without explicit user “implement all increments”
- **Duplicate pyramid** — acceptance and unit tests with the same assertions on the same in-process API
- **Per-increment markdown sprawl** — `test-lists/fizz-for-three.md`, `acceptance-examples/buzz-for-five.md`, etc., when one feature file suffices
- **Retrospective checklists** — `[x]` on markdown before failing tests existed
- **Big-bang delivery** — full test file + full production file in one write; no RED in transcript
- Whole-feature acceptance file while doing one slice (unless that file is sectioned and only one section active)
- Skip TDD for behavior provable at unit layer
- Run ATDD when no outer seam (library/kata in one package)
- Forget to mark parent `increments/…` line `[x]`
- **Circular oracle** — expected output computed only by calling production code under test for the same requirement
- Continue to next increment without user ask
- **Done after one verify step** when the project defines more (delivery-process §2; lint, SonarQube, etc.)
- **Unit-only default** without test strategy table ([`test-strategy-selection.md`](../../../docs/test-strategy-selection.md))
- **Ignoring configured CI jobs** (mutation, contract, component) when slice matches
- **Skipping re-verify** after a production or refactor edit because tests were green earlier
- Skipping **change-surface search** after factory/API/rename changes (§3)
