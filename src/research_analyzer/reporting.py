import json
from itertools import combinations
from pathlib import Path

from research_analyzer.analyzer import DataAnalyzer
from research_analyzer.data_cleaner import validate_row, is_missing


def _build_data_quality_summary(dataset):
    """Summarize row completeness, duplicate records, and column diversity."""
    columns = dataset.info()["column_names"]
    empty_row_numbers = []
    duplicate_row_numbers = []
    seen_rows = set()
    non_missing_counts = {column: 0 for column in columns}
    distinct_values = {column: set() for column in columns}
    rows_with_missing_values = 0

    for row_number, row in enumerate(dataset.data, start=1):
        row_has_missing = False
        row_is_empty = True
        for column in columns:
            value = row.get(column)
            if is_missing(value):
                row_has_missing = True
                continue
            row_is_empty = False
            normalized = str(value).strip()
            non_missing_counts[column] += 1
            distinct_values[column].add(normalized)
        if row_has_missing:
            rows_with_missing_values += 1
        if row_is_empty:
            empty_row_numbers.append(row_number)

        fingerprint = tuple(
            (column, "" if is_missing(row.get(column)) else str(row[column]).strip())
            for column in columns
        )
        if fingerprint in seen_rows:
            duplicate_row_numbers.append(row_number)
        else:
            seen_rows.add(fingerprint)

    distinct_counts = {
        column: len(values) for column, values in distinct_values.items()
    }
    constant_columns = [
        column for column, count in distinct_counts.items() if count == 1
    ]
    return {
        "total_rows": len(dataset.data),
        "rows_with_missing_values": rows_with_missing_values,
        "empty_row_numbers": empty_row_numbers,
        "duplicate_row_numbers": duplicate_row_numbers,
        "duplicate_row_count": len(duplicate_row_numbers),
        "non_missing_value_counts": non_missing_counts,
        "distinct_value_counts": distinct_counts,
        "constant_columns": constant_columns,
    }


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

    invalid_rows = []
    for row_number, row in enumerate(dataset.data, start=1):
        result = validate_row(row)
        if result is not True:
            invalid_rows.append({"row_number": row_number, "errors": result})

    return {
        "dataset": info,
        "column_types": column_types,
        "validation": dataset.validate(),
        "invalid_rows": invalid_rows,
        "missing_values": missing_values,
        "missing_value_percentages": missing_value_percentages,
        "column_completeness_percentages": column_completeness_percentages,
        "data_quality": _build_data_quality_summary(dataset),
        "duplicate_student_ids": dataset.find_duplicates(),
        "numeric_summary": numeric_summary,
        "pearson_correlations": correlations,
        "interpretation_notes": [
            "Variance and standard deviation use the population formula (divide by N).",
            "Quartiles use the median-of-halves convention.",
            "IQR outliers are potential observations to investigate, not automatic errors.",
            "Pearson correlation describes linear association, not causation.",
            "Pairwise Pearson correlations use complete, finite numeric pairs only.",
            "Duplicate Student_ID checks are unavailable when the dataset has no Student_ID column; blank identifiers are ignored.",
            "Duplicate row numbers identify repeated records after the first occurrence.",
            "Empty row numbers and all row references are one-based data-row positions and exclude the CSV header.",
            "Row validation follows the included student-performance schema; other datasets require their own validation rules.",
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
