# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 22:05:51 2021

@author: matth
"""
import numpy as np
def kMedoids(D, k, tmax=100):
    # determine dimensions of distance matrix D
    
    m, n = D.shape
    
    # randomly initialize an array of k medoid indices
    idx = np.arange(m)
    M = np.sort(np.random.choice(idx, replace = False, size = k), axis = None)
    
    # create a copy of the array of medoid indices
    Mnew = np.copy(M)
    
    # initialize a dictionary to represent clusters
    C = {}
    
    for t in range(tmax):
        # determine clusters, i.e. arrays of data indices
        J = np.argmin(D[:,M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J==kappa)[0]

        # update cluster medoids
        for kappa in range(k):
            J = np.mean(D[np.ix_(C[kappa],C[kappa])],axis=1)
            
            j = np.argmin(J)
            Mnew[kappa] = C[kappa][j]
        np.sort(Mnew)
        
        # check for convergence
        
        if np.array_equal(M, Mnew):
            break
        M = np.copy(Mnew)
    
    else:
        # final update of cluster memberships
        J = np.argmin(D[:,M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J==kappa)[0]
    
    return M, C


if __name__ == "__main__":
    
    D = np.random.random(size = (10,10))

    for i in range(D.shape[0]):
        D[i,i] = 0
        for j in range(i,D.shape[0]):
            D[j,i] = D[i,j]
        

    M, C = kMedoids(D, 7)

    print(M, C)

