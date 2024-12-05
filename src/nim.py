# Brouillon pour un jeu de nim

import numpy as np
from .player import player

class nim_game:

    def __init__(self, computer_player : player) :

        self.computer = computer_player
        self.n_sticks = self.computer.n_cups
        # self.state = "computer_playing"
        self.played_numbers = np.zeros(self.n_sticks)

        self.check = (self.computer.n_cups == self.n_sticks)

        if self.computer.position == "first":
            # self.players = ["computer","trainer"]
            self.state = "computer_playing"
        
        elif self.computer.position == "second":
            # self.players = ["trainer","computer"]
            self.state = "player_playing"

        elif self.computer.position == "random":
            self.state = ["computer_playing","player_playing"][np.intc(np.random.choice(np.array([0,1])))]

        if self.check:
            pass
        else:
            raise ValueError("Le nombre de verres et le nombre d'allumettes ne correspondent pas.")
        
        return

    def suited_play(self,n):

        if (n>=1) and (n<=2):
            return True
        
        else:
            return False

    def remove_sticks(self,n):
        self.n_sticks -= n
        return
    
    def computer_turn(self):

        played = self.computer.cups[self.n_sticks-1].play()
        self.remove_sticks(played)

        if self.n_sticks > 1:
            self.state = "player_playing"

        elif self.n_sticks == 1:
            self.state = "finished"
            self.winner = "player"

        else:
            self.state = "finished"
            self.winner = "computer"

        return 
    
    def player_turn(self,n):

        if self.state == "player_playing":
        
            if self.suited_play(n):
                self.remove_sticks(n)
            
            if self.n_sticks > 1:
                self.state = "computer_playing"

            elif self.n_sticks == 1:
                self.state = "finished"
                self.winner = "computer"

            else:
                self.state = "finished"
                self.winner = "player"

        return

    def run_turn(self) :

        print(self.state)

        if self.state == "init":
            self.state = "computer_playing"

        elif self.state == "computer_playing":
            self.computer_turn()

        elif self.state == "finished":
            print(f"Winner : {self.winner}")

        return
    
    def reset(self):

        self.n_sticks = self.computer.n_cups

        if self.computer.position == "first":
            # self.players = ["computer","trainer"]
            self.state = "computer_playing"
        
        elif self.computer.position == "second":
            # self.players = ["trainer","computer"]
            self.state = "player_playing"

        elif self.computer.position == "random":
            self.state = ["computer_playing","player_playing"][np.intc(np.random.choice(np.array([0,1])))]
            
        return