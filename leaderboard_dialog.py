from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


# View della Leaderboard
class LeaderboardDialog:
    def __init__(self,controller):
        self.dialog = QDialog()

        self.w = QWidget(self.dialog)
        self.grid = QGridLayout()

        b = QLabel(text="Beginner")
        i = QLabel(text="Intermediate")
        e = QLabel(text="Expert")
        self.grid.addWidget(b,0,0)
        self.grid.addWidget(i,0,3)
        self.grid.addWidget(e,0,6)

        hspacer = QSpacerItem(50, 1)
        self.grid.addItem(hspacer, 0, 2)

        hspacer2 = QSpacerItem(50, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.grid.addItem(hspacer2, 0, 5)


        B , I , E = controller.leaderboardModel.getFile()

        lenB = B.__len__()
        lenI = I.__len__()
        lenE = E.__len__()

        for i in range(min(lenB,11)):
            l = QLabel(text=B[i][0])
            self.grid.addWidget(l, i+1, 0)
            l = QLabel(text=B[i][1])
            self.grid.addWidget(l, i+1, 1)

        for i in range(min(lenI, 11)):
            l = QLabel(text=I[i][0])
            self.grid.addWidget(l, i+1, 3)
            l = QLabel(text=I[i][1])
            self.grid.addWidget(l, i+1, 4)

        for i in range(min(lenE, 11)):
            l = QLabel(text=E[i][0])
            self.grid.addWidget(l, i+1, 6)
            l = QLabel(text=E[i][1])
            self.grid.addWidget(l, i+1, 7)


        self.w.setLayout(self.grid)

        self.dialog.resize(self.w.sizeHint())
        self.dialog.setWindowTitle("Leaderboard")

# View di quando vinco
class InsertWinnerDialog:
    def __init__(self):
        self.dialog = QDialog()

        self.w = QWidget(self.dialog)
        self.grid = QGridLayout()
        l = QLabel(text="Insert Name")
        self.grid.addWidget(l,1,0)
        self.textinputs = QLineEdit()
        self.grid.addWidget(self.textinputs, 1, 1)
        self.configbutton = QPushButton(text="Insert")
        self.grid.addWidget(self.configbutton, 2, 1, 2, 1)

        self.w.setLayout(self.grid)
        self.dialog.resize(self.w.sizeHint())
        self.dialog.setWindowTitle("YOU WIN")