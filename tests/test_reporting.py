import json
import tempfile
import unittest
from pathlib import Path

from research_analyzer.dataset import Dataset
from research_analyzer.reporting import build_analysis_report, save_analysis_report


class TestAnalysisReporting(unittest.TestCase):
    def setUp(self):
        self.dataset = Dataset("unused.csv")
        self.dataset.data = [
            {
                "Student_ID": "101",
                "Age": "20",
                "Attendance": "80",
                "Study_Hours": "2",
                "Previous_Score": "70",
                "Sleep_Hours": "7",
                "Internet_Usage": "3",
                "Final_Score": "75",
            },
            {
                "Student_ID": "102",
                "Age": "21",
                "Attendance": "90",
                "Study_Hours": "4",
                "Previous_Score": "80",
                "Sleep_Hours": "8",
                "Internet_Usage": "4",
                "Final_Score": "85",
            },
            {
                "Student_ID": "102",
                "Age": "22",
                "Attendance": "95",
                "Study_Hours": "6",
                "Previous_Score": "85",
                "Sleep_Hours": "6",
                "Internet_Usage": "5",
                "Final_Score": "95",
            },
        ]

    def test_report_contains_dataset_quality_and_statistics(self):
        report = build_analysis_report(self.dataset)

        self.assertEqual(report["dataset"]["rows"], 3)
        self.assertEqual(report["validation"], {"valid": 3, "invalid": 0})
        self.assertEqual(report["duplicate_student_ids"], ["102"])
        self.assertEqual(report["missing_values"]["Study_Hours"], 0)
        self.assertEqual(report["numeric_summary"]["Study_Hours"]["mean"], 4)
        self.assertEqual(report["numeric_summary"]["Study_Hours"]["count"], 3)

    def test_report_contains_pairwise_correlations(self):
        report = build_analysis_report(self.dataset)
        pair = next(
            item for item in report["pearson_correlations"]
            if item["first_column"] == "Study_Hours"
            and item["second_column"] == "Final_Score"
        )

        self.assertGreater(pair["pearson_r"], 0.9)

    def test_save_report_creates_parent_and_round_trips_json(self):
        report = build_analysis_report(self.dataset)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "report.json"
            returned_path = save_analysis_report(report, path)

            self.assertEqual(returned_path, path)
            with path.open(encoding="utf-8") as file:
                loaded = json.load(file)

        self.assertEqual(loaded["dataset"]["rows"], 3)
        self.assertEqual(loaded["numeric_summary"]["Study_Hours"]["mean"], 4)


    def test_empty_dataset_produces_empty_summary_without_crashing(self):
        dataset = Dataset("unused.csv")

        report = build_analysis_report(dataset)

        self.assertEqual(report["dataset"], {
            "rows": 0,
            "columns": 0,
            "column_names": [],
        })
        self.assertEqual(report["column_types"], {})
        self.assertEqual(report["validation"], {"valid": 0, "invalid": 0})
        self.assertEqual(report["numeric_summary"], {})
        self.assertEqual(report["pearson_correlations"], [])

    def test_empty_dataset_report_can_be_saved_as_valid_json(self):
        report = build_analysis_report(Dataset("unused.csv"))

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty_report.json"
            save_analysis_report(report, path)
            with path.open(encoding="utf-8") as file:
                loaded = json.load(file)

        self.assertEqual(loaded["dataset"]["rows"], 0)
        self.assertEqual(loaded["numeric_summary"], {})

    def test_missing_value_percentages_are_reported_per_column(self):
        self.dataset.data[0]["Study_Hours"] = ""

        report = build_analysis_report(self.dataset)

        self.assertEqual(report["missing_values"]["Study_Hours"], 1)
        self.assertAlmostEqual(
            report["missing_value_percentages"]["Study_Hours"],
            100 / 3,
            places=2,
        )
        self.assertEqual(report["missing_value_percentages"]["Age"], 0)

    def test_empty_dataset_has_no_missing_value_percentages(self):
        report = build_analysis_report(Dataset("unused.csv"))

        self.assertEqual(report["missing_value_percentages"], {})

    def test_rejects_non_json_output_path(self):
        with self.assertRaises(ValueError):
            save_analysis_report({}, "report.csv")


if __name__ == "__main__":
    unittest.main()
