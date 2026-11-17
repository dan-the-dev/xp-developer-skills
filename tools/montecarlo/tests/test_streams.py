import os
import random
import sys
import unittest

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


if __name__ == "__main__":
    unittest.main()
