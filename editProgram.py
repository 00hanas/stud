import csv
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QColor, QBrush, QPainter, QPen
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QWidget, QMessageBox, QTableWidgetItem, QStyledItemDelegate
from studentsData import loadStudents
import programsData

CSV_FILE = "programs.csv"
EDIT_MODE_COLOR = QColor("#FFF3CD")  # Light yellow for edit mode
DEFAULT_COLOR = QColor("#FFFFFF")  # White for normal state

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
    editButton.clicked.connect(lambda _, idx=row_idx: enable_edit_mode(int(idx), tableWidget, main_window))
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
    deleteButton.clicked.connect(lambda _, idx=row_idx: delete_program(idx, tableWidget, main_window))
    layout.addWidget(deleteButton)

    actions.setLayout(layout)

    column_count = tableWidget.columnCount()  # Get total column count
    tableWidget.setCellWidget(row_idx, column_count - 1, actions)  # Place in last column
    tableWidget.setColumnWidth(column_count - 1, 120)

import re
COLLEGES_FILE = "colleges.csv"
PROGRAMS_FILE = "programs.csv"
def validate_constraints(row_data, row_index=None, is_edit=False):
    college_code = row_data.get("College Code", "").strip().upper()
    program_code = row_data.get("Program Code", "").strip().upper()

    #Program Code must not duplicate
    if not is_edit or (is_edit and row_index is not None):
        if check_existence_in_csv(PROGRAMS_FILE, "Program Code", program_code, exclude_index=row_index):
            return f"Program Code '{program_code}' already exists. Please choose a different one."

    if not check_existence_in_csv(COLLEGES_FILE, "College Code", college_code):
        return f"College Code '{college_code}' does not exist. Please add it on College Page."

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
    
def save_edited_row(row_idx, tableWidget, main_window=None):
    """Saves the edited row and updates the CSV file."""
    with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        HEADERS = reader.fieldnames
        data = list(reader)

    # Old values (originally stored in the table)
    old_program_code = data[row_idx]["Program Code"] 
    old_college_code = data[row_idx]["College Code"] 

    # Get new values from the table
    updated_values = {HEADERS[col_idx]: tableWidget.item(row_idx, col_idx).text().strip() for col_idx in range(len(HEADERS))}
    new_program_code = updated_values["Program Code"]
    new_college_code = updated_values["College Code"]

    #validate constraints
    error_msg = validate_constraints(updated_values, row_index=row_idx, is_edit=True)
    if error_msg:
        QMessageBox.warning(None, "Validation Error", error_msg)
        return

    if not new_program_code or not new_college_code:
        QMessageBox.warning(None, "Error", "Program Code and College Code cannot be empty.")
        return

    # Search for the matching row
    data[row_idx] = updated_values

    # Write back to CSV
    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(data)

    # Update students.csv if Program Code or College Code changed
    update_students_program(old_program_code, new_program_code, old_college_code, new_college_code)

    QMessageBox.information(None, "Success", "Program updated successfully!")

    # Disable editing and restore Edit/Delete buttons
    for col_idx in range(len(HEADERS)):
        item = tableWidget.item(row_idx, col_idx)
        if item:
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

    tableWidget.setItemDelegateForRow(row_idx, None)
    create_edit_delete_buttons(row_idx, tableWidget, main_window)

    # Refresh students table
    if main_window and hasattr(main_window.ui, 'tableWidget'):
        main_window.ui.tableWidget.clearContents()
        main_window.ui.tableWidget.setRowCount(0)
        loadStudents(main_window.ui.tableWidget)



def update_students_program(old_program_code, new_program_code, old_college_code, new_college_code):
    """Updates the Program Code and College Code in students.csv and the table widget."""
    with open("students.csv", "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        HEADERS = reader.fieldnames
        data = list(reader)

    for row in data:
        if row["Program Code"] == old_program_code:
            row["Program Code"] = new_program_code  # Update program code

    with open("students.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(data)

    
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
            save_edited_row(row_idx, tableWidget, main_window)  # Save changes
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


def delete_program(row_idx, tableWidget, main_window=None):
    """Deletes a program and updates students' program code to 'N/A'."""
    
    with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        HEADERS = reader.fieldnames
        data = list(reader)
    

    program_code = data[row_idx]["Program Code"]

    confirm = QMessageBox.question(None, "Confirm Delete", 
        f"Are you sure you want to delete this program? Students enrolled will have their Program Code set to 'N/A'.",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

    if confirm == QMessageBox.StandardButton.No:
        return

    # Remove program from programs.csv
    del data[row_idx]

    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(data)

    # Update students.csv (set Program Code to "N/A")
    update_students_program(program_code)

    QMessageBox.information(None, "Success", "Program deleted. Students' records updated.")


    programsData.loadPrograms(tableWidget, main_window)
    loadStudents(main_window.ui.tableWidget)


def update_students_program(old_program_code, new_program_code=None, old_college_code=None, new_college_code=None):
    """Updates the Program Code and College Code in students.csv when a program is edited."""
    with open("students.csv", "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        HEADERS = reader.fieldnames
        data = list(reader)

    for row in data:
        if row["Program Code"] == old_program_code:
            if new_program_code is None:  # If deleting, set program to "N/A"
                row["Program Code"] = "N/A"
            else:
                row["Program Code"] = new_program_code

    with open("students.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(data)
