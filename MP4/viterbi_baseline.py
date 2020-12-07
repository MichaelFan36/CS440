"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
from collections import Counter
import time

def baseline(train, test):
    '''
    TODO: implement the baseline algorithm. This function has time out limitation of 1 minute.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
            test data (list of sentences, no tags on the words)
            E.g  [[word1,word2,...][word1,word2,...]]
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''

#     raise Exception("You must implement me")
    predicts = [] 
    word_tag_map = dict()
    word_counter = Counter()
    tag_counter = Counter()
    tag_sorted = []
    for sentence in train:
        for word in sentence:
                word_counter[word] += 1
                tag_counter[word[1]] += 1
    for word in word_counter:
        if word[0] not in word_tag_map:
                word_tag_map[word[0]] = []
                word_tag_map[word[0]].append((word[1], word_counter[word]))
        else:            
                word_tag_map[word[0]].append((word[1], word_counter[word]))
                word_tag_map[word[0]].sort(key=lambda x: x[1])
    tag_sorted = sorted(tag_counter.items(), key=lambda  x: x[1])
    
    for sentence in test:
            temp_list = []
            for word in sentence:
                    if word in word_tag_map:
                            temp_list.append((word, word_tag_map[word][len(word_tag_map[word]) - 1][0]))
                    else:
                            temp_list.append((word, tag_sorted[len(tag_sorted) - 1][0]))
            predicts.append(temp_list)
    return predicts


def viterbi_p1(train, test):
    '''
    TODO: implement the simple Viterbi algorithm. This function has time out limitation for 3 mins.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no tags on the words)
            E.g [[word1,word2...]]
    output: list of sentences with tags on the words
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''

    raise Exception("You must implement me")
    predicts = []

    return predicts

def viterbi_p2(train, test):
    '''
    TODO: implement the optimized Viterbi algorithm. This function has time out limitation for 3 mins.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no tags on the words)
            E.g [[word1,word2...]]
    output: list of sentences with tags on the words
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''


    predicts = []
    raise Exception("You must implement me")
    return predicts