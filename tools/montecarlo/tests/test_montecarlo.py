import contextlib
import csv
import io
import json
import math
import os
import random
import sys
import tempfile
import unittest
from datetime import date, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXAMPLES = os.path.join(ROOT, "examples")
sys.path.insert(0, ROOT)

import montecarlo as mc  # noqa: E402

ALL_DAYS = mc.Calendar.from_spec("all")
WORKDAYS = mc.Calendar.from_spec("workdays")
HEADER = "id,type,tags,ready_at,started_at,completed_at\n"


def write(directory, name, content):
    path = os.path.join(directory, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)
    return path


def items_from(csv_text, calendar=ALL_DAYS):
    with tempfile.TemporaryDirectory() as tmp:
        rows = mc.read_history_rows(write(tmp, "h.csv", csv_text))
    return mc.build_items(rows, calendar)


def run_cli(*args):
    stdout, stderr = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        code = mc.main(list(args))
    return code, stdout.getvalue(), stderr.getvalue()


class LeadAndCycleTime(unittest.TestCase):
    def test_lead_and_cycle_time_in_calendar_days(self):
        items, rejected = items_from(
            HEADER + "A-101,feature,checkout,2026-09-01T09:00:00Z,2026-09-03T08:30:00Z,2026-09-08T16:45:00Z\n"
        )
        self.assertEqual(rejected, [])
        item = items[0]
        self.assertAlmostEqual(item.lead_time, 7.323, places=3)
        self.assertAlmostEqual(item.cycle_time, 5.344, places=3)
        self.assertFalse(item.lead_fallback)

    def test_lead_time_falls_back_to_started_at_when_ready_at_is_missing(self):
        items, _ = items_from(HEADER + 'A-103,feature,"reporting;export",,2026-09-07T09:10:00Z,2026-09-15T17:00:00Z\n')
        item = items[0]
        self.assertTrue(item.lead_fallback)
        self.assertEqual(item.lead_time, item.cycle_time)
        self.assertEqual(item.tags, ("reporting", "export"))

    def test_working_day_calendar_skips_the_weekend(self):
        items, _ = items_from(
            HEADER + "A-101,feature,,2026-09-01T09:00:00Z,2026-09-03T08:30:00Z,2026-09-08T16:45:00Z\n", WORKDAYS
        )
        self.assertAlmostEqual(items[0].lead_time, 5.323, places=3)
        self.assertAlmostEqual(items[0].cycle_time, 3.344, places=3)

    def test_holidays_are_not_counted(self):
        calendar = mc.Calendar.from_spec("all", {date(2026, 9, 2)})
        start, end = datetime(2026, 9, 1), datetime(2026, 9, 4)
        self.assertAlmostEqual(calendar.working_days_between(start, end), 2.0)

    def test_item_without_started_at_has_no_cycle_time_but_counts_as_completed(self):
        items, rejected = items_from(HEADER + "A-1,bug,,,,2026-09-04T10:00:00Z\n")
        self.assertEqual(rejected, [])
        self.assertIsNone(items[0].cycle_time)
        self.assertIsNone(items[0].lead_time)
        self.assertIn("no_started_at", items[0].flags)


class MalformedRecords(unittest.TestCase):
    def test_malformed_records_are_rejected_with_a_reason(self):
        _, rejected = items_from(
            HEADER
            + ",feature,,,2026-09-01,2026-09-02\n"
            + "B-1,feature,,,2026-09-01,\n"
            + "B-2,feature,,,2026-09-01,not-a-date\n"
            + "B-3,feature,,,yesterday,2026-09-02\n"
            + "B-4,feature,,soon,2026-09-01,2026-09-02\n"
            + "B-5,feature,,,2026-09-05,2026-09-02\n"
            + "B-6,feature,,2026-09-05,,2026-09-02\n"
            + "B-7,feature,,,2026-09-01,2026-09-02\n"
            + "B-7,feature,,,2026-09-01,2026-09-03\n"
        )
        self.assertEqual(
            [r.reason for r in rejected],
            [
                "missing_id",
                "missing_completed_at",
                "invalid_completed_at",
                "invalid_started_at",
                "invalid_ready_at",
                "started_after_completed",
                "ready_after_completed",
                "duplicate_id",
            ],
        )

    def test_missing_required_column_is_a_clear_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write(tmp, "h.csv", "id,started_at\nA-1,2026-09-01\n")
            with self.assertRaisesRegex(mc.InputError, "completed_at"):
                mc.read_history_rows(path)

    def test_missing_file_is_a_clear_error(self):
        with self.assertRaisesRegex(mc.InputError, "non trovato"):
            mc.read_history_rows("/nonexistent/history.csv")

    def test_rejections_are_counted_in_the_report_and_control_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            history = os.path.join(EXAMPLES, "history.csv")
            with open(history, encoding="utf-8") as handle:
                content = handle.read() + "BAD-1,feature,,,2026-09-01,garbage\n"
            path = write(tmp, "h.csv", content)
            code, _, _ = run_cli("epic", "--history", path, "--as-of", "2026-10-12", "--remaining", "5",
                                 "--seed", "1", "--trials", "200", "--out-dir", tmp)
            self.assertEqual(code, 0)
            with open(os.path.join(tmp, "result.json"), encoding="utf-8") as handle:
                report = json.load(handle)
            self.assertEqual(report["data"]["rejected"]["count"], 1)
            self.assertEqual(report["data"]["rejected"]["reasons"], {"invalid_completed_at": 1})
            with open(os.path.join(tmp, "control.csv"), encoding="utf-8") as handle:
                statuses = [row["status"] for row in csv.DictReader(handle)]
            self.assertEqual(statuses.count("rejected"), 1)

    def test_json_history_is_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write(tmp, "h.json", json.dumps({"items": [
                {"id": "J-1", "started_at": "2026-09-01", "completed_at": "2026-09-03", "tags": ["a", "b"]},
            ]}))
            items, rejected = mc.build_items(mc.read_history_rows(path), ALL_DAYS)
        self.assertEqual(rejected, [])
        self.assertEqual(items[0].tags, ("a", "b"))
        self.assertAlmostEqual(items[0].cycle_time, 2.0)


