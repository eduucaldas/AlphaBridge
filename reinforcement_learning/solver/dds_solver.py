from solver import dds
from utils.deal import convert_deal
import numpy as np
import ctypes

class Solver:
    def __init__(self, deal, m=5):
        dds.SetMaxThreads(0)
        self.deal = deal
        self.m = m
    
    def solve(self, bidding):
        tableDealPBN = dds.ddTableDealPBN()
        table = dds.ddTableResults()
        myTable = ctypes.pointer(table)
        tableDealPBN.cards = convert_deal(self.deal)
        res = dds.CalcDDtablePBN(tableDealPBN, myTable)
        if res != dds.RETURN_NO_FAULT:
            raise NameError('Solving Error')
        else:
            score = list(map(list,myTable.contents.resTable))
            score = [score[i][0] for i in range(5)]
            return score[bidding]
        
    def mean_solve(self, bidding):
        score = 0
        for _ in range(self.m):
            np.random.shuffle(self.deal[26:])
            table = self.solve(bidding)
            score += table
        return score/self.m
        
    
