class Dataset:

    def __init__(self, data, file_path):
        self.data = data
        self.file_path = file_path

    def show_info(self):
        print(self.data)
        print(f"File: {self.file_path}")
        print(f"Rows: {len(self.data)}")

dataset = Dataset(["row1", "row2"], "test.csv")
dataset2 = Dataset(["row3", "row4", "row5"], "another.csv")
dataset.show_info()
dataset2.show_info()