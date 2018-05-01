# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 12:02:36 2018

@author: pepou
"""

import numpy as np

def longest_color(X):
    c = [0, 0, 0, 0]
    for k in range(4):
        for i in range(13):
            c[k] += X[13*k + i]
    maxi = np.argmax(c)
    res = [0]*4
    res[maxi] = 1
    return res

points = ([0]*9+[1, 2, 3, 4]) * 4

def strongest_color(X):
    c = [0, 0, 0, 0]
    for k in range(4):
        for i in range(13):
            c[k] += X[13*k + i] * points[13*k+i]
    maxi = np.argmax(c)
    res = [0]*4
    res[maxi] = 1
    return res

def high_low(lead):
    if lead % 13 < 10:
        return [1, 0]
    return [0, 1]

def add_color(X, y):
    
    x = []
    Y = []
    for k in range(len(X)):
        color = y[k] // 13
        y_=[0]*4
        y_[color] = 1
        [a, b, c, d] = y_
        x.append(np.concatenate([X[k][:13], [a], X[k][13:26], [b], X[k][26:39], [c], X[k][39:], [d]]))
        Y.append(high_low(y[k]))
        
    return np.array(x), np.array(Y)
    
    