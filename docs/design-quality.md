# Design quality — agent playbook

How AMPD agents apply Simple Design during **REFACTOR**, **new-increment** done, and **post-increment / PR** review.

**Compass** ([`simple-design.md`](simple-design.md)):

> Simple Design + YAGNI as the compass; Object Calisthenics mandatory; patterns as emerged destinations (Kerievsky).

Read with: [`object-calisthenics.md`](object-calisthenics.md), [`design-patterns.md`](design-patterns.md).

---

## Decision order (every structure pass)

1. **Tests green** — Beck rule 1. If red, not a design pass.
2. **Object Calisthenics** on touched OO code — mandatory ([`object-calisthenics.md`](object-calisthenics.md)). Fix breaches with the smallest Fowler moves (Extract Method, early return instead of `else`, Move Method, Introduce Parameter Object / value object, etc.).
3. **Beck rules 2–4** — reveals intention, no duplication, fewest elements.
4. **Pattern only if smell remains** with evidence (rule of three / duplicated type-switch / OCP pressure) — refactor **toward** Strategy, State, Factory Method, Null Object, … ([`design-patterns.md`](design-patterns.md)).
5. **Away from pattern** if the hierarchy is speculative or single-implementation theater.

Never pick a GoF pattern in GREEN “to be ready.” Never skip calisthenics because “a Strategy will fix it later.”

---

## Smell → simple move → pattern destination

| Smell | First simple moves | Pattern destination (when evidence) | Do not |
|-------|-------------------|-------------------------------------|--------|
| Nested indentation | Extract Method until one level | — | Leave deep nesting in an Action |
| `else` / `else if` chain | Guard clauses; extract; polymorphism | Strategy / State / subclasses | Keep procedural multi-case Action |
| `switch`/if on type or state selecting **behavior** | Extract Method per branch; then Replace Conditional with Polymorphism | State or Strategy; Factory Method holds the **only** switch | Duplicate the same switch in many methods |
| Same type/state conditional in 2+ places | — | Replace Type Code with State/Strategy | Copy-paste another `if` |
| Getter chain / ask-then-act | Tell Don’t Ask; Move Method | — | Getter eradication on pure DTOs at the edge |
| Primitive that means a domain idea | Wrap that concept | Value object (not always GoF) | Wrap every `string` at the HTTP edge |
| Collection + other fields on one type | Extract first-class collection | — | Anemic “helpers” elsewhere |
| Algorithm varies, already duplicated | Extract | Strategy | Abstract Factory for one family you don’t have |
| “Do nothing” null checks everywhere | Extract | Null Object | Optional wrapping with no behavior |
| Shared steps, varying hooks | Extract skeleton | Template Method | Deep inheritance for one variation |
| One concrete Strategy/State class | Inline Method / Inline Class | Refactor **away** | Keep empty hierarchy for “future” |

---

## Evidence thresholds (patterns)

| Evidence | Action |
|----------|--------|
| One simple alternate path | Calisthenics only (guards / extract / no `else`) — **no** new hierarchy |
| Two clear cases, no duplication elsewhere | Prefer calisthenics + clear names; pattern optional if it *reduces* elements and clarifies intention |
| Three similar cases, **or** same conditional duplicated, **or** new case would edit N switches | Refactor toward Strategy/State/polymorphism |
| Pattern present with a single implementation and no near second case | Refactor away |

This matches the TDD/refactoring **rule of three** and Beck **fewest elements**.

---

## Return payload — Design field

Delivery invocations that touch OO production code include:

```markdown
### Design
- Simple Design: ok | gaps (list)
- Object Calisthenics: compliant | breaches fixed | breach+exception (reason)
- Patterns: none | toward <Name> (why) | away from <Name> (why)
- Follow-ups: none | <file or note>
```

See [`delivery-process.md`](delivery-process.md) §10.

---

## Blocking vs non-blocking

| Finding | Increment done / PR |
|---------|---------------------|
| Calisthenics breach on OO code **introduced or substantially edited** this slice, no boundary exception | **Blocking** / must-fix |
| Duplicated type/state behavior switch introduced this slice | **Blocking** — refactor toward polymorphism or fix before done |
| Speculative pattern (YAGNI / single unused hierarchy) | **Blocking** to remove or inline before done if introduced this slice |
| Pre-existing calisthenics debt outside change surface | Non-blocking suggest / follow-up (Boy Scout only inside touched code) |
| Optional deeper extract that already passes calisthenics | Non-blocking |

---

## Anti-patterns

- **Procedural god Action** — one class branches on many domain cases with `if`/`else` instead of polymorphic types.
- **Pattern theater** — Strategy/State/Factory with no second variant and no clearer intention.
- **Calisthenics theater** — wrapping every primitive or exploding types so Beck rule 4 fails.
- **GREEN design** — implementing a full pattern before a failing test demands the behavior.
- **Golden hammer** — every conditional becomes Strategy regardless of fewest elements.

---

## Related skills

- `skills/tdd` — REFACTOR applies this playbook at proximity
- `skills/increment-review` — flags calisthenics/pattern-theater breaches in the fast post-increment pass
- `skills/refactoring` — dedicated refactor, executing an `increment-review` fix brief, or legacy manual post-increment review
- `skills/new-increment` — Design note + done checklist
- `agents/pr-reviewer` — must-fix / should-fix from this file
