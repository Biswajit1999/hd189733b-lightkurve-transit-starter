import math
import unittest
from research.event_robustness import (bootstrap_depths, radius_ratio_sensitivity,
                                       theil_sen_slope, trend_permutation, validate)


class EventRobustnessTests(unittest.TestCase):
    def setUp(self):
        self.events = [(-2, 0.02, 10, 105), (-1, 0.021, 10, 105),
                       (1, 0.022, 10, 105), (2, 0.023, 10, 50),
                       (3, 0.024, 10, 105)]

    def test_depth_median_and_coverage(self):
        a = bootstrap_depths(self.events, draws=50)
        self.assertAlmostEqual(a["median_depth"], 0.022)
        self.assertEqual(a["baseline_100plus_events"], 4)
        self.assertAlmostEqual(a["baseline_100plus_median"], 0.0215)

    def test_bootstrap_reproducible(self):
        self.assertEqual(bootstrap_depths(self.events, draws=150, seed=12),
                         bootstrap_depths(self.events, draws=150, seed=12))

    def test_loo_robustness(self):
        a = bootstrap_depths(self.events, draws=100)
        self.assertAlmostEqual(a["max_abs_leave_one_event_out_shift"], 0.0005)

    def test_theil_sen_linear_trend(self):
        events = [(i, 0.02+0.001*i, 10, 10) for i in range(5)]
        self.assertAlmostEqual(theil_sen_slope(events), 0.001)

    def test_permutation_reproducible(self):
        self.assertEqual(trend_permutation(self.events, permutations=100, seed=3),
                         trend_permutation(self.events, permutations=100, seed=3))

    def test_constant_depth_null(self):
        events = [(i, 0.02, 10, 10) for i in range(5)]
        self.assertEqual(trend_permutation(events, permutations=50)["two_sided_permutation_p"], 1.0)

    def test_exact_nonlinear_radius_ratio(self):
        rows = radius_ratio_sensitivity(self.events, (0.0, 0.05), draws=80)
        self.assertAlmostEqual(rows[0]["radius_ratio_at_median_depth"], math.sqrt(0.022))
        self.assertAlmostEqual(rows[1]["radius_ratio_at_median_depth"] / rows[0]["radius_ratio_at_median_depth"], math.sqrt(1.05))

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            validate([(1, 0.02, 10, 10), (1, 0.03, 10, 10), (2, 0.02, 10, 10)])
        with self.assertRaises(ValueError):
            radius_ratio_sensitivity(self.events, (-0.01,))
        with self.assertRaises(ValueError):
            bootstrap_depths(self.events, draws=0)


if __name__ == "__main__":
    unittest.main()
