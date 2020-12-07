from collections import defaultdict
from collections import Counter
import numpy as np
import math
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def calculate_number(word_tag, emission_counter, hape_tag_counter, number_of_hape, tag_counter):
    result = 0
    if word_tag in emission_counter:
        if word_tag[1] in hape_tag_counter:
            result = np.log((emission_counter[word_tag] + 0.00001 * hape_tag_counter[word_tag[1]] + 0.0001579) / (tag_counter[word_tag[1]] + 0.00001 * hape_tag_counter[word_tag[1]] * len(tag_counter)))
        else:
            result = np.log((emission_counter[word_tag] + 0.00001 * (1 / number_of_hape) + 0.0001579) / (tag_counter[word_tag[1]] + 0.00001 * len(tag_counter)))
    else:
        if word_tag[1] in hape_tag_counter:
           result = np.log((0.00001 * hape_tag_counter[word_tag[1]] + 0.0001579) / (tag_counter[word_tag[1]] + 0.00001 * hape_tag_counter[word_tag[1]] * len(tag_counter)))
        else:
            result = np.log((0.00001 * (1 / number_of_hape) + 0.0001579) / (tag_counter[word_tag[1]] + 0.00001 * len(tag_counter)))
    return result
def extra(train,test):
    '''
    TODO: implement improved viterbi algorithm for extra credits.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
            test data (list of sentences, no tags on the words)
            E.g  [[word1,word2,...][word1,word2,...]]
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''

#     raise Exception("You must implement me")
    predicts = []
    tag_start_counter = Counter()
    tag_not_start_counter = Counter()
    tag_counter = Counter()
    transition_counter = Counter()
    transition_not_counter = Counter()
    emission_counter = Counter()
    emission_not_counter = Counter()
    hape_checker = dict()
    hape_tag_counter = Counter()
    number_of_hape = 0

    for sentence in train:
        tag_start_counter[sentence[0][1]] += 1
        for word in sentence:
            emission_counter[word] += 1
            tag_counter[word[1]] += 1
            if word[0] not in hape_checker:
                hape_checker[word[0]] = ("Shuyi", word[1])
            else:
                hape_checker[word[0]] = ("Yaoshui", word[1])
    
    for word in hape_checker:
        if hape_checker[word][0] == "Shuyi":
            number_of_hape += 1
            hape_tag_counter[hape_checker[word][1]] += 1

    for tag in hape_tag_counter:
        hape_tag_counter[tag] = hape_tag_counter[tag] / number_of_hape

    for tag in tag_counter: 
        if tag in  tag_start_counter:
            tag_start_counter[tag] = np.log((tag_start_counter[tag] + 0.0000001)/(len(train) + len(tag_counter)))
        else:
            tag_not_start_counter[tag] = np.log(0.0000001/(len(train) + len(tag_counter)))

        if tag in hape_tag_counter:
            emission_not_counter[tag] = np.log(0.0000001 * hape_tag_counter[tag] / (tag_counter[tag] + 0.0000001 * hape_tag_counter[tag] * len(tag_counter)))
        else:
            emission_not_counter[tag] = np.log(0.0000001 * (1 / number_of_hape) / (tag_counter[tag] + 0.0000001 * len(tag_counter)))

    for word_tag in emission_counter:
        if word_tag[1] in hape_tag_counter:
            emission_counter[word_tag] = np.log((emission_counter[word_tag] + 0.0000001 * hape_tag_counter[word_tag[1]]) / (tag_counter[word_tag[1]] + 0.0000001 * hape_tag_counter[word_tag[1]] * len(tag_counter)))
        else:
            emission_counter[word_tag] = np.log((emission_counter[word_tag] + 0.0000001 * (1 / number_of_hape)) / (tag_counter[word_tag[1]] + 0.0000001 * len(tag_counter)))

    for sentence in train:
        for i in range(len(sentence) - 1):
            pair = (sentence[i][1], sentence[i+1][1])
            transition_counter[pair] += 1
            transition_not_counter[pair[0]] += 1
        
    for pair in transition_counter:
        transition_counter[pair] = np.log((transition_counter[pair] + 0.0000001) / (tag_counter[pair[0]] + 0.0000001 * len(tag_counter)))

    for tag in transition_not_counter:
        transition_not_counter[tag] = np.log(0.0000001 / (tag_counter[tag] + 0.0000001*len(tag_counter)))


    for sentence in test:
        temp_list = []
        Dynamic_list = []
        for i in range(len(sentence)):
            word_dict = dict()
            if i == 0:
                for tag in tag_counter:
                    if tag in tag_start_counter:
                        word_dict[(sentence[i], tag)] = [tag_start_counter[tag], 'None']
                    else:
                        word_dict[(sentence[i], tag)] = [tag_not_start_counter[tag], 'None']
                    if (sentence[i], tag) in emission_counter:
                        word_dict[(sentence[i], tag)][0] += emission_counter[(sentence[i], tag)]
                    else:
                        word_dict[(sentence[i], tag)][0] += emission_not_counter[tag]
                Dynamic_list.append(word_dict)
            else:
                for tag in tag_counter:
                    temp_list = []
                    for word_tag in Dynamic_list[i-1]:
                        if (word_tag[1], tag) in transition_counter:
                            probability = Dynamic_list[i-1][word_tag][0] + transition_counter[(word_tag[1], tag)]
                        else:
                            probability = Dynamic_list[i-1][word_tag][0] + transition_not_counter[word_tag[1]]
                        
                        if (sentence[i], tag) in emission_counter:
                            probability += emission_counter[(sentence[i], tag)]
                        else:
                            probability += emission_not_counter[tag]
                        temp_list.append((probability, word_tag[1]))
                    temp_list.sort(key = lambda x: x[0])
                    word_dict[(sentence[i], tag)] = [temp_list[len(temp_list)-1][0], temp_list[len(temp_list)-1][1]]
                Dynamic_list.append(word_dict)

        largest_probability = -float("inf")
        largest_key = tuple()
        for word_tag in Dynamic_list[len(Dynamic_list) - 1]:
            if Dynamic_list[len(Dynamic_list)-1][word_tag][0] > largest_probability:
                largest_probability = Dynamic_list[len(Dynamic_list)-1][word_tag][0]
                largest_key = word_tag
        temp_list = []
        last_state = largest_key
        for i in range(len(Dynamic_list)-1, -1, -1):
            temp_list.append(last_state)
            if i >= 1:
                last_state = (sentence[i-1], Dynamic_list[i][last_state][1])
        temp_list.reverse()
        predicts.append(temp_list)
    return predicts