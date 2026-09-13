from research_analyzer.data_loader import load_csv
from research_analyzer.data_cleaner import validate_row

data = load_csv("data/raw/student_performance.csv")

valid_rows = 0
invalid_rows = 0

for row in data:
    result = validate_row(row)

    if result:
        valid_rows += 1

    else:
        invalid_rows += 1

print(f"Total rows: {len(data)}")
print(f"Valid rows: {valid_rows}")
print(f"Invalid rows: {invalid_rows}")