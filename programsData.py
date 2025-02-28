import csv
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem
from editProgram import create_edit_delete_buttons

CSV_FILE = "programs.csv"

def loadPrograms(tableWidget, main_window=None):
    
    with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        HEADERS = reader.fieldnames
        data = list(reader)

        tableWidget.setColumnCount(len(HEADERS) + 1)
        tableWidget.setHorizontalHeaderLabels(HEADERS + ["Actions"])
        tableWidget.horizontalHeader().setVisible(True)

        if data:
            tableWidget.setRowCount(len(data))
            for row_idx, row_data in enumerate(data):
                for col_idx, header in enumerate(HEADERS):
                    value = row_data.get(header, "").strip()
                    item = QTableWidgetItem(value)
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    tableWidget.setItem(row_idx, col_idx, item)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                # Create Edit/Delete buttons
                create_edit_delete_buttons(row_idx, tableWidget, main_window)


