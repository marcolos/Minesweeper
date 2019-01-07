from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import random
import time

IMG_BOMB = QImage("./images/bomb.png")
IMG_FLAG = QImage("./images/flag.png")
IMG_START = QImage("./images/rocket.png")
IMG_CLOCK = QImage("./images/clock-select.png")

NUM_COLORS = {
    1: QColor('#f44336'),
    2: QColor('#9C27B0'),
    3: QColor('#3F51B5'),
    4: QColor('#03A9F4'),
    5: QColor('#00BCD4'),
    6: QColor('#4CAF50'),
    7: QColor('#E91E63'),
    8: QColor('#FF9800')
}

LEVELS = [
    (8, 10),
    (16, 40),
    (24, 99)
]

STATUS_READY = 0
STATUS_PLAYING = 1
STATUS_FAILED = 2
STATUS_SUCCESS = 3


class Model(QObject):

    STATUS_ICONS = {
        STATUS_READY: "./images/smiley.png",
        STATUS_PLAYING: "./images/smiley.png",
        STATUS_FAILED: "./images/cross.png",
        STATUS_SUCCESS: "./images/smiley-lol.png",
    }

    statusUpdate = pyqtSignal(int)

    def __init__(self):
        super().__init__(parent=None)
        self.b_size, self.n_mines = LEVELS[1]  # Inizializzo n° caselle e n° bombe
        self._counter=0;
        self.caselline = []
        tmp =[]
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                casellina = Casellina(x,y)
                tmp.append(casellina)
            self.caselline.append(tmp)  # caselline sarà  caselline[x][y]
            tmp = []

        self.reset_map()  # Resetta e Reimposta gli attributi dei quadratini (aggiunge le bombe, i numerini e gli spazzi liberi alle caselline)
        self.update_status(STATUS_READY)  # Imposta lo stato a Ready (pronto per giocare, ma ancora non è stata effettuata nessuna mossa).

    def getCaselline(self):
        return self.caselline

    def reset_map(self):
        # Pulisce tutte le mine dai quadratini
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = self.caselline[x][y]
                w.reset() #Chiama la reset() della classe Quadratino

        #Aggiunge le mine ai quadratini
        positions = []
        while len(positions) < self.n_mines:
            x, y = random.randint(0, self.b_size - 1), random.randint(0, self.b_size - 1)
            if (x, y) not in positions:
                w = self.caselline[x][y]
                w.is_mine = True
                positions.append((x, y))

        #Funzione che viene utilizzata subito dopo. Conta il numero di bombe nell'intorno della casellina. Usa la funzione get_surrounding definita dopo
        def get_adjacency_n(x, y):
            positions = self.get_surrounding(x, y)
            n_mines = sum(1 if w.is_mine else 0 for w in positions)

            return n_mines

        #Aggiunge i numeri ai quadratini che hanno delle bombe accanto
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = self.caselline[x][y] #ritorna un Casellina
                w.adjacent_n = get_adjacency_n(x, y) #setto l'attibuto adjacent_n della classe Casellina. Sarebbe il n° di bombe accanto alla casella


    #Restituisce l'array positions il quale contiene tutte le Caselline intorno alla Casellina selezionata
    def get_surrounding(self, x, y):  #surrounding = circostante
        positions = []

        for xi in range(max(0, x - 1), min(x + 2, self.b_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.b_size)):
                positions.append(self.caselline[xi][yi])  ## FORSE INVERTIRE X-Y

        return positions


    #Quando pigio il bottone del layout orizzontale
    def button_pressed(self):
        if self.status == STATUS_PLAYING:
            self.update_status(STATUS_FAILED)
            self.reveal_map()  #scopre le caselline

        elif self.status == STATUS_FAILED:
            self.update_status(STATUS_READY)
            self.reset_map()  #resetta la mappa

    #Scopre tutte le caselline, rivelando dove erano situate bombe e numeri
    def reveal_map(self):
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = self.caselline[x][y]
                w.reveal()

    # Slot associato al signal started. Viene chiamato quando clicco su una casellina. Controlla che sia il primo click. Se è così fa partire il timer senno non fa niente
    def trigger_start(self, *args):
        if self.status != STATUS_PLAYING:
            # First click.
            self.update_status(STATUS_PLAYING)

    # Slot associato al signal expandable. Viene chiamato quando clicco su una casellina.
    def expand_reveal(self, x, y):
        for xi in range(max(0, x - 1), min(x + 2, self.b_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.b_size)):
                w = self.caselline[xi][yi]
                if not w.is_mine:
                    w.click()  # Se non è una mina chiama la click()

    # Slot associato al signal finished. Viene chiamato quando clicco su una casellina.
    def game_over(self):
        self.reveal_map()
        self.update_status(STATUS_FAILED)

    # Quando lo stato si aggiorna viene emesso il segnale statusUpdate, il quale è collagato alla statusUpdateView nel controllor
    # Serve per notificare al controllor che lo stato è cambiato, in modo che il controllor possa far partire il timer alla view e cambiare icona a seconda dello stato
    def update_status(self, status):
        self.status = status
        self.statusUpdate.emit(self.status)




