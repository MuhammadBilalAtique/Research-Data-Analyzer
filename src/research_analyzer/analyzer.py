from research_analyzer.statistics import calculate_mean, calculate_median, calculate_mode, calculate_minimum, calculate_maximum, calculate_range, calculate_variance, calculate_standard_deviation

class DataAnalyzer:

    def __init__(self, values):
        self.values = values
        
    def mean(self):
        result = calculate_mean(self.values)
        return result

    def median(self):
        result = calculate_median(self.values)
        return result

    def mode(self):
        result = calculate_mode(self.values)
        return result 

    def minimum(self):
        result = calculate_minimum(self.values)
        return result

    def maximum(self):
        result = calculate_maximum(self.values)
        return result

    def range(self):
        result = calculate_range(self.values)
        return result

    def variance(self):
        result = calculate_variance(self.values)
        return result

    def standard_deviation(self):
        result = calculate_standard_deviation(self.values)
        return result 

    def extract_column(self, data, column):
        values = []

        for row in data:
            values.append(float(row[column]))

        self.values = values
        return values