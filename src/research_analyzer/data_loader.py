import csv

def load_csv(file_path):

    lst = []

    if file_path.endswith(".csv"):
    
        try:
            with open(file_path, newline='', encoding='utf-8') as f:

                reader = csv.DictReader(f)

                for row in reader:
                    lst.append(row)

            return lst

        except FileNotFoundError:
            print(f"ERROR: Could not find dataset: {file_path}")

        except PermissionError:
            print(f"ERROR: Permission denied: {file_path}")

    else:
        print("Error: File must be a CSV file")    


data = load_csv("data/raw/student_performance.csv")

print(data)
