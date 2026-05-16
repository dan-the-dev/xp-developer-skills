# Spike anti-patterns

## Branch and lifecycle

- **Spike on main or `feat/…`** — experiment mixed with delivery; hard to discard
- **Merge spike branch** as finished feature without ATDD/TDD/legacy workflow
- **No spike report** — team forgets what was learned
- **Eternal `spike/…`** — no time box, branch open for weeks

## Testing and design

- **Full test pyramid on spike branch** — wasted effort on throwaway code
- **TDD test list or ATDD catalog** on spike — wrong skill; belongs after promotion
- **Refactoring for cleanliness** on spike — defer to delivery
- **No checks when a 10-line script would prove the point** — over-manual is OK; over-engineering is not

## Mislabeling

- **“Spike” for schedule pressure** — knowledge is not the limit
- **Spike to skip acceptance** — use **atdd** when business alignment matters
- **Spike instead of bugfix** — known defect needs reproduction + fix
- **Spike instead of legacy harness** — changing prod without tests needs **legacy-testing**

## Organizational

- **Multiple overlapping spikes** without backlog clarity — refine questions
- **Spike code copied into prod** without rewrite and tests
- **CI required green on spike branch** — optional; do not block learning on delivery gates unless team explicitly wants smoke only
