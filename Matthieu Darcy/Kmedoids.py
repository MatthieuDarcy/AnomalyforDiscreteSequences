# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 22:05:51 2021

@author: matth
"""
import numpy as np

def heuristic_init(D, k):
    return np.argpartition(np.sum(D, axis=1), k - 1)[:k]
    
def kMedoids(D, k, tmax=100, init = "heuristic"):
    # determine dimensions of distance matrix D
    
    m, n = D.shape
    
    if init == "heuristic":
        M = heuristic_init(D, k)
        
    elif init == "random":
        idx = np.arange(D.shape[0])
        M = np.sort(np.random.choice(idx, replace = False, size = k), axis = None)
    else: 
        print("Error initialization method")
    
    # create a copy of the array of medoid indices
    Mnew = np.copy(M)
    
    # initialize a dictionary to represent clusters
    C = {}
    #print(M)
    for t in range(tmax):
        # determine clusters, i.e. arrays of data indices
        J = np.argmin(D[:,M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J==kappa)[0]
        
        #print(J, C)
        
        # update cluster medoids
        
        for kappa in range(k):
            J_new = np.mean(D[np.ix_(C[kappa],C[kappa])],axis=1)
            #print("cluster", C[kappa])
            #print("J", kappa, J_new)
            j = np.argmin(J_new)
            Mnew[kappa] = C[kappa][j]
        np.sort(Mnew)
        
        # check for convergence
        
        if np.array_equal(M, Mnew):
            break
        M = np.copy(Mnew)
        J = np.copy(J_new)
    
    else:
        # final update of cluster memberships
        J = np.argmin(D[:,M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J==kappa)[0]
    
    print("Terminated in {} iterations".format(t))
    return M, C


if __name__ == "__main__":
    np.random.seed(0)
    D = np.random.random(size = (10,10))

    for i in range(D.shape[0]):
        D[i,i] = 0
        for j in range(i,D.shape[0]):
            D[j,i] = D[i,j]
        

    M, C = kMedoids(D, 5)

    print(M, C)