# Classe per creare le caselline nelle quali possono esserci numeri o bombe
class Casellina(QWidget):
    # Questi 3 segnali verrano utilizzati quando cliccheremo su una casellina
        # expandable: è un signal collegato allo slot expand_reveal, il quale espande le caselline vuote. Viene emesso dalla click()
        # started: è un signal collegato allo slot trigger_start, il quale controlla se è stata la prima mossa
        # finished: è un signal collegato allo slot game_over, il quale rileva tutta la mappa e aggiorna lo stato a STATUS_FAILED

    expandable = pyqtSignal(int,int)  # creo un oggetto di tipo pyqtSignal al quale vengono passati due int al costruttore
    started = pyqtSignal()  # creo un oggetto di tipo pyqtSignal
    finished = pyqtSignal()  # creo un oggetto di tipo pyqtSignal

    def __init__(self, x, y, *args, **kwargs):
        super(Casellina, self).__init__(*args, **kwargs)

        self.setFixedSize(QSize(20, 20))

        self.x = x
        self.y = y


    def reset(self):
        self.is_start = False
        self.is_mine = False  # Indica se in questa casellina c'è una mina o no
        self.adjacent_n = 0  # Indica il numero di mine adiacenti a questa casellina

        self.is_revealed = False
        self.is_flagged = False

        self.update()


    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        r = event.rect()

        if self.is_revealed:
            color = self.palette().color(QPalette.Background)
            outer, inner = color, color
        else:
            outer, inner = Qt.gray, Qt.lightGray  # Se non è rivelata assegna a outer = il colore grigio, ed a inner il colore grigio chiaro

        p.fillRect(r, QBrush(inner))
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        if self.is_revealed:
            if self.is_start:  # Se è l'inizio disegna il razzo
                p.drawPixmap(r, QPixmap(IMG_START))

            elif self.is_mine:  # Se è una bomba disegna la bomba
                p.drawPixmap(r, QPixmap(IMG_BOMB))

            elif self.adjacent_n > 0:  # Se adjacent è > 0 disegna il numerino
                pen = QPen(NUM_COLORS[self.adjacent_n])
                p.setPen(pen)
                f = p.font()
                f.setBold(True)
                p.setFont(f)
                p.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, str(self.adjacent_n))

        elif self.is_flagged:  # Se è flaggato disegna in flag
            p.drawPixmap(r, QPixmap(IMG_FLAG))


    def flag(self):
        self.is_flagged = True
        self.update()

        self.started.emit()  # esegue la trigger_start, la quale controlla se è stata la prima mossa


    def reveal(self):
        self.is_revealed = True
        self.update()


    def click(self):   # Viene chiamata appena premo su una casellina con il sinistro (Vedere la mouseReleaseEvent)
        if not self.is_revealed:
            self.reveal()
            if self.adjacent_n == 0:
                self.expandable.emit(self.x, self.y)  # Quando la casellina è vuota la espando(scopro anche quelle accanto finche non trovo numeri o bombe)

        self.started.emit()  # esegue la trigger_start, la quale controlla se è stata la prima mossa


    def mouseReleaseEvent(self, e):  # Da qui parte tutta la parte di premere sulle caselline

        if (e.button() == Qt.RightButton and not self.is_revealed):
            self.flag()  # Chiamo la flag() quando premo con il destro

        elif (e.button() == Qt.LeftButton):
            self.click()  # Chiamo la click() quando prmo con il sinistro

            if self.is_mine:  # Se nella casellina c'è la mina emetto il segnale di fine
                self.finished.emit()  # esegue la game_over

