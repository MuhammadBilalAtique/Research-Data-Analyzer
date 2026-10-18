import csv
from pathlib import Path


def load_csv(file_path):
    """Load a CSV into dictionaries or raise a clear exception on bad input."""
    path = Path(file_path)
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a .csv file, received: {path.name}")
    try:
        with path.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames:
                raise ValueError(f"CSV file has no header row: {path}")
            headers = [h.strip() if h else "" for h in reader.fieldnames]
            if any(not h for h in headers):
                raise ValueError("CSV headers cannot be empty.")
            if len(set(headers)) != len(headers):
                raise ValueError("CSV contains duplicate column names.")
            rows = []
            for line_number, row in enumerate(reader, start=2):
                if None in row:
                    raise ValueError(f"Row {line_number} has more values than the header.")
                rows.append({key.strip(): (value if value is not None else "") for key, value in row.items()})
            return rows
    except FileNotFoundError as error:
        raise FileNotFoundError(f"CSV file not found: {path}") from error
    except PermissionError as error:
        raise PermissionError(f"Permission denied while reading: {path}") from error
