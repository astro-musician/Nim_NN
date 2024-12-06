import numpy as np
import matplotlib.pyplot as plt

from src.player import player, train, game

n_trains = np.arange(501) #np.concatenate((np.arange(50),np.arange(50,501,10)))
n_games = 100
n_sticks = 8
clever_training = False
position = "random"

winrates = np.zeros((len(n_trains),n_games))

for n in range(len(n_trains)):

    NN_n_trains = train(
        n_trains=n_trains[n],
        n_sticks=n_sticks,
        show_progressbar=False,
        saveplayer=False,
        position=position,
        clever_training=clever_training
        )[0]

    for i in range(n_games):

        winner = game(computer_player=NN_n_trains,n_sticks=n_sticks,clever_training=clever_training).play_game()[1]

        if winner == "computer":

            winrates[n,i] = 1

mean_winrates = np.mean(winrates,axis=1)
err_winrates = np.std(winrates,axis=1)/np.sqrt(n_games)

# plt.errorbar(n_trains,mean_winrates,yerr=err_winrates,fmt='ro ')
plt.plot(n_trains,mean_winrates,'r. ')
plt.grid()
plt.xlim([0,1.1*np.max(n_trains)])
plt.ylim([0,1])
plt.xlabel("Entraînements",fontsize=15)
plt.yticks(0.1*np.arange(11))
plt.ylabel(f"Taux de victoires sur {n_games} parties",fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.title(f"Ordinateur jouant au jeu de nim ({n_sticks} bâtons) \n Départ aléatoire, entraîneur idiot",fontsize=15)
plt.savefig("statistiques_ordinateur_nim.png")
plt.show()