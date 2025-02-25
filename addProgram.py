from PyQt6.QtWidgets import QDialog, QMessageBox  # Change from QWidget to QDialog
from addprogramui import Ui_ProgramForm
from programsData import loadPrograms
from collegecode import load_college_codes
import csv
import os

class AddProgramForm(QDialog):  # Use QDialog instead of QWidget
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ProgramForm()
        self.ui.setupUi(self)
        self.setModal(True)  # Make it a modal window (blocks main window until closed)

        #CollegeCode ComboBox
        self.populate_college_codes()
        # Connect Save button
        self.ui.pushButton.clicked.connect(self.save_program)

    def populate_college_codes(self):
        """Populate the combo box with college codes"""
        college_codes = load_college_codes()
        self.ui.comboBox.addItems(college_codes)

    def save_program(self):
        """Saves program details to CSV and updates tableWidget_2 in the main window."""
        college_code = self.ui.comboBox.currentText()
        program_code = self.ui.lineEdit_2.text()
        program_name = self.ui.lineEdit_3.text()

        if not college_code or not program_code or not program_name:
            err_box = QMessageBox(self)
            err_box.setIcon(QMessageBox.Icon.Warning)
            err_box.setWindowTitle("Input Error")
            err_box.setText("Please fill in all required fields.")
            err_box.setStyleSheet("background-color: #043927; color: white; border-radius: 5px; padding: 10px;")  # Apply the same style
            err_box.exec()
            return

        csv_file = "programs.csv"
        file_exists = os.path.isfile(csv_file)

        with open(csv_file, "a", newline="\n") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Program Code", "Program Name", "College Code"])  # Add headers if new file
            writer.writerow([program_code, program_name, college_code])

        # Show confirmation message
            success_box = QMessageBox(self)
            success_box.setIcon(QMessageBox.Icon.Information)
            success_box.setWindowTitle("Success")
            success_box.setText("Program added successfully!")
            success_box.setStyleSheet("background-color: #043927; color: white; border-radius: 5px; padding: 10px;")
            success_box.exec()  # Show the message box

        # Refresh tableWidget_2 in the main window
        if self.parent():
            loadPrograms(self.parent().ui.tableWidget_2)

        self.accept()  # Close dialog properly