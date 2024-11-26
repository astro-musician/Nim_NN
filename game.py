import pickle
from GUI import nim_against_nn_GUI
from src.nim_against_nn import nim_game_against_nn
from src.training_NN import NN_nim_player
from src.nn_utils import *

with open("nn_saves/nim_nn_100_trains.pkl","rb") as f:
    NN_trained = pickle.load(f)

nim_game_against_nn(NN_trained).run_game()