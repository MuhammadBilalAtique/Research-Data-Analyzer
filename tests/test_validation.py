import unittest

from research_analyzer.data_cleaner import clean_data, find_missing_values, validate_row


def valid_student_row():
    return {"Student_ID": "S001", "Age": "20", "Attendance": "85", "Study_Hours": "4.5", "Previous_Score": "72", "Sleep_Hours": "7", "Internet_Usage": "3.5", "Final_Score": "78"}


class TestNumericValidation(unittest.TestCase):
    def test_accepts_valid_boundary_values(self):
        row = valid_student_row(); row.update({"Study_Hours": "0", "Previous_Score": "100", "Sleep_Hours": "24", "Internet_Usage": "0", "Final_Score": "0"})
        self.assertIs(validate_row(row), True)
    def test_rejects_non_finite_values(self):
        for field in ["Study_Hours", "Previous_Score", "Sleep_Hours", "Internet_Usage", "Final_Score"]:
            for value in ["nan", "inf", "-inf"]:
                with self.subTest(field=field, value=value):
                    row = valid_student_row(); row[field] = value
                    self.assertIsNot(validate_row(row), True)
    def test_rejects_negative_hours_and_usage(self):
        for field in ["Study_Hours", "Sleep_Hours", "Internet_Usage"]:
            with self.subTest(field=field):
                row = valid_student_row(); row[field] = "-0.1"
                self.assertIsNot(validate_row(row), True)
    def test_rejects_hours_and_usage_above_24(self):
        for field in ["Study_Hours", "Sleep_Hours", "Internet_Usage"]:
            with self.subTest(field=field):
                row = valid_student_row(); row[field] = "24.1"
                self.assertIsNot(validate_row(row), True)
    def test_rejects_scores_outside_zero_to_one_hundred(self):
        for field in ["Previous_Score", "Final_Score"]:
            for value in ["-1", "100.1"]:
                with self.subTest(field=field, value=value):
                    row = valid_student_row(); row[field] = value
                    self.assertIsNot(validate_row(row), True)
    def test_none_is_reported_as_a_missing_required_value(self):
        row = valid_student_row(); row["Sleep_Hours"] = None
        result = validate_row(row)
        self.assertIsInstance(result, list)
        self.assertIn("Value of Sleep_Hours is missing", result)
    def test_clean_data_normalizes_none_and_non_string_values(self):
        rows = [{"Name": None, "Score": 87}]
        clean_data(rows)
        self.assertEqual(rows, [{"Name": "", "Score": "87"}])
    def test_missing_value_counts_accept_none_and_whitespace(self):
        rows = [{"Value": None}, {"Value": "  "}, {"Value": "present"}]
        self.assertEqual(find_missing_values(rows), {"Value": 2})


if __name__ == "__main__": unittest.main()
