# classify.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/27/2018
# Extended by Daniel Gonzales (dsgonza2@illinois.edu) on 3/11/2020

"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.

train_set - A Numpy array of 32x32x3 images of shape [7500, 3072].
            This can be thought of as a list of 7500 vectors that are each
            3072 dimensional.  We have 3072 dimensions because there are
            each image is 32x32 and we have 3 color channels.
            So 32*32*3 = 3072. RGB values have been scaled to range 0-1.

train_labels - List of labels corresponding with images in train_set
example: Suppose I had two images [X1,X2] where X1 and X2 are 3072 dimensional vectors
         and X1 is a picture of a dog and X2 is a picture of an airplane.
         Then train_labels := [1,0] because X1 contains a picture of an animal
         and X2 contains no animals in the picture.

dev_set - A Numpy array of 32x32x3 images of shape [2500, 3072].
          It is the same format as train_set
"""
import numpy as np
import math as math

def trainPerceptron(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    # return the trained W and b parameters 
    W = np.zeros(len(train_set[1]))
    b = 0
    for i in range(max_iter):
        for j in range(train_set.shape[0]):
            if np.dot(W, train_set[j,:]) + b > 0:
                if train_labels[j] != 1:
                    W = W + (train_labels[j]-0.5) * 2 * learning_rate * train_set[j,:]
                    b = b + (train_labels[j]-0.5) * 2 * learning_rate
            else:
                if train_labels[j] != 0:
                    W = W + (train_labels[j]-0.5) * 2 * learning_rate * train_set[j,:]
                    b = b + (train_labels[j]-0.5) * 2 * learning_rate
    return W, b

def classifyPerceptron(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    # Train perceptron model and return predicted labels of development set
    W,b = trainPerceptron(train_set, train_labels, learning_rate, max_iter)
    result = []
    for i in range(dev_set.shape[0]):
        if np.dot(W, dev_set[i]) + b > 0:
            result.append(1)
        else:
            result.append(0)
    return result

def sigmoid(x):
    # TODO: Write your code here
    # return output of sigmoid function given input x
    return 1/(1+math.exp(-x))

def trainLR(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    # return the trained W and b parameters 
    W = np.zeros(train_set.shape[1])
    b = 0
    for i in range(max_iter):
        gradient = np.zeros(W.shape)
        derivative = 0
        for j in range(train_set.shape[0]):
            gradient = gradient + (train_labels[j]-sigmoid(np.dot(W, train_set[j]) + b)) * train_set[j, :]
            derivative = derivative + (train_labels[j]-sigmoid(np.dot(W, train_set[j]) + b))
        W = W + learning_rate * gradient / train_set.shape[0]
        b = b + learning_rate * derivative / train_set.shape[0]
    return W, b

def classifyLR(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    # Train LR model and return predicted labels of development set
    W,b  = trainLR(train_set, train_labels, learning_rate, max_iter)
    result = []
    for i in range(dev_set.shape[0]):
        if sigmoid(np.dot(W, dev_set[i, :])+ b) >= 0.5:
            result.append(1)
        else:
            result.append(0)
    return result

import heapq as hp

def Euclidean(x,y):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))

def classifyEC(train_set, train_labels, dev_set, k):
    # Write your code here if you would like to attempt the extra credit
    result = []
    heap = []
    size = 0
    for i in range(dev_set.shape[0]):
        size = 0
        count = 0
        for j in range(train_set.shape[0]):
            hp.heappush(heap, (-Euclidean(dev_set[i,:], train_set[j,:]), train_labels[j]))
            size += 1
            if size > k:
                hp.heappop(heap)
        for z in range(k):
            if hp.heappop(heap)[1] == 1:
                count += 1
        if 2 * count > k:
            result.append(1)
        else:
            result.append(0)
    return result
