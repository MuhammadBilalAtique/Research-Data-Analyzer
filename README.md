# Research Data Analyzer

A modular Python project for cleaning, validating, exploring, and analyzing research-style tabular data in CSV files. The project is being developed as a step-by-step research portfolio project, with an emphasis on transparent data-quality checks and reproducible analysis.

## Features

- Load CSV files with clear errors for missing files, invalid extensions, missing headers, and duplicate headers.
- Inspect dataset dimensions, column names, and detected column types.
- Clean surrounding whitespace, count missing values, validate student records, and detect duplicate IDs.
- Report missing-value counts and per-column missing-value percentages in the structured report, alongside per-column completeness percentages. Empty datasets return empty percentage mappings rather than dividing by zero.
- Calculate mean, median, mode, minimum, maximum, range, population variance, and population standard deviation.
- Calculate quartiles and IQR, and flag potential outliers using the 1.5 × IQR rule.
- Calculate Pearson correlation between numeric columns using rows where both values are available.
- Create optional exploratory visualizations: a histogram for one column, comparative box plots, and a Pearson correlation heatmap.
- Save visualizations to image files or return figures for further customization.
- Export cleaned records to CSV and a machine-readable analysis report to JSON.
- Include dataset quality checks, numeric summaries, outlier results, and pairwise correlations in the JSON report.
- Test dataset operations, statistics, reporting, visualization helpers, and CSV input/output with Python's `unittest` framework; tests can also be run with `pytest`.
- Run the unit-test suite automatically through GitHub Actions when changes are pushed to `main` or a pull request targets `main`.

## Project structure

```text
research-data-analyzer/
├── .github/workflows/
│   └── tests.yml
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
│   ├── statistics.py
│   └── visualization.py
├── tests/
├── pyproject.toml
└── README.md
```

## Setup and run

Python 3.10 or newer is required. From the repository root:

```bash
python -m venv .venv
# Windows PowerShell: .\\.venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
python -m research_analyzer.main
```

By default, the analysis command reads `data/raw/student_performance.csv` and writes two files:

- `data/processed/student_performance_cleaned.csv` — cleaned rows for downstream use.
- `data/processed/analysis_report.json` — a structured report containing dataset information, data-quality checks, missing-value counts, missing-value and completeness percentages, descriptive statistics, outlier flags, and correlations.

The JSON report is intended to be easy to inspect now and reuse later in a notebook, dashboard, or research workflow.

### Exploratory visualizations (optional)

Install the visualization extra to add Matplotlib without making it a requirement for the core CSV and statistics features:

```bash
python -m pip install -e ".[visualization]"
```

The plotting functions return Matplotlib figures. They can display the figure in an interactive environment or save it to a path:

```python
from research_analyzer.dataset import Dataset
from research_analyzer.visualization import (
    plot_distribution,
    plot_boxplot,
    plot_correlation_heatmap,
)

dataset = Dataset("data/raw/student_performance.csv")
dataset.load()
dataset.clean()

plot_distribution(dataset, "Final_Score", "data/processed/final_score_histogram.png")
plot_boxplot(dataset, ["Previous_Score", "Final_Score"],
             "data/processed/score_boxplot.png")
plot_correlation_heatmap(dataset, output_path="data/processed/correlation_heatmap.png")
```

The heatmap uses the project's existing pairwise Pearson correlation implementation. Correlation is descriptive and does not establish causation. If a column has no numeric values, or fewer than two columns are selected for a heatmap, the plotting helper raises a clear `ValueError`.

### Use custom file paths

You can analyze another CSV without changing the source code by providing paths:

```bash
python -m research_analyzer.main --input data/raw/my_dataset.csv --output data/processed/my_dataset_cleaned.csv --report data/processed/my_dataset_report.json
```

The current row validator is tailored to the included student-performance schema; the CLI paths are configurable, but arbitrary datasets may need their own validation rules.

## Run tests

Run the project's unit tests from the repository root:

```bash
python -m unittest discover -s tests -v
```

Alternatively, after installing `pytest`:

```bash
python -m pytest
```

Visualization tests are skipped automatically when Matplotlib is not installed. Install the visualization extra to run them. GitHub Actions is configured to install the project and run the `unittest` suite on pushes to `main` and pull requests targeting `main`. A configured workflow does not by itself mean a particular run has passed; check the repository's Actions tab for the result of each run.

## Statistical conventions and limitations

- Variance and standard deviation use the population formula (divide by N).
- Quartiles use the median-of-halves convention; other tools may use different percentile interpolation methods.
- IQR outliers are observations strictly outside Q1 - 1.5 × IQR and Q3 + 1.5 × IQR. A flagged value is a prompt for investigation, not automatically an error.
- Pearson correlation measures linear association, not causation. It is undefined for constant columns or fewer than two paired values.
- Correlation skips rows where either selected value is blank or nonnumeric.
- Missing-value percentages are calculated per column as missing count divided by the total row count, multiplied by 100, and rounded to two decimal places. Completeness percentage is 100 minus the missing-value percentage. For an empty dataset, both percentage mappings are empty.
- The included student dataset is illustrative and should not support real-world educational or policy claims.

## Suggested workflow

Load and inspect the data, clean whitespace, review missing values and duplicates, check validation counts, inspect descriptive statistics and outliers, explore correlations and visualizations, then review both exported files before interpreting results. For dependable use, run the test suite after making changes and review the GitHub Actions result.
