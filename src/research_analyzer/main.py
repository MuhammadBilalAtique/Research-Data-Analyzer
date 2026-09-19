from research_analyzer.data_loader import load_csv
from research_analyzer.data_cleaner import clean_data, validate_row, find_duplicates
from research_analyzer.data_writer import save_csv

data = load_csv("data/raw/student_performance.csv")
cleaned_data = clean_data(data)

duplicates = find_duplicates(cleaned_data)

if duplicates:
    print("Duplicate Student IDs: ")
    for student_id in duplicates:
        print(f"  - {student_id}")

else:
    print("No Duplicate Student IDs Found")

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