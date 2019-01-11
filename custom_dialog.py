from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# View del Custom
class CustomDialog:
    def __init__(self):
        self.dialog = QDialog()
        self.dialog.resize(250, 100)

        self.w = QWidget(self.dialog)
        self.grid = QGridLayout()
        l = QLabel(text="Size")
        l2 = QLabel(text="Bombs")
        self.grid.addWidget(l,1,0)
        self.grid.addWidget(l2,2,0)
        self.textinputs = QLineEdit()
        self.textinputs2 = QLineEdit()
        self.grid.addWidget(self.textinputs, 1, 1)
        self.grid.addWidget(self.textinputs2, 2, 1)
        self.configbutton = QPushButton(text="Reconfigure")
        self.grid.addWidget(self.configbutton, 3, 1, 2, 1)
        self.w.setLayout(self.grid)

        self.dialog.setWindowTitle("Custom")


