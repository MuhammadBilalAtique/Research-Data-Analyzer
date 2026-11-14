import unittest

from research_analyzer.dataset import Dataset
from research_analyzer.reporting import build_analysis_report
from research_analyzer.validation import NumericRule, ValidationSchema


class TestValidationSchema(unittest.TestCase):
    def setUp(self):
        self.schema = ValidationSchema(
            required_fields=("Record_ID", "Age", "Score"),
            numeric_rules={
                "Age": NumericRule(minimum=18, maximum=100, integer=True),
                "Score": NumericRule(minimum=0, maximum=100),
            },
            identifier_column="Record_ID",
        )

    @staticmethod
    def valid_row(record_id="R001", age="20", score="87.5"):
        return {"Record_ID": record_id, "Age": age, "Score": score}

    def test_accepts_values_on_inclusive_boundaries(self):
        self.assertIs(
            self.schema.validate(self.valid_row(age="18", score="100")),
            True,
        )

    def test_reports_missing_required_keys_and_values(self):
        errors = self.schema.validate({"Record_ID": "", "Age": "20"})
        self.assertIn("Value of Record_ID is missing", errors)
        self.assertIn("The Score key is missing", errors)

    def test_rejects_non_numeric_and_non_finite_values(self):
        for value in ("not-a-number", "nan", "inf", "-inf"):
            with self.subTest(value=value):
                self.assertIsInstance(
                    self.schema.validate(self.valid_row(score=value)),
                    list,
                )

    def test_enforces_numeric_ranges(self):
        self.assertIn(
            "Score must be at least 0",
            self.schema.validate(self.valid_row(score="-0.1")),
        )
        self.assertIn(
            "Score must be at most 100",
            self.schema.validate(self.valid_row(score="100.1")),
        )

    def test_enforces_integer_rules(self):
        self.assertIn(
            "Age must be an integer",
            self.schema.validate(self.valid_row(age="20.5")),
        )

    def test_numeric_fields_can_be_optional(self):
        optional_schema = ValidationSchema(
            numeric_rules={"Optional_Score": NumericRule(minimum=0, maximum=10)}
        )
        self.assertIs(optional_schema.validate({"Name": "Sample"}), True)
        self.assertIs(optional_schema.validate({"Optional_Score": ""}), True)

    def test_rejects_invalid_schema_definitions(self):
        with self.assertRaises(ValueError):
            NumericRule(minimum=10, maximum=1)
        with self.assertRaises(ValueError):
            ValidationSchema(required_fields=("Name", "Name"))

    def test_dataset_uses_schema_and_configured_identifier(self):
        dataset = Dataset("unused.csv", validation_schema=self.schema)
        dataset.data = [
            self.valid_row("R001"),
            self.valid_row("R001", age="17"),
            self.valid_row("R002"),
        ]

        self.assertEqual(dataset.validate(), {"valid": 2, "invalid": 1})
        self.assertEqual(dataset.find_duplicates(), ["R001"])

    def test_analysis_report_uses_configured_schema(self):
        dataset = Dataset("unused.csv", validation_schema=self.schema)
        dataset.data = [
            self.valid_row("R001"),
            self.valid_row("R002", age="17"),
        ]

        report = build_analysis_report(dataset)

        self.assertEqual(report["validation"], {"valid": 1, "invalid": 1})
        self.assertEqual(report["identifier_column"], "Record_ID")
        self.assertEqual(report["duplicate_identifiers"], [])
        self.assertIsNone(report["duplicate_student_ids"])
        self.assertEqual(report["invalid_rows"][0]["row_number"], 2)


if __name__ == "__main__":
    unittest.main()
