import csv
import os
from PyQt6.QtWidgets import QWidget, QMessageBox, QDialog, QVBoxLayout, QPushButton, QLabel
from addStudentui import Ui_Form
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from studentsData import loadStudents
from programcode import loadprograms
from editStudent  import check_existence_in_csv

class CustomDialog(QDialog):
    """A custom dialog for displaying messages."""
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setStyleSheet("background-color: #043927; color: white; border-radius: 5px; padding: 10px;")

        layout = QVBoxLayout()

        # Message Label
        label = QLabel(message)
        label.setStyleSheet("color: white; font-size: 14px;")
        layout.addWidget(label)

        # OK Button
        button = QPushButton("OK")
        button.setStyleSheet("background-color: white; color: #043927; border-radius: 5px; padding: 5px;")
        button.clicked.connect(self.accept)
        layout.addWidget(button)

        self.setLayout(layout)

class AddStudentForm(QWidget):
    def __init__(self, main_window):
        """Initialize the Add Student Form"""
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.main_window = main_window  # Reference to MainApp
        

        #Program Code ComboBox
        self.populate_programs()


        id_validator = QRegularExpressionValidator(QRegularExpression(r"^\d{4}-\d{4}$"))
        self.ui.lineEdit_3.setValidator(id_validator)  # Apply the validator to ID field
        
        # Connect Save button to save function
        self.ui.pushButton.clicked.connect(self.save_student)

    def populate_programs(self):
        """Populate the combo box with college codes"""
        programCode = loadprograms()
        self.ui.comboBox_4.addItems(programCode)

    def save_student(self):
        """Collects student data and saves it to a CSV file."""
        # Get user inputs
        first_name = self.ui.lineEdit.text().strip()
        last_name = self.ui.lineEdit_2.text().strip()
        student_id = self.ui.lineEdit_3.text().strip()

        if not student_id:
            QMessageBox.warning(None, "Input Error", "Student ID is required.")
            return
        if not self.ui.lineEdit_3.hasAcceptableInput():
            QMessageBox.warning(None, "Input Error", "Invalid ID format! Use XXXX-XXXX.")
            return
        
        STUDENTS_FILE = "students.csv"
        if check_existence_in_csv(STUDENTS_FILE, "ID Number", student_id):
            QMessageBox.warning(None, "Duplicate ID", f"Student ID: {student_id} already exists!", QMessageBox.StandardButton.Ok)
            return
        
        year_level = self.ui.comboBox.currentText()
        gender = self.ui.comboBox_2.currentText()
        program_name = self.ui.comboBox_4.currentText()

        # Check if any required field is empty
        if not first_name or not last_name or not student_id or not year_level or not gender or not program_name:
            QMessageBox.warning(None, "Input Error", "Please fill in all required fields.")
            return  

        # Define the CSV file path
        csv_file = "students.csv"
        # Check if file exists to determine whether to write headers
        file_exists = os.path.exists(csv_file)

        try:
            # Append the student data to the CSV file
            with open(csv_file, mode="a", newline="") as file:
                writer = csv.writer(file)

                # Write header only if file is new
                if not file_exists:
                    writer.writerow(["Student ID", "First Name", "Last Name", "Year Level", "Gender", "Program Name"])
            
                writer.writerow([student_id, first_name, last_name, year_level, gender, program_name])
            
            # Reload the main table with updated data
            loadStudents(self.main_window.ui.tableWidget)

            # Show confirmation message
            QMessageBox.information(None, "Success", "Student added successfully!")

        # Close the Add Student Form after saving
            self.close()

        except Exception as e:
            error_box = QMessageBox(self)
            error_box.setIcon(QMessageBox.Icon.Critical)
            error_box.setWindowTitle("Error")
            error_box.setText(f"An error occurred: {str(e)}")
            error_box.setStyleSheet("background-color: #043927; color: white; border-radius: 5px; padding: 10px;")
            error_box.exec()  # Show error message
    