import csv
import os
from PyQt6.QtWidgets import QWidget, QMessageBox, QDialog, QVBoxLayout, QPushButton, QLabel, QTableWidget
from addui import Ui_Form
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from studentsData import loadStudents
from collegecode import load_college_codes
from programcode import load_programs

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
        self.programs_by_college = load_programs() 

        #CollegeCode ComboBox
        self.populate_college_codes()

        self.ui.comboBox_3.currentTextChanged.connect(self.populate_programs)

        id_validator = QRegularExpressionValidator(QRegularExpression(r"^\d{4}-\d{4}$"))
        self.ui.lineEdit_3.setValidator(id_validator)  # Apply the validator to ID field
        
        # Connect Save button to save function
        self.ui.pushButton.clicked.connect(self.save_student)

    def populate_college_codes(self):
        """Populate the combo box with college codes"""
        college_codes = load_college_codes()
        self.ui.comboBox_3.addItems(college_codes)

    def populate_programs(self):
        """Update program options based on the selected college code"""
        selected_college = self.ui.comboBox_3.currentText()
        self.ui.comboBox_4.clear()  # Assuming comboBox_4 is for Program Code
        
        if selected_college in self.programs_by_college:
            self.ui.comboBox_4.addItems(self.programs_by_college[selected_college])

    def save_student(self):
        """Collects student data and saves it to a CSV file."""
        # Get user inputs
        first_name = self.ui.lineEdit.text().strip()
        last_name = self.ui.lineEdit_2.text().strip()
        student_id = self.ui.lineEdit_3.text().strip()

        if not student_id:
            self.show_message("Input Error", "Student ID is required.", QMessageBox.Icon.Warning)
            return
        if not self.ui.lineEdit_3.hasAcceptableInput():
            self.show_message("Input Error", "Invalid ID format! Use XXXX-XXXX.", QMessageBox.Icon.Warning)
            return
        
        year_level = self.ui.comboBox.currentText()
        gender = self.ui.comboBox_2.currentText()
        college_code = self.ui.comboBox_3.currentText()
        program_name = self.ui.comboBox_4.currentText()

        # Check if any required field is empty
        if not first_name or not last_name or not student_id or not year_level or not gender or not college_code or not program_name:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Input Error")
            msg_box.setText("Please fill in all required fields.")
            msg_box.setStyleSheet("background-color: #043927; color: white; border-radius: 5px; padding: 10px;")  # Apply the same style
            msg_box.exec()  # Show the message box
            return  # Stop execution
        

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
                    writer.writerow(["Student ID", "First Name", "Last Name", "Year Level", "Gender", "Program Name","College Code"])
            
                writer.writerow([student_id, first_name, last_name, year_level, gender, program_name, college_code])
            # Reload the main table with updated data
            loadStudents(self.main_window.ui.tableWidget)

            # Show confirmation message
            success_box = QMessageBox(self)
            success_box.setIcon(QMessageBox.Icon.Information)
            success_box.setWindowTitle("Success")
            success_box.setText("Student added successfully!")
            success_box.setStyleSheet("background-color: #043927; color: white; border-radius: 5px; padding: 10px;")
            success_box.exec()  # Show the message box

        # Close the Add Student Form after saving
            self.close()

        except Exception as e:
            error_box = QMessageBox(self)
            error_box.setIcon(QMessageBox.Icon.Critical)
            error_box.setWindowTitle("Error")
            error_box.setText(f"An error occurred: {str(e)}")
            error_box.setStyleSheet("background-color: #043927; color: white; border-radius: 5px; padding: 10px;")
            error_box.exec()  # Show error message
    
    def show_message(self, title, message, icon):
        """Reusable function to show message dialogs."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStyleSheet("background-color: #043927; color: white; border-radius: 5px; padding: 10px;")
        msg_box.exec()