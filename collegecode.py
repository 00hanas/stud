import csv

def load_college_codes():
    college_codes = []
    with open("colleges.csv", mode="r", newline="") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 2:  # Ensure valid row
                college_code = row[0].strip()  # Extract only college code
                college_codes.append(college_code)
    return college_codes
