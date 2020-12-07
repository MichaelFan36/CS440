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
This is the main entry point for Part 2 of this MP. You should only modify code
within this file for Part 2 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


import numpy as numpy
import math
from collections import Counter





def naiveBayesMixture(train_set, train_labels, dev_set, bigram_lambda,unigram_smoothing_parameter, bigram_smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    bigram_lambda - float between 0 and 1

    unigram_smoothing_parameter - Laplace smoothing parameter for unigram model (between 0 and 1)

    bigram_smoothing_parameter - Laplace smoothing parameter for bigram model (between 0 and 1)

    pos_prior - positive prior probability (between 0 and 1)
    """
 


    # TODO: Write your code here
    Pos_count = Counter()
    Neg_count = Counter()
    Bi_Pos_count = Counter()
    Bi_Neg_count = Counter()
    result = list()

    for i in range(len(train_set)):
        for word in train_set[i]:
            if train_labels[i]:
                Pos_count[word] += 1
            else:
                Neg_count[word] += 1

    for i in range(len(train_set)):
        for j in range(len(train_set[i]) - 1):
            if train_labels[i]:
                Bi_Pos_count[(train_set[i][j], train_set[i][j + 1])] += 1
            else:
                Bi_Neg_count[(train_set[i][j], train_set[i][j + 1])] += 1

    Pos_total = sum(Pos_count.values())
    Neg_total = sum(Neg_count.values())
    Bi_Pos_total = sum(Bi_Pos_count.values())
    Bi_Neg_total = sum(Bi_Neg_count.values())

    # print(Pos_total)
    # print(Neg_total)
    # print(Bi_Pos_total)
    # print(Bi_Neg_total)

    log_Bi_Lamba = numpy.log(bigram_lambda)
    log_not_Bi_Lamba = numpy.log(1 - bigram_lambda)
    logpos = numpy.log(pos_prior)
    notlogpos = numpy.log(1 - pos_prior)
    log_pos_prior_final = 0.0
    log_not_pos_prior_final = 0.0
    for i in range(len(dev_set)):
        log_pos_prior = logpos
        log_not_pos_prior = notlogpos
        for word in dev_set[i]:
            if word in Pos_count:
                log_pos_prior += numpy.log((Pos_count[word] + unigram_smoothing_parameter) / (Pos_total + unigram_smoothing_parameter * numpy.absolute(len(Pos_count))))
            else:
                log_pos_prior += numpy.log(unigram_smoothing_parameter / (Pos_total + unigram_smoothing_parameter * numpy.absolute(len(Pos_count))))

            if word in Neg_count:
                log_not_pos_prior += numpy.log((Neg_count[word] + unigram_smoothing_parameter) / (Neg_total + unigram_smoothing_parameter * numpy.absolute(len(Neg_count))))
            else:
                log_not_pos_prior += numpy.log(unigram_smoothing_parameter / (Neg_total + unigram_smoothing_parameter * numpy.absolute(len(Neg_count))))

        log_pos_prior += log_not_Bi_Lamba
        log_not_pos_prior += log_not_Bi_Lamba

        log_pos_prior_final += numpy.exp(log_pos_prior)
        log_not_pos_prior_final += numpy.exp(log_not_pos_prior)

        log_pos_prior = logpos
        log_not_pos_prior = notlogpos
        for j in range(len(dev_set[i]) - 1):
            if (dev_set[i][j], dev_set[i][j + 1]) in Bi_Pos_count:
                log_pos_prior += numpy.log((Bi_Pos_count[(dev_set[i][j], dev_set[i][j + 1])] + bigram_smoothing_parameter) / (Bi_Pos_total + bigram_smoothing_parameter * len(Bi_Pos_count)))
            else:
                log_pos_prior += numpy.log(bigram_smoothing_parameter / (Bi_Pos_total + bigram_smoothing_parameter * len(Bi_Pos_count)))
        
            if (dev_set[i][j], dev_set[i][j + 1]) in Bi_Neg_count:
                log_not_pos_prior += numpy.log((Bi_Neg_count[(dev_set[i][j], dev_set[i][j + 1])] + bigram_smoothing_parameter) / (Bi_Neg_total + bigram_smoothing_parameter * len(Bi_Neg_count)))
            else:
                log_not_pos_prior += numpy.log(bigram_smoothing_parameter / (Bi_Neg_total + bigram_smoothing_parameter * len(Bi_Neg_count)))

        log_pos_prior += log_Bi_Lamba
        log_not_pos_prior += log_Bi_Lamba
        log_pos_prior_final += numpy.exp(log_pos_prior)
        log_not_pos_prior_final += numpy.exp(log_not_pos_prior)

        if log_pos_prior_final >= log_not_pos_prior_final:
            result.append(1)
        else:
            result.append(0)
            
    return result