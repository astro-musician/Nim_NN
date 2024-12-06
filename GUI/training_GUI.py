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
    QCheckBox,
    QComboBox,
    QPushButton
)

class TrainingWindow(QMainWindow):

    def __init__(self,language):
        super().__init__()

        self.language = language
        self.text = self.language.training_NN_GUI_text

        self.setFixedSize(QSize(500,500))
        self.setStyleSheet("font-size : 20px")
        self.setWindowTitle(self.text["window_title"])
        layout = QVBoxLayout()

        self.n_sticks = 4
        self.n_trains = 1
        self.clever_training = False
        self.computer_position = "random"

        self.n_sticks_label = QLabel(f"{self.text["n_sticks"]} : {self.n_sticks}")
        layout.addWidget(self.n_sticks_label)

        self.n_sticks_slider = QSlider(Qt.Orientation.Horizontal)
        self.n_sticks_slider.setMinimum(4)
        self.n_sticks_slider.setMaximum(20)
        self.n_sticks_slider.valueChanged.connect(self.n_sticks_select)
        layout.addWidget(self.n_sticks_slider)

        self.n_trains_label = QLabel(f"{self.text["n_trains"]} : {self.n_trains}")
        layout.addWidget(self.n_trains_label)

        self.n_trains_slider = QSlider(Qt.Orientation.Horizontal)
        self.n_trains_slider.setMinimum(1)
        self.n_trains_slider.setMaximum(200)
        self.n_trains_slider.valueChanged.connect(self.n_trains_select)
        layout.addWidget(self.n_trains_slider)

        self.computer_position_label = QLabel(f"{self.text["computer_position"]}")
        layout.addWidget(self.computer_position_label)

        self.computer_position_box = QComboBox()
        self.computer_position_box.addItems([self.text["random"],self.text["first"],self.text["second"]])
        self.computer_position_box.currentIndexChanged.connect(self.computer_position_select)
        layout.addWidget(self.computer_position_box)

        self.clever_training_checkbox = QCheckBox(text=self.text["clever_training"])
        self.clever_training_checkbox.setCheckState(Qt.CheckState.Unchecked)
        self.clever_training_checkbox.stateChanged.connect(self.clever_training_select)
        layout.addWidget(self.clever_training_checkbox)

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
    
    def computer_position_select(self,i:int):
        self.computer_position = ["random","first","second"][i]
        return
    
    def clever_training_select(self,s:str):
        self.clever_training = (s == Qt.CheckState.Checked.value)
        return
    
    def run_training(self):
        train(self.n_trains, n_sticks=self.n_sticks, position=self.computer_position, clever_training=self.clever_training)
        return

def run_training(language):

    training_app = QApplication(sys.argv)
    window = TrainingWindow(language=language)
    window.show()
    training_app.exec()

    pass
    
    

        


