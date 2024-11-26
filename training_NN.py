import pickle
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from multiprocessing import Pool, cpu_count
from nim_computer import nim_game_training
from nn_utils import double_layer_nn, backpropagation_MH
from activation_functions import *

parser = ArgumentParser()
parser.add_argument("--train",default=False,action='store_true')
execute_training = parser.parse_args().train

n_cpus = cpu_count()

def softmax_for_nim(x,n_max):
    choices = np.arange(1,n_max+1)
    probs = softmax(x)[0]
    return np.random.choice(a=choices,p=probs)

class NN_nim_player:

    def __init__(self,NN,n_sticks,n_max,n_trains,adversarial):
        self.NN = NN
        self.n_sticks = n_sticks
        self.n_max = n_max
        self.n_trains = n_trains
        self.adversarial = adversarial
        pass

class NN_training:

    def __init__(self,n_trains=10,adversarial=False):

        self.n_trains = n_trains
        self.adversarial = adversarial
        self.activations = [np.sin,self.softmax_for_nim]
        self.games_per_step = 1000
        self.max_tries = 10000

        self.n_sticks = 12
        self.n_max = 2
        self.n_hidden = 1
        self.notrain = double_layer_nn(weights=[np.ones((1,self.n_hidden)),np.ones((self.n_hidden,self.n_max))],biases=[np.zeros((1,self.n_hidden)),np.zeros((self.n_hidden,self.n_max))],activations=self.activations)
        self.NN = self.notrain

        if self.adversarial:
            self.NN_trainer = double_layer_nn(weights=[0.1*np.ones((1,self.n_hidden)),0.1*np.ones((self.n_hidden,self.n_max))],biases=[np.zeros((1,self.n_hidden)),np.zeros((self.n_hidden,self.n_max))],activations=self.activations)

        else:
            self.NN_trainer = None

        pass

    def softmax_for_nim(self,x):
        return softmax_for_nim(x,self.n_max)
    

    def score_func(self,NN):

        # if __name__=="__main__":
        #     with Pool() as pool:
        #         scores = np.array([pool.map(nim_game_training(NN,n_sticks=self.n_sticks).score,n_cpus*[NN]) for i in range(self.games_per_step//n_cpus)])
        #         return np.sum(scores)

        scores = [nim_game_training(NN,n_sticks=self.n_sticks).score for i in range(self.games_per_step)]
        return np.sum(scores)

    def train(self):

        self.NN_trained = backpropagation_MH(self.NN,self.score_func,self.n_trains)

        with open(f"nn_saves/nim_nn_{self.n_trains}_trains.pkl","wb") as f:
            pickle.dump(NN_nim_player(self.NN_trained,self.n_sticks,self.n_max,self.n_trains,self.adversarial),f)

        return

if execute_training:
    NN_training(n_trains=100).train()


            
