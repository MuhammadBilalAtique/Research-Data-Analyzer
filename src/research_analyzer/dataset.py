from research_analyzer.data_loader import load_csv
from research_analyzer.data_cleaner import clean_data, validate_row, find_missing_values as check_missing_values, find_duplicates as check_duplicates
from research_analyzer.data_writer import save_csv


class Dataset:

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

    def load(self):
        self.data = load_csv(self.file_path)

    def info(self):
        if not self.data:
            return {
                "rows": 0,
                "columns": 0,
                "column_names": []
            }

        return {
            "rows": len(self.data),
            "columns": len(self.data[0]),
            "column_names": list(self.data[0].keys())
        }

    def get_column_types(self):
        if not self.data:
            return {}

        column_types = {}

        for column in self.data[0].keys():
            values = []

            for row in self.data:
                value = row[column]

                if value.strip() != "":
                    values.append(value)

            if not values:
                column_types[column] = "empty"
                continue

            is_numeric = True

            for value in values:
                try:
                    float(value)
                except ValueError:
                    is_numeric = False
                    break

            if is_numeric:
                column_types[column] = "numeric"
            else:
                column_types[column] = "text"

        return column_types

    def get_numeric_columns(self):
        column_types = self.get_column_types()
        numeric_columns = []

        for column, column_type in column_types.items():
            if column_type == "numeric":
                numeric_columns.append(column)

        return numeric_columns

    def get_column_values(self, column):
        values = []

        for row in self.data:
            values.append(float(row[column]))

        return values

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
