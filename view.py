from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

IMG_BOMB = QImage("./images/bomb.png")
IMG_FLAG = QImage("./images/flag.png")
IMG_START = QImage("./images/rocket.png")
IMG_CLOCK = QImage("./images/timer.png")


class MinesweeperView(object):
    def __init__(self,controller):
        w = QWidget()  # Definisco lo widget per inserirci dentro il layout
        hb = QHBoxLayout()  # Definisco un layout orizzontale

        # Creo la label contenente il n° di bombe (es. 40)
        self.mines = QLabel()
        self.mines.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # Creo la label contenente il tempo (inizialmente posto a 000)
        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # Setto il carattere delle label (font,size,weight)
        f = self.mines.font()  # La funz font() restituisce il font della label (dunque è il font di default della label)
        f.setPointSize(24)  # Setto la size a 24
        f.setWeight(75)  # Setto la larghezza a 75
        self.mines.setFont(f)  # Setto il font della label mines
        self.clock.setFont(f)  # Setto il fon della label clock

        # Creo il timer
        self._timer = QTimer()

        # Imposto il testo del n° di mine e del timer, rispettivamente a n_mines e a 000
        self.mines.setText("%03d" % controller.model.n_mines)
        self.clock.setText("%03d" % controller.model.counter)

        # Creo il bottone (all'inizio sarà una croce verde) e lo setto in dimensione ed icona
        self.button = QPushButton()
        self.button.setFixedSize(QSize(32, 32))
        self.button.setIconSize(QSize(32, 32))
        self.button.setIcon(QIcon("./images/smiley.png"))
        self.button.setFlat(True)

        # Creo una label l la quale sarà l'immagina della bomba sulla sinistra
        l = QLabel()
        l.setPixmap(QPixmap.fromImage(IMG_BOMB))
        l.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Aggiungo al layout orizzontale l,mines,button,clock
        hb.addWidget(l)
        hb.addWidget(self.mines)
        hb.addWidget(self.button)
        hb.addWidget(self.clock)

        # Aggiungo un altra label l quale sarà l'immagine dell'orologio sulla destra
        l = QLabel()
        l.setPixmap(QPixmap.fromImage(IMG_CLOCK))
        l.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        hb.addWidget(l)  # La vado ad aggiungere al layout orizz

        #  _______________________________________________
        # | immBomb | n°mines | button | clock | immClock |  -> hb
        #  –––––––––––––––––––––––––––––––––––––––––––––––

        # Creo un layout verticale
        vb = QVBoxLayout()
        vb.addLayout(hb)  # Ci aggiungo hb

        # Creo un layout a griglia
        self.grid = QGridLayout()
        self.grid.setSpacing(5)  # Imposto lo spazio tra le griglie

        caselline=controller.model.getCaselline()  # Matrice contente tutte le caselline
        for x in range(0, controller.model.getSize()):  # Scorriamo la matrice
            for y in range(0, controller.model.getSize()):
                self.grid.addWidget(caselline[x][y], x, y) # Aggiungiamo la caselline alla grid  ## FORSE INVERTIRE X-Y
                # Nell addWidget bisogna mettere prima y e poi x perchè questa funzione prende (QWidjet,row, column)
                # Facciamo quindi un inserimento per colonna (riempiamo prima tutta la 1° colonna e via di seguito)

        vb.addLayout(self.grid)  # Inserisco il layout a griglia dentro il layout verticale
        w.setLayout(vb)  # Metto il layout dentro al widget
        controller.setCentralWidget(w)  # Imposto il widget contenente il layout vert centrale

        #  _______________________________________________
        # | immBomb | n°mines | button | clock | immClock |  -> hb
        #  –––––––––––––––––––––––––––––––––––––––––––––––
        # |                                               |       -> vb
        # |                   GRID                        |
        # |_______________________________________________|

        # E' LA STATUS BAR (quella infondo alla pagina)
        # self.statusbar = QStatusBar(controller)
        # controller.setStatusBar(self.statusbar)

        # MENUBAR (è la barra)
        self.menuBar = QMenuBar(controller)
        self.menuBar.setGeometry(QRect(0, 0, 643, 22))
        self.menuBar.setDefaultUp(False)
        self.menuBar.setNativeMenuBar(False)

        # MENU GAME
        self.menu_Game = QMenu(self.menuBar)
        self.action_Beginner = QAction(controller)
        self.action_Intermediate = QAction(controller)
        self.action_Expert = QAction(controller)
        self.action_Custom = QAction(controller)
        self.menu_Game.addAction(self.action_Beginner)
        self.menu_Game.addAction(self.action_Intermediate)
        self.menu_Game.addAction(self.action_Expert)
        self.menu_Game.addAction(self.action_Custom)
        self.menu_Game.setTitle("&Game")
        self.action_Beginner.setText("&Beginner")
        self.action_Intermediate.setText("&Intermediate")
        self.action_Expert.setText("&Expert")
        self.action_Custom.setText("&Custom")
        self.menuBar.addAction(self.menu_Game.menuAction())

        # LEADERBOARD
        self.action_Leaderboard = QAction(controller)
        self.action_Leaderboard.setText("&Leaderboard")
        self.menuBar.addAction(self.action_Leaderboard)

        # MENU HELP
        self.menu_Help = QMenu(self.menuBar)
        self.action_About = QAction(controller)
        self.menu_Help.addAction(self.action_About)
        self.menu_Help.setTitle("&Help")
        self.action_About.setText("&About")
        self.menuBar.addAction(self.menu_Help.menuAction())


        controller.setMenuBar(self.menuBar)





