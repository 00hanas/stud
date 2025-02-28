import csv
import re
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QColor, QBrush, QPainter, QPen
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QWidget, QMessageBox, QStyledItemDelegate, QTableWidgetItem
import studentsData

CSV_FILE = "students.csv"

EDIT_MODE_COLOR = QColor("#FFF3CD")  #  edit mode
DEFAULT_COLOR = QColor("#FFFFFF")  # normal state

class EditDelegate(QStyledItemDelegate):
    """Custom delegate to enforce font color during editing."""
    def paint(self, painter: QPainter, option, index):
        painter.save()
        painter.setPen(QPen(QColor("#043927")))  # Set font color to #043927
        super().paint(painter, option, index)
        painter.restore()

    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        editor.setStyleSheet("color: #043927;")  # Ensure text color stays #043927
        return editor

def create_edit_delete_buttons(row_idx, tableWidget, main_window=None):
    """Creates Edit and Delete buttons for a row."""
    actions = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Edit button
    editButton = QPushButton()
    editButton.setFixedSize(20, 20)
    editButton.setIcon(QIcon("edit icon.png"))
    editButton.setStyleSheet("""
    QPushButton{
        background-color: #043927;
        border: 0px;
        border-radius: 5px;              
    }
    QPushButton:hover{
        background-color: #065f46;     
    }
    """)
    editButton.clicked.connect(lambda _, idx=row_idx: enable_edit_mode(idx, tableWidget,main_window))
    layout.addWidget(editButton)

    # Delete button
    deleteButton = QPushButton()
    deleteButton.setFixedSize(20, 20)
    deleteButton.setIcon(QIcon("delete icon.png"))
    deleteButton.setStyleSheet("""
    QPushButton{
        background-color: #8B0000;
        border: 0px;
        border-radius: 5px;             
    }
    QPushButton:hover{
        background-color: #B22222;           
    }
    """)
    deleteButton.clicked.connect(lambda _, idx=row_idx: delete_student(idx, tableWidget, main_window))
    layout.addWidget(deleteButton)

    actions.setLayout(layout)

    column_count = tableWidget.columnCount()  # Get total column count
    tableWidget.setCellWidget(row_idx, column_count - 1, actions)  # Place in last column
    tableWidget.setColumnWidth(column_count - 1, 120)

import re
COLLEGES_FILE = "colleges.csv"
PROGRAMS_FILE = "programs.csv"
STUDENTS_FILE = "students.csv"

def validate_constraints(row_data, row_index=None, is_edit=False):
    """Validates constraints for student records before saving."""

    id_number = row_data.get("ID Number", "").strip()
    gender = row_data.get("Gender", "").strip().capitalize()
    year_level = row_data.get("Year Level", "").strip()
    program_code = row_data.get("Program Code", "").strip().upper()

    # Validate ID Number format: XXXX-XXXX (e.g., 2024-0001)
    if not re.match(r"^\d{4}-\d{4}$", id_number):
        return f"Invalid ID Number format: {id_number}. Must be XXXX-XXXX."
    
    #ID Number must be unique
    if not is_edit or (is_edit and row_index is not None):
        if check_existence_in_csv(STUDENTS_FILE, "ID Number", id_number, exclude_index=row_index):
            return f"Duplicate ID Number: {id_number}. Must be unique."

    # Validate Gender: Must be Male or Female
    if gender not in ["Male", "Female"]:
        return f"Invalid Gender: {gender}. Must be 'Male' or 'Female'."

    # Validate Year Level: Must be between 1 and 7
    if not year_level.isdigit() or not (1 <= int(year_level) <= 7):
        return f"Invalid Year Level: {year_level}. Must be between 1 and 7."
    
    # Validate Program Code: Must exist in programs.csv
    if not check_existence_in_csv(PROGRAMS_FILE, "Program Code", program_code):
        return f"Invalid Program Code: {program_code}. Program does not exist. Add it on the Program Page."

    return None  # No validation errors

