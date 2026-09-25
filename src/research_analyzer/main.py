from research_analyzer.data_loader import load_csv
from research_analyzer.data_cleaner import clean_data, validate_row, find_duplicates, find_missing_values
from research_analyzer.data_writer import save_csv
from research_analyzer.statistics import (
    calculate_mean, 
    extract_column, 
    calculate_median, 
    calculate_mode, 
    calculate_minimum,
    calculate_maximum,
    calculate_range

) 
data = load_csv("data/raw/student_performance.csv")
cleaned_data = clean_data(data)

study_hours = extract_column(cleaned_data, "Study_Hours")

print(study_hours)
print(type(study_hours[0]))

mean_study_hours = calculate_mean(study_hours)
print(f"Mean Study Hours: {mean_study_hours}")

median_study_hours = calculate_median(study_hours)
print(f"Median Study Hours: {median_study_hours}")

mode_study_hours = calculate_mode(study_hours)
print(f"Mode Study Hours: {mode_study_hours}")

minimum_study_hours = calculate_minimum(study_hours)
print(f"Minimum Study Hours: {minimum_study_hours}")

maximum_study_hours = calculate_maximum(study_hours)
print(f"Maximum Study Hours: {maximum_study_hours}")

range_study_hours = calculate_range(study_hours)
print(f"Range of Study Hours: {range_study_hours}")

missing_values = find_missing_values(cleaned_data)
print("Missing Value Analysis:")

for field, count in missing_values.items():
    print(f"  - {field}: {count}")

duplicates = find_duplicates(cleaned_data)

if duplicates:
    print("Duplicate Student IDs: ")
    for student_id in duplicates:
        print(f"  - {student_id}")

else:
    print("No duplicate Student IDs found.")

save_csv(cleaned_data, "data/processed/student_performance_cleaned.csv")

valid_rows = 0
invalid_rows = 0

for row in cleaned_data:

    result = validate_row(row)

    if result is True:
        valid_rows += 1

    else:
        invalid_rows += 1

        print("Invalid row:")

        for error in result:
            print(f"   - {error}")

print(f"Total rows: {len(data)}")
print(f"Valid rows: {valid_rows}")
print(f"Invalid rows: {invalid_rows}")