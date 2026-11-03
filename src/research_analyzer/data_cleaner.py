import math


def find_missing_values(data):
    missing_counts = {}
    for row in data:
        for key, value in row.items():
            if key not in missing_counts: missing_counts[key] = 0
            if is_missing(value): missing_counts[key] += 1
    return missing_counts


def find_duplicates(data, id_column="Student_ID"):
    """Return repeated non-empty identifiers, or None when the column is absent."""
    if not data: return []
    if id_column not in data[0]: return None
    seen_ids, duplicates = set(), []
    for row in data:
        value = row.get(id_column)
        if is_missing(value): continue
        identifier = str(value).strip()
        if identifier in seen_ids: duplicates.append(identifier)
        else: seen_ids.add(identifier)
    return duplicates


def clean_value(value):
    """Normalize a cell to trimmed text; treat None as an empty cell."""
    return "" if value is None else str(value).strip()


def clean_row(row):
    for key, value in row.items(): row[key] = clean_value(value)
    return row


def clean_data(data):
    for index, row in enumerate(data): data[index] = clean_row(row)
    return data


def is_missing(value):
    """Return True for None, empty strings, and whitespace-only values."""
    return value is None or str(value).strip() == ""


def validate_row(row):
    missing_fields, errors = [], []
    required_fields = ["Age", "Attendance", "Study_Hours", "Previous_Score", "Sleep_Hours", "Internet_Usage", "Final_Score"]
    for field in required_fields:
        if field not in row:
            missing_fields.append(field); errors.append(f"The {field} key is missing"); continue
        if is_missing(row[field]):
            missing_fields.append(field); errors.append(f"Value of {field} is missing"); continue
    numeric_rules = {
        "Age": (int, 10, 80, "Age must be between 10 and 80", "integer"),
        "Attendance": (int, 0, 100, "Attendance must be between 0 and 100", "integer"),
        "Study_Hours": (float, 0, 24, "Study Hours must be between 0 and 24", "number"),
        "Previous_Score": (float, 0, 100, "Previous Score must be between 0 and 100", "number"),
        "Sleep_Hours": (float, 0, 24, "Sleep Hours must be between 0 and 24", "number"),
        "Internet_Usage": (float, 0, 24, "Internet Usage must be between 0 and 24", "number"),
        "Final_Score": (float, 0, 100, "Final Score must be between 0 and 100", "number"),
    }
    for field, (converter, minimum, maximum, range_error, value_kind) in numeric_rules.items():
        if field in missing_fields: continue
        try:
            value = converter(row[field])
            if not math.isfinite(value): errors.append(f"{field} must be a finite {value_kind}")
            elif value < minimum or value > maximum: errors.append(range_error)
        except (ValueError, TypeError):
            errors.append(f"The value {row[field]} in {field} must be an {value_kind}" if value_kind == "integer" else f"The value {row[field]} in {field} must be a number")
    return errors if errors else True
