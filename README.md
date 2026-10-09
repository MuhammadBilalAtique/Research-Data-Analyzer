# Research Data Analyzer

A beginner-friendly Python project for loading, cleaning, validating, and analyzing research-style tabular data from CSV files.

## Features

- Load CSV datasets using Python's built-in `csv` module.
- Inspect dataset dimensions, column names, and detected column types.
- Clean whitespace from data values.
- Validate student records and report invalid rows.
- Count missing values and detect duplicate student IDs.
- Calculate descriptive statistics for numeric columns:
  - Mean and median
  - Mode
  - Minimum, maximum, and range
  - Population variance and standard deviation
- Save the cleaned dataset as a new CSV file.

## Project structure

```text
research-data-analyzer/
├── data/
│   ├── raw/
│   │   └── student_performance.csv
│   └── processed/
├── src/
│   └── research_analyzer/
│       ├── analyzer.py
│       ├── data_cleaner.py
│       ├── data_loader.py
│       ├── data_writer.py
│       ├── dataset.py
│       └── statistics.py
└── main.py
```

## Run the project

1. Make sure Python 3 is installed.
2. Open a terminal in the project root directory.
3. Run:

```bash
python main.py
```

The program reads `data/raw/student_performance.csv`, prints dataset information and descriptive statistics, reports missing values, duplicate IDs, and validation totals, then writes the cleaned data to `data/processed/student_performance_cleaned.csv`.

## Dataset

The sample dataset contains student-related fields such as age, study hours, attendance, previous score, sleep hours, internet usage, and final score.

## Purpose

This project is part of a step-by-step journey in Python programming and research-oriented data analysis. The statistics are implemented as reusable functions to make the calculations easier to understand and test.
