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
def compute_occ_same_letter(string, letter):
    count = 0
    for i, element in enumerate(string):
        if element == letter and i < len(string)-1:
            if string[i+1] == letter:
                count += 1
    return count
#%%
def compute_occ_letter(string, letter):
    count = 0
    len_string = len(string)
    len_letter = len(letter)
    for i in range(len(string)- len_letter):
        substring = string[i: i + len_letter]
        if substring == letter:
            count += 1
    return count

#%%          
def compute_markov_chain(A, X):
    n_alphabet = A.shape[0]
    P = np.zeros(shape = (n_alphabet, n_alphabet))
    Q = np.zeros(shape= (n_alphabet,1))
    
    # Coumpute N (total number of letters)
    N = 0

    
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
            elif letter_1 == letter_2:
                for l, word in enumerate(X):
                    p += compute_occ_same_letter(word, letter_1)
            else:
                for l, word in enumerate(X):
                    p += word.count(substring)
            
            if p != 0:
                P[j, i] = p/Q[i]
            
    return Q/np.sum(Q), P

def compute_markov_chain_multi(A, A_letter, X):
    n_alphabet = A.shape[0]
    n_letter =A_letter.shape[0]
    P = np.zeros(shape = (n_letter, n_alphabet))
    Q = np.zeros(shape= (n_alphabet,1))

    
    for i, letter in enumerate(A): 
        total_occurence = 0
        # First compute the unnormalized measure Qi 
        for word in X:
            total_occurence += compute_occ_letter(word[:-1], letter)
        
        Q[i] = total_occurence
    
    # Compute the transition probabilities
    for i, letter_1 in enumerate(A):
        for j, letter_2 in enumerate(A_letter):

            substring = letter_1 + letter_2
            p = 0
            
            # If the occurence of the letter i is 0, then probability of the transition is 0
            if Q[i]== 0:
                P[:, i] = 0
            elif letter_1 == letter_2:
                print("same")
                for l, word in enumerate(X):
                    p += compute_occ_same_letter(word, letter_1)
            else:
                for l, word in enumerate(X):
                    p += compute_occ_letter(word, substring)
            
            if p != 0:
                P[j, i] = p/Q[i]
            
    return Q/np.sum(Q), P
    

def compute_probability(X_test, A, Q, P):
    prob = np.zeros(X_test.shape[0])
    
    for i, word in enumerate(X_test):
        prob_word = 0
        for j, letter in enumerate(word):
            # For the first letter, the probability is the base probability
            if j == 0:
                idx = np.where(A == letter)[0][0]
                prob_word += Q[idx, 0]
                
                # Look up the next letter
                next_letter = word[j+1]
                idx_next = np.where(A == next_letter)[0][0]
                prob_word *= P[idx_next, idx]
                # Set the index to be the next one
                idx = idx_next
            elif j < len(word)-1:          
                # Look upè the next letter
                next_letter = word[j+1]
                
                # Find the index of the next letter and the TP
                idx_next = np.where(A == next_letter)[0][0]
                prob_word *= P[idx_next, idx]
                # print(letter, next_letter)
                # print(idx_next, idx)
                # print(P[idx_next, idx])
                idx = idx_next
                
        # print(prob_word)        
        prob[i] = prob_word
    return prob
            
def compute_probability_multi(X_test, A , alphabet, Q, P):
    prob = np.zeros(X_test.shape[0])
    n = len(A[0])
    for i, word in enumerate(X_test):
        prob_word = 0
        for j in range(len(word) - n):
            substring = word[j: j + n]
            # For the first letter, the probability is the base probability
            if j == 0:
                idx = np.where(A == substring)[0][0]
                prob_word += Q[idx, 0]
                
                # Look up the next letter
                next_letter = word[j+n]
                idx_next = np.where(alphabet == next_letter)[0][0]
                prob_word *= P[idx_next, idx]
            elif j < len(word)-1:          
                # Look upè the next letter
                next_letter = word[j+n]
                idx = np.where(A == substring)[0][0]
                # Find the index of the next letter and the TP
                idx_next = np.where(alphabet == next_letter)[0][0]
                prob_word *= P[idx_next, idx]

                
        # print(prob_word)        
        prob[i] = prob_word
    return prob
    
if __name__ == "__main__":
    import string
    # alphabet = np.array(list(string.ascii_lowercase))
    # vocab = []
    # for i in range(1000):
    #     word_array = np.random.choice(alphabet, 200, replace = True)
    #     word = ''
    #     for letter in word_array:
    #         word += letter
    #     vocab.append(word)
    # vocab = np.array(vocab)
    # Q, P = compute_markov_chain(alphabet, vocab)
    # print(np.sum(Q))
    # print(np.sum(P, axis = 0))


    alphabet = np.array(np.array(['C', 'A']))
    vocab = []
    #np.random.seed(0)
    for i in range(1000):
        word_array = np.random.choice(alphabet, 5, replace = True)
        word = ''
        for letter in word_array:
            word += letter
        vocab.append(word)
    vocab = np.array(vocab)
    Q, P = compute_markov_chain(alphabet, vocab)
    print(np.sum(Q))
    print(np.sum(P, axis = 0))
    
    from itertools import permutations, combinations_with_replacement


    comb = list(combinations_with_replacement('CA', 2))
    A = []
    temp = []
    for element in comb:
        temp.append(''.join(element))
    for letter in temp:
        for p in permutations(letter):
            A.append(''.join(p))
        
    A = np.unique(np.array(A))

    Q, P = compute_markov_chain_multi(A, alphabet, vocab)
    print(np.sum(Q))
    print(np.sum(P, axis = 0))
    
#%%

    print(compute_probability_multi(np.array([vocab[0]]), A, alphabet, Q, P))
    print(vocab[0])