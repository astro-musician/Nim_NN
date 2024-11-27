from src.nim_against_nn import nim_game_against_nn
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLCDNumber, 
    QMainWindow, 
    QVBoxLayout, 
    QWidget, 
    QApplication,
    QSpinBox,
    QPushButton
    )

class GameWindow(QMainWindow):

    def __init__(self,game):
        super().__init__()

        self.game = game

        self.layout = QVBoxLayout()

        self.starter = QPushButton()
        self.starter.clicked.connect(self.start)
        self.starter.setText("START")

        self.sticks_number = QLCDNumber()
        self.sticks_number.display(self.game.n_sticks)

        self.played_number = QSpinBox()
        self.played_number.setMinimum(1)
        self.played_number.setMaximum(self.game.n_max)
        self.played_number.valueChanged.connect(self.player_turn)
        
        self.layout.addWidget(self.starter)
        self.layout.addWidget(self.sticks_number)
        self.layout.addWidget(self.played_number)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

        pass

    def player_turn(self,n:int):
        self.game.player_turn(n)
        pass

    def start(self):

        self.starter.clicked.connect(self.game.reset)
        self.starter.setText("RESET")
        self.game.start()

        return

def run_game(game):

    nim_game = QApplication(sys.argv)
    window = GameWindow(game=game)
    window.show()
    nim_game.exec()
    # game.run_game()

    pass


