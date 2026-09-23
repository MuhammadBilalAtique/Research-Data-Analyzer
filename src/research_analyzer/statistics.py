def calculate_mean(values):

    if not isinstance(values, list):
        print("Error: values must be a list of numbers.")
        return None

    if values == []:
        return None

    try:
        mean_sum = sum(values)
        mean_value = len(values)

        mean = mean_sum / mean_value

        return mean

    except TypeError:
        print("Error: All values must be numbers.")
        return None


def extract_column(data, column):

    values = []

    for row in data:
        values.append(float(row[column]))

    return values



def calculate_median(values):

    if not isinstance(values, list):
        print("Error: values must be a list of numbers.")
        return None

    if values == []:
        return None

    values.sort()

    if len(values) % 2 == 1:
        middle = len(values) // 2
        median = values[middle]
        return median 
    
    middle = len(values) // 2
    median = (values[middle - 1] + values[middle]) / 2
    return median 

def calculate_mode(values):

    if not isinstance(values, list):
        print("Error: values must be a list of numbers.")
        return None
    
    if values == []:
        return None

    frequency = {}

    for value in values:
        if value not in frequency:
            frequency[value] = 1

        else:
            frequency[value] += 1

    highest_count = 0
    modes = []

    for value, count in frequency.items():
        if count > highest_count:
            highest_count = count
            modes = []
            modes.append(value)

        elif count == highest_count:
            modes.append(value)

    if highest_count == 1:
        return None

    return modes 
   