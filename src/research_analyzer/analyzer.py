from research_analyzer.statistics import calculate_mean, calculate_median, calculate_mode, calculate_minimum, calculate_maximum

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