from research_analyzer.data_loader import load_csv
from research_analyzer.data_cleaner import clean_data, validate_row, find_missing_values as check_missing_values, find_duplicates as check_duplicates
from research_analyzer.data_writer import save_csv


class Dataset:

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

    def load(self):
        self.data = load_csv(self.file_path)

    def clean(self):
        self.data = clean_data(self.data)

    def save(self, file_path):
        save_csv(self.data, file_path)

    def validate(self):
        valid_rows = 0
        invalid_rows = 0

        for row in self.data:
            result = validate_row(row)

            if result is True:
                valid_rows += 1
            else:
                invalid_rows += 1

        return {
            "valid": valid_rows,
            "invalid": invalid_rows
        }

    def find_missing_values(self):
        result = check_missing_values(self.data)
        return result

    def find_duplicates(self):
        result = check_duplicates(self.data)
        return result
