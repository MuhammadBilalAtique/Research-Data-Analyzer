import unittest

from research_analyzer.dataset import Dataset
from research_analyzer.reporting import build_analysis_report


class TestDataQualitySummary(unittest.TestCase):
    def test_report_includes_missing_duplicate_empty_and_constant_diagnostics(self):
        dataset = Dataset("quality.csv")
        dataset.data = [
            {"ID": "A", "Group": "control", "Score": "10"},
            {"ID": "B", "Group": "control", "Score": ""},
            {"ID": "B", "Group": "control", "Score": ""},
            {"ID": None, "Group": "control", "Score": None},
            {"ID": "", "Group": "control", "Score": ""},
            {},
        ]
        quality = build_analysis_report(dataset)["data_quality"]
        self.assertEqual(quality["total_rows"], 6)
        self.assertEqual(quality["rows_with_missing_values"], 5)
        self.assertEqual(quality["empty_row_numbers"], [6])
        self.assertEqual(quality["duplicate_row_numbers"], [3])
        self.assertEqual(quality["duplicate_row_count"], 1)
        self.assertEqual(
            quality["non_missing_value_counts"],
            {"ID": 3, "Group": 5, "Score": 1},
        )
        self.assertEqual(
            quality["distinct_value_counts"],
            {"ID": 2, "Group": 1, "Score": 1},
        )
        self.assertEqual(quality["constant_columns"], ["Group", "Score"])

    def test_empty_dataset_has_well_formed_quality_summary(self):
        self.assertEqual(
            build_analysis_report(Dataset("empty.csv"))["data_quality"],
            {
                "total_rows": 0, "rows_with_missing_values": 0,
                "empty_row_numbers": [], "duplicate_row_numbers": [],
                "duplicate_row_count": 0, "non_missing_value_counts": {},
                "distinct_value_counts": {}, "constant_columns": [],
            },
        )

    def test_distinct_values_normalize_numeric_objects_and_strings(self):
        dataset = Dataset("objects.csv")
        dataset.data = [{"Value": 1}, {"Value": "1"}, {"Value": 2}]
        quality = build_analysis_report(dataset)["data_quality"]
        self.assertEqual(quality["distinct_value_counts"]["Value"], 2)


if __name__ == "__main__":
    unittest.main()
