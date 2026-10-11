import unittest

from research_analyzer.statistics import calculate_mean, calculate_median


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


if __name__ == "__main__":
    unittest.main()