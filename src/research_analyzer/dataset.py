import math

from research_analyzer.data_loader import load_csv
from research_analyzer.data_cleaner import (
    clean_data, validate_row, is_missing,
    find_missing_values as check_missing_values,
    find_duplicates as check_duplicates,
)
from research_analyzer.data_writer import save_csv
from research_analyzer.statistics import (
    calculate_correlation, calculate_quartiles, calculate_iqr,
    find_outliers_iqr,
)


class Dataset:
    """In-memory dataset with CSV persistence and exploratory operations."""

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

    def _column_names(self):
        """Return the ordered union of keys across all rows."""
        return list(dict.fromkeys(key for row in self.data for key in row))

    def load(self):
        self.data = load_csv(self.file_path)
        return self.data

    def info(self):
        columns = self._column_names()
        return {"rows": len(self.data), "columns": len(columns), "column_names": columns}

    def get_column_types(self):
        result = {}
        for column in self._column_names():
            values = [
                row[column] for row in self.data
                if column in row and not is_missing(row[column])
            ]
            if not values:
                result[column] = "empty"
                continue
            try:
                numeric = all(
                    not isinstance(value, bool) and math.isfinite(float(value))
                    for value in values
                )
            except (ValueError, TypeError, OverflowError):
                numeric = False
            result[column] = "numeric" if numeric else "text"
        return result

    def get_numeric_columns(self):
        return [
            name for name, kind in self.get_column_types().items()
            if kind == "numeric"
        ]

    def get_column_values(self, column):
        if column not in self._column_names():
            raise KeyError(f"Column not found: {column}")
        values = []
        for row in self.data:
            value = row.get(column)
            if is_missing(value):
                continue
            if isinstance(value, bool):
                raise ValueError(f"Column {column!r} contains a non-numeric value.")
            try:
                number = float(value)
            except (ValueError, TypeError, OverflowError) as error:
                raise ValueError(
                    f"Column {column!r} contains a non-numeric value: {value!r}"
                ) from error
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
        columns = self._column_names()
        if first_column not in columns:
            raise KeyError(f"Column not found: {first_column}")
        if second_column not in columns:
            raise KeyError(f"Column not found: {second_column}")
        pairs = []
        for row in self.data:
            first, second = row.get(first_column), row.get(second_column)
            if is_missing(first) or is_missing(second):
                continue
            if isinstance(first, bool) or isinstance(second, bool):
                continue
            try:
                x, y = float(first), float(second)
            except (ValueError, TypeError, OverflowError):
                continue
            if math.isfinite(x) and math.isfinite(y):
                pairs.append((x, y))
        if len(pairs) < 2:
            return None
        return calculate_correlation(
            [pair[0] for pair in pairs], [pair[1] for pair in pairs]
        )
