import numpy as np
import matplotlib.pyplot as plt

from src.training_by_hand_utils import train

n_trains = [5,10,20,50,100,200,500]
n_trainings_per_n_train = 50
n_sticks = 9

winrates = np.zeros((len(n_trains),n_trainings_per_n_train))

for n in range(len(n_trains)):
    for i in range(n_trainings_per_n_train):
        winrate = train(n_trains=n_trains[n],n_sticks=n_sticks,show_progressbar=False)[1]
        winrates[n,i] = winrate

mean_winrates = np.mean(winrates,axis=1)
err_winrates = np.std(winrates,axis=1)

plt.errorbar(n_trains,mean_winrates,yerr=err_winrates,fmt='ro ')
plt.grid()
plt.xlim([0,1.1*np.max(n_trains)])
plt.ylim([0,1])
plt.xlabel("Entraînements",fontsize=15)
plt.ylabel("Taux de victoires",fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.title(f"Ordinateur jouant au jeu de nim ({n_sticks} bâtons)",fontsize=15)
plt.savefig("statistiques_ordinateur_nim.png")
plt.show()