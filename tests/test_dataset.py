import unittest

from research_analyzer.dataset import Dataset


class TestDatasetColumnTypes(unittest.TestCase):

    def setUp(self):
        self.dataset = Dataset("unused.csv")

    def test_empty_dataset_has_no_column_types(self):
        self.assertEqual(self.dataset.get_column_types(), {})

    def test_detects_numeric_and_text_columns(self):
        self.dataset.data = [
            {"Age": "20", "Name": "Bilal", "Score": "87.5"},
            {"Age": "21", "Name": "Sara", "Score": "91"},
        ]

        self.assertEqual(
            self.dataset.get_column_types(),
            {"Age": "numeric", "Name": "text", "Score": "numeric"},
        )

    def test_ignores_blank_values_when_detecting_column_type(self):
        self.dataset.data = [
            {"Age": "20", "Name": ""},
            {"Age": " ", "Name": "Bilal"},
        ]

        self.assertEqual(
            self.dataset.get_column_types(),
            {"Age": "numeric", "Name": "text"},
        )

    def test_classifies_a_column_with_only_blank_values_as_empty(self):
        self.dataset.data = [
            {"Optional": ""},
            {"Optional": "   "},
        ]

        self.assertEqual(self.dataset.get_column_types(), {"Optional": "empty"})

    def test_non_finite_numbers_are_not_classified_as_numeric(self):
        self.dataset.data = [
            {"Value": "NaN"},
            {"Value": "inf"},
        ]

        self.assertEqual(self.dataset.get_column_types(), {"Value": "text"})

    def test_get_numeric_columns_returns_only_numeric_columns(self):
        self.dataset.data = [
            {"Age": "20", "Name": "Bilal", "Score": "87.5", "Optional": ""},
        ]

        self.assertEqual(self.dataset.get_numeric_columns(), ["Age", "Score"])


if __name__ == "__main__":
    unittest.main()
