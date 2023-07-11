from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit

class NewCollectionDialog(QDialog):
    return_value = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Collection")
        self.setFixedSize(200, 100)

        layout = QVBoxLayout()
        label = QLabel("Enter the new collection name:")
        layout.addWidget(label)

        self.text_input = QLineEdit()
        layout.addWidget(self.text_input)

        button = QPushButton("Create")
        button.clicked.connect(self.create_btn)
        layout.addWidget(button)

        self.setLayout(layout)

    def create_btn(self):
        # note about signal
        value = self.text_input.text() # this is a value that the signal will return
        if len(value) == 0:
            return # you're not funny
        self.return_value.emit(value) # a function in the mainwindow that handles the signal MUST include the same signal name
        self.close()

class NewDatabaseDialog(QDialog):
    return_value = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Database")
        self.setFixedSize(200, 100)

        layout = QVBoxLayout()
        label = QLabel("Enter the new database name:")
        layout.addWidget(label)

        self.text_input = QLineEdit()
        layout.addWidget(self.text_input)

        button = QPushButton("Create")
        button.clicked.connect(self.create_btn)
        layout.addWidget(button)

        self.setLayout(layout)

    def create_btn(self):
        # note about signal
        value = self.text_input.text() # this is a value that the signal will return
        if len(value) == 0:
            return # you're not funny
        self.return_value.emit(value) # a function in the mainwindow that handles the signal MUST include the same signal name
        self.close()