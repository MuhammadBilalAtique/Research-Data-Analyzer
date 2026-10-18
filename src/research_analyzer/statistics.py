from math import sqrt, isfinite


def _validate_numeric_list(values, function_name):
    if not isinstance(values, list):
        print(f"Error: values must be a list of numbers for {function_name}.")
        return False
    if not values:
        return False
    if any(not isinstance(v, (int, float)) or isinstance(v, bool) or not isfinite(v) for v in values):
        print(f"Error: All values must be finite numbers for {function_name}.")
        return False
    return True


def calculate_mean(values):
    return sum(values) / len(values) if _validate_numeric_list(values, "mean") else None


def calculate_median(values):
    if not _validate_numeric_list(values, "median"):
        return None
    ordered = sorted(values)
    middle = len(ordered) // 2
    return ordered[middle] if len(ordered) % 2 else (ordered[middle - 1] + ordered[middle]) / 2


def calculate_mode(values):
    if not _validate_numeric_list(values, "mode"):
        return None
    frequencies = {}
    for value in values:
        frequencies[value] = frequencies.get(value, 0) + 1
    highest = max(frequencies.values())
    return None if highest == 1 else [v for v, count in frequencies.items() if count == highest]


def calculate_minimum(values):
    return min(values) if _validate_numeric_list(values, "minimum") else None


def calculate_maximum(values):
    return max(values) if _validate_numeric_list(values, "maximum") else None


def calculate_range(values):
    return max(values) - min(values) if _validate_numeric_list(values, "range") else None


def calculate_variance(values):
    if not _validate_numeric_list(values, "variance"):
        return None
    mean = sum(values) / len(values)
    return sum((v - mean) ** 2 for v in values) / len(values)


def calculate_standard_deviation(values):
    variance = calculate_variance(values)
    return sqrt(variance) if variance is not None else None


def calculate_quartiles(values):
    """Return (Q1, Q2, Q3) using the median-of-halves convention."""
    if not _validate_numeric_list(values, "quartiles"):
        return None
    ordered = sorted(values)
    middle = len(ordered) // 2
    lower = ordered[:middle]
    upper = ordered[middle + 1:] if len(ordered) % 2 else ordered[middle:]

    def median(items):
        mid = len(items) // 2
        return items[mid] if len(items) % 2 else (items[mid - 1] + items[mid]) / 2

    return (median(lower) if lower else ordered[0], median(ordered), median(upper) if upper else ordered[-1])


def calculate_iqr(values):
    quartiles = calculate_quartiles(values)
    return quartiles[2] - quartiles[0] if quartiles is not None else None


def find_outliers_iqr(values):
    """Return observations outside the 1.5 × IQR fences, in input order."""
    quartiles = calculate_quartiles(values)
    if quartiles is None:
        return None
    q1, _, q3 = quartiles
    spread = q3 - q1
    low, high = q1 - 1.5 * spread, q3 + 1.5 * spread
    return [v for v in values if v < low or v > high]


def calculate_correlation(x_values, y_values):
    """Calculate Pearson's r for paired numeric lists, or None if undefined."""
    if not _validate_numeric_list(x_values, "correlation") or not _validate_numeric_list(y_values, "correlation"):
        return None
    if len(x_values) != len(y_values):
        print("Error: correlation lists must have the same length.")
        return None
    if len(x_values) < 2:
        return None
    x_mean, y_mean = sum(x_values) / len(x_values), sum(y_values) / len(y_values)
    x_dev = [v - x_mean for v in x_values]
    y_dev = [v - y_mean for v in y_values]
    x_ss, y_ss = sum(v * v for v in x_dev), sum(v * v for v in y_dev)
    if x_ss == 0 or y_ss == 0:
        return None
    return sum(x_dev[i] * y_dev[i] for i in range(len(x_values))) / sqrt(x_ss * y_ss)
