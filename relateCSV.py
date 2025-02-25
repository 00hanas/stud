import pandas as pd
import os

# Load CSV files into DataFrames (create empty DataFrame if file doesn't exist)
students_file = "students.csv"
programs_file = "programs.csv"
college_file = "colleges.csv"

students_df = pd.read_csv(students_file) if os.path.exists(students_file) else pd.DataFrame(columns=["Student ID", "First Name", "Last Name", "Year Level", "Gender", "Program Code", "College Code"])
programs_df = pd.read_csv(programs_file) if os.path.exists(programs_file) else pd.DataFrame(columns=["Program Code", "Program Name", "College Code"])
college_df = pd.read_csv(college_file) if os.path.exists(college_file) else pd.DataFrame(columns=["College Code", "College Name"])

# Function to add a new student
def add_student(student_id, first_name, last_name, year_level, gender, program_code, college_code):
    global students_df

    # Check if student already exists
    if student_id in students_df["Student ID"].values:
        raise ValueError(f"Student ID {student_id} already exists!")

    # Check if program_code exists in programs_df
    if program_code not in programs_df["Program Code"].values:
        raise ValueError(f"Program Code {program_code} does not exist!")

    # Check if college_code exists in college_df
    if college_code not in college_df["College Code"].values:
        raise ValueError(f"College Code {college_code} does not exist!")

    # Add new student record
    new_student = pd.DataFrame([{
        "Student ID": student_id,
        "First Name": first_name,
        "Last Name": last_name,
        "Year Level": year_level,
        "Gender": gender,
        "Program Code": program_code,
        "College Code": college_code
    }])

    # Append to students DataFrame
    students_df = pd.concat([students_df, new_student], ignore_index=True)
    save_changes()

# Function to update program code in all related files
def update_program_code(old_code, new_code, new_name=None):
    global students_df, programs_df
    
    students_df.loc[students_df["Program Code"] == old_code, "Program Code"] = new_code
    programs_df.loc[programs_df["Program Code"] == old_code, "Program Code"] = new_code
    if new_name:
        programs_df.loc[programs_df["Program Code"] == new_code, "Program Name"] = new_name

# Function to update college code in all related files
def update_college_code(old_code, new_code, new_name=None):
    global students_df, programs_df, college_df

    students_df.loc[students_df["College Code"] == old_code, "College Code"] = new_code
    programs_df.loc[programs_df["College Code"] == old_code, "College Code"] = new_code
    college_df.loc[college_df["College Code"] == old_code, "College Code"] = new_code
    if new_name:
        college_df.loc[college_df["College Code"] == new_code, "College Name"] = new_name

# Function to save changes
def save_changes():
    global students_df, programs_df, college_df

    students_df.to_csv(students_file, index=False)
    programs_df.to_csv(programs_file, index=False)
    college_df.to_csv(college_file, index=False)
