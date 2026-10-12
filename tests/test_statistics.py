import unittest

from research_analyzer.statistics import calculate_mean, calculate_median, calculate_mode, calculate_minimum, calculate_maximum, calculate_range, calculate_variance, calculate_standard_deviation


class TestCalculateMean(unittest.TestCase):

    def test_mean_of_positive_numbers(self):
        self.assertEqual(calculate_mean([2, 4, 6]), 4)

    def test_mean_of_decimal_numbers(self):
        self.assertEqual(calculate_mean([1.5, 2.5, 3.0]), 2.3333333333333335)

    def test_mean_of_empty_list(self):
        self.assertIsNone(calculate_mean([]))

    def test_mean_with_non_list_input(self):
        self.assertIsNone(calculate_mean("2, 4, 6"))

    def test_mean_with_non_numeric_values(self):
        self.assertIsNone(calculate_mean([2, "hello", 6]))


class TestCalculateMedian(unittest.TestCase):

    def test_median_of_odd_number_of_values(self):
        self.assertEqual(calculate_median([7, 2, 5]), 5)

    def test_median_of_even_number_of_values(self):
        self.assertEqual(calculate_median([8, 2, 6, 4]), 5)

    def test_median_of_decimal_numbers(self):
        self.assertEqual(calculate_median([1.5, 3.5, 2.5]), 2.5)
    
    def test_median_of_empty_list(self):
        self.assertIsNone(calculate_median([]))
    
    def test_median_with_non_list_input(self):
        self.assertIsNone(calculate_median("2, 4, 6"))

    def test_median_with_single_value(self):
        self.assertEqual(calculate_median([7]), 7)

    def test_median_with_negative_numbers(self):
        self.assertEqual(calculate_median([-5, -1, -3]), -3)

    def test_median_with_duplicate_values(self):
        self.assertEqual(calculate_median([2, 4, 4, 6]), 4)
    
    def test_median_with_non_numeric_values(self):
        self.assertIsNone(calculate_median([2, "hello", 6]))

    def test_median_with_mixed_numeric_types(self):
        self.assertEqual(calculate_median([2, 3.5, 5]), 3.5)

    def test_median_does_not_modify_original_list(self):
        values = [8, 2, 6, 4]
        calculate_median(values)
        self.assertEqual(values, [8, 2, 6, 4])
    
    def test_median_with_all_negative_even_values(self):
        self.assertEqual(calculate_median([-8, -2, -6, -4]), -5)

    def test_median_with_zero_values(self):
        self.assertEqual(calculate_median([0, 0, 0]), 0)

    def test_median_with_boolean_values(self):
        self.assertIsNone(calculate_median([True, False, True]))


class TestCalculateMode(unittest.TestCase):

    def test_mode_with_one_repeated_value(self):
        self.assertEqual(calculate_mode([1, 2, 2, 3]), [2])

    def test_mode_with_multiple_modes(self):
        self.assertEqual(calculate_mode([1, 1, 2, 2, 3]), [1, 2])

    def test_mode_with_no_repeated_values(self):
        self.assertIsNone(calculate_mode([1, 2, 3, 4]))

    def test_mode_with_empty_list(self):
        self.assertIsNone(calculate_mode([]))

    def test_mode_with_non_list_input(self):
        self.assertIsNone(calculate_mode("1, 2, 2"))

    def test_mode_with_zero(self):
        self.assertEqual(calculate_mode([0, 0, 1, 2]), [0])

    def test_mode_with_negative_numbers(self):
        self.assertEqual(calculate_mode([-2, -2, -1, 0]), [-2])

    def test_mode_with_decimal_numbers(self):
        self.assertEqual(calculate_mode([1.5, 1.5, 2.5]), [1.5])
    
    def test_mode_with_non_numeric_values(self):
        self.assertIsNone(calculate_mode([1, "hello", 1]))

    def test_mode_with_boolean_values(self):
        self.assertIsNone(calculate_mode([True, False, True]))

    def test_mode_with_mixed_numeric_types(self):
        self.assertEqual(calculate_mode([2, 2.0, 3]), [2])

    def test_mode_with_all_equal_values(self):
        self.assertEqual(calculate_mode([5, 5, 5, 5]), [5])

    def test_mode_does_not_modify_original_list(self):
        values = [3, 1, 3, 2]
        calculate_mode(values)
        self.assertEqual(values, [3, 1, 3, 2])


