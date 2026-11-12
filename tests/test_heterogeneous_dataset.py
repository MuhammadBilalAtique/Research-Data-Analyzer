import unittest

from research_analyzer.dataset import Dataset


class TestHeterogeneousDatasetHandling(unittest.TestCase):
    def setUp(self):
        self.dataset = Dataset("unused.csv")
        self.dataset.data = [
            {"Name": "Bilal", "Score": 87, "Optional": None},
            {"Name": "Sara", "Score": "92", "Extra": "note"},
            {"Name": "Ali", "Score": " ", "Optional": "yes"},
        ]

    def test_info_uses_ordered_union_of_all_row_keys(self):
        self.assertEqual(
            self.dataset.info(),
            {"rows": 3, "columns": 4,
             "column_names": ["Name", "Score", "Optional", "Extra"]},
        )

    def test_column_types_handle_missing_keys_none_and_numeric_objects(self):
        self.assertEqual(
            self.dataset.get_column_types(),
            {"Name": "text", "Score": "numeric",
             "Optional": "text", "Extra": "text"},
        )

    def test_missing_counts_include_absent_keys_and_none(self):
        self.assertEqual(
            self.dataset.find_missing_values(),
            {"Name": 0, "Score": 1, "Optional": 2, "Extra": 2},
        )

    def test_numeric_values_skip_missing_and_accept_numeric_objects(self):
        self.assertEqual(self.dataset.get_column_values("Score"), [87.0, 92.0])

    def test_unknown_column_raises_key_error(self):
        with self.assertRaisesRegex(KeyError, "Column not found"):
            self.dataset.get_column_values("Unknown")

    def test_non_numeric_column_value_raises_clear_error(self):
        self.dataset.data = [{"Score": "12"}, {"Score": "not numeric"}]
        with self.assertRaisesRegex(ValueError, "non-numeric"):
            self.dataset.get_column_values("Score")

    def test_correlation_skips_missing_and_nonnumeric_pairs(self):
        self.dataset.data = [
            {"x": 1, "y": 2}, {"x": "2", "y": "4"},
            {"x": None, "y": 6}, {"x": 4, "y": "not available"},
            {"x": 5, "y": 10},
        ]
        self.assertAlmostEqual(self.dataset.correlation("x", "y"), 1.0)

    def test_correlation_rejects_unknown_columns(self):
        with self.assertRaises(KeyError):
            self.dataset.correlation("missing", "Score")


if __name__ == "__main__":
    unittest.main()
