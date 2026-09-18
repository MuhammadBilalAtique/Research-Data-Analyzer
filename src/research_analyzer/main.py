from research_analyzer.data_loader import load_csv
from research_analyzer.data_cleaner import clean_data, validate_row

data = load_csv("data/raw/student_performance.csv")

cleaned_data = clean_data(data)

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