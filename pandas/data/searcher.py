#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 11:39:33 2018

@author: scander.mustapha
"""
import pandas as pd
import numpy as np

BIDSMAP = {
            'P': 0, 'R': 1, 'D': 2,
           '1N': 3, '1S': 4, '1H': 5, '1D': 6, '1C': 7,
           '2N': 8, '2S': 9, '2H': 10, '2D': 11, '2C': 12,
           '3N': 13, '3S': 14, '3H': 15, '3D': 16, '3C': 17,
           '4N': 18, '4S': 19, '4H': 20, '4D': 21, '4C': 22,
           '5N': 23, '5S': 24, '5H': 25, '5D': 26, '5C': 27,
           '6N': 28, '6S': 29, '6H': 30, '6D': 31, '6C': 32,
           '7N': 33, '7S': 34, '7H': 35, '7D': 36, '7C': 37
           }

def vectorize_hand(hand):
    v = np.zeros(52)
    for c in hand:
        v[c] = 1
    return v

def leader_hand(i,leader, south, west, north, east):
    p = leader[i]
    if p == 0:
        return south[i]
    elif p == 1:
        return west[i]
    elif p == 2:
        return north[i]
    else:
        return east[i]

def search_bidding(bidding):
    df = pd.read_hdf('./data/store.hdf5')
    bidding = bidding.split(",")
    query_string = " & ".join(
            ["bidding{i} == {bid}".format(i=i+1,bid=BIDSMAP[bidding[i]]) for i in range(len(bidding))]
            )
    dfq = df.query(query_string)
    del df
    south = list(dfq[["south{i}".format(i=i) for i in range(1,14)]].values)
    west = list(dfq[["west{i}".format(i=i) for i in range(1,14)]].values)
    north = list(dfq[["north{i}".format(i=i) for i in range(1,14)]].values)
    east = list(dfq[["east{i}".format(i=i) for i in range(1,14)]].values)
    leader = dfq.leader.values
    leader = [leader_hand(i, leader, south, west, north, east) for i in range(len(leader))]
    lead = list(dfq.lead.values)
    return pd.DataFrame({"south":south,"west":west,"north":north,"east":east,"leader":leader,"lead":lead})