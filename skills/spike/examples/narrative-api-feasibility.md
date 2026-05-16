# Narrative example — API latency spike (disposable branch)

Fictional; adapt branch names and tools to the repo.

---

## Charter

```markdown
# Spike charter — vendor X quote API latency

Branch: spike/vendor-x-quote-latency
Time box: 4 hours
Hypothesis: Vendor X quote API returns within 200ms p95 for our typical payload (50 line items).
Success: Measured p95 ≤ 200ms over 20 calls in dev credentials.
Failure: p95 > 200ms or auth/setup blocks calls.
Out of scope: production adapter, ATDD catalog, test list, error UX, caching design.
```

Branch **`spike/vendor-x-quote-latency`** created from `main`. No work on `feat/shipping-quotes`.

---

## Explore (throwaway code)

- Small script `spike_scripts/call_vendor_x.py` on spike branch only — hardcoded fixture payload.
- Run 20 calls; log timings to stdout.
- **No** unit test package, **no** pyramid, **no** refactor of main app.

Optional: one assertion in script `assert p95_ms <= 200` to fail fast — **only** to prove the charter.

---

## Result

- p95 ≈ 340ms → **failure** of hypothesis.
- Evidence: pasted timing summary in spike report.

---

## End

- **Recommendation:** discard branch; promote to **product** only if business accepts slower quotes OR try **follow-up spike** `spike/vendor-x-with-cache-prototype` (new charter).
- Branch **deleted** (or left unmerged). Report kept in `docs/spikes/vendor-x-quote-latency.md`.
- If product continues: new **`feat/…`** branch + **`skills/atdd`** for business rules, **`skills/tdd`** for implementation — **not** merge of spike script.

---

## Lesson

Isolation + disposable code avoided coupling a half-baked client into `main`. The **report** was the deliverable; the script was not.
