import sys
from PyQt5.QtWidgets import QApplication
from controller import Minesweeper


app = QApplication(sys.argv)
window = Minesweeper()
window.show()
sys.exit(app.exec_())