class Throughput(unittest.TestCase):
    def sample(self, csv_text, as_of, weeks=0):
        items, _ = items_from(csv_text)
        return mc.select_sample(items, as_of, weeks, [], [])

    def test_days_without_completions_are_included_as_zero(self):
        sample = self.sample(
            HEADER + "A,,,,,2026-09-01T10:00:00\nB,,,,,2026-09-01T12:00:00\nC,,,,,2026-09-04T10:00:00\n",
            as_of=date(2026, 9, 6),
        )
        throughput = mc.compute_throughput(sample, ALL_DAYS, "day")
        self.assertEqual(throughput.values, [2, 0, 0, 1, 0])

    def test_completion_on_a_non_working_day_goes_to_the_previous_working_day(self):
        sample = self.sample(HEADER + "A,,,,,2026-09-04T10:00:00\nB,,,,,2026-09-05T10:00:00\n", as_of=date(2026, 9, 8))
        throughput = mc.compute_throughput(sample, WORKDAYS, "day")
        self.assertEqual(throughput.periods, [(date(2026, 9, 4), 2), (date(2026, 9, 7), 0)])

    def test_weekly_throughput_includes_empty_weeks(self):
        sample = self.sample(
            HEADER + "A,,,,,2026-08-03T10:00:00\nB,,,,,2026-08-20T10:00:00\n", as_of=date(2026, 8, 31)
        )
        throughput = mc.compute_throughput(sample, ALL_DAYS, "week")
        self.assertEqual(throughput.values, [1, 0, 1, 0])

    def test_zero_throughput_everywhere_is_insufficient_history(self):
        throughput = mc.Throughput("day", [(date(2026, 9, 1), 0)])
        with self.assertRaisesRegex(mc.InputError, "Storico insufficiente"):
            mc.make_draw(throughput, "uniform", lambda p: None)


class Simulation(unittest.TestCase):
    def test_when_counts_periods_until_target_is_reached(self):
        runs = mc.simulate_sequence([5], lambda rng, p: 2, trials=3, rng=random.Random(1))
        self.assertEqual(runs, [[3], [3], [3]])

    def test_epics_group_two_never_finishes_before_group_one(self):
        rng = random.Random(7)
        values = [0, 0, 1, 2, 3, 0, 1]
        draw = lambda r, p: values[r.randrange(len(values))]  # noqa: E731
        runs = mc.simulate_sequence([4, 0, 6, 3], draw, 2000, rng, splits=[(1.0, 1.5)] * 4)
        for reached in runs:
            self.assertEqual(reached, sorted(reached))

    def test_group_with_nothing_left_finishes_with_the_previous_one(self):
        runs = mc.simulate_sequence([0, 2], lambda rng, p: 1, trials=1, rng=random.Random(1))
        self.assertEqual(runs, [[0, 2]])

    def test_split_rate_raises_the_count(self):
        rng = random.Random(3)
        draws = [mc.apply_split(10, (1.0, 1.5), rng) for _ in range(500)]
        self.assertTrue(all(10 <= d <= 15 for d in draws))
        self.assertGreater(max(draws), 10)
        self.assertEqual(mc.apply_split(10, (1.2, 1.2), rng), 12)

    def test_how_many_sums_the_available_periods(self):
        self.assertEqual(mc.simulate_how_many(4, lambda rng, p: 3, 2, random.Random(1)), [12, 12])

    def test_percentiles_read_as_within_and_at_least(self):
        values = list(range(1, 101))
        self.assertEqual(mc.percentile_within(values, 85), 85)
        self.assertEqual(mc.percentile_at_least(values, 85), 16)
        self.assertEqual(mc.percentile_within([10] * 3, 50), 10)

    def test_horizon_exceeded_is_reported_as_infinite(self):
        runs = mc.simulate_sequence([1], lambda rng, p: 0, 1, random.Random(1), max_periods=5)
        self.assertEqual(runs, [[math.inf]])


