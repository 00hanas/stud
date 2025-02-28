import csv
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QColor, QBrush, QPainter, QPen
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QWidget, QMessageBox, QStyledItemDelegate
from editStudent import check_existence_in_csv




CSV_FILE = "colleges.csv"
EDIT_MODE_COLOR = QColor("#FFF3CD")  
DEFAULT_COLOR = QColor("#FFFFFF")  

class EditDelegate(QStyledItemDelegate):
    """Custom delegate to enforce font color during editing."""
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter: QPainter, option, index):
        painter.save()
        painter.setPen(QPen(QColor("#043927")))  
        super().paint(painter, option, index)
        painter.restore()

    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        editor.setStyleSheet("color: #043927;")  
        return editor


def create_edit_delete_buttons(row_idx, tableWidget, main_window):
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
    
    # Pass main_window explicitly
    editButton.clicked.connect(lambda _, idx=row_idx: enable_edit_mode(idx, tableWidget, main_window))

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
    deleteButton.clicked.connect(lambda _, idx=row_idx: delete_college(idx, tableWidget, main_window))
    layout.addWidget(deleteButton)

    actions.setLayout(layout)

    column_count = tableWidget.columnCount()  # Get total column count
    tableWidget.setCellWidget(row_idx, column_count - 1, actions)  # Place in last column
    tableWidget.setColumnWidth(column_count - 1, 120)

def validate_constraints(row_data, row_index=None, is_edit=False):
    college_code = row_data.get("College Code", "").strip().upper()

    #No duplicates of College Code
    if not is_edit or (is_edit and row_index is not None):
        if check_existence_in_csv(CSV_FILE, "College Code", college_code, exclude_index=row_index):
            return f"Duplicate College Code: {college_code}. Must be unique."

def save_edited_row(row_idx, tableWidget, main_window):
    """Saves the edited row and updates the colleges.csv file."""
    # Read the current table data
    with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        HEADERS = reader.fieldnames
        data = list(reader)
    
    # original code
    old_college_code = data[row_idx]["College Code"]

    # read the edited values
    row_data = {HEADERS[col_idx]: tableWidget.item(row_idx, col_idx).text().strip() for col_idx in range(len(HEADERS))}

    # Check if any cell is empty
    for header, value in row_data.items():
        if value == "":
            QMessageBox.warning(None, "Input Error", f"The field '{header}' cannot be empty.")
            return

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
            item.setBackground(QBrush(Qt.GlobalColor.transparent))

    # Write updated data back to CSV
    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(data)


    QMessageBox.information(None, "Success", "College updated successfully!")

    # Disable editing and restore Edit/Delete buttons
    for col_idx in range(len(HEADERS)):
        item = tableWidget.item(row_idx, col_idx)
        if item:
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  

    tableWidget.setItemDelegateForRow(row_idx, None) 
    create_edit_delete_buttons(row_idx, tableWidget, main_window)

    update_programs_file(old_college_code, row_data["College Code"]) 

    from collegesData import loadColleges
    loadColleges(main_window.ui.tableWidget_3, main_window)

    from programsData import loadPrograms
    loadPrograms(main_window.ui.tableWidget_2, main_window)

import csv

def update_programs_file(old_college_code, new_college_code):
    
    file_name = "programs.csv"
    
    with open(file_name, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        data = list(reader)

   
    for row in data:
        if row["College Code"] == old_college_code:
            row["College Code"] = new_college_code

    with open(file_name, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


def enable_edit_mode(row_idx, tableWidget, main_window):
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
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)  # Enable editing
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
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    item.setBackground(QBrush(Qt.GlobalColor.transparent))

            # Restore Edit/Delete buttons
            create_edit_delete_buttons(row_idx, tableWidget, main_window)

    saveButton.clicked.connect(save_or_cancel)
    layout.addWidget(saveButton) 

    layout.addWidget(saveButton)

    actions.setLayout(layout)
    tableWidget.setCellWidget(row_idx, column_count - 1, actions)


def delete_college(row_idx, tableWidget, main_window):
    with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        HEADERS = reader.fieldnames
        data = list(reader)


    college_code = data[row_idx]["College Code"]

    confirm = QMessageBox.question(None, "Confirm Delete", 
        f"Are you sure you want to delete this college? Programs will be removed, and students' Program Code will be set to 'N/A'.",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

    if confirm == QMessageBox.StandardButton.No:
        return

    # Remove college from colleges.csv
    del data[row_idx]

    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(data)

    # Remove related programs and update students
    null_programs_college(college_code)

    QMessageBox.information(None, "Success", "College deleted. Programs' records updated.")

    from collegesData import loadColleges
    loadColleges(main_window.ui.tableWidget_3, main_window)
    from programsData import loadPrograms
    loadPrograms(main_window.ui.tableWidget_2, main_window)
     


def null_programs_college(college_code):
    """Updates the College Code in programs.csv when a college is edited."""
    with open("programs.csv", "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        HEADERS = reader.fieldnames
        data = list(reader)

    for row in data:
        if row["College Code"] == college_code:
           row["College Code"] = "N/A"

    with open("programs.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(data)
