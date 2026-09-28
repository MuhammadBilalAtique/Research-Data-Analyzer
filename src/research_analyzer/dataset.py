from research_analyzer.data_loader import load_csv
from research_analyzer.data_cleaner import clean_data, validate_row


class Dataset:

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

    def load(self):
        self.data = load_csv(self.file_path)

    def clean(self):
        self.data = clean_data(self.data)

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