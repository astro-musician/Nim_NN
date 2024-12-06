import sys
import pickle
from src.player import player, train
from src.nim import nim_game
from .nim_against_nn_GUI import run_game, GameWindow
from texts import english, francais
from pathlib import Path
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QSlider,
    QLineEdit,
    QProgressBar,
    QCheckBox,
    QComboBox,
    QPushButton
)

class TrainingWindow(QMainWindow):

    def __init__(self,language):
        super().__init__()

        self.language = language
        self.text = self.language.training_NN_GUI_text

        self.setFixedSize(QSize(800,500))
        self.setStyleSheet("font-size : 20px")
        self.setWindowTitle(self.text["window_title"])
        self.layout = QGridLayout()

        self.n_sticks = 4
        self.n_trains = 1
        self.clever_training = False
        self.computer_position = "random"

        self.n_sticks_label = QLabel(f"{self.text["n_sticks"]} : {self.n_sticks}")
        self.layout.addWidget(self.n_sticks_label,1,1)

        self.n_sticks_slider = QSlider(Qt.Orientation.Horizontal)
        self.n_sticks_slider.setMinimum(4)
        self.n_sticks_slider.setMaximum(20)
        self.n_sticks_slider.valueChanged.connect(self.n_sticks_select)
        self.layout.addWidget(self.n_sticks_slider,1,2)

        self.n_trains_label = QLabel(f"{self.text["n_trains"]} : {self.n_trains}")
        self.layout.addWidget(self.n_trains_label,2,1)

        self.n_trains_slider = QSlider(Qt.Orientation.Horizontal)
        self.n_trains_slider.setMinimum(1)
        self.n_trains_slider.setMaximum(200)
        self.n_trains_slider.valueChanged.connect(self.n_trains_select)
        self.layout.addWidget(self.n_trains_slider,2,2)

        self.computer_position_label = QLabel(f"{self.text["computer_position"]}")
        self.layout.addWidget(self.computer_position_label,3,1)

        self.computer_position_box = QComboBox()
        self.computer_position_box.addItems([self.text["random"],self.text["first"],self.text["second"]])
        self.computer_position_box.currentIndexChanged.connect(self.computer_position_select)
        self.layout.addWidget(self.computer_position_box,3,2)

        self.clever_training_checkbox = QCheckBox(text=self.text["clever_training"])
        self.clever_training_checkbox.setCheckState(Qt.CheckState.Unchecked)
        self.clever_training_checkbox.stateChanged.connect(self.clever_training_select)
        self.layout.addWidget(self.clever_training_checkbox,4,2)

        self.showstats_button = QPushButton(text=self.text["showstats"])
        self.showstats_button.clicked.connect(self.showstats)
        self.layout.addWidget(self.showstats_button,5,2)

        self.run_training_button = QPushButton(self.text["run_training"])
        self.run_training_button.clicked.connect(self.run_training)
        self.layout.addWidget(self.run_training_button,5,1)

        self.run_game_button = QPushButton(self.text["run_game"])
        self.run_game_button.clicked.connect(self.run_game)
        self.layout.addWidget(self.run_game_button,6,1)

        self.game_window = None
        self.statswindow = None

        self.update_train_game_buttons()

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def n_sticks_select(self,n:int):
        self.n_sticks = n
        self.n_sticks_label.setText(f"{self.text["n_sticks"]} : {self.n_sticks}")
        self.update_train_game_buttons()
        return 
    
    def n_trains_select(self,n:int):
        self.n_trains = n
        self.n_trains_label.setText(f"{self.text["n_trains"]} : {self.n_trains}")
        self.update_train_game_buttons()
        return 
    
    def computer_position_select(self,i:int):
        self.computer_position = ["random","first","second"][i]
        self.update_train_game_buttons()
        return
    
    def clever_training_select(self,s:str):
        self.clever_training = (s == Qt.CheckState.Checked.value)
        self.update_train_game_buttons()
        return
    
    def nn_savefile(self) -> str:
        return f"nn_saves/sticks{self.n_sticks}_trains{self.n_trains}_position_{self.computer_position}_clever_training_{self.clever_training}.pkl"
    
    def nn_statsfile(self) -> str:
        return f"nn_saves/sticks{self.n_sticks}_trains{self.n_trains}_position_{self.computer_position}_clever_training_{self.clever_training}.png"

    def update_train_game_buttons(self):

        if Path(self.nn_savefile()).is_file():

            self.run_game_button.setEnabled(True)
            self.run_training_button.setText(self.text["train_again"])

        else:

            self.run_game_button.setEnabled(False)
            self.run_training_button.setText(self.text["run_training"])

        if Path(self.nn_statsfile()).is_file():

            self.showstats_button.setEnabled(True)

        else:

            self.showstats_button.setEnabled(False)

        pass

    def showstats(self):

        if self.statswindow == None:
            self.statswindow = StatsWindow(imagefile=self.nn_statsfile())

        self.statswindow.show()

        pass

    def run_training(self):
        train(self.n_trains, n_sticks=self.n_sticks, position=self.computer_position, clever_training=self.clever_training)
        self.update_train_game_buttons()
        return
    
    def run_game(self):

        try:

            with open(self.nn_savefile(),"rb") as f:
                computer_player = pickle.load(f)

            self.game = nim_game(computer_player=computer_player)

            if self.game_window == None:
                self.game_window = GameWindow(game=self.game,language=self.language)

            self.game_window.show()

        except FileNotFoundError:

            print(f"No computer was trained with these parameters.")
            self.update_train_game_buttons()

        pass

class StatsWindow(QMainWindow):

    def __init__(self,imagefile):
        super().__init__()

        self.layout = QGridLayout()

        self.label = QLabel("test")
        self.imagefile = imagefile
        self.image = QPixmap(self.imagefile)
        self.label.setPixmap(self.image)
        self.layout.addWidget(self.label,1,1)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        pass

def run_training(language):

    training_app = QApplication(sys.argv)
    window = TrainingWindow(language=language)
    window.show()
    training_app.exec()

    pass
    
    

        


