# TypeScript Examples — Bugfix

These examples demonstrate safe bugfix workflows in TypeScript repositories.

---

## Example 1 — Undefined Price Formatting

User request:
"Cart crashes when product price is undefined."

### Branch

bugfix/STR-310-undefined-price-format

### RED

```ts
it("returns fallback label for undefined price", () => {
  expect(formatPrice(undefined)).toBe("N/A");
});
```

Run:

```bash
pnpm vitest format-price.spec.ts
```

Result:

- failing

### GREEN

```ts
if (price == null) {
  return "N/A";
}
```

### Verification

```bash
pnpm vitest format-price.spec.ts
pnpm vitest cart
```

Result:

- passing
