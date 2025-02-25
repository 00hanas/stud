from PyQt6.QtWidgets import QWidget, QStackedWidget, QGridLayout
from students import loadStudents

class StackedWidgetManager(QWidget):
    def __init__(self, ui):
        super().__init__()

        self.ui = ui  # Store reference to main UI
        self.layout = QGridLayout(self)  # Set main layout

        # Create the QStackedWidget
        self.stackedWidget = QStackedWidget()
        self.layout.addWidget(self.stackedWidget, 0, 0, 1, 1)  # Add to layout

        # Create pages
        self.page_students = QWidget()
        self.page_programs = QWidget()
        self.page_colleges = QWidget()

        self.page_students.setLayout(QGridLayout())
        self.page_programs.setLayout(QGridLayout())
        self.page_colleges.setLayout(QGridLayout())


        # Add widgets to QStackedWidget
        self.stackedWidget.addWidget(self.page_students)  # Index 0
        self.stackedWidget.addWidget(self.page_programs)  # Index 1
        self.stackedWidget.addWidget(self.page_colleges)  # Index 2

        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.layout.setSpacing(0)  # Remove unnecessary spacing
        self.layout.setColumnStretch(0, 1)
        self.layout.setRowStretch(0, 1)



    def switchToStudents(self):
        self.stackedWidget.setCurrentWidget(self.page_students)

    def switchToPrograms(self):
        self.stackedWidget.setCurrentWidget(self.page_programs)

    def switchToColleges(self):
        self.stackedWidget.setCurrentWidget(self.page_colleges)