import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from view import MinesweeperView
from model import MinesweeperModel
from custom_dialog import CustomDialog
from save_resume import Save,Resume
from leaderboard_dialog import LeaderboardDialog,InsertWinnerDialog
from leaderboard_model import LeaderboardModel

LEVELS = (
    [9,10],
    [16,40],
    [25,99]
)

# PER TESTING
# LEVELS = (
#     [21, 2],
#     [22, 3],
#     [23,4]
# )


# CONTROLLER
class Minesweeper(QMainWindow):
    def __init__(self):
        super().__init__()

        # Partita normale senza riesumare niente
        self.r = Resume()
        if self.r.A is None:

            # Instantiate a model.
            self.model = MinesweeperModel()

        # Riesumo la vecchia partita
        else:
            status,counter,n_caselline_open,size,n_mines,n_caselline_flagged = self.r.getValue()
            M = self.r.getMatrix()

            # Instantiate a model.
            self.model = MinesweeperModel(M = M, STATUS = status,counter = counter,n_caselline_open = n_caselline_open,LEVEL=[size,n_mines], n_caselline_flagged = n_caselline_flagged)


        # Instantiate a view.
        self.view = MinesweeperView(self)

        # Instanzio la view del Custom.
        self.customDialog = CustomDialog()

        # Instanzio il modello della Leaderboard
        self.leaderboardModel = LeaderboardModel()
        # Instanzio la view, del Leaderboard.
        self.leaderboardDialog = LeaderboardDialog(self)
        # Instanzio la view, della Vittoria.
        self.insertWinner = InsertWinnerDialog()

        # Connetto tutti i segnali della partita normale
        self.connectSignal()

        self.resize(self.sizeHint())

        # Chiamo questa funzione per emettere il primo segnale
        self.model.update_status(self.model.status)
        self.model.isFlagged(0)


    def connectSignal(self):
        # Connetto segnali delle caselline agli slot
        for x in range(0, self.model.b_size):
            for y in range(0, self.model.b_size):
                c = self.model.getCaselline()
                c[x][y].started.connect(self.model.trigger_start)
                c[x][y].expandable.connect(self.model.expand_reveal)
                c[x][y].finished.connect(self.model.game_over)
                c[x][y].controlWin.connect(self.model.isWin)
                c[x][y].controlFlag.connect(self.model.isFlagged)

        self.model.notifyFlagged.connect(self.updateViewFlag)

        # Connetto il bottone della view (quello con l'emoticon) alla funzione button_pressed
        self.view.button.pressed.connect(self.model.button_pressed)

        # Connetto il timer alla everysecond
        self.view._timer.timeout.connect(self.everysecond)

        # La uso per notificare l'aggiornamento dello status del model. Quando lo status del model cambia viene lanciato il segnale statusUpdate, il quale chiama la statusUpdateView(slot)
        self.model.statusUpdate.connect(self.statusUpdateView)

        # Connetto le action del Menu bar
        self.view.action_Beginner.triggered.connect(self.on_configureBeginner)
        self.view.action_Intermediate.triggered.connect(self.on_configureIntermediate)
        self.view.action_Expert.triggered.connect(self.on_configureExpert)
        # Connetto il CustomDialog alla dialog.exec_ in modo da farlo eseguire quango premo nel Custom del Menu bar
        self.view.action_Custom.triggered.connect(self.customDialog.dialog.exec_)
        # Connetto il bottone della CustomDialog
        self.customDialog.configbutton.clicked.connect(self.on_configure)
        # Connetto la leaderboard alla dialog.exec_ in modo da farlo eseguire quango premo nel Leaderboard del Menu bar
        self.view.action_Leaderboard.triggered.connect(self.leaderboardDialog.dialog.exec_)
        # Connetto il bottone della insertWinner
        self.insertWinner.configbutton.clicked.connect(self.insert_winner)


    # Aggiorna Timer ed Icona
    def statusUpdateView(self,status):
        self.view.button.setIcon(QIcon(self.model.STATUS_ICONS[status]))
        if status == 0: # STATUS_READY
            self.model.counter = 0
            self.view.clock.setText("%03d" % self.model.counter)
        if status == 1: # STATUS_PLAYING
            self.view._timer.start(1000)
        if status == 2: #STATUS_FAILED
            self.view._timer.stop()
        if status == 3: #STATUS_SUCCESS
            self.view._timer.stop()
            if ([self.model.b_size,self.model.n_mines] == LEVELS[0] or LEVELS[1] or LEVELS[2]):
                if self.model.oldWin is False:
                    self.insertWinner.dialog.exec_()

    # Slot incremento timer
    def everysecond(self):
        self.model.counter = self.model.counter+1
        self.view.clock.setText("%03d" % self.model.counter)

    # Slot aggiornamento n°bombe - n°caselline flaggate
    def updateViewFlag(self):
        self.view.mines.setText("%03d" % (self.model.n_mines - self.model.n_caselline_flagged))

    # Slot configurazione Custom
    def on_configure(self):
        try:
            size = int(self.customDialog.textinputs.text())
            n_bombs = int(self.customDialog.textinputs2.text())
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

        self.model = MinesweeperModel(LEVEL=[size,n_bombs])
        self.view = MinesweeperView(self)
        self.customDialog = CustomDialog()
        self.leaderboardModel = LeaderboardModel()
        self.leaderboardDialog = LeaderboardDialog(self)
        self.insertWinner = InsertWinnerDialog()
        self.connectSignal()
        self.resize(self.sizeHint())

    # Configurazione Beginner
    def on_configureBeginner(self):
        size,n_bombs = LEVELS[0]
        self.model = MinesweeperModel(LEVEL=[size, n_bombs])
        self.view = MinesweeperView(self)
        self.customDialog = CustomDialog()
        self.leaderboardModel = LeaderboardModel()
        self.leaderboardDialog = LeaderboardDialog(self)
        self.insertWinner = InsertWinnerDialog()
        self.connectSignal()
        self.resize(self.sizeHint())

    # Configurazione Intermediate
    def on_configureIntermediate(self):
        size, n_bombs = LEVELS[1]
        self.model = MinesweeperModel(LEVEL=[size, n_bombs])
        self.view = MinesweeperView(self)
        self.customDialog = CustomDialog()
        self.leaderboardModel = LeaderboardModel()
        self.leaderboardDialog = LeaderboardDialog(self)
        self.insertWinner = InsertWinnerDialog()
        self.connectSignal()
        self.resize(self.sizeHint())

    # Configurazione Expert
    def on_configureExpert(self):
        size, n_bombs = LEVELS[2]
        self.model = MinesweeperModel(LEVEL=[size, n_bombs])
        self.view = MinesweeperView(self)
        self.customDialog = CustomDialog()
        self.leaderboardModel = LeaderboardModel()
        self.leaderboardDialog = LeaderboardDialog(self)
        self.insertWinner = InsertWinnerDialog()
        self.connectSignal()
        self.resize(self.sizeHint())

    # Salvataggio. Viene chiamata quando chiudo l'applicazione
    def closeEvent(self, event):
        save = Save(self)
        QMainWindow.closeEvent(self,event)

    # Inserimento vincitore nella Leaderboard
    def insert_winner(self):
        B,I,E = self.leaderboardModel.getFile()
        name = self.insertWinner.textinputs.text()
        time = str(self.model.counter)
        tmp = []
        tmp.append(name)
        tmp.append(time)

        if ([self.model.b_size, self.model.n_mines] == LEVELS[0]):
            B.append(tmp)
            B.sort(key=lambda x: int(x[1]))
            self.leaderboardModel.CSVwrite(B,'./sav/beginner_leaderboard.csv')
        if ([self.model.b_size, self.model.n_mines] == LEVELS[1]):
            I.append(tmp)
            I.sort(key=lambda x: int(x[1]))
            self.leaderboardModel.CSVwrite(I,'./sav/intermediate_leaderboard.csv')
        if ([self.model.b_size, self.model.n_mines] == LEVELS[2]):
            E.append(tmp)
            E.sort(key=lambda x: int(x[1]))
            self.leaderboardModel.CSVwrite(E,'./sav/expert_leaderboard.csv')

        self.insertWinner.dialog.reject()  # Chiudo la QDialog dell' insertWinner
        self.leaderboardDialog = LeaderboardDialog(self)  # Aggiorno la leaderboard ricreando l'oggetto
        self.view.action_Leaderboard.triggered.connect(self.leaderboardDialog.dialog.exec_) # connetto il segnale all'oggetto ricreato