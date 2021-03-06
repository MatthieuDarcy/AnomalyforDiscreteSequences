# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 23:33:12 2021

@author: matth
"""
import numpy as np
from helper_functions import pairwise_distance

# Compute the distance to the nearest k neighbor

# Input: D distance pairwise matrix, k: kth nearest neighbor
def distance_k_neighbor(D, k):
    n_points = D.shape[0]
    distance = np.zeros(n_points)
    
    distance = np.partition(D, axis = -1, kth = k)[:, k]
    return distance

# D is the distance matrix, C the clusters, M the medoids
def distance_clusters(D, C, M ):
    distance = np.zeros(D.shape[0])
    for c in C:
        cluster = C[c]
        m = M[c]
        distance[cluster] =  D[cluster][:, m]
    return distance
        
def assign_to_cluster(X_test, M, metric):
    # Compute the similarity
    dist = pairwise_distance(X_test, metric, Y = M)

    assign = np.argmax(dist, axis = 1)
    
    return assign, np.max(dist, axis = -1)