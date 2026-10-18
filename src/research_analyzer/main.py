from itertools import combinations

from research_analyzer.dataset import Dataset
from research_analyzer.analyzer import DataAnalyzer


def main():
    dataset = Dataset("data/raw/student_performance.csv")
    dataset.load()
    dataset.clean()
    info = dataset.info()

    print("Dataset Information")
    print(f"Rows: {info['rows']}")
    print(f"Columns: {info['columns']}")
    print(f"Column names: {', '.join(info['column_names'])}")

    print("\nColumn Types")
    for column, kind in dataset.get_column_types().items():
        print(f"- {column}: {kind}")

    numeric_columns = dataset.get_numeric_columns()
    print("\nDescriptive Statistics")
    for column in numeric_columns:
        analyzer = DataAnalyzer(dataset.get_column_values(column))
        print(f"\n{column}")
        print(f"  Mean: {analyzer.mean()}")
        print(f"  Median: {analyzer.median()}")
        print(f"  Mode: {analyzer.mode()}")
        print(f"  Minimum / maximum: {analyzer.minimum()} / {analyzer.maximum()}")
        print(f"  Range: {analyzer.range()}")
        print(f"  Population variance: {analyzer.variance()}")
        print(f"  Population standard deviation: {analyzer.standard_deviation()}")
        print(f"  Quartiles (Q1, Q2, Q3): {analyzer.quartiles()}")
        print(f"  IQR: {analyzer.iqr()}")
        print(f"  Potential IQR outliers: {analyzer.outliers_iqr()}")

    print("\nMissing Values")
    for column, count in dataset.find_missing_values().items():
        print(f"- {column}: {count}")
    duplicates = dataset.find_duplicates()
    print(f"\nDuplicate Student IDs: {duplicates if duplicates else 'None'}")

    validation = dataset.validate()
    print("\nValidation")
    print(f"Valid rows: {validation['valid']}")
    print(f"Invalid rows: {validation['invalid']}")

    print("\nPearson Correlations")
    for first, second in combinations(numeric_columns, 2):
        coefficient = dataset.correlation(first, second)
        if coefficient is not None:
            print(f"- {first} vs {second}: {coefficient:.3f}")

    output = dataset.save("data/processed/student_performance_cleaned.csv", fieldnames=info["column_names"])
    print(f"\nCleaned CSV saved to: {output}")


if __name__ == "__main__":
    main()
