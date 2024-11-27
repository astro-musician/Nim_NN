import pickle
from GUI.nim_against_nn_GUI import GameWindow, run_game
from src.nim_against_nn import nim_game_against_nn

with open("nn_saves/nim_nn_100_trains.pkl","rb") as f:
    NN_trained = pickle.load(f)

game = nim_game_against_nn(NN_trained)

run_game(game=game)

