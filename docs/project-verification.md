# Project verification (shared)

Language- and project-agnostic rules for **every AMPD agent and skill that touches code**. Compose with [`delivery-process.md`](delivery-process.md) §2 (slice boundary) and §10 (return payload).

---

## 1. When to verify

| Moment | Requirement |
|--------|-------------|
| **After every meaningful code change** | Re-run the **narrowest applicable checks** so you know you did not break what you just touched — at minimum the **affected automated tests** (RED/GREEN/REFACTOR step, bugfix edit, refactor mechanical step, harness addition). |
| **Before claiming a slice complete** | **Discover and run every applicable verify step** the project defines for the language/module you touched — not only the test runner. |
| **After fixing a verify failure** | Re-run the **full applicable set** for the slice boundary, not only the step that failed. |

**Principle:** Fast feedback during work; **complete** project gates at the boundary. Never declare done after a subset when the project defines more.

**Spike exception:** On an isolated `spike/` branch, run checks only when they **directly prove the charter** ([`skills/spike/SKILL.md`](../skills/spike/SKILL.md)). Promotion to delivery skills requires full verification on a **new** branch.

---

## 2. Discover verify steps (do not assume)

Inspect the **current repository** before editing:

| Source | Look for |
|--------|----------|
| README, CONTRIBUTING, AGENTS.md | Documented verify commands, “how to run checks” |
| Package scripts | `npm run test`, `lint`, `check`, `verify`, `ci` |
| Makefile / Taskfile / justfile | `make test`, `make lint`, `make check` |
| CI config | `.github/workflows/`, `.gitlab-ci.yml`, Jenkinsfile, CircleCI |
| Mutation / property config | `stryker.conf.*`, `pitest`, `cargo-mutants`, Hypothesis/fast-check usage |
| Pre-commit / hooks | `.pre-commit-config.yaml`, husky, lefthook |
| Language tooling | `pyproject.toml`, `Cargo.toml`, `go.mod`, Maven/Gradle, etc. |
| Static analysis / quality | `sonar-project.properties`, SonarCloud badge, `.codeclimate.yml`, Semgrep, CodeQL workflow |
| Editor / IDE config | `.editorconfig`, formatter configs |

Build a **verify inventory** for the scope you will touch. Typical categories (include only what **this project** defines):

1. **Tests** — unit, integration, contract, component, e2e, smoke, **mutation**, **property-based**
2. **Build / compile** — package, bundle, link
3. **Typecheck** — tsc, mypy, pyright, etc.
4. **Lint** — ESLint, Ruff, clippy, golangci-lint, etc.
5. **Format** — Prettier, rustfmt, gofmt check, etc.
6. **Static analysis / code quality platform** — SonarQube, SonarCloud, CodeClimate, etc.
7. **Architecture / import rules** — deptrac, ArchUnit, custom lint
8. **Packaging / smoke** — installable artifact, container build, migration up/down
9. **Other project gates** — license scan, commitlint, i18n key coverage, etc.

If a category is **not** configured in the project, do not invent it. If it **is** configured, it is **mandatory** at the slice boundary.

---

## 3. Lint, format, and formal rules

When the project defines lint, format, or style gates:

- **Run them** as part of the applicable verify set at slice boundary.
- **Fix violations you introduced** — do not leave new warnings or errors for reviewers or CI.
- Prefer **project-native fix commands** (`npm run lint:fix`, `cargo fmt`, etc.) when available; otherwise edit manually to match existing style.
- **Do not weaken** rules (disable eslint-disable, `@SuppressWarnings`, `# noqa` without team convention) to force green unless the user explicitly approves.

During micro-iterations, run lint on **touched files** when a fast scoped command exists; run the **full lint gate** before claiming done.

---

## 4. Code quality platforms (SonarQube and equivalents)

When the project uses **SonarQube**, **SonarCloud**, **CodeClimate**, or similar:

1. **Discover** how analysis runs — local scanner (`sonar-scanner`, `sonar`), CI job, or PR decoration.
2. **Before claiming done**, ensure your changes do not introduce **new** issues the platform reports:
   - **Bugs**, **vulnerabilities**, **code smells** at or above the project’s quality gate
   - **Coverage** regressions if the project enforces coverage on changed code
   - **Duplication** or **complexity** threshold failures if gated
3. **Fix or justify** — resolve issues in code you touched; if a finding is pre-existing debt outside your slice, **state that explicitly with evidence** (do not imply the slice is clean).
4. **Target:** leave the project **without new warnings or errors** attributable to your change. If the gate fails only on pre-existing debt, report pass/fail per step honestly.

If no local scanner is documented, run the **same CI check** the project uses (e.g. push to a branch and read check output, or run the documented CI-equivalent script locally).

---

## 5. Verification table (reporting)

End every delivery invocation that touched code with a table like:

| Step | Command / job | Result |
|------|---------------|--------|
| Unit tests | `npm test` | pass |
| Lint | `npm run lint` | pass |
| Typecheck | `npm run typecheck` | pass |
| SonarQube | `sonar-scanner` / CI `sonar` job | pass (no new issues) |

Include **every step you ran**. Mark **skipped** only when genuinely not applicable to the scope, with a one-line reason.

---

## 6. Pre-existing failures

If verification fails on debt **outside** your slice:

- State that explicitly with command output or issue ids.
- Do **not** imply the slice is done.
- Do **not** silently ignore lint/sonar failures you could have fixed in files you edited.

---

## 7. Anti-patterns

- Declaring done after **only** unit tests when CI also runs lint, typecheck, or Sonar
- Skipping verify after a refactor step because “tests were green a minute ago”
- Adding broad suppressions instead of fixing violations
- Assuming no Sonar because you did not search for `sonar-project.properties` or CI jobs
- Reporting “tests pass” without listing other gates the project defines

---

## Composition

| Consumer | Uses especially |
|----------|-----------------|
| All code-touching agents | §1–5 before done; §1 during work |
| `skills/tdd`, `skills/bugfix`, `skills/refactoring` | §1 after each micro-step |
| `skills/new-increment`, `skills/legacy-testing`, `skills/atdd` | §2–4 at increment/slice boundary |
| `pr-reviewer` | §5 — ask for evidence; flag missing lint/sonar |
| `skills/spike` | §1 spike exception only |

See also [`technical-excellence-catalog.md`](technical-excellence-catalog.md) §B–D (test layers and gates) and [`test-strategy-selection.md`](test-strategy-selection.md) (when to adopt each practice).
