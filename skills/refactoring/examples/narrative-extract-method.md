# Narrative example — Extract Function (language-agnostic)

Story, not live code.

---

## Goal

A long `checkout(cart)` mixes **total calculation** and **shipping policy**. Extract pure **shipping** logic for readability; **no** change to totals customers see.

---

## Baseline

- Tests green: `pnpm test src/checkout`
- **Hat:** refactor only

---

## Steps (each followed by same test command)

1. **Rename** misleading locals inside `checkout` if needed (optional pre-step).
2. **Extract Function** — select shipping lines into `shippingLinesFor(cart)` in the same file.
   - Run tests → green.
3. **Move Function** — move `shippingLinesFor` to `shipping.ts` (or module idiomatic to the repo).
   - Run tests → if red (cycle/import): **revert move**, fix **single** issue (e.g. wrong export) in **one** follow-up step — still mechanical.
4. **Widen** — run `pnpm test` (full unit suite) once shared module exists.

---

## Anti-narrative (what not to do)

Extract **and** add a new “premium shipping” rule in the same edit — **two hats**. Instead: extract until green, commit `refactor:`; **then** add premium shipping with new tests and `feat:`.

---

## Outcome

Same checkout totals; shipping policy lives in one **named** place — easier to find “where the pilot sits” next time.
