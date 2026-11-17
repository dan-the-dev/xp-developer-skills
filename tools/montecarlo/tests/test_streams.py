import math
import os
import random
import sys
import tempfile
import unittest
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import montecarlo as mc  # noqa: E402


def work(*items, done=None):
    data = {"items": list(items)}
    if done is not None:
        data["done"] = done
    return data


class WorkInput(unittest.TestCase):
    def test_duplicate_id_is_an_input_error(self):
        with self.assertRaisesRegex(mc.InputError, "duplicat.*I1"):
            mc.parse_work(work({"id": "I1"}, {"id": "I1"}))

    def test_dependency_on_unknown_id_is_an_input_error(self):
        with self.assertRaisesRegex(mc.InputError, "I9"):
            mc.parse_work(work({"id": "I1", "depends_on": ["I9"]}))

    def test_cycle_is_an_input_error_naming_the_cycle(self):
        with self.assertRaisesRegex(mc.InputError, "ciclo.*I1 → I2 → I3 → I1"):
            mc.parse_work(work({"id": "I1", "depends_on": ["I3"]}, {"id": "I2", "depends_on": ["I1"]},
                               {"id": "I3", "depends_on": ["I2"]}))

    def test_self_dependency_is_a_cycle(self):
        with self.assertRaisesRegex(mc.InputError, "ciclo"):
            mc.parse_work(work({"id": "I1", "depends_on": ["I1"]}))

    def test_dependency_on_a_done_item_is_satisfied(self):
        items = mc.parse_work(work({"id": "I1", "depends_on": ["I0"]}, done=["I0"]))
        self.assertEqual(items[0].depends_on, ())

    def test_item_split_rate_wins_over_the_global_default(self):
        items = mc.parse_work(work({"id": "I1"}, {"id": "I2", "split_rate": "1.0-1.5"}), default_split=(1.2, 1.2))
        self.assertEqual([i.split for i in items], [(1.2, 1.2), (1.0, 1.5)])

    def test_file_order_is_the_priority(self):
        items = mc.parse_work(work({"id": "B"}, {"id": "A"}))
        self.assertEqual([i.id for i in items], ["B", "A"])

    def test_empty_work_is_an_input_error(self):
        with self.assertRaisesRegex(mc.InputError, "nessun item"):
            mc.parse_work(work())


ONE = mc.per_stream(lambda rng, period: 1)


def specs(*items, done=None):
    return mc.parse_work(work(*items, done=done))


def chain(prefix, length, first_depends_on=()):
    items = []
    for n in range(1, length + 1):
        deps = [f"{prefix}{n - 1}"] if n > 1 else list(first_depends_on)
        items.append({"id": f"{prefix}{n}", "depends_on": deps})
    return items


def run_once(work_specs, streams, draw=ONE):
    return mc.simulate_streams(work_specs, streams, draw, trials=1, rng=random.Random(1))[0]


