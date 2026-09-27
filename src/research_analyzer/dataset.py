from research_analyzer.data_loader import load_csv

class Dataset:

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

    def load(self):
        self.data = load_csv(self.file_path)

    def show_info(self):
        print(self.data)
        print(f"File: {self.file_path}")
        print(f"Rows: {len(self.data)}")
