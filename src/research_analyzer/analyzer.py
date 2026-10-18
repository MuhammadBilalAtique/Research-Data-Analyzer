from research_analyzer.statistics import (
    calculate_mean, calculate_median, calculate_mode, calculate_minimum,
    calculate_maximum, calculate_range, calculate_variance,
    calculate_standard_deviation, calculate_quartiles, calculate_iqr,
    find_outliers_iqr,
)


class DataAnalyzer:
    """Convenience wrapper for descriptive statistics on a numeric list."""

    def __init__(self, values):
        self.values = values

    def mean(self): return calculate_mean(self.values)
    def median(self): return calculate_median(self.values)
    def mode(self): return calculate_mode(self.values)
    def minimum(self): return calculate_minimum(self.values)
    def maximum(self): return calculate_maximum(self.values)
    def range(self): return calculate_range(self.values)
    def variance(self): return calculate_variance(self.values)
    def standard_deviation(self): return calculate_standard_deviation(self.values)
    def quartiles(self): return calculate_quartiles(self.values)
    def iqr(self): return calculate_iqr(self.values)
    def outliers_iqr(self): return find_outliers_iqr(self.values)
