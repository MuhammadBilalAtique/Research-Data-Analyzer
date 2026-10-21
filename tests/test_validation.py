import unittest

from research_analyzer.data_cleaner import validate_row


def valid_student_row():
    return {
        "Student_ID": "S001",
        "Age": "20",
        "Attendance": "85",
        "Study_Hours": "4.5",
        "Previous_Score": "72",
        "Sleep_Hours": "7",
        "Internet_Usage": "3.5",
        "Final_Score": "78",
    }


class TestNumericValidation(unittest.TestCase):
    def test_accepts_valid_boundary_values(self):
        row = valid_student_row()
        row.update({
            "Study_Hours": "0",
            "Previous_Score": "100",
            "Sleep_Hours": "24",
            "Internet_Usage": "0",
            "Final_Score": "0",
        })

        self.assertIs(validate_row(row), True)

    def test_rejects_non_finite_values(self):
        for field in [
            "Study_Hours", "Previous_Score", "Sleep_Hours",
            "Internet_Usage", "Final_Score",
        ]:
            for value in ["nan", "inf", "-inf"]:
                with self.subTest(field=field, value=value):
                    row = valid_student_row()
                    row[field] = value
                    self.assertIsNot(validate_row(row), True)

    def test_rejects_negative_hours_and_usage(self):
        for field in ["Study_Hours", "Sleep_Hours", "Internet_Usage"]:
            with self.subTest(field=field):
                row = valid_student_row()
                row[field] = "-0.1"
                self.assertIsNot(validate_row(row), True)

    def test_rejects_hours_and_usage_above_24(self):
        for field in ["Study_Hours", "Sleep_Hours", "Internet_Usage"]:
            with self.subTest(field=field):
                row = valid_student_row()
                row[field] = "24.1"
                self.assertIsNot(validate_row(row), True)

    def test_rejects_scores_outside_zero_to_one_hundred(self):
        for field in ["Previous_Score", "Final_Score"]:
            for value in ["-1", "100.1"]:
                with self.subTest(field=field, value=value):
                    row = valid_student_row()
                    row[field] = value
                    self.assertIsNot(validate_row(row), True)


if __name__ == "__main__":
    unittest.main()
