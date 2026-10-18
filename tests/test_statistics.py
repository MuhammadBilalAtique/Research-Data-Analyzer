import math
import unittest

from research_analyzer.statistics import (
    calculate_mean, calculate_median, calculate_mode, calculate_minimum,
    calculate_maximum, calculate_range, calculate_variance,
    calculate_standard_deviation, calculate_quartiles, calculate_iqr,
    find_outliers_iqr, calculate_correlation,
)


class TestDescriptiveStatistics(unittest.TestCase):
    def test_mean_calculates_average(self):
        self.assertEqual(calculate_mean([2, 4, 6]), 4)

    def test_median_handles_odd_and_even_lists(self):
        self.assertEqual(calculate_median([9, 1, 5]), 5)
        self.assertEqual(calculate_median([1, 3, 5, 7]), 4)

    def test_mode_returns_all_values_tied_for_highest_frequency(self):
        self.assertEqual(calculate_mode([1, 1, 2, 2, 3]), [1, 2])

    def test_mode_returns_none_when_no_value_repeats(self):
        self.assertIsNone(calculate_mode([1, 2, 3]))

    def test_minimum_maximum_and_range(self):
        values = [8, -2, 5, 11]
        self.assertEqual(calculate_minimum(values), -2)
        self.assertEqual(calculate_maximum(values), 11)
        self.assertEqual(calculate_range(values), 13)

    def test_population_variance(self):
        self.assertAlmostEqual(calculate_variance([2, 4, 6]), 8 / 3)

    def test_population_standard_deviation(self):
        self.assertAlmostEqual(calculate_standard_deviation([2, 4, 6]), math.sqrt(8 / 3))

    def test_empty_lists_return_none(self):
        for function in [calculate_mean, calculate_median, calculate_mode, calculate_minimum, calculate_maximum, calculate_range, calculate_variance, calculate_standard_deviation, calculate_quartiles, calculate_iqr, find_outliers_iqr]:
            with self.subTest(function=function.__name__):
                self.assertIsNone(function([]))

    def test_quartiles_and_iqr(self):
        self.assertEqual(calculate_quartiles([1, 2, 3, 4, 5, 6, 7, 8]), (2.5, 4.5, 6.5))
        self.assertEqual(calculate_iqr([1, 2, 3, 4, 5, 6, 7, 8]), 4.0)

    def test_iqr_outlier_detection(self):
        self.assertEqual(find_outliers_iqr([1, 2, 3, 4, 5, 100]), [100])

    def test_pearson_correlation_positive_and_negative(self):
        self.assertAlmostEqual(calculate_correlation([1, 2, 3], [2, 4, 6]), 1.0)
        self.assertAlmostEqual(calculate_correlation([1, 2, 3], [6, 4, 2]), -1.0)

    def test_correlation_undefined_for_constant_values(self):
        self.assertIsNone(calculate_correlation([2, 2, 2], [1, 2, 3]))

    def test_rejects_non_finite_values(self):
        self.assertIsNone(calculate_mean([1, float("nan")]))


if __name__ == "__main__":
    unittest.main()
