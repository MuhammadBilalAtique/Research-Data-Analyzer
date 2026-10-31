import math

from research_analyzer.data_loader import load_csv
from research_analyzer.data_cleaner import (
    clean_data, validate_row,
    find_missing_values as check_missing_values,
    find_duplicates as check_duplicates,
)
from research_analyzer.data_writer import save_csv
from research_analyzer.statistics import calculate_correlation, calculate_quartiles, calculate_iqr, find_outliers_iqr


class Dataset:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

    def load(self):
        self.data = load_csv(self.file_path)
        return self.data

    def info(self):
        if not self.data:
            return {"rows": 0, "columns": 0, "column_names": []}
        return {"rows": len(self.data), "columns": len(self.data[0]), "column_names": list(self.data[0].keys())}

    def get_column_types(self):
        if not self.data:
            return {}
        result = {}
        for column in self.data[0]:
            values = [row.get(column, "").strip() for row in self.data if row.get(column, "").strip()]
            if not values:
                result[column] = "empty"
                continue
            try:
                numeric = all(math.isfinite(float(value)) for value in values)
            except (ValueError, TypeError):
                numeric = False
            result[column] = "numeric" if numeric else "text"
        return result

    def get_numeric_columns(self):
        return [name for name, kind in self.get_column_types().items() if kind == "numeric"]

    def get_column_values(self, column):
        if self.data and column not in self.data[0]:
            raise KeyError(f"Column not found: {column}")
        values = []
        for row in self.data:
            value = row.get(column, "").strip()
            if not value:
                continue
            number = float(value)
            if not math.isfinite(number):
                raise ValueError(f"Column {column!r} contains a non-finite number.")
            values.append(number)
        return values

    def clean(self):
        self.data = clean_data(self.data)
        return self.data

    def save(self, file_path, fieldnames=None):
        return save_csv(self.data, file_path, fieldnames=fieldnames)

    def validate(self):
        valid = sum(validate_row(row) is True for row in self.data)
        return {"valid": valid, "invalid": len(self.data) - valid}

    def find_missing_values(self):
        return check_missing_values(self.data)

    def find_duplicates(self, id_column="Student_ID"):
        """Find repeated identifiers; return None if the requested column is absent."""
        return check_duplicates(self.data, id_column=id_column)

    def column_quartiles(self, column):
        return calculate_quartiles(self.get_column_values(column))

    def column_iqr(self, column):
        return calculate_iqr(self.get_column_values(column))

    def column_outliers(self, column):
        return find_outliers_iqr(self.get_column_values(column))

    def correlation(self, first_column, second_column):
        """Pearson correlation using rows with numeric values in both columns."""
        if not self.data:
            return None
        pairs = []
        for row in self.data:
            first, second = row.get(first_column, "").strip(), row.get(second_column, "").strip()
            if not first or not second:
                continue
            try:
                x, y = float(first), float(second)
            except ValueError:
                continue
            if math.isfinite(x) and math.isfinite(y):
                pairs.append((x, y))
        if len(pairs) < 2:
            return None
        return calculate_correlation([p[0] for p in pairs], [p[1] for p in pairs])
