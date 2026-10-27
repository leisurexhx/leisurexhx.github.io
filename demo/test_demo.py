"""Tests for a synthetic illustration, not for the institution's trading engine."""
import math
import unittest
from partial_adjustment_demo import illustrate


class DemoTests(unittest.TestCase):
    def test_five_days_retains_old_support(self):
        r = illustrate(5)
        self.assertEqual((r.old_names, r.new_names), (100, 0))
        self.assertAlmostEqual(r.eta, 1 - 2 ** (-1 / 5))

    def test_fast_update_adopts_new_support(self):
        r = illustrate(.5)
        self.assertEqual((r.old_names, r.new_names), (0, 100))

    def test_tie_is_explicitly_old_first(self):
        r = illustrate(1)
        self.assertAlmostEqual(r.eta, .5)
        self.assertEqual(r.old_names, 100)

    def test_weights_remain_a_simplex(self):
        for h in [.5, 1, 1.5, 5, 10, 100]:
            r = illustrate(h, 23)
            self.assertEqual(len(r.weights), 23)
            self.assertAlmostEqual(math.fsum(r.weights.values()), 1)
            self.assertTrue(all(w >= 0 for w in r.weights.values()))

    def test_invalid_half_life(self):
        for h in [0, -1, math.inf, math.nan]:
            with self.assertRaises(ValueError):
                illustrate(h)

    def test_invalid_name_budget(self):
        for n in [0, -1, 1.2, True]:
            with self.assertRaises(ValueError):
                illustrate(5, n)


if __name__ == '__main__':
    unittest.main()
