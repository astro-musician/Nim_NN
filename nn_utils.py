# Fonctions utilisées par un réseau de neurones très simple (sortie booléenne)

import numpy as np
import jax.numpy as jnp
from jax import grad, random
import numpyro
import numpyro.distributions as dist
from numpyro.infer import NUTS, MCMC
from numpyro.infer.initialization import init_to_value
import progressbar
from activation_functions import *

class neuron:

    def __init__(self,weight,bias,activation):

        self.weight = weight
        self.bias = bias
        # self.n_in = np.shape(weight)[0]
        # self.n_out = np.shape(weight)[1]
        self.activation = activation

        pass

    def new_weight(self,sig_weight=0.1):

        new_weight = np.random.normal(size=np.shape(self.weight))*sig_weight + self.weight

        return new_weight
    
    def new_bias(self,sig_bias=0.1):
        
        new_bias = np.random.normal(size=np.shape(self.bias))*sig_bias + self.bias

        return new_bias
    
    def output(self,x):
        return self.activation(np.dot(x,self.weight)+self.bias)
    
    def new_output(self,x):
        return self.activation(np.dot(x,self.new_weight)+self.new_bias)
    
class double_layer_nn:

    def __init__(self,weights,biases,activations):

        self.weights = weights
        self.biases = biases
        self.activations = activations
        self.learning_rate = 0.1
        self.n_in = np.shape(self.weights[0])[0]
        self.n_hidden = np.shape(self.weights[0])[1]
        self.n_out = np.shape(self.weights[1])[1]

        self.neuron1 = neuron(weights[0],biases[0],self.activations[0])
        self.neuron2 = neuron(weights[1],biases[1],self.activations[1])

        self.new_neuron1 = neuron(self.new_weights()[0],self.new_biases()[0],self.activations[0])
        self.new_neuron2 = neuron(self.new_weights()[1],self.new_biases()[1],self.activations[1])

        pass

    def new_weights(self):

        return [self.neuron1.new_weight(),self.neuron2.new_weight()]
    
    def new_biases(self):

        return [self.neuron1.new_bias(),self.neuron2.new_bias()]

    def output(self,x):
        out = self.neuron2.output(self.neuron1.output(x))
        return out
        # if np.shape(out)==(1,1):
        #     return out[0,0]
        # else:
        #     return out
    
    def new_output(self,x):
        new_neuron1 = neuron(self.new_weights()[0],self.new_biases()[0],self.activations[0])
        new_neuron2 = neuron(self.new_weights()[1],self.new_biases()[1],self.activations[1])
        out = new_neuron2.output(new_neuron1.output(x))
        return out
        # if np.shape(out)==(1,1):
        #     return out[0,0]
        # else:
        #     return out

    def grad_backpropagation(self,score_func,data):
        """
        score_func must be written with jax.numpy instead of numpy
        """

        score_for_grad = lambda x, w1, w2, b1, b2: score_func( self.activations[1]( jnp.dot( self.activations[0]( jnp.dot ( x , w1 ) + b1 ) , w2 ) + b2) )
        score_grad = grad(score_for_grad,argnums=[1,2,3,4])
        score_grad_value = score_grad(data,self.weights[0],self.weights[1],self.biases[0],self.biases[1])

        dw1 = score_grad_value[0]
        dw2 = score_grad_value[1]
        db1 = score_grad_value[2]
        db2 = score_grad_value[3]

        # print(f"{dw1} \n {dw2} \n {db1} \n {db2} \n")

        new_w1 = self.weights[0] + dw1*self.learning_rate
        new_w2 = self.weights[1] + dw2*self.learning_rate
        new_b1 = self.biases[0] + db1*self.learning_rate
        new_b2 = self.biases[1] + db2*self.learning_rate

        # self.weights = [new_w1,new_w2]
        # self.biases = [new_b1,new_b2]

        return [new_w1,new_w2,new_b1,new_b2]
    
    def mse(self):

        max_weight_range = 10
        max_bias_range = 10

        w1 = numpyro.sample('w1',dist.Uniform(low=jnp.zeros(jnp.shape(self.weights[0])),high=max_weight_range*jnp.ones(jnp.shape(self.weights[0]))))
        w2 = numpyro.sample('w2',dist.Uniform(low=jnp.zeros(jnp.shape(self.weights[1])),high=max_weight_range*jnp.ones(jnp.shape(self.weights[1]))))
        b1 = numpyro.sample('b1',dist.Uniform(low=-max_bias_range*jnp.ones(jnp.shape(self.biases[0])),high=max_bias_range*jnp.ones(jnp.shape(self.biases[0]))))
        b2 = numpyro.sample('b2',dist.Uniform(low=-max_bias_range*jnp.ones(jnp.shape(self.biases[1])),high=max_bias_range*jnp.ones(jnp.shape(self.biases[1]))))

        prop = self.activations[1]( jnp.dot( self.activations[0]( jnp.dot( self.data , w1 ) + b1 ) , w2 ) + b2 )

        numpyro.sample('likelihood',dist.Normal(prop),obs=self.results)

        return
    
    def MCMC(self,data,results):
        
        self.data = data
        self.results = results
        self.n_trains = 2000

        init = {
            'w1':self.weights[0],
            'w2':self.weights[1],
            'b1':self.biases[0],
            'b2':self.biases[1]
        }

        rng_key = random.PRNGKey(0)
        kernel = NUTS(self.mse,init_strategy=(init_to_value(values=init)))
        mcmc = MCMC(kernel,num_warmup=self.n_trains//2,num_samples=self.n_trains//2,progress_bar=True)
        mcmc.run(rng_key)

        chain = mcmc.get_samples()

        return chain
    
    # def score_for_grad(self,w1,w2,b1,b2,score_func):
    #     return lambda x: score_func( self.activations[1]( np.dot( self.activations[0]( np.dot ( x , w1 ) + b1 ) , w2 ) + b2) )
    
def backpropagation_MH_step(NN,score_func,step:int):
        """
        A single backpropagation step of the double layer network NN based on Metropolis-Hastings algorithms.

        Inputs : 
        - The Neural Network at the given step
        - The SCORE function taking NN and returning its SCORE
        - the step number

        Outputs : 
        - boolean noting the sucess/failure of the slightly modified NN
        - the new NN depending on the result
        """
        test_weights = NN.new_weights()
        test_biases = NN.new_biases()

        NN_test = double_layer_nn(test_weights,test_biases,NN.activations)
        best_score = score_func(NN)
        new_score = score_func(NN_test)
        # print(f"\n Best : {best_score} \n New : {new_score}")

        if new_score >= best_score:
            new_step = step + 1
            NN_new = NN_test
        else:
            new_step = step
            NN_new = NN

        return [new_step,NN_new]

def backpropagation_MH(NN_init,score_func,n_trains:int,show_progressbar=True):
    """
    Backpropagation for reinforcement learning.
    """
    NN = NN_init

    widgets = [
        '[ (',
        progressbar.Timer(),
        ') ',
        progressbar.Bar('█'),
        progressbar.Percentage(),
        ']'
    ]

    if show_progressbar:

        bar = progressbar.ProgressBar(maxval=n_trains, widgets=widgets).start()

    step = 1
    while step < n_trains:
        step, NN = backpropagation_MH_step(NN,score_func,step)
        if show_progressbar:
            bar.update(step)

    print(
        f"\n Trained neural network {n_trains} times \n "
    )

    return NN