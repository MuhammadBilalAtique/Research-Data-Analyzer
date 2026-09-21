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
    
#print(calculate_mean(None))
#print(calculate_mean("hello"))
#print(calculate_mean([10, 20, "30"]))