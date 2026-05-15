# Gherkin examples — good vs bad (illustrative)

Same business rule: shipping applies when cart weight is **above** 10 kg.

---

## Good — domain language, clear outcome

```gherkin
Feature: Shipping by cart weight

  Scenario: Shipping applies above threshold
    Given a cart weighing 11 kg
    And the cart contains shippable items
    When the customer checks out
    Then the order total includes a shipping line of 5 EUR
```

Why it works:

- Steps describe **business state** and **outcome**.
- Amount is explicit data from Discuss.
- Short enough to read in a PR.

---

## Acceptable — Scenario Outline from Discuss table

```gherkin
  Scenario Outline: Shipping by weight
    Given a cart weighing <weight> kg
    When the customer checks out
    Then shipping is <shipping>

    Examples:
      | weight | shipping |
      | 9      | excluded |
      | 11     | included |
```

Ensure **Examples** match what the business agreed (including boundary 10 kg).

---

## Bad — UI script, weak Then

```gherkin
  Scenario: Checkout page
    Given I am on "/cart"
    When I click the element with id "checkout"
    And I wait 3 seconds
    Then I see ".modal"
```

Problems:

- Coupled to URLs and CSS.
- `wait 3 seconds` invites flake.
- **Then** does not state a business outcome.

---

## Bad — duplicate catalog without link

Feature file invents scenarios never recorded in `acceptance-examples/*.md` — reviewers cannot see scope. **Fix:** add catalog lines or link each scenario to a catalog bullet.

---

## Pragmatic alternative — code-first

Catalog entry (canonical):

```markdown
- [ ] Given cart 11 kg, when checkout, then total includes shipping — (pending)
```

Automation:

```text
# pseudo — project-native test DSL
test("checkout includes shipping when weight above 10kg", ...)
```

Gherkin is **optional** when the catalog + test name carry the same clarity for your team.
