from GUI.nim_against_nn_GUI import GameWindow, run_game
from src.nim import nim_game
from src.player import player
from texts import francais, english
import pickle

# if __name__=="__main":

with open("nn_saves/sticks8_trains100_position_random_clever_training_False.pkl","rb") as f:
    computer_player = pickle.load(f)

game = nim_game(computer_player=computer_player)

run_game(game=game,language=francais)