import unittest

from research_analyzer.statistics import calculate_mean


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


if __name__ == "__main__":
    unittest.main()