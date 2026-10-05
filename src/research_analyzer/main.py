from research_analyzer.dataset import Dataset
from research_analyzer.analyzer import DataAnalyzer

dataset = Dataset("data/raw/student_performance.csv")
dataset.load()

dataset_info = dataset.info()

print("Dataset Information:")
print(f"Rows: {dataset_info['rows']}")
print(f"Columns: {dataset_info['columns']}")
print(f"Column Names: {dataset_info['column_names']}")

column_types = dataset.get_column_types()

print("Column Types:")

for column, column_type in column_types.items():
    print(f"  - {column}: {column_type}")

numeric_columns = dataset.get_numeric_columns()

print("Numeric Columns:")

for column in numeric_columns:
    print(f"  - {column}")

dataset.clean()
cleaned_data = dataset.data

numeric_columns = dataset.get_numeric_columns()

for column in numeric_columns:

    values = dataset.get_column_values(column)
    analyzer = DataAnalyzer(values)

    print(f"\nStatistics for {column}:")
    print(f"Mean: {analyzer.mean()}")
    print(f"Median: {analyzer.median()}")
    print(f"Mode: {analyzer.mode()}")
    print(f"Minimum: {analyzer.minimum()}")
    print(f"Maximum: {analyzer.maximum()}")
    print(f"Range: {analyzer.range()}")
    print(f"Variance: {analyzer.variance()}")
    print(f"Standard Deviation: {analyzer.standard_deviation()}")

missing_values = dataset.find_missing_values()
print("Missing Value Analysis:")

for field, count in missing_values.items():
    print(f"  - {field}: {count}")

duplicates = dataset.find_duplicates()

if duplicates:
    print("Duplicate Student IDs: ")
    for student_id in duplicates:
        print(f"  - {student_id}")

else:
    print("No duplicate Student IDs found.")

dataset.save("data/processed/student_performance_cleaned.csv")

validation_result = dataset.validate()

print(f"Total rows: {len(dataset.data)}")
print(f"Valid rows: {validation_result['valid']}")
print(f"Invalid rows: {validation_result['invalid']}")