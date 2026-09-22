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


#print(calculate_median([7, 2, 5, 1, 9]))
#print(calculate_median([2, 4, 6, 8]))


#test_data = [
#    {"Study_Hours": "4.5"},
#    {"Study_Hours": "6.0"},
#    {"Study_Hours": "2.5"},
#    {"Study_Hours": "7.0"}
#]

#values = extract_column(test_data, "Study_Hours")

#print(values)
#print(calculate_mean(values))

#print(calculate_mean(None))
#print(calculate_mean("hello"))
#print(calculate_mean([10, 20, "30"]))