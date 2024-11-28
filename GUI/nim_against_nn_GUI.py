from src.nim import nim_game
from texts import english, francais
import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QLCDNumber, 
    QMainWindow, 
    QVBoxLayout, 
    QWidget, 
    QApplication,
    QSpinBox,
    QPushButton,
    QLabel
    )

class GameWindow(QMainWindow):

    def __init__(self,game):
        super().__init__()

        self.text = francais.nim_game_GUI_text

        self.setFixedSize(QSize(500,500))
        self.setStyleSheet("font-size : 25px")
        self.setWindowTitle(self.text["window_title"])

        self.game = game
        self.total_sticks = game.n_sticks

        self.layout = QVBoxLayout()

        self.reset_button = QPushButton()
        self.reset_button.clicked.connect(self.reset)
        self.reset_button.setText(self.text['reset_button'])

        self.sticks_number_label = QLabel(f"{self.text["sticks"]} : ")

        self.sticks_number = QLCDNumber()
        self.sticks_number.display(self.game.n_sticks)

        self.current_player = QLabel()
        self.current_player.setText(f"{self.text["current_player"]} : {self.text["you"]}")
        self.current_player.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.played_number_box_label = QLabel()
        self.played_number_box_label.setText(self.text["n_played_label"])

        self.played_number_box = QSpinBox()
        self.played_number_box.setMinimum(1)
        self.played_number_box.setMaximum(2)
        self.played_number_box.valueChanged.connect(self.possible_played_number)
        self.played_number = 1

        self.validate_play_button = QPushButton()
        self.validate_play_button.setText(self.text["play_button"])
        self.validate_play_button.clicked.connect(self.player_turn)
        # self.validate_play_button.setEnabled(True)

        self.computer_play_button = QPushButton()
        self.computer_play_button.setText(self.text["computer_play_button"])
        self.computer_play_button.clicked.connect(self.computer_turn)
        # self.computer_play_button.setEnabled(False)
        
        self.layout.addWidget(self.reset_button)
        self.layout.addWidget(self.sticks_number_label)
        self.layout.addWidget(self.sticks_number)
        self.layout.addWidget(self.current_player)
        self.layout.addWidget(self.played_number_box_label)
        self.layout.addWidget(self.played_number_box)
        self.layout.addWidget(self.validate_play_button)
        self.layout.addWidget(self.computer_play_button)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)    

        # self.game.run_turn()

        print(self.game.state)

        if self.game.state == "player_playing":
            self.computer_play_button.setEnabled(False)

        elif self.game.state == "computer_playing":
            self.validate_play_button.setEnabled(False)
            self.played_number_box.setEnabled(False)

        return

    def deactivate_play_buttons(self):

        self.validate_play_button.setEnabled(False)
        self.played_number_box.setEnabled(False)
        self.computer_play_button.setEnabled(False)

        return
    
    def switch_player_to_computer(self):

        self.validate_play_button.setEnabled(False)
        self.played_number_box.setEnabled(False)
        self.computer_play_button.setEnabled(True)

        return
    
    def switch_computer_to_player(self):

        self.validate_play_button.setEnabled(True)
        self.played_number_box.setEnabled(True)
        self.computer_play_button.setEnabled(False)

        return
    
    def update_buttons(self):

        if self.game.state == "computer_playing":
            self.switch_player_to_computer()

        elif self.game.state == "player_playing":
            self.switch_computer_to_player()

        elif self.game.state == "finished":
            self.deactivate_play_buttons()

        return

    def possible_played_number(self,n:int):
        self.played_number = n
        return 

    def player_turn(self):

        self.game.player_turn(self.played_number)
        self.sticks_number.display(self.game.n_sticks)

        if self.game.state == "finished":
            self.current_player.setText(f"{self.text["winner"]} : {self.text[self.game.winner]}")

        elif self.game.state == "computer_playing":
            self.current_player.setText(f"{self.text["current_player"]} : {self.text["computer"]}")

        self.update_buttons()

        return
    
    def computer_turn(self):

        self.game.computer_turn()
        self.sticks_number.display(self.game.n_sticks)

        if self.game.state == "finished":
            self.current_player.setText(f"{self.text["winner"]} : {self.text[self.game.winner]}")

        elif self.game.state == "player_playing":
            self.current_player.setText(f"{self.text["current_player"]} : {self.text["you"]}")
        
        self.update_buttons()

        return
    
    def reset(self):

        self.game.reset()
        self.sticks_number.display(self.game.n_sticks)
        self.current_player.setText(f"{self.text["current_player"]} : {self.text["you"]}")
        self.update_buttons()

        return

def run_game(game):

    nim_game = QApplication(sys.argv)
    window = GameWindow(game=game)
    window.show()
    nim_game.exec()

    pass


