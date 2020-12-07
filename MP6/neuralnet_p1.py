# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019

"""
You should only modify code within this file for part 1 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class NeuralNet(torch.nn.Module):
    def __init__(self, lrate,loss_fn,in_size,out_size):
        """
        Initialize the layers of your neural network
        @param lrate: The learning rate for the model.
        @param loss_fn: The loss function
        @param in_size: Dimension of input
        @param out_size: Dimension of output
        The network should have the following architecture (in terms of hidden units):
        in_size -> 128 ->  out_size
        """
        super(NeuralNet, self).__init__()
        self.loss_fn = loss_fn
        self.lrate = lrate
        self.in_size = in_size
        self.out_size = out_size
        self.hidden_layer = nn.Linear(in_size, 128)
        self.output_layer = nn.Linear(128, out_size)
        self.model = nn.Sequential(self.hidden_layer,
                                   self.output_layer)
        self.optimizer = optim.SGD(self.model.parameters(),lr = lrate)

    def get_parameters(self):
        """ Get the parameters of your network
        @return params: a list of tensors containing all parameters of the network
        """
        return self.model.parameters()


    def forward(self, x):
        """ A forward pass of your autoencoder
        @param x: an (N, in_size) torch tensor
        @return y: an (N, out_size) torch tensor of output from the network
        """
        m = nn.Sigmoid()
        s = m(self.hidden_layer(x))
        output = self.output_layer(s)
        return output

    def step(self, x,y):
        """
        Performs one gradient step through a batch of data x with labels y
        @param x: an (N, in_size) torch tensor
        @param y: an (N,) torch tensor
        @return L: total empirical risk (mean of losses) at this time step as a float
        """
        self.optimizer.zero_grad()
        output = self.forward(x)
        L = self.loss_fn(output, y)
        L.backward()
        self.optimizer.step()
        return L

def fit(train_set,train_labels,dev_set,n_iter,batch_size=100):
    """ Fit a neural net.  Use the full batch size.
    @param train_set: an (N, 784) torch tensor
    @param train_labels: an (N,) torch tensor
    @param dev_set: an (M, 784) torch tensor
    @param n_iter: int, the number of batches to go through during training (not epoches)
                   when n_iter is small, only part of train_set will be used, which is OK,
                   meant to reduce runtime on autograder.
    @param batch_size: The size of each batch to train on.
    # return all of these:
    @return losses: list of total loss (as type float) after each iteration. Ensure len(losses) == n_iter
    @return yhats: an (M,) NumPy array of approximations to labels for dev_set
    @return net: A NeuralNet object
    # NOTE: This must work for arbitrary M and N
    """

    net = NeuralNet(1, nn.CrossEntropyLoss(), 784, 3)
    losses = []

    train_mean = train_set.mean(dim=0, keepdim = True)
    train_std = train_set.std(dim=0, keepdim = True)
    train_set = (train_set - train_mean) / train_std

    dev_mean = dev_set.mean(dim=0, keepdim = True)
    dev_std = dev_set.std(dim=0, keepdim = True)
    dev_set = (dev_set - dev_mean) / dev_std
    

    for i in range(0, n_iter):
        index = int(i % (len(train_set)/batch_size))
        losses.append(net.step(train_set[index*batch_size:(index+1)*batch_size], train_labels[index*batch_size:(index+1)*batch_size]))

    newlist = net(dev_set).detach().numpy()
    yhats = np.argmax(newlist, axis=1)
    losses = [float(loss) for loss in losses]
    return losses,yhats,net
