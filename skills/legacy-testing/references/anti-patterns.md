# Legacy testing anti-patterns

## Harness and process

- **Production-first change** in untested code “because deadline.”
- **Skipping dependency break** — writing tests that only pass with full production cluster.
- **One mega-PR** “characterization of everything” — no pinch point discipline.

## Characterization

- Snapshots of **noise** (timestamps, ids, stack traces) locked forever.
- Tests named after **lines** instead of behaviors.
- **Conflating** bug wish with baseline — characterization must match **today** unless you explicitly document intentional behavior change.

## Test doubles

- **Over-mocking** so tests mirror wishful design, not legacy truth.
- **Under-isolating** — tests become flaky integration dice.

## Architecture fantasy

- “We must **rewrite** before tests” — usually false; **sprout** and seams first.
- **Subclass override** everywhere with no plan to converge on **DI** — permanent testing subclass zoo.

## Team / CD

- Turning **off** CI for legacy branch months.
- **Manual** only verification “for now” — becomes permanent.

## Cross-skill confusion

- Calling **refactoring** what you did when you **changed** outputs without tests — that’s **gambling**, not Fowler.
- Using **bugfix** flow without **any** runnable repro — run **`legacy-testing`** until the harness exists or scope is reduced.
