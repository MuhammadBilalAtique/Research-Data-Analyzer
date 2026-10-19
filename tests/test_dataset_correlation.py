import unittest

from research_analyzer.dataset import Dataset


class TestDatasetCorrelation(unittest.TestCase):
    def setUp(self):
        self.dataset = Dataset("unused.csv")

    def test_calculates_positive_correlation_between_columns(self):
        self.dataset.data = [
            {"Study_Hours": "1", "Final_Score": "2"},
            {"Study_Hours": "2", "Final_Score": "4"},
            {"Study_Hours": "3", "Final_Score": "6"},
        ]

        self.assertAlmostEqual(self.dataset.correlation("Study_Hours", "Final_Score"), 1.0)

    def test_skips_rows_with_blank_or_nonnumeric_values(self):
        self.dataset.data = [
            {"Study_Hours": "1", "Final_Score": "2"},
            {"Study_Hours": "2", "Final_Score": "4"},
            {"Study_Hours": "", "Final_Score": "6"},
            {"Study_Hours": "4", "Final_Score": "not available"},
            {"Study_Hours": "5", "Final_Score": "10"},
        ]

        self.assertAlmostEqual(self.dataset.correlation("Study_Hours", "Final_Score"), 1.0)

    def test_returns_none_when_fewer_than_two_complete_pairs_exist(self):
        self.dataset.data = [
            {"Study_Hours": "1", "Final_Score": "2"},
            {"Study_Hours": "2", "Final_Score": ""},
            {"Study_Hours": "", "Final_Score": "6"},
        ]

        self.assertIsNone(self.dataset.correlation("Study_Hours", "Final_Score"))

    def test_returns_none_when_a_column_is_constant(self):
        self.dataset.data = [
            {"Study_Hours": "2", "Final_Score": "1"},
            {"Study_Hours": "2", "Final_Score": "2"},
            {"Study_Hours": "2", "Final_Score": "3"},
        ]

        self.assertIsNone(self.dataset.correlation("Study_Hours", "Final_Score"))

    def test_empty_dataset_returns_none(self):
        self.assertIsNone(self.dataset.correlation("Study_Hours", "Final_Score"))


if __name__ == "__main__":
    unittest.main()
