import csv
from pathlib import Path


def save_csv(data, file_path, fieldnames=None):
    """Save dictionary rows to CSV, creating parent folders if necessary."""
    path = Path(file_path)
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a .csv output path, received: {path.name}")
    if data:
        if not all(isinstance(row, dict) for row in data):
            raise TypeError("Every data row must be a dictionary.")
        inferred = list(data[0].keys())
        if any(list(row.keys()) != inferred for row in data):
            raise ValueError("All rows must have the same columns in the same order.")
        if fieldnames is not None and list(fieldnames) != inferred:
            raise ValueError("Provided fieldnames do not match the row columns.")
        fieldnames = inferred
    elif fieldnames is None:
        raise ValueError("fieldnames are required when saving an empty dataset.")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    return path
