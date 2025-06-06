import csv
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem
from editStudent import create_edit_delete_buttons

CSV_FILE = "students.csv"

def loadStudents(tableWidget, main_window=None):

    with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)  # Read CSV as dictionaries
        HEADERS = reader.fieldnames
        data = list(reader)  # Convert to a list of dictionaries

        tableWidget.setColumnCount(len(HEADERS) + 1)  
        tableWidget.setHorizontalHeaderLabels(HEADERS + ["Actions"])
        tableWidget.horizontalHeader().setVisible(True)

        if data:  
            tableWidget.setRowCount(len(data))  

            for row_idx, row_data in enumerate(data):  # Iterate over rows
                for col_idx, header in enumerate(reader.fieldnames):  # Iterate over columns
                    value = row_data.get(header, "").strip() # Get value by column name
                    item = QTableWidgetItem(value)  # Create a table item
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Read-only
                    tableWidget.setItem(row_idx, col_idx, item)  # Add item to table
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                # Create Edit/Delete buttons
                create_edit_delete_buttons(row_idx, tableWidget, main_window)
 





