def is_missing(value):

    return value.strip() == ""

def validate_row(row):

    required_fields = [
        "Age",
        "Attendance",
        "Study_Hours",
        "Previous_Score",
        "Sleep_Hours",
        "Internet_Usage",
        "Final_Score"
    ]

    for field in required_fields:

        if field not in row:
            print(f"The {field} key is missing")
            return False 

        if is_missing(row[field]):
            print(f"Value of {field} is missing")
            return False

    try:
        age = int(row["Age"])
        if age < 10 or age > 80:
            print("Age must be between 10 and 80")
            return False
        
    except ValueError:
        print(f"Error: The Value {row['Age']} in age must be an integer")
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

    try:
        previous_score = float(row["Previous_Score"])
        if previous_score < 0 or previous_score > 100:
            print("Score must be between 0 and 100")
            return False 
    
    except ValueError:
        print(f"The value {row['Previous_Score']} in previous_score must be a number")
        return False

    try:
        sleep_hours = float(row["Sleep_Hours"])
    
    except ValueError:
        print(f"The value {row['Sleep_Hours']} in sleep_hours must be a number")
        return False

    try:
        internet_usage = float(row["Internet_Usage"])
    
    except ValueError:
        print(f"The value {row['Internet_Usage']} in internet_usage must be a number")
        return False

    try:
        final_score = float(row["Final_Score"])
        if final_score < 0 or final_score > 100:
            print("Score must be between 0 and 100")
            return False 
        
    except ValueError:
        print(f"The value {row['Final_Score']} in final_score must be a number")
        return False
    
   
    return True



row = { 
    "Age" : "20",
    "Attendance" : "85",
    "Study_Hours" : "4.5",
    "Previous_Score" : "75.5",
    "Sleep_Hours" : "3.5",
    "Internet_Usage" : "8.5",
    "Final_Score" : "85"
}

#result = validate_row(row)
#print(result)
