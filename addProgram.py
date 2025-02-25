from PyQt6.QtWidgets import QDialog, QMessageBox 
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
        self.setModal(True)  

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
            QMessageBox.warning(None, "Input Error", "Please fill in all required fields.")
            return

        csv_file = "programs.csv"
        file_exists = os.path.isfile(csv_file)

        with open(csv_file, "a", newline="\n") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Program Code", "Program Name", "College Code"])  # Add headers if new file
            writer.writerow([program_code, program_name, college_code])

        QMessageBox.information(None, "Success", "Program added successfully!")

        # Refresh tableWidget_2 in the main window
        if self.parent():
            loadPrograms(self.parent().ui.tableWidget_2)

        self.accept()  # Close dialog properly