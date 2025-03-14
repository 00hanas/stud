from PyQt6.QtWidgets import QDialog, QMessageBox
from addcollegeui import Ui_CollegeForm
from collegesData import loadColleges
import csv
import os
from editStudent import check_existence_in_csv

class AddCollegeForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_CollegeForm()
        self.ui.setupUi(self)
        self.setModal(True)

        self.ui.pushButton.clicked.connect(self.save_college)

    def save_college(self):
        college_code = self.ui.lineEdit.text()
        college_name = self.ui.lineEdit_2.text()
        
        csv_file = "colleges.csv"
        file_exists = os.path.isfile(csv_file)

        if check_existence_in_csv(csv_file, "College Code", college_code):
            QMessageBox.warning(None, "Duplicate College Code", f"College Code: {college_code} already exists!", QMessageBox.StandardButton.Ok)
            return

        if not college_code or not college_name:
            QMessageBox.warning(None, "Input Error", "Please fill in all required fields.")
            return

        with open(csv_file, "a", newline="\n") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["College Code", "College Name"])  # Add headers if new file
            writer.writerow([college_code, college_name])

        QMessageBox.information(None, "Success", "College added successfully!")

        # Refresh tableWidget_2 in the main window
        if self.parent():
            loadColleges(self.parent().ui.tableWidget_3)

        self.accept()  # Close dialog properly