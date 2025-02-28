import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from mainui import Ui_MainWindow 
from studentsData import loadStudents
from programsData import loadPrograms
from collegesData import loadColleges
from addStudent import AddStudentForm
from addProgram import AddProgramForm
from addCollege import AddCollegeForm
from sortTable import sort_table
from searchTable import search_table

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()  # Create an instance of the UI class
        self.ui.setupUi(self)


        # Connect search for Students page
        self.ui.lineEdit.textChanged.connect(lambda: search_table(self.ui.tableWidget, self.ui.lineEdit, self.ui.comboBox))  
        self.ui.comboBox.currentTextChanged.connect(lambda: search_table(self.ui.tableWidget, self.ui.lineEdit, self.ui.comboBox))  

        # Connect search for Programs page
        self.ui.lineEdit_2.textChanged.connect(lambda: search_table(self.ui.tableWidget_2, self.ui.lineEdit_2, self.ui.comboBox_6))  
        self.ui.comboBox_6.currentTextChanged.connect(lambda: search_table(self.ui.tableWidget_2, self.ui.lineEdit_2, self.ui.comboBox_6))  

        # Connect search for Colleges page
        self.ui.lineEdit_3.textChanged.connect(lambda: search_table(self.ui.tableWidget_3, self.ui.lineEdit_3, self.ui.comboBox_9))  
        self.ui.comboBox_9.currentTextChanged.connect(lambda: search_table(self.ui.tableWidget_3, self.ui.lineEdit_3, self.ui.comboBox_9))  

        #addstudent
        self.ui.pushButton.clicked.connect(self.show_addui)

        #addprogram
        self.ui.pushButton_11.clicked.connect(self.show_addprogramui)

        #addcollege
        self.ui.pushButton_12.clicked.connect(self.show_addcollegeui)

        #sortTable1
        self.ui.comboBox_2.currentTextChanged.connect(self.apply_sort)  # Connect ComboBox change
        self.ui.comboBox_3.currentTextChanged.connect(self.apply_sort)  # Connect Sort Order change

        #sortTable2
        self.ui.comboBox_4.currentTextChanged.connect(self.apply_sort2)  # Connect ComboBox change
        self.ui.comboBox_5.currentTextChanged.connect(self.apply_sort2)  # Connect Sort Order change

        #sortTable3
        self.ui.comboBox_7.currentTextChanged.connect(self.apply_sort3)  # Connect ComboBox change
        self.ui.comboBox_8.currentTextChanged.connect(self.apply_sort3)  # Connect Sort Order change

        self.ui.tabWidget.setCurrentIndex(0)

        #switching tabs at tab1
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(1))
        self.ui.pushButton_4.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(2))

        #switching tabs at tab2
        self.ui.pushButton_5.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(0))
        self.ui.pushButton_7.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(2))

        #switching tabs at tab3
        self.ui.pushButton_8.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(0))
        self.ui.pushButton_9.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(1))

        if hasattr(self.ui, 'tableWidget'):
            loadStudents(self.ui.tableWidget, self)  # Pass tableWidget to function

        if hasattr(self.ui, 'tableWidget_2'):  # Assuming tableWidget_2 is on page 2
            loadPrograms(self.ui.tableWidget_2, self) 

        if hasattr(self.ui, 'tableWidget_3'):  # Assuming tableWidget_2 is on page 2
            loadColleges(self.ui.tableWidget_3, self) 

    def show_addui(self):
        self.add_student_window = AddStudentForm(self)
        if self.add_student_window.exec():
            loadStudents(self.ui.tableWidget, self)
    def show_addcollegeui(self):
        self.add_college_window = AddCollegeForm(self)
        if self.add_college_window.exec():  # Wait for dialog to close
            loadColleges(self.ui.tableWidget_3, self)  # Reload colleges
    def show_addprogramui(self):
        self.add_program_window = AddProgramForm(self)
        if self.add_program_window.exec():  # Wait for dialog to close
            loadPrograms(self.ui.tableWidget_2, self)  # Reload programs # Reload programs
    
    def apply_sort(self):
        
        column_name = self.ui.comboBox_2.currentText()  # Get selected column
        ascending = self.ui.comboBox_3.currentText() == "Ascending"  # Check sort order

        sort_table(self.ui.tableWidget, column_name, ascending)

    def apply_sort2(self):
        
        column_name = self.ui.comboBox_4.currentText()  # Get selected column
        ascending = self.ui.comboBox_5.currentText() == "Ascending"  # Check sort order

        sort_table(self.ui.tableWidget_2, column_name, ascending)
    
    def apply_sort3(self):
        
        column_name = self.ui.comboBox_7.currentText()  # Get selected column
        ascending = self.ui.comboBox_8.currentText() == "Ascending"  # Check sort order

        sort_table(self.ui.tableWidget_3, column_name, ascending)

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create the application
    window = MainApp()  # Initialize main window
    window.show()  # Show the main window on the screen
    sys.exit(app.exec())  # Run the event loop
