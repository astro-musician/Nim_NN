# Brouillon pour un jeu de nim

import numpy as np
from .training_NN import NN_nim_player, NN_training

class nim_game_against_nn:

    def __init__(self,NN_trained):

        """
        NN : double_layer_network from nn_utils, previously trained
        """

        self.NN = NN_trained.NN
        self.n_sticks = NN_trained.n_sticks
        self.n_max = NN_trained.n_max

        self.sticks = np.arange(self.n_sticks) + 1
        self.players = ['Player','NN']

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

        self.remove_sticks(n)

        if self.n_sticks > 0:
            self.state = "computer_playing"
        else:
            self.state = "finished"
            self.winner = "player"
        
        pass

    def computer_turn(self):

        n_proposed = self.NN.output(self.n_sticks)
        n_played = np.clip(n_proposed,a_min=1,a_max=len(self.sticks))
        self.remove_sticks(n_played)

        if self.n_sticks > 0:
            self.state = "player_playing"
        else:
            self.state = "finished"
            self.winner = "computer"

    def run_game(self):

        self.state = "computer_playing"

        while self.state != "finished":

            if self.state == "computer_playing":

                self.computer_turn()

            elif self.state == "player_playing":

                print(f"\n {self.n_sticks} sticks remaining. \n")
                n = input("Played number : ")

                while not self.n_is_suited(n):
                    print(f"Please choose an int between 1 and {self.n_max}.\n")
                    n = input("Played number : ")

                self.player_turn(int(n))

        print(f"Winner : {self.winner}")

        pass

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