class EndToEnd(unittest.TestCase):
    def run_mode(self, *args):
        with tempfile.TemporaryDirectory() as tmp:
            code, _, err = run_cli(*args, "--config", os.path.join(EXAMPLES, "config.json"),
                                   "--demo", "--trials", "2000", "--out-dir", tmp)
            self.assertEqual(code, 0, err)
            with open(os.path.join(tmp, "result.json"), encoding="utf-8") as handle:
                report = json.load(handle)
            self.assertTrue(os.path.isfile(os.path.join(tmp, "summary.md")))
            self.assertTrue(os.path.isfile(os.path.join(tmp, "control.csv")))
        return report

    def test_same_seed_gives_same_result_in_every_mode(self):
        groups = os.path.join(EXAMPLES, "groups.json")
        for args in (("single", "--type", "feature"), ("epic", "--remaining", "24", "--deadline", "2026-11-30"),
                     ("epics", "--groups", groups, "--split-rate", "1.0-1.3")):
            with self.subTest(mode=args[0]):
                self.assertEqual(self.run_mode(*args)["result"], self.run_mode(*args)["result"])

    def test_epics_report_is_ordered_and_consistent(self):
        report = self.run_mode("epics", "--groups", os.path.join(EXAMPLES, "groups.json"))
        self.assertTrue(report["result"]["sequence_consistent"])
        groups = report["result"]["groups"]
        self.assertEqual([g["name"] for g in groups], ["Onboarding", "Reporting", "Export"])
        self.assertEqual(groups[1]["remaining"], 6)
        for earlier, later in zip(groups, groups[1:]):
            for a, b in zip(earlier["percentiles"], later["percentiles"]):
                self.assertLessEqual(a["periods"], b["periods"])

    def test_small_sample_is_flagged_low_reliability_but_still_shown(self):
        report = self.run_mode("epic", "--remaining", "5", "--type", "chore")
        self.assertEqual(report["reliability"]["level"], "low")
        self.assertTrue(any("Campione piccolo" in w for w in report["reliability"]["warnings"]))
        self.assertIsNotNone(report["result"]["when"]["percentiles"][0]["date"])

    def test_short_history_is_flagged_low_reliability(self):
        report = self.run_mode("epic", "--remaining", "5", "--window-weeks", "4")
        self.assertTrue(any("Storico breve" in w for w in report["reliability"]["warnings"]))

    def test_single_item_in_progress_conditions_on_its_age(self):
        report = self.run_mode("single", "--type", "feature", "--elapsed-days", "4")
        result = report["result"]
        self.assertLess(result["conditional_sample_size"], result["sample_size"])
        self.assertTrue(all(p["days"] is None or p["days"] > 4 for p in result["percentiles"]))

    def test_empty_window_is_a_clear_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, _, err = run_cli("epic", "--history", os.path.join(EXAMPLES, "history.csv"),
                                   "--as-of", "2026-01-01", "--remaining", "3", "--demo", "--out-dir", tmp)
        self.assertEqual(code, 2)
        self.assertIn("ERRORE", err)


class ExampleDataGuard(unittest.TestCase):
    def test_example_history_is_refused_without_demo(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, _, err = run_cli("epic", "--config", os.path.join(EXAMPLES, "config.json"),
                                   "--remaining", "3", "--out-dir", tmp)
            self.assertEqual(code, 2)
            self.assertIn("dati di esempio", err)
            self.assertIn("chiedi", err)
            self.assertFalse(os.path.exists(os.path.join(tmp, "result.json")))

    def test_demo_runs_on_example_history_and_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out, err = run_cli("epic", "--config", os.path.join(EXAMPLES, "config.json"), "--demo",
                                     "--remaining", "3", "--trials", "200", "--out-dir", tmp)
            self.assertEqual(code, 0, err)
            with open(os.path.join(tmp, "result.json"), encoding="utf-8") as handle:
                report = json.load(handle)
        self.assertTrue(report["data"]["demo"])
        self.assertEqual(report["reliability"]["level"], "low")
        self.assertTrue(any("DEMO" in w for w in report["reliability"]["warnings"]))
        self.assertIn("DEMO", out)

    def test_user_history_is_not_a_demo(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(EXAMPLES, "history.csv"), encoding="utf-8") as handle:
                path = write(tmp, "h.csv", handle.read())
            code, _, err = run_cli("epic", "--history", path, "--as-of", "2026-10-12", "--remaining", "3",
                                   "--trials", "200", "--out-dir", tmp)
            self.assertEqual(code, 0, err)
            with open(os.path.join(tmp, "result.json"), encoding="utf-8") as handle:
                self.assertFalse(json.load(handle)["data"]["demo"])


if __name__ == "__main__":
    unittest.main()
