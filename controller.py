import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from view import MinesweeperView
from model import MinesweeperModel,Casellina
from custom_dialog import CustomDialog
from save_resume import Save,Resume
from leaderboard_dialog import LeaderboardDialog,InsertWinnerDialog
from leaderboard_model import LeaderboardModel

# LEVELS = (
#     [9,10],
#     [16,40],
#     [25,99]
# )

LEVELS = (
    [21, 2],
    [22, 3],
    [23,4]
)

# CONTROLLER
class Minesweeper(QMainWindow):
    def __init__(self):
        super().__init__()

        # Partita normale senza riesumare niente
        self.r = Resume()
        if self.r.A is None:

            # Instantiate a model.
            self._model = MinesweeperModel()

        # Riesumo la vecchia partita
        else:
            status,counter,n_caselline_open,size,n_mines = self.r.getValue()
            M = self.r.getMatrix()

            caselline = []
            tmp=[]
            for x in range(0, size):
                for y in range(0, size):
                    is_mine, adjacent_n, is_revealed, is_flagged = M[x][y].split()
                    is_mine = eval(is_mine)
                    adjacent_n = int(adjacent_n)
                    is_revealed = eval(is_revealed)
                    is_flagged = eval(is_flagged)
                    casellina = Casellina(x,y,is_mine = is_mine,adjacent_n = adjacent_n,is_revealed = is_revealed, is_flagged = is_flagged )
                    tmp.append(casellina)
                caselline.append(tmp)
                tmp = []

            # Instantiate a model.
            self._model = MinesweeperModel(M = caselline, STATUS = status,counter = counter,n_caselline_open = n_caselline_open,LEVEL=[size,n_mines])

        # Instantiate a view.
        self._view = MinesweeperView(self)

        # Instanzio la view del Custom.
        self._customDialog = CustomDialog()

        # Instanzio il modello della Leaderboard
        self._leaderboardModel = LeaderboardModel()
        # Instanzio la view, del Leaderboard.
        self._leaderboardDialog = LeaderboardDialog(self)
        # Instanzio la view, della Vittoria.
        self._insertWinner = InsertWinnerDialog()

        # Connetto tutti i segnali della partita normale più uno
        self.connectSignal()

        # Chiamo questa funzione per emettere il primo segnale
        self._model.update_status(self._model.status)


    def connectSignal(self):
        # Connetto segnali delle caselline agli slot
        for x in range(0, self._model.b_size):
            for y in range(0, self._model.b_size):
                c = self._model.getCaselline()
                c[x][y].started.connect(self._model.trigger_start)
                c[x][y].expandable.connect(self._model.expand_reveal)
                c[x][y].finished.connect(self._model.game_over)
                c[x][y].controlWin.connect(self._model.isWin)


        # Connetto il bottone della view (quello con l'emoticon) alla funzione button_pressed
        self._view.button.pressed.connect(self.button_pressed)

        # Connetto il timer alla everysecond
        self._view._timer.timeout.connect(self.everysecond)

        # La uso per notificare l'aggiornamento dello status del model. Quando lo status del model cambia viene lanciato il segnale statusUpdate, il quale chiama la statusUpdateView(slot)
        self._model.statusUpdate.connect(self.statusUpdateView)


        # Connetto le action del Menu bar
        self._view.action_Beginner.triggered.connect(self.on_configureBeginner)
        self._view.action_Intermediate.triggered.connect(self.on_configureIntermediate)
        self._view.action_Expert.triggered.connect(self.on_configureExpert)
        # Connetto il CustomDialog alla dialog.exec_ in modo da farlo eseguire quango premo nel Custom del Menu bar
        self._view.action_Custom.triggered.connect(self._customDialog.dialog.exec_)
        # Connetto il bottone della CustomDialog
        self._customDialog._configbutton.clicked.connect(self.on_configure)
        # Connetto la leaderboard alla dialog.exec_ in modo da farlo eseguire quango premo nel Leaderboard del Menu bar
        self._view.action_Leaderboard.triggered.connect(self._leaderboardDialog.dialog.exec_)
        # Connetto il bottone della insertWinner
        self._insertWinner._configbutton.clicked.connect(self.insertWinner)


    # Aggiorna Timer ed Icona
    def statusUpdateView(self,status):
        self._view.button.setIcon(QIcon(self._model.STATUS_ICONS[status]))
        if status == 0: # STATUS_READY
            self._model._counter = 0
            self._view.clock.setText("%03d" % self._model._counter)
        if status == 1: # STATUS_PLAYING
            self._view._timer.start(1000)
        if status == 2: #STATUS_FAILED
            self._view._timer.stop()
        if status == 3: #STATUS_SUCCESS
            self._view._timer.stop()
            if ([self._model.b_size,self._model.n_mines] == LEVELS[0] or LEVELS[1] or LEVELS[2]):
                if self._model.oldWin is False:
                    self._insertWinner.dialog.exec_()

    # Incrementa il timer
    def everysecond(self):
        self._model._counter = self._model._counter+1
        self._view.clock.setText("%03d" % self._model._counter)

    # Quando pigio il bottone del layout orizzontale
    def button_pressed(self):
        self._model._n_caselline_open = 0
        if self._model.status == MinesweeperModel.STATUS_PLAYING:
            self._model.update_status(MinesweeperModel.STATUS_FAILED)
            self._model.reveal_map()  # scopre le caselline

        elif self._model.status == MinesweeperModel.STATUS_FAILED or MinesweeperModel.STATUS_SUCCESS:
            self._model.update_status(MinesweeperModel.STATUS_READY)
            self._model.reset_map()  # resetta la mappa
            self._model.oldWin = False

    # Configurazione Custom
    def on_configure(self):
        try:
            size = int(self._customDialog._textinputs.text())
            n_bombs = int(self._customDialog._textinputs2.text())
            if(size<LEVELS[0][0]):
                size = LEVELS[0][0]
            if(size>50):
                size = 50
            if (n_bombs<1):
                n_bombs=1
            if (n_bombs>size*size):
                n_bombs = size*size -1
        except ValueError:
            size,n_bombs = LEVELS[0]

        self._model = MinesweeperModel(LEVEL=[size,n_bombs])
        self._view = MinesweeperView(self)
        self._customDialog = CustomDialog()
        self._leaderboardModel = LeaderboardModel()
        self._leaderboardDialog = LeaderboardDialog(self)
        self._insertWinner = InsertWinnerDialog()
        self.connectSignal()
        self.resize(self.sizeHint())

    # Configurazione Beginner
    def on_configureBeginner(self):
        size,n_bombs = LEVELS[0]
        self._model = MinesweeperModel(LEVEL=[size, n_bombs])
        self._view = MinesweeperView(self)
        self._customDialog = CustomDialog()
        self._leaderboardModel = LeaderboardModel()
        self._leaderboardDialog = LeaderboardDialog(self)
        self._insertWinner = InsertWinnerDialog()
        self.connectSignal()
        self.resize(self.sizeHint())

    # Configurazione Intermediate
    def on_configureIntermediate(self):
        size, n_bombs = LEVELS[1]
        self._model = MinesweeperModel(LEVEL=[size, n_bombs])
        self._view = MinesweeperView(self)
        self._customDialog = CustomDialog()
        self._leaderboardModel = LeaderboardModel()
        self._leaderboardDialog = LeaderboardDialog(self)
        self._insertWinner = InsertWinnerDialog()
        self.connectSignal()
        self.resize(self.sizeHint())

    # Configurazione Expert
    def on_configureExpert(self):
        size, n_bombs = LEVELS[2]
        self._model = MinesweeperModel(LEVEL=[size, n_bombs])
        self._view = MinesweeperView(self)
        self._customDialog = CustomDialog()
        self._leaderboardModel = LeaderboardModel()
        self._leaderboardDialog = LeaderboardDialog(self)
        self._insertWinner = InsertWinnerDialog()
        self.connectSignal()
        self.resize(self.sizeHint())

    # Salvataggio. Viene chiamata quando chiudo l'applicazione
    def closeEvent(self, event):
        save = Save(self)
        QMainWindow.closeEvent(self,event)

    # Inserimento vincitore nella Leaderboard
    def insertWinner(self):
        B,I,E = self._leaderboardModel.getFile()
        name = self._insertWinner._textinputs.text()
        time = str(self._model._counter)
        tmp = []
        tmp.append(name)
        tmp.append(time)

        if ([self._model.b_size, self._model.n_mines] == LEVELS[0]):
            B.append(tmp)
            B.sort(key=lambda x: int(x[1]))
            self._leaderboardModel.CSVwrite(B,'./sav/beginner_leaderboard.csv')
        if ([self._model.b_size, self._model.n_mines] == LEVELS[1]):
            I.append(tmp)
            I.sort(key=lambda x: int(x[1]))
            self._leaderboardModel.CSVwrite(I,'./sav/intermediate_leaderboard.csv')
        if ([self._model.b_size, self._model.n_mines] == LEVELS[2]):
            E.append(tmp)
            E.sort(key=lambda x: int(x[1]))
            self._leaderboardModel.CSVwrite(E,'./sav/expert_leaderboard.csv')

        self._insertWinner.dialog.reject()  # Chiudo la QDialog dell' insertWinner
        self._leaderboardDialog = LeaderboardDialog(self)  # Aggiorno la leaderboard ricreando l'oggetto
        self._view.action_Leaderboard.triggered.connect(self._leaderboardDialog.dialog.exec_) # connetto il segnale all'oggetto ricreato