import csv
import tempfile
import unittest
from pathlib import Path

from research_analyzer.data_loader import load_csv
from research_analyzer.data_writer import save_csv


class TestCsvIO(unittest.TestCase):
    def test_round_trip_preserves_rows_and_creates_parent(self):
        rows = [{"Name": "Bilal", "Score": "87"}, {"Name": "Sara", "Score": "92"}]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "scores.csv"
            save_csv(rows, path)
            self.assertEqual(load_csv(path), rows)

    def test_load_supports_utf8_bom(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bom.csv"
            path.write_text("\ufeffName,Score\nBilal,87\n", encoding="utf-8")
            self.assertEqual(load_csv(path), [{"Name": "Bilal", "Score": "87"}])

    def test_missing_file_raises_clear_error(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(FileNotFoundError, "CSV file not found"):
                load_csv(Path(directory) / "missing.csv")

    def test_rejects_non_csv_extension(self):
        with self.assertRaises(ValueError):
            load_csv("dataset.txt")

    def test_rejects_csv_without_header(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.csv"
            path.write_text("", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "no header"):
                load_csv(path)

    def test_rejects_duplicate_headers(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.csv"
            path.write_text("Name,Name\nBilal,Atique\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                load_csv(path)

    def test_empty_dataset_can_be_saved_with_headers(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.csv"
            save_csv([], path, fieldnames=["Name", "Score"])
            with path.open(newline="", encoding="utf-8") as file:
                self.assertEqual(next(csv.reader(file)), ["Name", "Score"])

    def test_empty_dataset_requires_headers(self):
        with self.assertRaises(ValueError):
            save_csv([], "empty.csv")


if __name__ == "__main__":
    unittest.main()
