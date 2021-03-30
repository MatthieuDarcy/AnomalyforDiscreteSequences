# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 13:09:24 2021

@author: matth
"""

import numpy as np
# Builds the transition matrix and base measure of a markov system (probabilities are estimated using frequency)

# A in the alphabet, X the data shape = (n, 1)
# returns P (transition matrix) and Q (base measure)

# Everything is string based

def compute_markov_chain(A, X):
    n_alphabet = A.shape[0]
    P = np.zeros(shape = (n_alphabet, n_alphabet))
    Q = np.zeros(shape= (n_alphabet,1))
    
    # Coumpute N (total number of letters)
    N = 0
    for word in X:
        N += len(word[:-1])
    print(N)
    
    for i, letter in enumerate(A): 
        total_occurence = 0
        # First compute the unnormalized measure Qi 
        for word in X:
            total_occurence += word[:-1].count(letter)
        
        Q[i] = total_occurence
    
    # Compute the transition probabilities
    for i, letter_1 in enumerate(A):
        for j, letter_2 in enumerate(A):
            substring = letter_1 + letter_2
            p = 0
            
            # If the occurence of the letter i is 0, then probability of the transition is 0
            if Q[i]== 0:
                P[:, i] = 0
                P[i,i] = 1
            else:
                for l, word in enumerate(X):
                    p += word.count(substring)
                P[j, i] = p/Q[i]
            
    return Q/N, P

def compute_probability(X_test, A, Q, P):
    prob = np.zeros(X_test.shape[0])
    
    for i, word in enumerate(X_test):
        prob_word = 0
        for j, letter in enumerate(word):
            # For the first letter, the probability is the base probability
            if j == 0:
                idx = np.where(A == letter)[0]
                prob_word += Q[idx, 0]
            else:            
                # Look up the next letter
                idx_next = np.where(word == letter)[0]
                print(idx_next)
                prob_word *= P[idx_next, idx]
                idx = idx_next
                
        print(prob_word)        
        prob[i] = prob_word
    return prob
            


