import csv

def load_programs():
    """Load programs into a dictionary grouped by College Code."""
    programs_by_college = {}
    
    with open("programs.csv", mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            if len(row) >= 3:  # Ensure valid row
                program_code, program_name, college_code = row
                if college_code not in programs_by_college:
                    programs_by_college[college_code] = []
                programs_by_college[college_code].append(program_code)  # Store only program codes
    
    return programs_by_college

def loadprograms():
    program_codes = []
    with open("programs.csv", mode="r", newline="") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 2:  # Ensure valid row
                program_code = row[0].strip()  # Extract only college code
                program_codes.append(program_code)  # Append to list
    return program_codes
