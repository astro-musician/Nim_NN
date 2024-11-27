# Brouillon pour un jeu de nim

import numpy as np
import time
from .training_NN import NN_nim_player, NN_training

class nim_game_against_nn:

    def __init__(self,NN_trained):

        """
        NN_trained.NN : double_layer_network from nn_utils, previously trained
        """

        self.NN_nim_player = NN_trained
        self.NN = NN_trained.NN
        self.n_sticks = NN_trained.n_sticks
        self.n_max = NN_trained.n_max
        self.state = "init"

        pass

    def remove_sticks(self,n):
        self.n_sticks -= n
        return
    
    def n_is_suited(self,n: any) -> bool:
        '''
        Vérifie que le coup est permis.
        '''
        try:
            n=int(n)
            return (n>=1) and (n<=self.n_max)
        except ValueError:
            return False
        
    def player_turn(self,n):

        if self.state == "player_playing":

            self.remove_sticks(n)

            if self.n_sticks > 0:

                self.state = "computer_playing"
                self.run_turn()

            else:

                self.state = "finished"
                self.winner = "player"
                self.run_turn()
        
        return

    def computer_turn(self):

        if self.state == "computer_playing":

            time.sleep(1)

            n_proposed = self.NN.output(self.n_sticks)
            n_played = np.clip(n_proposed,a_min=1,a_max=self.n_sticks)
            self.remove_sticks(n_played)

            if self.n_sticks > 0:

                self.state = "player_playing"
                self.run_turn()

            else:
                self.state = "finished"
                self.winner = "computer"
                self.run_turn()

            print(f"\n Computer played and removed {n_played} sticks.")

        return

    def reset(self):

        self.state = "init"
        self.n_sticks = self.NN_nim_player.n_sticks

        return
    
    def start(self):

        self.state = "computer_playing"
        self.run_turn()

        return

    def run_turn(self):

        if self.state == "init":

            self.state = "computer_playing"

        elif self.state == "computer_playing":

                    self.computer_turn()

        elif self.state == "finished":

            print(f"Winner : {self.winner}")

        return

    # def run_game_old(self):

    #     turn = 0

    #     print("C'est parti !")
    #     print(self.sticks)

    #     while len(self.sticks) > 0:

    #         playing = self.players[turn%2]

    #         if playing=='NN': # Neural Network turn
    #             print("Ordinateur :")
    #             n_proposed = self.NN.output(len(self.sticks))
    #             n_played = np.clip(n_proposed,a_min=1,a_max=len(self.sticks))
    #             self.remove_sticks(n_played)
    #             print(self.sticks)

    #         else: # Player turn
    #             print("Joueur")
    #             n = input("Nombre d'allumettes à retirer : ")

    #             while not self.n_is_suited(n):
    #                 print("Veuillez choisir un nombre entre 1 et "+str(self.n_max))
    #                 n = input("Nombre d'allumettes à retirer : ")

    #             n_played = int(n)
    #             self.remove_sticks(n_played)
    #             print(self.sticks)

    #         turn += 1

    #     winner = self.players[(turn-1)%2]

    #     if winner=="Player":
    #         print("Gagné !")
    #     else:
    #         print("Perdu !")

    #     return 