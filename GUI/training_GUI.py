import sys
import pickle
from src.player import player, train
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

        self.setFixedSize(QSize(500,500))
        self.setStyleSheet("font-size : 25px")
        self.setWindowTitle(self.text["window_title"])
        layout = QVBoxLayout()

        self.n_sticks = 4
        self.n_trains = 1

        self.n_sticks_label = QLabel(f"{self.text["n_sticks"]} : {self.n_sticks}")
        layout.addWidget(self.n_sticks_label)

        self.n_sticks_slider = QSlider(Qt.Orientation.Horizontal)
        self.n_sticks_slider.setMinimum(4)
        self.n_sticks_slider.setMaximum(12)
        self.n_sticks_slider.valueChanged.connect(self.n_sticks_select)
        layout.addWidget(self.n_sticks_slider)

        self.n_trains_label = QLabel(f"{self.text["n_trains"]} : {self.n_trains}")
        layout.addWidget(self.n_trains_label)

        self.n_trains_slider = QSlider(Qt.Orientation.Horizontal)
        self.n_trains_slider.setMinimum(1)
        self.n_trains_slider.setMaximum(200)
        self.n_trains_slider.valueChanged.connect(self.n_trains_select)
        layout.addWidget(self.n_trains_slider)

        self.run_training_button = QPushButton(self.text["run_training"])
        self.run_training_button.clicked.connect(self.run_training)
        layout.addWidget(self.run_training_button)

        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

    def n_sticks_select(self,n:int):
        self.n_sticks = n
        self.n_sticks_label.setText(f"{self.text["n_sticks"]} : {self.n_sticks}")
        return 
    
    def n_trains_select(self,n:int):
        self.n_trains = n
        self.n_trains_label.setText(f"{self.text["n_trains"]} : {self.n_trains}")
        return 
    
    def run_training(self):
        train(self.n_trains,n_sticks = self.n_sticks)
        return

def run_training():

    training_app = QApplication(sys.argv)
    window = TrainingWindow()
    window.show()
    training_app.exec()

    pass
    
    

        


