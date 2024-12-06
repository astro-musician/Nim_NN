Ce programme a été écrit dans le but de faire découvrir les réseaux de neurones, en partenariat avec la Maison pour la Science à Paris. Il crée des réseaux de neurones à une couche, les entraîne à jouer au jeu de nim et permet ensuite de jouer contre eux. L'idée est de montrer qu'on peut entraîner très rapidement de tels réseaux par ordinateur, en jouant un grand nombre de parties en peu de temps. Il s'agit d'une réplique numérique d'une activité réalisée "en débranché", qui s'inscrit dans sa continuité.

- INSTALLATION

Il est nécessaire d'avoir python3.* et git installés pour utiliser ce code.

Commencez par ouvrir une fenêtre de terminal, puis rendez-vous dans le dossier où vous souhaitez télécharger le code (la commande pour avancer dans un dossier est cd dossier). Ensuite, exécutez ces trois commandes :
---------------------
git clone git@github.com:astro-musician/Nim_NN.git
cd Nim_NN
bash makepyenv
---------------------

Ou bien, pour tout installer en un seul coup, téléchargez le fichier install.sh, positionnez-le dans votre dossier de code et exécutez la commande :

---------------------
bash install.sh
---------------------

- LANCEMENT

Rendez-vous dans le dossier Nim_NN, puis exécutez depuis le terminal au choix :

---------------------
source .nn-env/bin/activate
python3 __main__.py
---------------------

ou

---------------------
bash Nim-NN.sh
---------------------

Je réfléchis actuellement à faire de ce programme un exécutable afin d'éviter l'installation de python et git.

- RÈGLES DU JEU

Le jeu de Nim se joue à un contre un. Au départ, on dispose un certain nombre de bâtons sur une table. Tour à tour, chaque joueur doit choisir de retirer entre un et un nombre maximal de bâtons. Pour gagner, il faut retirer le dernier bâton. 

- STRATÉGIE GAGNANTE

On peut démontrer que si le nombre maximal de bâtons qu'on est autorisé à retirer d'un coup est n, alors une stratégie gagnante est de faire en sorte que lorsque l'adversaire joue, le nombre de bâtons restants soit toujours un multiple de n+1. Ainsi, si le nombre initial de bâtons est un multiple de n+1, le second joueur dispose d'une stratégie gagnante à coup sûr ; sinon, c'est le premier joueur qui a l'avantage. Ce programme ne traite que le cas n=2 pour rester abordable, mais permet de modifier le nombre initial de bâtons. 

Connaître l'existence de cette stratégie permet de mieux appréhender les statistiques du réseau de neurones entraîné : on remarquera notamment qu'il reste indécis pour un nombre de bâtons divisible par 3, car quoi qu'il fasse il a de fortes chances de perdre.	

