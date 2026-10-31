import math


def find_missing_values(data):
    missing_counts = {}

    for row in data:
        for key, value in row.items():
            if key not in missing_counts:
                missing_counts[key] = 0

            if is_missing(value):
                missing_counts[key] += 1

    return missing_counts


def find_duplicates(data, id_column="Student_ID"):
    """Return repeated non-empty identifiers, or None when the column is absent."""
    if not data:
        return []

    if id_column not in data[0]:
        return None

    seen_ids = set()
    duplicates = []

    for row in data:
        value = row.get(id_column)
        if value is None or not str(value).strip():
            continue

        identifier = str(value).strip()
        if identifier in seen_ids:
            duplicates.append(identifier)
        else:
            seen_ids.add(identifier)

    return duplicates


def clean_value(value):
    return value.strip()


def clean_row(row):
    for key, value in row.items():
        row[key] = clean_value(value)

    return row


def clean_data(data):
    for i, row in enumerate(data):
        data[i] = clean_row(row)

    return data


def is_missing(value):
    return value.strip() == ""


def validate_row(row):
    missing_fields = []
    errors = []

    required_fields = [
        "Age",
        "Attendance",
        "Study_Hours",
        "Previous_Score",
        "Sleep_Hours",
        "Internet_Usage",
        "Final_Score",
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
        except ValueError:
            errors.append(
                f"Error: The value {row['Age']} in Age must be an integer"
            )

    if "Attendance" not in missing_fields:
        try:
            attendance = int(row["Attendance"])
            if attendance < 0 or attendance > 100:
                errors.append("Attendance must be between 0 and 100")
        except ValueError:
            errors.append(
                f"Error: The value {row['Attendance']} in Attendance must be an integer"
            )

    if "Study_Hours" not in missing_fields:
        try:
            study_hours = float(row["Study_Hours"])
            if not math.isfinite(study_hours) or study_hours < 0 or study_hours > 24:
                errors.append("Study Hours must be a finite number between 0 and 24")
        except ValueError:
            errors.append(
                f"The value {row['Study_Hours']} in Study_Hours must be a number"
            )

    if "Previous_Score" not in missing_fields:
        try:
            previous_score = float(row["Previous_Score"])
            if not math.isfinite(previous_score):
                errors.append("Previous Score must be a finite number")
            elif previous_score < 0 or previous_score > 100:
                errors.append("Previous Score must be between 0 and 100")
        except ValueError:
            errors.append(
                f"The value {row['Previous_Score']} in Previous_Score must be a number"
            )

    if "Sleep_Hours" not in missing_fields:
        try:
            sleep_hours = float(row["Sleep_Hours"])
            if not math.isfinite(sleep_hours) or sleep_hours < 0 or sleep_hours > 24:
                errors.append("Sleep Hours must be a finite number between 0 and 24")
        except ValueError:
            errors.append(
                f"The value {row['Sleep_Hours']} in Sleep_Hours must be a number"
            )

    if "Internet_Usage" not in missing_fields:
        try:
            internet_usage = float(row["Internet_Usage"])
            if not math.isfinite(internet_usage) or internet_usage < 0 or internet_usage > 24:
                errors.append("Internet Usage must be a finite number between 0 and 24")
        except ValueError:
            errors.append(
                f"The value {row['Internet_Usage']} in Internet_Usage must be a number"
            )

    if "Final_Score" not in missing_fields:
        try:
            final_score = float(row["Final_Score"])
            if not math.isfinite(final_score):
                errors.append("Final Score must be a finite number")
            elif final_score < 0 or final_score > 100:
                errors.append("Final Score must be between 0 and 100")
        except ValueError:
            errors.append(
                f"The value {row['Final_Score']} in Final_Score must be a number"
            )

    if errors:
        return errors

    return True
