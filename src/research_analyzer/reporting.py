import json
from itertools import combinations
from pathlib import Path

from research_analyzer.analyzer import DataAnalyzer


def build_analysis_report(dataset):
    """Build a JSON-serializable summary of a cleaned Dataset."""
    info = dataset.info()
    column_types = dataset.get_column_types()
    numeric_columns = dataset.get_numeric_columns()
    numeric_summary = {}

    for column in numeric_columns:
        values = dataset.get_column_values(column)
        analyzer = DataAnalyzer(values)
        numeric_summary[column] = {
            "count": len(values),
            "mean": analyzer.mean(),
            "median": analyzer.median(),
            "mode": analyzer.mode(),
            "minimum": analyzer.minimum(),
            "maximum": analyzer.maximum(),
            "range": analyzer.range(),
            "population_variance": analyzer.variance(),
            "population_standard_deviation": analyzer.standard_deviation(),
            "quartiles": analyzer.quartiles(),
            "iqr": analyzer.iqr(),
            "potential_outliers": analyzer.outliers_iqr(),
        }

    correlations = []
    for first, second in combinations(numeric_columns, 2):
        correlations.append({
            "first_column": first,
            "second_column": second,
            "pearson_r": dataset.correlation(first, second),
        })

    missing_values = dataset.find_missing_values()
    row_count = info["rows"]
    missing_value_percentages = {
        column: round(count / row_count * 100, 2)
        for column, count in missing_values.items()
    } if row_count else {}
    column_completeness_percentages = {
        column: round(100 - percentage, 2)
        for column, percentage in missing_value_percentages.items()
    }

    return {
        "dataset": info,
        "column_types": column_types,
        "validation": dataset.validate(),
        "missing_values": missing_values,
        "missing_value_percentages": missing_value_percentages,
        "column_completeness_percentages": column_completeness_percentages,
        "duplicate_student_ids": dataset.find_duplicates(),
        "numeric_summary": numeric_summary,
        "pearson_correlations": correlations,
        "interpretation_notes": [
            "Variance and standard deviation use the population formula (divide by N).",
            "Quartiles use the median-of-halves convention.",
            "IQR outliers are potential observations to investigate, not automatic errors.",
            "Pearson correlation describes linear association, not causation.",
            "Duplicate Student_ID checks are unavailable when the dataset has no Student_ID column; blank identifiers are ignored.",
        ],
    }


def save_analysis_report(report, file_path):
    """Write a JSON report, creating parent directories when needed."""
    path = Path(file_path)
    if path.suffix.lower() != ".json":
        raise ValueError(f"Expected a .json report path, received: {path.name}")

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2, allow_nan=False)
        file.write("\n")
    return path
