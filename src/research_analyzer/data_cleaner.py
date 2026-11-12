import math


def find_missing_values(data):
    """Count missing cells per column, including keys absent from a row."""
    columns = list(dict.fromkeys(key for row in data for key in row))
    return {
        column: sum(
            1 for row in data
            if column not in row or is_missing(row[column])
        )
        for column in columns
    }


def find_duplicates(data, id_column="Student_ID"):
    """Return repeated non-empty identifiers, or None when the column is absent."""
    if not data:
        return []
    if not any(id_column in row for row in data):
        return None
    seen_ids, duplicates = set(), []
    for row in data:
        value = row.get(id_column)
        if is_missing(value):
            continue
        identifier = str(value).strip()
        if identifier in seen_ids:
            duplicates.append(identifier)
        else:
            seen_ids.add(identifier)
    return duplicates


def clean_value(value):
    """Normalize a cell to trimmed text; treat None as an empty cell."""
    return "" if value is None else str(value).strip()


def clean_row(row):
    for key, value in row.items():
        row[key] = clean_value(value)
    return row


def clean_data(data):
    for index, row in enumerate(data):
        data[index] = clean_row(row)
    return data


def is_missing(value):
    """Return True for None, empty strings, and whitespace-only values."""
    return value is None or str(value).strip() == ""


def validate_row(row):
    missing_fields = []
    errors = []
    required_fields = [
        "Age", "Attendance", "Study_Hours", "Previous_Score",
        "Sleep_Hours", "Internet_Usage", "Final_Score",
    ]
    for field in required_fields:
        if field not in row:
            missing_fields.append(field)
            errors.append(f"The {field} key is missing")
            continue
        if is_missing(row[field]):
            missing_fields.append(field)
            errors.append(f"Value of {field} is missing")
            continue
    if "Age" not in missing_fields:
        try:
            age = int(row["Age"])
            if age < 10 or age > 80:
                errors.append("Age must be between 10 and 80")
        except (ValueError, TypeError):
            errors.append(f"Error: The value {row['Age']} in Age must be an integer")
    if "Attendance" not in missing_fields:
        try:
            attendance = int(row["Attendance"])
            if attendance < 0 or attendance > 100:
                errors.append("Attendance must be between 0 and 100")
        except (ValueError, TypeError):
            errors.append(f"Error: The value {row['Attendance']} in Attendance must be an integer")
    rules = {
        "Study_Hours": (0, 24, "Study Hours must be a finite number between 0 and 24"),
        "Previous_Score": (0, 100, "Previous Score must be between 0 and 100"),
        "Sleep_Hours": (0, 24, "Sleep Hours must be a finite number between 0 and 24"),
        "Internet_Usage": (0, 24, "Internet Usage must be a finite number between 0 and 24"),
        "Final_Score": (0, 100, "Final Score must be between 0 and 100"),
    }
    for field, (minimum, maximum, range_error) in rules.items():
        if field in missing_fields:
            continue
        try:
            value = float(row[field])
            if not math.isfinite(value):
                errors.append(f"{field} must be a finite number")
            elif value < minimum or value > maximum:
                errors.append(range_error)
        except (ValueError, TypeError):
            errors.append(f"The value {row[field]} in {field} must be a number")
    return errors if errors else True
