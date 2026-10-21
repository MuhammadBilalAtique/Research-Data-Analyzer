import unittest

from research_analyzer.main import parse_args


class TestCommandLineArguments(unittest.TestCase):
    def test_defaults_preserve_existing_project_paths(self):
        args = parse_args([])

        self.assertEqual(args.input, "data/raw/student_performance.csv")
        self.assertEqual(args.output, "data/processed/student_performance_cleaned.csv")
        self.assertEqual(args.report, "data/processed/analysis_report.json")

    def test_custom_paths_can_be_provided(self):
        args = parse_args([
            "--input", "research/input.csv",
            "--output", "results/clean.csv",
            "--report", "results/summary.json",
        ])

        self.assertEqual(args.input, "research/input.csv")
        self.assertEqual(args.output, "results/clean.csv")
        self.assertEqual(args.report, "results/summary.json")


if __name__ == "__main__":
    unittest.main()
