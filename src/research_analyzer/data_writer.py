import csv


def save_csv(data, file_path):

    if not data:
        return

    fieldnames = data[0].keys()

    with open(file_path, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        writer.writerows(data)