import numpy as np
import matplotlib.pyplot as plt
import progressbar
import pickle
import time
from copy import deepcopy

class cup:

    def __init__(self,blue=2,yellow=2):

        self.blue = blue
        self.yellow = yellow

        return

    def play(self):

        weight_blue = self.blue/(self.blue+self.yellow)
        weight_yellow = self.yellow/(self.blue+self.yellow)
        n_played = np.random.choice(np.array([1,2]),p=np.array([weight_blue,weight_yellow]))

        return n_played
    
    def reset(self):

        self.blue = 2
        self.yellow = 2

        return
    
class player:

    def __init__(self,n_cups=8,position="first"):

        self.position = position
        self.n_cups = n_cups
        self.cups = []
        for n in range(self.n_cups):
            self.cups.append(cup())

        pass

class game:

    def __init__(self, computer_player : player, n_sticks=8, clever_training=False ) :

        self.n_sticks = n_sticks
        self.computer = deepcopy(computer_player)
        self.computer_position = computer_player.position
        self.played_numbers = np.zeros(self.n_sticks)
        self.clever_training = clever_training

        if self.computer_position == "first":
            # self.players = ["computer","trainer"]
            self.state = "computer_playing"
        
        elif self.computer_position == "second":
            # self.players = ["trainer","computer"]
            self.state = "trainer_playing"

        elif self.computer_position == "random":
            self.state = ["computer_playing","trainer_playing"][np.intc(np.random.choice(np.array([0,1])))]

        self.check = (self.computer.n_cups == self.n_sticks)

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
    
    def trainer_turn(self):
        played = np.random.choice(np.array([1,2]))
        # print(f"\n Trainer : {played} \n")
        self.remove_sticks(played)

        if self.n_sticks > 1:
            self.state = "computer_playing"

        elif self.n_sticks == 1:
            self.state = "finished"
            self.winner = "computer"

        else:
            self.state = "finished"
            self.winner = "trainer"

        return played
    
    def clever_trainer_turn(self):

        if self.n_sticks%3 !=0 :
            # played = self.n_sticks%3
            best_play = self.n_sticks%3
            possible_plays = np.concatenate((np.array([best_play]),np.arange(1,3)[np.arange(1,3)!=best_play]))
            played = np.random.choice(possible_plays,p=np.array([0.9,0.1])) # The trainer must be able to make a mistake, otherwise winrate == 0
        else:
            played = np.random.choice(np.array([1,2]))

        self.remove_sticks(played)

        if self.n_sticks > 1:
            self.state = "computer_playing"

        elif self.n_sticks == 1:
            self.state = "finished"
            self.winner = "computer"

        else:
            self.state = "finished"
            self.winner = "trainer"

        return played
    
    def computer_turn(self):
        played = self.computer.cups[self.n_sticks-1].play()
        # print(f"\n Computer : {played}")
        self.remove_sticks(played)

        if self.n_sticks > 1:
            self.state = "trainer_playing"

        elif self.n_sticks == 1:
            self.state = "finished"
            self.winner = "trainer"

        else:
            self.state = "finished"
            self.winner = "computer"

        return played

    def play_game(self) -> list[player,str]:

        # turn = 0

        while self.state != "finished":

            # current_player = self.players[turn%2]

            if self.state == "trainer_playing":
                if self.clever_training:
                    n_played = self.clever_trainer_turn()
                else:
                    n_played = self.trainer_turn()

            elif self.state == "computer_playing":
                n_played = self.computer_turn()
                self.played_numbers[self.n_sticks-1+n_played] = n_played # The update needs to be made at the state before the computer played

            if not self.suited_play(n_played):
                raise ValueError("CHEATER")

            # self.remove_sticks(n_played)

            # turn += 1

        # winner = self.players[(turn-1)%2]
        new_computer = self.computer
        self.played_numbers = np.intc(self.played_numbers)

        if self.winner == "computer":

            for i in range(len(self.played_numbers)):

                if self.played_numbers[i] == 1:
                    new_computer.cups[i].blue += 1

                elif self.played_numbers[i] == 2:
                    new_computer.cups[i].yellow += 1

        else:

            for i in range(len(self.played_numbers)):

                if self.played_numbers[i] == 1:
                    if new_computer.cups[i].blue > 0:
                        new_computer.cups[i].blue -= 1

                elif self.played_numbers[i] == 2:
                    if new_computer.cups[i].yellow > 0:
                        new_computer.cups[i].yellow -= 1

                else:
                    None

                if new_computer.cups[i].blue + new_computer.cups[i].yellow == 0:
                    new_computer.cups[i].reset()

        return [new_computer,self.winner]
    
    
