# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018
# Modified by Jaewook Yeom 02/02/2020

"""
This is the main entry point for Part 1 of MP3. You should only modify code
within this file for Part 1 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as numpy
import math
from collections import Counter


def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter you provided with --laplace (1.0 by default)

    pos_prior - positive prior probability (between 0 and 1)
    """



    # TODO: Write your code here
    Pos_count = Counter()
    Neg_count = Counter()
    result = list()
    for i in range(len(train_set)):
        for word in train_set[i]:
            if train_labels[i]:
                Pos_count[word] += 1
            else:
                Neg_count[word] += 1
                
    Pos_total = sum(Pos_count.values())
    Neg_total = sum(Neg_count.values())

    Probability_Pos = dict()
    Probability_Neg = dict()
    for word in Pos_count:
        Probability_Pos[word] = (Pos_count[word] + smoothing_parameter) / (Pos_total + smoothing_parameter * numpy.absolute(len(Pos_count)))
    for word in Neg_count:
        Probability_Neg[word] = (Neg_count[word] + smoothing_parameter) / (Neg_total + smoothing_parameter * numpy.absolute(len(Neg_count)))
    

    for i in range(len(dev_set)):
        log_pos_prior = numpy.log(pos_prior)
        log_not_pos_prior = numpy.log(1 - pos_prior)
        for word in dev_set[i]:
            if word in Pos_count:
                log_pos_prior += numpy.log(Probability_Pos[word])
            else:
                log_pos_prior += numpy.log(smoothing_parameter / (Pos_total + smoothing_parameter * numpy.absolute(len(Pos_count))))

            if word in Neg_count:
                log_not_pos_prior += numpy.log(Probability_Neg[word])
            else:
                log_not_pos_prior += numpy.log(smoothing_parameter / (Neg_total + smoothing_parameter * numpy.absolute(len(Neg_count))))

        if log_pos_prior > log_not_pos_prior:
            result.append(1)
        else:
            result.append(0)
            
    return result