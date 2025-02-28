from PyQt6.QtWidgets import QDialog, QMessageBox
from addcollegeui import Ui_CollegeForm
import csv
import os
from editStudent import check_existence_in_csv

class AddCollegeForm(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_CollegeForm()
        self.ui.setupUi(self)
        self.setModal(True)
        self.main_window = main_window

        self.ui.pushButton.clicked.connect(self.save_college)


    def save_college(self):
        college_code = self.ui.lineEdit.text().strip()
        college_name = self.ui.lineEdit_2.text().strip()
        
        csv_file = "colleges.csv"
        file_exists = os.path.isfile(csv_file)

        if check_existence_in_csv(csv_file, "College Code", college_code):
            QMessageBox.warning(self, "Duplicate College Code", f"College Code: {college_code} already exists!", QMessageBox.StandardButton.Ok)
            return

        if not college_code or not college_name:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return

        with open(csv_file, "a", newline="\n") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["College Code", "College Name"])  
            writer.writerow([college_code, college_name])

        QMessageBox.information(self, "Success", "College added successfully!")

        self.accept()  # Close dialog properly

        from collegesData import loadColleges
        
        loadColleges(self.main_window.ui.tableWidget_3, self)

        