class TestCalculateMinimum(unittest.TestCase):

    def test_minimum_of_positive_numbers(self):
        self.assertEqual(calculate_minimum([5, 2, 8, 1]), 1)

    def test_minimum_of_negative_numbers(self):
        self.assertEqual(calculate_minimum([-5, -2, -8, -1]), -8)

    def test_minimum_of_decimal_numbers(self):
        self.assertEqual(calculate_minimum([2.5, 1.2, 3.8]), 1.2)

    def test_minimum_with_duplicate_values(self):
        self.assertEqual(calculate_minimum([3, 1, 1, 4]), 1)

    def test_minimum_of_single_value(self):
        self.assertEqual(calculate_minimum([7]), 7)

    def test_minimum_with_zero(self):
        self.assertEqual(calculate_minimum([0, 5, -2]), -2)

    def test_minimum_of_empty_list(self):
        self.assertIsNone(calculate_minimum([]))

    def test_minimum_with_non_list_input(self):
        self.assertIsNone(calculate_minimum((3, 1, 2)))

    def test_minimum_with_non_numeric_values(self):
        self.assertIsNone(calculate_minimum([1, "hello", 3]))

    def test_minimum_with_boolean_values(self):
        self.assertIsNone(calculate_minimum([True, 2, 3]))

    def test_minimum_with_mixed_numeric_types(self):
        self.assertEqual(calculate_minimum([2, 1.5, 3]), 1.5)

    def test_minimum_does_not_modify_original_list(self):
        values = [4, 2, 7, 1]
        original_values = values.copy()

        calculate_minimum(values)

        self.assertEqual(values, original_values)


class TestCalculateMaximum(unittest.TestCase):

    def test_maximum_of_positive_numbers(self):
        self.assertEqual(calculate_maximum([5, 2, 8, 1]), 8)

    def test_maximum_of_negative_numbers(self):
        self.assertEqual(calculate_maximum([-5, -2, -8, -1]), -1)

    def test_maximum_of_decimal_numbers(self):
        self.assertEqual(calculate_maximum([2.5, 1.2, 3.8]), 3.8)

    def test_maximum_with_duplicate_values(self):
        self.assertEqual(calculate_maximum([3, 4, 4, 1]), 4)

    def test_maximum_of_single_value(self):
        self.assertEqual(calculate_maximum([7]), 7)

    def test_maximum_with_zero(self):
        self.assertEqual(calculate_maximum([0, 5, -2]), 5)

    def test_maximum_of_empty_list(self):
        self.assertIsNone(calculate_maximum([]))

    def test_maximum_with_non_list_input(self):
        self.assertIsNone(calculate_maximum((3, 1, 2)))

    def test_maximum_with_non_numeric_values(self):
        self.assertIsNone(calculate_maximum([1, "hello", 3]))

    def test_maximum_with_boolean_values(self):
        self.assertIsNone(calculate_maximum([True, 2, 3]))

    def test_maximum_with_mixed_numeric_types(self):
        self.assertEqual(calculate_maximum([2, 1.5, 3]), 3)

    def test_maximum_does_not_modify_original_list(self):
        values = [4, 2, 7, 1]
        original_values = values.copy()

        calculate_maximum(values)

        self.assertEqual(values, original_values)


class TestCalculateRange(unittest.TestCase):

    def test_range_of_positive_numbers(self):
        self.assertEqual(calculate_range([5, 2, 8, 1]), 7)

    def test_range_of_negative_numbers(self):
        self.assertEqual(calculate_range([-5, -2, -8, -1]), 7)

    def test_range_with_positive_and_negative_numbers(self):
        self.assertEqual(calculate_range([-5, 2, 8, -1]), 13)

    def test_range_of_decimal_numbers(self):
        self.assertAlmostEqual(calculate_range([2.5, 1.2, 3.8]), 2.6)

    def test_range_with_duplicate_values(self):
        self.assertEqual(calculate_range([3, 4, 4, 1]), 3)

    def test_range_of_single_value(self):
        self.assertEqual(calculate_range([7]), 0)

    def test_range_of_equal_values(self):
        self.assertEqual(calculate_range([5, 5, 5]), 0)

    def test_range_of_empty_list(self):
        self.assertIsNone(calculate_range([]))

    def test_range_with_non_list_input(self):
        self.assertIsNone(calculate_range((3, 1, 2)))

    def test_range_with_non_numeric_values(self):
        self.assertIsNone(calculate_range([1, "hello", 3]))

    def test_range_with_boolean_values(self):
        self.assertIsNone(calculate_range([True, 2, 3]))

    def test_range_does_not_modify_original_list(self):
        values = [4, 2, 7, 1]
        original_values = values.copy()

        calculate_range(values)

        self.assertEqual(values, original_values)