def train(n_trains:int, n_sticks:int, position = "first", clever_training=False, show_progressbar=True, saveplayer=True) -> list[player,float]:

    training_player = player(n_cups=n_sticks,position=position)
    wins = 0

    widgets = [
    '[ (',
    progressbar.Timer(),
    ') ',
    progressbar.Bar('█'),
    progressbar.Percentage(),
    ']'
]
    
    if show_progressbar:
        bar = progressbar.ProgressBar(maxval=n_trains-1, widgets=widgets).start()

    for n in range(n_trains):

        new_game = game(computer_player=training_player,n_sticks=n_sticks,clever_training=clever_training)
        training_player, winner = new_game.play_game()

        if winner == "computer":
            wins += 1
        
        if show_progressbar:
            bar.update(n)

    winrate = wins/n_trains

    if show_progressbar:

        print(
            f"\n Ordinateur entraîné sur {n_trains} parties."
            f"\n Taux de victoires : {round(100*winrate)}%"
        )

        for n in range(n_sticks):
            print(
                f"Gobelet {n+1} : \n {training_player.cups[n].blue} \t {training_player.cups[n].yellow} \n"
            )

    fig, axes = plt.subplots(1,training_player.n_cups-1,figsize=(n_sticks,6))
    plt.subplots_adjust(wspace=1)
    fig.supylabel("Proportion de jetons",fontsize=15)

    for i in range(training_player.n_cups-1):
        ax = axes[i]
        n_jetons = training_player.cups[i+1].blue + training_player.cups[i+1].yellow
        blue_weights = training_player.cups[i+1].blue/n_jetons
        yellow_weights = training_player.cups[i+1].yellow/n_jetons
        ax.hist([0.5],[0.5,1.5],weights=[blue_weights],color='blue')
        ax.hist([1.5],[1.5,2.5],weights=[yellow_weights],color='orange')
        # ax.plot([1,1],[0,training_player.cups[i+1].blue/(training_player.cups[i+1].blue + training_player.cups[i+1].yellow)],linewidth=10,color='blue')
        # ax.plot([2,2],[0,training_player.cups[i+1].yellow/(training_player.cups[i+1].blue + training_player.cups[i+1].yellow)],linewidth=10,color='orange')
        ax.axis('off')
        ax.set_xlim([0.5,2.5])
        ax.xaxis.set_ticks([1,2])
        ax.tick_params(labelsize=15)
        ax.set_ylim([0,1])
        ax.yaxis.set_ticklabels([])
        ax.yaxis.set_ticks([])
        ax.set_title(i+2,fontsize=20)
        text_jeton = [" jeton"," jetons"][int(n_jetons!=1)]
        ax.text(x=0.5,y=-0.1,s=str(n_jetons)+text_jeton,fontsize=12)

    plt.savefig(f"nn_saves/sticks{n_sticks}_trains{n_trains}_state.png")
    plt.close()
    # print("Saved NN histogram")

    if saveplayer:

        with open(f"nn_saves/sticks{n_sticks}_trains{n_trains}_position_{position}_clever_training_{clever_training}.pkl","wb") as f:
            pickle.dump(training_player,f)

    return [training_player,winrate]

if __name__=="__main__":

    train(10,n_sticks=8)


            


