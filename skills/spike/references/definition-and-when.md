# Definition and when to spike

## Definition (Extreme Programming)

A **spike solution** is a **very simple program** (or experiment) used to explore a **tough technical or design problem**. It addresses **only that problem** and ignores other concerns. **Most spikes are not good enough to keep** — expect to throw them away. Goals:

- **Reduce technical risk**
- **Improve reliability of estimates**
- Answer: *What is the simplest thing we can try that convinces us we are on the right track?*

Sources: [XP — Create a spike solution](http://www.extremeprogramming.org/rules/spike.html); [C2 — Spike Solution](https://c2.com/xp/SpikeSolution.html) (Kent Beck, Ward Cunningham).

---

## Knowledge-limited, not time-limited

Kent Beck’s guidance (often cited): spikes help when the team is **knowledge-limited** — you genuinely do not know if an approach works — not when you only lack calendar time but already know what to build.

If requirements and approach are clear, use delivery skills instead.

---

## Good triggers

- **Library / API** — will it do what we need? licensing? ergonomics?
- **Integration** — can system A talk to B with acceptable auth and data?
- **Performance envelope** — rough bound (e.g. under 200ms for N rows) before design commitment
- **Feasibility** — is this algorithm or platform constraint survivable?
- **Estimate** — how big is the unknown slice? (spike to bound, not to implement)
- **Walking skeleton** — thinnest path to see wiring (still disposable on `spike/…` branch)

---

## When not to spike

| Situation | Use instead |
|-----------|-------------|
| Known bug, wrong behavior | **`skills/bugfix`** |
| Agreed feature, need examples + tests | **`skills/atdd`** → **`skills/tdd`** |
| Untested code you must change in prod | **`skills/legacy-testing`** |
| Structure only, tests already green | **`skills/refactoring`** |
| “We’re late, skip design” | Not a spike — that’s schedule pressure |

---

## Experiment vs product

A spike is an **experiment**: isolated branch, disposable code, **report** as the durable artifact. Product work starts **after** promotion on a **non-spike** workflow.
