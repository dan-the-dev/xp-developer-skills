# JavaScript Examples — Bugfix

These examples demonstrate safe bugfix workflows in JavaScript repositories.

---

## Example 1 — Null Email Crash

User request:
"Fix crash when email is null during account creation."

### Branch

bugfix/STR-142-null-email-validation

### RED

```js
it("returns validation error for null email", async () => {
  const response = await request(app)
    .post("/users")
    .send({ email: null });

  expect(response.status).toBe(400);
});
```

Run:

```bash
npm test users-api.spec.js
```

Result:
- failing

### GREEN

```js
if (!payload.email) {
  throw new ValidationError("email required");
}
```

### Verification

```bash
npm test users-api.spec.js
npm test users
```

Result:
- passing
