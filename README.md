# Research Data Analyzer

A modular Python project for cleaning, validating, exploring, and analyzing research-style tabular data in CSV files.

## Features

- Load CSV files with clear errors for missing files, invalid extensions, missing headers, and duplicate headers.
- Inspect dataset dimensions, column names, and detected column types.
- Clean surrounding whitespace, count missing values, validate student records, and detect duplicate IDs.
- Calculate mean, median, mode, minimum, maximum, range, population variance, and population standard deviation.
- Calculate quartiles and IQR, and flag potential outliers using the 1.5 × IQR rule.
- Calculate Pearson correlation between numeric columns using rows where both values are available.
- Export cleaned records to CSV and a machine-readable analysis report to JSON.
- Include dataset quality checks, numeric summaries, outlier results, and pairwise correlations in the JSON report.
- Test dataset operations, statistics, reporting, and CSV input/output with unittest or pytest.

## Project structure

```text
research-data-analyzer/
├── data/raw/student_performance.csv
├── data/processed/
│   ├── student_performance_cleaned.csv
│   └── analysis_report.json
├── src/research_analyzer/
│   ├── analyzer.py
│   ├── data_cleaner.py
│   ├── data_loader.py
│   ├── data_writer.py
│   ├── dataset.py
│   ├── main.py
│   ├── reporting.py
│   └── statistics.py
├── tests/
├── pyproject.toml
└── README.md
```

## Setup and run

Python 3.10 or newer is required. From the repository root:

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
python -m research_analyzer.main
```

The analysis command reads `data/raw/student_performance.csv` and writes two files:

- `data/processed/student_performance_cleaned.csv` — cleaned rows for downstream use.
- `data/processed/analysis_report.json` — structured quality checks, descriptive statistics, outlier flags, and correlations.

The JSON report is intended to be easy to inspect now and reuse later in a notebook, dashboard, or research workflow.

## Run tests

```bash
python -m unittest discover -s tests -v
# alternatively, after installing pytest:
python -m pytest
```

## Statistical conventions and limitations

- Variance and standard deviation use the population formula (divide by N).
- Quartiles use the median-of-halves convention; other tools may use different percentile interpolation methods.
- IQR outliers are observations strictly outside Q1 - 1.5 × IQR and Q3 + 1.5 × IQR. A flagged value is a prompt for investigation, not automatically an error.
- Pearson correlation measures linear association, not causation. It is undefined for constant columns or fewer than two paired values.
- Correlation skips rows where either selected value is blank or nonnumeric.
- The included student dataset is illustrative and should not support real-world educational or policy claims.

## Suggested workflow

Load and inspect the data, clean whitespace, review missing values and duplicates, check validation counts, inspect descriptive statistics and outliers, explore correlations, then review both exported files before interpreting results.
