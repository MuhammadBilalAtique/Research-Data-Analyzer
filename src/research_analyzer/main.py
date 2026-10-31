import argparse
from itertools import combinations

from research_analyzer.dataset import Dataset
from research_analyzer.analyzer import DataAnalyzer
from research_analyzer.reporting import build_analysis_report, save_analysis_report


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Clean and analyze a CSV dataset, then export CSV and JSON results."
    )
    parser.add_argument(
        "--input",
        default="data/raw/student_performance.csv",
        help="Path to the source CSV file.",
    )
    parser.add_argument(
        "--output",
        default="data/processed/student_performance_cleaned.csv",
        help="Path for the cleaned CSV output.",
    )
    parser.add_argument(
        "--report",
        default="data/processed/analysis_report.json",
        help="Path for the JSON analysis report.",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    dataset = Dataset(args.input)
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
    if duplicates is None:
        print("\nDuplicate Student IDs: Not checked (Student_ID column is absent)")
    else:
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

    output = dataset.save(
        args.output,
        fieldnames=info["column_names"],
    )
    print(f"\nCleaned CSV saved to: {output}")

    report = build_analysis_report(dataset)
    report_path = save_analysis_report(
        report,
        args.report,
    )
    print(f"Analysis report saved to: {report_path}")


if __name__ == "__main__":
    main()