class StreamSimulation(unittest.TestCase):
    def test_a_chain_of_three_on_two_streams_ends_at_period_three(self):
        run = run_once(specs(*chain("A", 3)), streams=2)
        self.assertEqual(run.finished, [1, 2, 3])
        self.assertEqual(run.end, 3)

    def test_two_independent_chains_of_three_end_at_period_three(self):
        run = run_once(specs(*chain("A", 3), *chain("B", 3)), streams=2)
        self.assertEqual(run.end, 3)
        self.assertEqual(run.idle_blocked, 0)

    def test_item_unblocked_in_period_t_is_available_from_t_plus_one(self):
        run = run_once(specs(*chain("A", 3), *chain("B", 3, first_depends_on=["A1"])), streams=2)
        self.assertEqual(run.finished, [1, 2, 3, 2, 3, 4])
        self.assertEqual(run.end, 4)

    def test_leftover_capacity_does_not_reach_an_item_unblocked_in_the_same_period(self):
        run = run_once(specs(*chain("A", 3)), streams=1, draw=mc.per_stream(lambda rng, period: 5))
        self.assertEqual(run.finished, [1, 2, 3])

    def test_leftover_capacity_moves_to_the_next_ready_item(self):
        run = run_once(specs({"id": "A"}, {"id": "B"}, {"id": "C"}), streams=1,
                       draw=mc.per_stream(lambda rng, period: 2))
        self.assertEqual(run.finished, [1, 1, 2])

    def test_a_single_chain_is_not_faster_with_two_streams_and_the_extra_one_idles(self):
        one = run_once(specs(*chain("A", 4)), streams=1)
        two = run_once(specs(*chain("A", 4)), streams=2)
        self.assertEqual(two.end, one.end)
        self.assertEqual(two.idle_blocked + two.idle_drained, 4)
        self.assertEqual(one.idle_blocked + one.idle_drained, 0)

    def test_split_item_delays_its_dependents(self):
        plain = run_once(specs({"id": "A"}, {"id": "B", "depends_on": ["A"]}), streams=2)
        split = run_once(specs({"id": "A", "split_rate": "3"}, {"id": "B", "depends_on": ["A"]}), streams=2)
        self.assertEqual(plain.finished, [1, 2])
        self.assertEqual(split.finished, [3, 4])

    def test_throughput_drawn_by_an_idle_stream_is_lost(self):
        draws = mc.per_stream(lambda rng, period: 3)
        run = run_once(specs({"id": "A", "split_rate": "3"}, {"id": "B", "depends_on": ["A"]}), streams=2, draw=draws)
        self.assertEqual(run.finished, [1, 2])
        self.assertEqual(run.idle_blocked, 1)
        self.assertEqual(run.idle_drained, 1)

    def test_horizon_exceeded_is_infinite(self):
        runs = mc.simulate_streams(specs({"id": "A"}), 1, mc.per_stream(lambda r, p: 0), 1, random.Random(1),
                                   max_periods=5)
        self.assertEqual(runs[0].end, math.inf)

    def test_critical_items_are_those_finishing_last(self):
        runs = mc.simulate_streams(specs(*chain("A", 3), {"id": "B"}), 2, ONE, 10, random.Random(1))
        self.assertEqual(mc.criticality(runs, 4), [0.0, 0.0, 100.0, 0.0])

    def test_team_throughput_is_divided_between_the_streams(self):
        draws = mc.team_split(lambda rng, period: 5)
        shares = draws(random.Random(1), 1, 2)
        self.assertEqual(sorted(shares), [2, 3])
        self.assertEqual(mc.team_split(lambda rng, period: 4)(random.Random(1), 1, 2), [2, 2])


ALL_DAYS = mc.Calendar.from_spec("all")


def sample_from(csv_text, as_of):
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "h.csv")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(csv_text)
        items, _ = mc.build_items(mc.read_history_rows(path), ALL_DAYS)
    return mc.select_sample(items, as_of, 0, [], [])


# 2026-09-07 is a Monday; window Mon 7 → Thu 10 (as_of Fri 11).
WORKER_HISTORY = (
    "id,worker,completed_at\n"
    "A,W1,2026-09-07\nB,W1,2026-09-07\nC,W1,2026-09-09\n"
    "D,W2,2026-09-08\n"
    "E,W3,2026-09-10\n"
    "F,,2026-09-08\n"
)


class WorkerPool(unittest.TestCase):
    def pool(self, min_items=1):
        sample = sample_from(WORKER_HISTORY, date(2026, 9, 11))
        return mc.worker_pool(sample, ALL_DAYS, "day", min_items)

    def test_one_sample_per_period_per_worker_zeros_included(self):
        pool = self.pool()
        self.assertEqual(pool.throughput.values, [2, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1])
        self.assertEqual(pool.workers, {"W1": 3, "W2": 1, "W3": 1})

    def test_workers_below_the_threshold_are_left_out_and_reported(self):
        pool = self.pool(min_items=2)
        self.assertEqual(pool.workers, {"W1": 3})
        self.assertEqual(pool.below_threshold, {"W2": 1, "W3": 1})
        self.assertEqual(pool.throughput.values, [2, 0, 1, 0])

    def test_items_without_worker_are_excluded_and_counted(self):
        pool = self.pool()
        self.assertEqual(pool.without_worker, ["F"])
        self.assertNotIn("F", [i.id for i in pool.sample.items])
        self.assertEqual(pool.sample.filter_reason["F"], "no_worker")

    def test_weekday_sampling_uses_worker_periods_of_the_same_weekday(self):
        pool = self.pool()
        draw = mc.make_draw(pool.throughput, "weekday", lambda period: date(2026, 9, 14))  # a Monday
        values = {draw(random.Random(seed), 1) for seed in range(50)}
        self.assertEqual(values, {2, 0})

    def test_no_worker_column_is_an_explicit_error(self):
        sample = sample_from("id,completed_at\nA,2026-09-07\n", date(2026, 9, 11))
        with self.assertRaisesRegex(mc.InputError, "worker"):
            mc.worker_pool(sample, ALL_DAYS, "day", 1)


if __name__ == "__main__":
    unittest.main()
