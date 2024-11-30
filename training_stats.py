import numpy as np
import matplotlib.pyplot as plt

from src.player import player, train, game

n_trains = np.arange(1,31)
n_games = 100
n_sticks = 8

winrates = np.zeros((len(n_trains),n_games))

for n in range(len(n_trains)):

    NN_n_trains = train(n_trains=n_trains[n],n_sticks=n_sticks,show_progressbar=False,saveplayer=False)[0]

    for i in range(n_games):

        winner = game(computer_player=NN_n_trains,n_sticks=n_sticks).play_game()[1]

        if winner == "computer":

            winrates[n,i] = 1

mean_winrates = np.mean(winrates,axis=1)
err_winrates = np.std(winrates,axis=1)/np.sqrt(n_games)

plt.errorbar(n_trains,mean_winrates,yerr=err_winrates,fmt='ro ')
plt.grid()
plt.xlim([0,1.1*np.max(n_trains)])
plt.ylim([0,1])
plt.xlabel("Entraînements",fontsize=15)
plt.ylabel(f"Taux de victoires sur {n_games} parties",fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.title(f"Ordinateur jouant au jeu de nim ({n_sticks} bâtons)",fontsize=15)
plt.savefig("statistiques_ordinateur_nim.png")
plt.show()