from src.nim_against_nn import nim_game_against_nn
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLCDNumber, QMainWindow, QVBoxLayout, QWidget, QApplication

class GameWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        sticks_number = QLCDNumber()
        sticks_number.display(str(4))
        layout.addWidget(sticks_number)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        pass

def run_game():

    nim_game = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    nim_game.exec()

    pass


