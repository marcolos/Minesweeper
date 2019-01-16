import sys
from PyQt5.QtWidgets import QApplication
from Minesweeper.controller import Minesweeper


sys.setrecursionlimit(15000)
app = QApplication(sys.argv)
window = Minesweeper()
window.show()
sys.exit(app.exec_())