def validate_row(row):

    try:
        age = int(row["Age"])
    except ValueError:
        print(f"Error: The Value {row['Age']}in age must be an integer")
        return False 
    
    try:
        attendance = int(row["Attendance"])
        if attendance < 0 or attendance > 100:
            print("Attendance must be between 0 and 100")
            return False 
             
    except ValueError:
        print(f"Error: The value {row['Attendance']} in Attendance must be an Integer")
        return False

    try:
        study_hours = float(row["Study_Hours"])

    except ValueError:
        print(f"The value {row['Study_Hours']} in study_hours must be a number")
        return False
                    
   
    return True

row = { 
    "Age" : "20",
    "Attendance" : "85",
    "Study_Hours" : "abc"
}

result = validate_row(row)
print(result)