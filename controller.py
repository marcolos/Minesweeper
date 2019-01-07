import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from view import View
from model import Model


# CONTROLLER
class Minesweeper(QMainWindow):
    def __init__(self):
        super().__init__()

        # Instantiate a model.
        self._model = Model()

        # Instanzio una view
        self._view = View(self)  # Ho una _view alla quale ho passato un controller che a sua volta ha un _model

        # Connetto segnali delle caselline agli slot
        for x in range(0, self._model.b_size):
            for y in range(0, self._model.b_size):
                c = self._model.getCaselline()
                c[x][y].started.connect(self._model.trigger_start)
                c[x][y].expandable.connect(self._model.expand_reveal)
                c[x][y].finished.connect(self._model.game_over)

        self._model.statusUpdate.connect(self.statusUpdateView)
        self._view.button.pressed.connect(self._model.button_pressed)  # Connetto il bottone alla funzione button_pressed
        self._view._timer.timeout.connect(self.everysecond)

    # Aggiorna Timer ed Icona
    def statusUpdateView(self,status):
        #print(status)
        self._view.button.setIcon(QIcon(self._model.STATUS_ICONS[status]))
        if status == 0: # STATUS_READY
            self._model._counter = 0
            self._view.clock.setText("%03d" % self._model._counter)
        if status == 1: # STATUS_PLAYING
            self._view._timer.start(1000)
        if status == 2: #STATUS_FAILED
            self._view._timer.stop()

    def everysecond(self):
        self._model._counter = self._model._counter+1
        self._view.clock.setText("%03d" % self._model._counter)

app = QApplication(sys.argv)
window = Minesweeper()
window.show()
sys.exit(app.exec_())