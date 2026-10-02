from research_analyzer.data_writer import save_csv
from research_analyzer.dataset import Dataset
from research_analyzer.analyzer import DataAnalyzer

dataset = Dataset("data/raw/student_performance.csv")
dataset.load()

dataset.clean()
cleaned_data = dataset.data

analyzer = DataAnalyzer([])
study_hours = analyzer.extract_column(cleaned_data, "Study_Hours")

mean_study_hours = analyzer.mean()
print(f"Mean Study Hours: {mean_study_hours}")

median_study_hours = analyzer.median()
print(f"Median Study Hours: {median_study_hours}")

mode_study_hours = analyzer.mode()
print(f"Mode Study Hours: {mode_study_hours}")

minimum_study_hours = analyzer.minimum()
print(f"Minimum Study Hours: {minimum_study_hours}")

maximum_study_hours = analyzer.maximum()
print(f"Maximum Study Hours: {maximum_study_hours}")

range_study_hours = analyzer.range()
print(f"Range of Study Hours: {range_study_hours}")

variance_study_hours = analyzer.variance()
print(f"Variance of Study Hours: {variance_study_hours}")

std_dev_study_hours = analyzer.standard_deviation()
print(f"Standard Deviation of Study Hours: {std_dev_study_hours}")

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

save_csv(cleaned_data, "data/processed/student_performance_cleaned.csv")

validation_result = dataset.validate()

print(f"Total rows: {len(dataset.data)}")
print(f"Valid rows: {validation_result['valid']}")
print(f"Invalid rows: {validation_result['invalid']}")