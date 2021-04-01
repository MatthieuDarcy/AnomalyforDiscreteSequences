#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 09:39:41 2021

@author: mathieudagreou
"""

import numpy as np
import zipfile
import os

def build_Tk(sequence,k):
    Tk = []
    l_sequence = len(sequence)
    for w in range(l_sequence-k):
        Tk.append(sequence[w:w+k])
    return(Tk)

def frequency_score(Tk):
    unique_Tk = np.unique(Tk)
    n_windows = Tk.shape[0]
    frequences = np.zeros((n_windows,1))
    for w in unique_Tk:
        frequences[Tk == w] = 1/((Tk==w).sum())
    return(frequences)

def CDM(A,B):
    
    # Compression of A and B
    a = open("A.txt", "wb")
    b = open("B.txt", "wb")
    a.write(A.encode('ascii'))
    b.write(B.encode('ascii'))
    a.close()
    b.close()
    zipfile.ZipFile('A.zip','w',zipfile.ZIP_DEFLATED).write("A.txt")
    zipfile.ZipFile('B.zip', 'w',zipfile.ZIP_DEFLATED).write("A.txt")
    
    # Compression of the concatenation of A and B
    ab = open("AB.txt", "wb")
    C = A+B
    ab.write(C.encode('ascii'))
    ab.close()
    zipfile.ZipFile('AB.zip', 'w', zipfile.ZIP_DEFLATED).write("AB.txt")
    
    return(os.path.getsize("AB.zip")/(os.path.getsize("A.zip")+os.path.getsize("B.zip")))


def kolmogorov_anomaly(data):
    loc_anomaly = 0
    while len(data)>2:
        l = len(data)
        left_cdm = CDM(''.join(data[0:l//2]),''.join(data));
        right_cdm = CDM(''.join(data[l//2:]),''.join(data));
        
        if left_cdm < right_cdm:
            loc_anomaly += l//2
            data = data[l//2:]
        else:
            data = data[0:l//2]
    return(loc_anomaly)
            
        

