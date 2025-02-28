from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget
from PyQt6.QtCore import Qt

def sort_table(tableWidget: QTableWidget, column_name: str, ascending: bool):

    # Get primary sort column index
    primary_col = get_column_index(tableWidget, column_name)

    # Determine the correct secondary column 
    possible_secondary_columns = ["First Name", "Program Code"]
    secondary_col = next((get_column_index(tableWidget, col) for col in possible_secondary_columns if get_column_index(tableWidget, col) is not None), None)

    if primary_col is None:
        return  # Invalid primary column, exit function

    # Extract table data
    rows = []
    for row in range(tableWidget.rowCount()):
        primary_value = tableWidget.item(row, primary_col).text() if tableWidget.item(row, primary_col) else ""
        secondary_value = tableWidget.item(row, secondary_col).text() if secondary_col is not None and tableWidget.item(row, secondary_col) else ""
        row_data = [tableWidget.item(row, col).text() if tableWidget.item(row, col) else "" for col in range(tableWidget.columnCount())]
        rows.append((primary_value, secondary_value, row_data))  # Store values for sorting

    # Sort data (Primary Sort -> Secondary Sort for ties)
    rows.sort(key=lambda x: (x[0], x[1]), reverse=not ascending)

    # Reinsert sorted data into the table
    for row_idx, (_, _, row_data) in enumerate(rows):
        for col_idx, value in enumerate(row_data):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align the text
            tableWidget.setItem(row_idx, col_idx, item)


def get_column_index(tableWidget: QTableWidget, column_name: str):
    """Gets the column index by matching the header name."""
    for col in range(tableWidget.columnCount()):
        if tableWidget.horizontalHeaderItem(col).text() == column_name:
            return col
    return None  