def check_existence_in_csv(csv_file, column_name, value, exclude_index=None):
    """Checks if a given value exists in a specific column of a CSV file."""
    with open(csv_file, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        value = value.strip().upper()
        for idx, row in enumerate(reader):  # Track row index
            cell_value = row[column_name].strip().upper()
            if cell_value == value:
                if exclude_index is not None and idx == exclude_index:
                    continue
                return True
    return False  # No duplicates found

def check_program_under_college(csv_file, college_code, program_code):
    """Checks if a program exists under a given college in programs.csv."""
    with open(csv_file, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Program Code"].strip().upper() == program_code and row["College Code"].strip().upper() == college_code:
                return True
    return False

def save_edited_row(row_idx, tableWidget, main_window=None):
    """Saves the edited row and updates the CSV file with validation."""
    
    with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        HEADERS = reader.fieldnames
        data = list(reader)

    # Extract edited row data
    row_data = {HEADERS[col_idx]: tableWidget.item(row_idx, col_idx).text().strip() for col_idx in range(len(HEADERS))}

    # Validate constraints
    
    error_message = validate_constraints(row_data, row_index=row_idx, is_edit=True)
    if error_message:
        QMessageBox.warning(None, "Validation Error", error_message)
        return

    # Update row with validated values
    for col_idx, header in enumerate(HEADERS):
        item = tableWidget.item(row_idx, col_idx)
        if item:
            data[row_idx][header] = row_data[header]
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item.setBackground(DEFAULT_COLOR)

    # Write updated data back to CSV
    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(data)

    QMessageBox.information(None, "Success", "Student record updated successfully!")

    # Disable editing and restore Edit/Delete buttons
    for col_idx in range(len(HEADERS)):
        item = tableWidget.item(row_idx, col_idx)
        if item:
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

    create_edit_delete_buttons(row_idx, tableWidget, main_window)

def enable_edit_mode(row_idx, tableWidget, main_window=None):
    """Switches a row to edit mode (hides Edit/Delete, shows Save)."""
    column_count = tableWidget.columnCount()
    delegate = EditDelegate(tableWidget)
    tableWidget.setItemDelegateForRow(row_idx, delegate)

    original_values = [tableWidget.item(row_idx, col_idx).text() if tableWidget.item(row_idx, col_idx) else "" 
                       for col_idx in range(column_count - 1)]
    
    # Make cells editable
    for col_idx in range(column_count - 1):
        item = tableWidget.item(row_idx, col_idx)
        if item:
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable) # Enable editing
            item.setBackground(EDIT_MODE_COLOR)  
            item.setForeground(QBrush(QColor("#043927")))  

    # Replace Edit/Delete buttons with Save button
    actions = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    saveButton = QPushButton()
    saveButton.setIcon(QIcon("save icon.png"))
    saveButton.setFixedSize(20, 20)
    saveButton.setStyleSheet("""
    QPushButton {
        background-color: #043927;
        border-radius: 5px;
        border: none;
        color: white;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: #065f46;
    }
""")
    
    def save_or_cancel():
        """Ask user for confirmation before saving or canceling edits."""
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Confirm Edit")
        msgBox.setText("Do you want to save the changes?")
        msgBox.setIcon(QMessageBox.Icon.Question)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msgBox.setDefaultButton(QMessageBox.StandardButton.Yes)
        
        result = msgBox.exec()

        if result == QMessageBox.StandardButton.Yes:
            save_edited_row(row_idx, tableWidget)  # Save changes
        else:
            # Restore original values
            for col_idx in range(column_count - 1):
                tableWidget.item(row_idx, col_idx).setText(original_values[col_idx])
            
            # Reset cell formatting
            for col_idx in range(column_count - 1):
                item = tableWidget.item(row_idx, col_idx)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Disable editing
                    item.setBackground(QBrush(Qt.GlobalColor.white))  # Reset background
                    item.setForeground(QBrush(Qt.GlobalColor.black))  # Reset text color

            # Restore Edit/Delete buttons
            create_edit_delete_buttons(row_idx, tableWidget, main_window)

    saveButton.clicked.connect(save_or_cancel)
    layout.addWidget(saveButton)

    actions.setLayout(layout)
    tableWidget.setCellWidget(row_idx, column_count - 1, actions)


def delete_student(row_idx, tableWidget, main_window=None):

    """Deletes a student from the table and updates the CSV file."""
    with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        HEADERS = reader.fieldnames
        data = list(reader)

    # Confirm deletion
    confirm = QMessageBox.question(None, "Confirm Delete", "Are you sure you want to delete this record?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    if confirm == QMessageBox.StandardButton.No:
        return

    # Remove selected row from data
    del data[row_idx]

    # Write updated data back to CSV
    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(data)

    studentsData.loadStudents(tableWidget, main_window)

    # Reload data if main_window is provided
    if main_window and hasattr(main_window.ui, 'tableWidget'):
        studentsData.loadStudents(main_window.ui.tableWidget)