class TestCalculateVariance(unittest.TestCase):

    def test_variance_of_positive_numbers(self):
        self.assertAlmostEqual(calculate_variance([2, 4, 6]), 8 / 3)

    def test_variance_of_negative_numbers(self):
        self.assertAlmostEqual(calculate_variance([-2, -4, -6]), 8 / 3)

    def test_variance_with_zero(self):
        self.assertAlmostEqual(calculate_variance([0, 2, 4]), 8 / 3)

    def test_variance_of_equal_values(self):
        self.assertEqual(calculate_variance([5, 5, 5]), 0)

    def test_variance_of_single_value(self):
        self.assertEqual(calculate_variance([7]), 0)

    def test_variance_of_decimal_numbers(self):
        self.assertAlmostEqual(calculate_variance([1.5, 2.5, 3.5]), 2 / 3)

    def test_variance_of_empty_list(self):
        self.assertIsNone(calculate_variance([]))

    def test_variance_with_non_list_input(self):
        self.assertIsNone(calculate_variance((1, 2, 3)))

    def test_variance_with_non_numeric_values(self):
        self.assertIsNone(calculate_variance([1, "hello", 3]))

    def test_variance_with_boolean_values(self):
        self.assertIsNone(calculate_variance([True, 2, 3]))

    def test_variance_with_mixed_numeric_types(self):
        self.assertAlmostEqual(calculate_variance([1, 2.5, 4]), 1.5)

    def test_variance_does_not_modify_original_list(self):
        values = [2, 4, 6]
        original_values = values.copy()

        calculate_variance(values)

        self.assertEqual(values, original_values)


class TestCalculateStandardDeviation(unittest.TestCase):

    def test_standard_deviation_of_positive_numbers(self):
        self.assertAlmostEqual(
            calculate_standard_deviation([2, 4, 6]),
            (8 / 3) ** 0.5
        )

    def test_standard_deviation_of_negative_numbers(self):
        self.assertAlmostEqual(
            calculate_standard_deviation([-2, -4, -6]),
            (8 / 3) ** 0.5
        )

    def test_standard_deviation_with_zero(self):
        self.assertAlmostEqual(
            calculate_standard_deviation([0, 2, 4]),
            (8 / 3) ** 0.5
        )

    def test_standard_deviation_of_equal_values(self):
        self.assertEqual(
            calculate_standard_deviation([5, 5, 5]),
            0
        )

    def test_standard_deviation_of_single_value(self):
        self.assertEqual(
            calculate_standard_deviation([7]),
            0
        )

    def test_standard_deviation_of_decimal_numbers(self):
        self.assertAlmostEqual(
            calculate_standard_deviation([1.5, 2.5, 3.5]),
            (2 / 3) ** 0.5
        )

    def test_standard_deviation_of_empty_list(self):
        self.assertIsNone(calculate_standard_deviation([]))

    def test_standard_deviation_with_non_list_input(self):
        self.assertIsNone(calculate_standard_deviation((1, 2, 3)))

    def test_standard_deviation_with_non_numeric_values(self):
        self.assertIsNone(
            calculate_standard_deviation([1, "hello", 3])
        )

    def test_standard_deviation_with_boolean_values(self):
        self.assertIsNone(
            calculate_standard_deviation([True, 2, 3])
        )

    def test_standard_deviation_with_mixed_numeric_types(self):
        self.assertAlmostEqual(
            calculate_standard_deviation([1, 2.5, 4]),
            1.5 ** 0.5
        )

    def test_standard_deviation_does_not_modify_original_list(self):
        values = [2, 4, 6]
        original_values = values.copy()

        calculate_standard_deviation(values)

        self.assertEqual(values, original_values)


if __name__ == "__main__":
    unittest.main()