import numpy as np
import matplotlib.pyplot as plt
import progressbar
import pickle
import time

class cup:

    def __init__(self):

        self.blue = 2
        self.yellow = 2

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

    def __init__(self,n_cups=8):

        self.n_cups = n_cups
        self.cups = []
        for n in range(self.n_cups):
            self.cups.append(cup())

        pass

class game:

    def __init__(self, computer_player : player, n_sticks=8 ) :

        self.n_sticks = n_sticks
        self.players = ["computer","trainer"]
        self.computer = computer_player
        self.played_numbers = np.zeros(self.n_sticks)

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
        return played
    
    def clever_trainer_turn(self):

        if self.n_sticks%3 !=0 :
            played = self.n_sticks%3
        else:
            played = np.random.choice(np.array([1,2]))

        return played
    
    def computer_turn(self):
        played = self.computer.cups[self.n_sticks-1].play()
        # print(f"\n Computer : {played}")
        return played

    def play_game(self) -> list[player,str]:

        turn = 0

        while self.n_sticks > 0:

            current_player = self.players[turn%2]

            if current_player == "trainer":
                n_played = self.clever_trainer_turn()

            elif current_player == "computer":
                n_played = self.computer_turn()
                self.played_numbers[self.n_sticks-1] = n_played

            if not self.suited_play(n_played):
                raise ValueError("CHEATER")

            self.remove_sticks(n_played)

            turn += 1

        winner = self.players[(turn-1)%2]
        new_computer = self.computer
        self.played_numbers = np.intc(self.played_numbers)

        if winner == "computer":

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

        return [new_computer,winner]
    
    
def train(n_trains:int, n_sticks:int, show_progressbar=True) -> list[player,float]:

    training_player = player(n_cups=n_sticks)
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

        new_game = game(computer_player=training_player,n_sticks=n_sticks)
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

    fig, axes = plt.subplots(1,training_player.n_cups)

    for i in range(training_player.n_cups):
        ax = axes[i]
        ax.plot([1,1],[0,training_player.cups[i].blue/(training_player.cups[i].blue + training_player.cups[i].yellow)],linewidth=2,color='blue')
        ax.plot([2,2],[0,training_player.cups[i].yellow/(training_player.cups[i].blue + training_player.cups[i].yellow)],linewidth=2,color='orange')
        ax.set_xlim([0,3])
        ax.xaxis.set_ticks([1,2])
        ax.set_ylim([0,1])
        ax.yaxis.set_ticklabels([])
        ax.yaxis.set_ticks([])
        ax.set_title(i+1)

    plt.savefig(f"nn_saves/sticks{n_sticks}_trains{n_trains}_state.png")

    with open(f"nn_saves/sticks{n_sticks}_trains{n_trains}.pkl","wb") as f:
        pickle.dump(training_player,f)

    return [training_player,winrate]

if __name__=="__main__":

    train(10,n_sticks=9)


            


