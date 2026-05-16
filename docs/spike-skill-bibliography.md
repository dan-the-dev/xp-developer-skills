# Bibliography — `skills/spike` skill

The skill body avoids long citations during procedures; use this page for traceability.

---

## Primary references

- **Extreme Programming.** [Create a spike solution](http://www.extremeprogramming.org/rules/spike.html) — simple program, single problem, often discarded; risk and estimates.

- **Beck, Kent; Cunningham, Ward (via C2 wiki).** [Spike Solution](https://c2.com/xp/SpikeSolution.html) — “simplest thing to convince us we are on the right track”; spikes when **knowledge-limited**.

- **Shore, James.** *The Art of Agile Development* (2nd ed.) — spike solutions practice; return to normal delivery after learning.

---

## Composed with AMPD delivery skills

| After spike | Skill |
|-------------|--------|
| Agreed acceptance / examples | `skills/atdd` |
| Programmer implementation | `skills/tdd` |
| Untested production change | `skills/legacy-testing` |
| Structure only, green tests | `skills/refactoring` |
| Known defect | `skills/bugfix` |

- **Feathers, Michael.** *Working Effectively with Legacy Code* — sprout/wrap and harness **after** you commit to change untested code; not a substitute for a feasibility spike.

- **Farley, David / Humble, Jez.** *Continuous Delivery* — keep experiments off the mainline; integrate learning via small, tested delivery increments after the spike.

---

## Optional context

- **SAFe — Spikes** — enabler stories (technical / functional / exploratory); useful vocabulary; AMPD keeps spikes **shorter** and **branch-isolated** by default.

---

## Map to skill emphasis

| Topic | Sources |
|-------|---------|
| Definition, throwaway code | XP.org; C2 |
| Isolated `spike/…` branch | AMPD policy; CD mainline discipline |
| No delivery test pyramid on spike | AMPD composition with atdd/tdd |
| Promotion | AMPD `promotion-and-handoff` reference |
| Time box | XP; Shore |

Update when new canonical sources are adopted.
