import numpy as np
import jax.numpy as jnp
import jax.random as random

def ReLU(x):
    return 0.5*(x+jnp.abs(x))

def gaussian(x):
    return jnp.exp(-x**2)

def sigmoid(x):
    return 1/(jnp.exp(-x)+1)

def msigmoid(x):
    return sigmoid(-x)

def linear(x):
    return x

def softmax(logits):
    exp_logits = np.exp(logits - np.max(logits, axis=1, keepdims=True))
    probs = exp_logits/np.sum(exp_logits, axis=1, keepdims=True)
    probs[:,-1] = 1 - np.sum(probs[:,:-1])
    # max_ll = jnp.max(probs,axis=1)[...,None]
    # indices = jnp.where(jnp.unique(probs==max_ll,axis=1))[1]
    
    return probs

def softplus(x):
    return jnp.log(1+jnp.exp(x))
