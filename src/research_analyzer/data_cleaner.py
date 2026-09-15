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
        "Final_Score"
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

        except ValueError:
            errors.append(
                f"The value {row['Study_Hours']} in Study_Hours must be a number"
            )

    if "Previous_Score" not in missing_fields:
        try:
            previous_score = float(row["Previous_Score"])

            if previous_score < 0 or previous_score > 100:
                errors.append("Previous Score must be between 0 and 100")

        except ValueError:
            errors.append(
                f"The value {row['Previous_Score']} in Previous_Score must be a number"
            )

    if "Sleep_Hours" not in missing_fields:
        try:
            sleep_hours = float(row["Sleep_Hours"])

        except ValueError:
            errors.append(
                f"The value {row['Sleep_Hours']} in Sleep_Hours must be a number"
            )

    if "Internet_Usage" not in missing_fields:
        try:
            internet_usage = float(row["Internet_Usage"])

        except ValueError:
            errors.append(
                f"The value {row['Internet_Usage']} in Internet_Usage must be a number"
            )

    if "Final_Score" not in missing_fields:
        try:
            final_score = float(row["Final_Score"])

            if final_score < 0 or final_score > 100:
                errors.append("Final Score must be between 0 and 100")

        except ValueError:
            errors.append(
                f"The value {row['Final_Score']} in Final_Score must be a number"
            )

    if errors:
        return errors

    return True




#row = {
    #"Age": "20",
    #"Attendance": "85",
    #"Study_Hours": "4.5",
    #"Previous_Score": "75.5",
    #"Sleep_Hours": "3.5",
    #"Internet_Usage": "8.5",
    #"Final_Score": "85"
#}

#result = validate_row(row)
#print(result)