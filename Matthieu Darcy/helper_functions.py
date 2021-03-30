# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 18:33:40 2021

@author: matth
"""


import numpy as np

# pairwise distance calculator
def pairwise_distance(X, metric, Y = None):
    # Assumes input X = (n,1) n i the number of points
    n = X.shape[0]
    if Y is None:
        distance_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i,n):
                distance_matrix[i,j] = metric(X[i], X[j])
                distance_matrix[j,i] = distance_matrix[i,j]
    else:
        m = Y.shape[0]
        distance_matrix = np.zeros((n, m))
        
        for i in range(n):
            for j in range(m):
                distance_matrix[i,j] = metric(X[i], Y[j])
        
    
    return distance_matrix


# Dynamic Programming implementation of LCS problem

# Input: array X, Y containing one string
def lcs(X, Y):
    # find the length of the strings
    
    if type(X) == list or type(X) == np.ndarray:
        X = X[0]
        Y = Y[0]
    m = len(X)
    n = len(Y)

    # declaring the array for storing the dp values
    L = [[None]*(n + 1) for i in range(m + 1)]

    """Following steps build L[m + 1][n + 1] in bottom up fashion
    Note: L[i][j] contains length of LCS of X[0..i-1]
    and Y[0..j-1]"""
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0 :
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1]+1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])

    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
    return L[m][n]
# end of function lcs

# normalized lcs score
def nLCS(X,Y):
    if type(X) == list or type(X) == np.ndarray:
        X = X[0]
        Y = Y[0]
    
    m = len(X)
    n = len(Y)
    l = lcs(X,Y)
    
    return l /np.sqrt(m*n)

def add_spaces(X):
    return np.array([word + ' ' for word in X])


