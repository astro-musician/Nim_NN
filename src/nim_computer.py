# Brouillon pour un jeu de nim

import numpy as np

#-----------------------------------------

class nim_game_training:

    def __init__(self,NN,n_sticks=12,n_max=2,adversarial=False,NN_trainer=None):

        """
        NN : double_layer_network from nn_utils
        """

        self.NN = NN
        self.n_sticks = n_sticks
        self.n_max = n_max
        self.adversarial = adversarial
        self.NN_trainer = NN_trainer
        self.sticks = np.arange(n_sticks)
        self.players = ['trainer','NN']
        self.winner, self.loser, self.score = self.run_game()

        pass

    def remove_sticks(self,n):
        self.sticks = self.sticks[:-n]
        return

    def run_game(self):

        turn = 0
        score = 0

        while len(self.sticks) > 0:

            playing = self.players[turn%2]

            if playing == 'NN':
                n_proposed = self.NN.output(len(self.sticks))
                n_played = np.clip(n_proposed,a_min=1,a_max=len(self.sticks))
                self.remove_sticks(n_played)

            else:
                    
                n_proposed = np.random.choice(np.arange( 1, np.min(np.array([self.n_max,len(self.sticks)]))+1 ))
                n_played = np.clip(n_proposed,a_min=1,a_max=len(self.sticks))
                self.remove_sticks(n_played)

            turn += 1

        loser = self.players[turn%2]
        winner = self.players[(turn-1)%2]

        if winner=='NN':
            score += 1
        else:
            score -=1

        return [winner,loser,score]



