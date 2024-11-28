from GUI.nim_against_nn_GUI import GameWindow, run_game
from src.nim import nim_game
from src.player import player
import pickle

with open("nn_saves/sticks8_trains100.pkl","rb") as f:
    computer_player = pickle.load(f)

game = nim_game(computer_player=computer_player)

run_game(game=game)