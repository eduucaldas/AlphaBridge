# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 14:40:38 2018

@author: pepou
"""
import numpy as np
import pandas as pd
import data.enums
import data.parser
from time import time

def search(df, bidding):
    bidding = bidding.split(",")
    query_string = " & ".join(
            ["bidding{i} == {bid}".format(i=i+1,bid=data.enums.BIDSMAP[bidding[i]]) for i in range(len(bidding))]
            )
    dfq = df.query(query_string)
    return dfq

def compatible_bids(seq):
    last = None
    s = seq.split(",")
    for k in range(len(s) - 1, -1, -1):
        if s[k] != "P":
            last = s[k]
            break
    if last == None or seq == "":
        return [x for x in data.enums.BIDSMAP]
    else:
        res = ["P","R","D"]
        seuil = data.enums.BIDSMAP[last]
        for x in data.enums.BIDSMAP:
            if data.enums.BIDSMAP[x] > seuil:
                res.append(x)
        return res

def itere(df, seq, leaves, pseudoLeaves, sons, nodes):
    n = len(seq)
    if len(seq) > 7 and seq[n-5:] == "P,P,P":
        leaves.append(seq)
    else:
        for x in compatible_bids(seq):
            if seq == "":
                bid = x
            else:
                bid = seq+","+x
            bidding = bid.split(",")
            query_string = " & ".join(
                    ["bidding{i} == {bid}".format(i=i+1,bid=data.enums.BIDSMAP[bidding[i]]) for i in range(len(bidding))]
                    )
            dfq = df.query(query_string)
            if len(dfq) == 0:
                del dfq
            elif len(dfq) <= 300:
                nodes[bid] = len(dfq)
                sons[seq].append(bid)
                if len(bid) > 5 and bid[n-5:] == "P,P,P":
                    leaves.append(bid)
                else:
                    pseudoLeaves.append(bid)
                del dfq
            else:
                nodes[bid] = len(dfq)
                sons[seq].append(bid)
                sons[bid] = []
                itere(dfq, bid, leaves, pseudoLeaves, sons, nodes)
                del dfq

def construct_tree():
    
    database = pd.read_hdf('store.hdfs')
    leaves = []
    pseudoLeaves = []
    nodes = {} # nombre de donnes associées à chaque séquence
    sons = {}
    sons[""] = []
    itere(database, "", leaves, pseudoLeaves, sons, nodes)
    return leaves, pseudoLeaves, sons, nodes
    
    
def main():
    
#    t = time()
#    (leaves, pseudoLeaves, sons, nodes) = construct_tree()
#    print("Temps de construction de l'arbre :\n" + str(time() - t))
    print()
    
if __name__ == '__main__':
  main()
    