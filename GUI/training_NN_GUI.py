import sys
import pickle
from src.training_NN import NN_training, NN_nim_player
from src.nn_utils import backpropagation_MH_step
from texts import english, francais
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QSlider,
    QLineEdit,
    QProgressBar,
    QPushButton
)

class TrainingWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.text = francais.training_NN_GUI_text

        self.setFixedSize(QSize(1000,500))
        self.setStyleSheet("font-size : 25px")
        self.setWindowTitle(self.text["window_title"])
        layout = QVBoxLayout()

        self.n_sticks = 10
        self.n_max = 2
        self.n_trains = 10
        self.games_per_step = 10

        self.n_sticks_label = QLabel(f"{self.text["n_sticks"]} : {self.n_sticks}")
        layout.addWidget(self.n_sticks_label)

        self.n_sticks_slider = QSlider(Qt.Orientation.Horizontal)
        self.n_sticks_slider.setMinimum(10)
        self.n_sticks_slider.setMaximum(30)
        self.n_sticks_slider.valueChanged.connect(self.n_sticks_select)
        layout.addWidget(self.n_sticks_slider)

        self.n_max_label = QLabel(f"{self.text["n_max"]} : {self.n_max}")
        layout.addWidget(self.n_max_label)

        self.n_max_slider = QSlider(Qt.Orientation.Horizontal)
        self.n_max_slider.setMinimum(2)
        self.n_max_slider.setMaximum(5)
        self.n_max_slider.valueChanged.connect(self.n_max_select)
        layout.addWidget(self.n_max_slider)

        self.n_trains_label = QLabel(f"{self.text["n_trains"]} : {self.n_trains}")
        layout.addWidget(self.n_trains_label)

        self.n_trains_slider = QSlider(Qt.Orientation.Horizontal)
        self.n_trains_slider.setMinimum(10)
        self.n_trains_slider.setMaximum(1000)
        self.n_trains_slider.valueChanged.connect(self.n_trains_select)
        layout.addWidget(self.n_trains_slider)

        self.games_per_step_label = QLabel(f"{self.text["games_per_step"]} : {self.games_per_step}")
        layout.addWidget(self.games_per_step_label)

        self.games_per_step_slider = QSlider(Qt.Orientation.Horizontal)
        self.games_per_step_slider.setMinimum(1)
        self.games_per_step_slider.setMaximum(1000)
        self.games_per_step_slider.valueChanged.connect(self.games_per_step_select)
        layout.addWidget(self.games_per_step_slider)

        self.run_training_button = QPushButton(self.text["run_training"])
        self.run_training_button.clicked.connect(self.run_training)
        # self.run_training_button.setEnabled(False)
        layout.addWidget(self.run_training_button)

        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

    def n_sticks_select(self,n:int):
        self.n_sticks = n
        self.n_sticks_label.setText(f"{self.text["n_sticks"]} : {self.n_sticks}")
        return 
        
    def n_max_select(self,n:int):
        self.n_max = n
        self.n_max_label.setText(f"{self.text["n_max"]} : {self.n_max}")
        return 
    
    def n_trains_select(self,n:int):
        self.n_trains = n
        self.n_trains_label.setText(f"{self.text["n_trains"]} : {self.n_trains}")
        return 
    
    def games_per_step_select(self,n:int):
        self.games_per_step = n
        self.games_per_step_label.setText(f"{self.text["games_per_step"]} : {self.games_per_step}")
        return 
    
    def run_training(self):
        NN_training(n_sticks=self.n_sticks,n_max=self.n_max,n_trains=self.n_trains,games_per_step=self.games_per_step).train()
        return

def show_training():

    training_app = QApplication(sys.argv)
    window = TrainingWindow()
    window.show()
    training_app.exec()

    pass
    
    

        


