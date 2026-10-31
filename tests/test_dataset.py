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


class TestDatasetOperations(unittest.TestCase):

    def setUp(self):
        self.dataset = Dataset("unused.csv")

    @staticmethod
    def valid_row(student_id="101", age="20"):
        return {
            "Student_ID": student_id,
            "Age": age,
            "Attendance": "85",
            "Study_Hours": "4.5",
            "Previous_Score": "75",
            "Sleep_Hours": "7",
            "Internet_Usage": "5",
            "Final_Score": "82",
        }

    def test_info_returns_zero_counts_for_empty_dataset(self):
        self.assertEqual(
            self.dataset.info(),
            {"rows": 0, "columns": 0, "column_names": []},
        )

    def test_info_reports_rows_columns_and_names(self):
        self.dataset.data = [
            {"Age": "20", "Name": "Bilal"},
            {"Age": "21", "Name": "Sara"},
        ]

        self.assertEqual(
            self.dataset.info(),
            {"rows": 2, "columns": 2, "column_names": ["Age", "Name"]},
        )

    def test_get_column_values_converts_numbers_and_skips_blanks(self):
        self.dataset.data = [
            {"Score": "87.5"},
            {"Score": ""},
            {"Score": " 91 "},
        ]

        self.assertEqual(self.dataset.get_column_values("Score"), [87.5, 91.0])

    def test_validate_counts_valid_and_invalid_rows(self):
        self.dataset.data = [
            self.valid_row(),
            self.valid_row(student_id="102", age="9"),
        ]

        self.assertEqual(self.dataset.validate(), {"valid": 1, "invalid": 1})

    def test_find_missing_values_counts_blanks_per_column(self):
        self.dataset.data = [
            {"Age": "20", "Name": "Bilal"},
            {"Age": "", "Name": " "},
            {"Age": "22", "Name": "Sara"},
        ]

        self.assertEqual(
            self.dataset.find_missing_values(),
            {"Age": 1, "Name": 1},
        )

    def test_find_duplicates_returns_repeated_student_ids(self):
        self.dataset.data = [
            {"Student_ID": "101"},
            {"Student_ID": "102"},
            {"Student_ID": "101"},
        ]

        self.assertEqual(self.dataset.find_duplicates(), ["101"])

    def test_find_duplicates_returns_empty_list_when_ids_are_unique(self):
        self.dataset.data = [
            {"Student_ID": "101"},
            {"Student_ID": "102"},
        ]

        self.assertEqual(self.dataset.find_duplicates(), [])

    def test_find_duplicates_returns_none_when_identifier_column_is_absent(self):
        self.dataset.data = [
            {"Name": "Bilal", "Score": "87"},
            {"Name": "Sara", "Score": "92"},
        ]

        self.assertIsNone(self.dataset.find_duplicates())

    def test_find_duplicates_can_use_a_custom_identifier_column(self):
        self.dataset.data = [
            {"Record_ID": "A-1", "Score": "87"},
            {"Record_ID": "A-2", "Score": "92"},
            {"Record_ID": "A-1", "Score": "90"},
        ]

        self.assertEqual(
            self.dataset.find_duplicates(id_column="Record_ID"),
            ["A-1"],
        )

    def test_find_duplicates_ignores_blank_identifiers(self):
        self.dataset.data = [
            {"Student_ID": "", "Score": "87"},
            {"Student_ID": "  ", "Score": "92"},
            {"Student_ID": "S001", "Score": "90"},
        ]

        self.assertEqual(self.dataset.find_duplicates(), [])


class TestDatasetPersistence(unittest.TestCase):

    def test_save_and_load_preserve_dataset_rows(self):
        import os
        import tempfile

        original_rows = [
            {
                "Student_ID": "101",
                "Age": "20",
                "Attendance": "85",
                "Study_Hours": "4.5",
                "Previous_Score": "75",
                "Sleep_Hours": "7",
                "Internet_Usage": "5",
                "Final_Score": "82",
            },
            {
                "Student_ID": "102",
                "Age": "21",
                "Attendance": "90",
                "Study_Hours": "5",
                "Previous_Score": "80",
                "Sleep_Hours": "8",
                "Internet_Usage": "3",
                "Final_Score": "88",
            },
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "round_trip.csv")

            saved_dataset = Dataset(file_path)
            saved_dataset.data = original_rows
            saved_dataset.save(file_path)

            loaded_dataset = Dataset(file_path)
            loaded_dataset.load()

        self.assertEqual(loaded_dataset.data, original_rows)


if __name__ == "__main__":
    unittest.main()
