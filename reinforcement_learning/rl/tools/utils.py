import rl.tools.dds as dds
import ctypes
from data.enums import CMAP
from multiprocessing import Pool
import numpy as np
    
def convert_card(n):
    return CMAP[n % 13], n//13

def convert_hand(hand):
    cards = [[], [], [], []]
    for c in hand:
        card, color = convert_card(c) 
        cards[color] += card
    res = []
    for c in cards:
        c.reverse()
        res.append("".join(c))
    return ".".join(res)


def hands_to_pbn(hands):
    south = convert_hand(hands[:13])
    west = convert_hand(hands[13:26])
    north = convert_hand(hands[26:39])
    east = convert_hand(hands[39:])
    res = "N:{north} {east} {south} {west}".format(north=north, east=east, south=south, west=west)
    return bytes(res, 'utf8')

"""
      North South East  West 
   NT     0     0     0     0
    S     0     0     0     0
    H     0     0     0     0
    D     0     0     0     0
    C     0     0     0     0
"""
def convert_table(myTable):
    l = list(map(list,myTable.contents.resTable))
    t = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
    t[0][0] = l[0][4]
    t[0][1] = l[2][4]
    t[0][2] = l[1][4]
    t[0][3] = l[3][4]
    for suit in range(4):
        t[suit+1][0] = l[0][suit]
        t[suit+1][1] = l[2][suit]
        t[suit+1][2] = l[1][suit]
        t[suit+1][3] = l[3][suit]
    return t

def solve_pbn(pbn):
    tableDealPBN = dds.ddTableDealPBN()
    table = dds.ddTableResults()
    myTable = ctypes.pointer(table)
    tableDealPBN.cards = pbn
    res = dds.CalcDDtablePBN(tableDealPBN, myTable)
    return convert_table(myTable)

def solve_deal(hands):
    pbn = hands_to_pbn(hands)
    return solve_pbn(pbn)


class Solver(object):

    def __init__(self):
        dds.InitStart(2, 4)
        self.tableDealPBN = dds.ddTableDealPBN()
        self.table = dds.ddTableResults()
        self.myTable = ctypes.pointer(self.table)

    def score1(self, trump, north, south, we):
        hands = np.concatenate((north, we[:13], south, we[13:]))
        s = self.solve(hands)
        return max([s[i][0] for i in range(5)]) - s[trump][0]

    def score2(self, north, south, we):
        hands = np.concatenate((north, we[:13], south, we[13:]))
        s = self.solve(hands)
        return np.max(s) - s

    def mean_score2(self, n, north, south, we):
        res = [self.score2(north, south, np.random.permutation(we)) for _ in range(n)]
        return sum(res)/n
    
    def mean_score(self, n, trump, north, south, we):
        res = [self.score1(trump, north, south, np.random.permutation(we)) for _ in range(n)]
        return sum(res)/n
    
    def solve(self, hands):
        hands = [int(k) for k in hands]
        self.tableDealPBN = dds.ddTableDealPBN()
        self.table = dds.ddTableResults()
        self.myTable = ctypes.pointer(self.table)
        self.tableDealPBN.cards = hands_to_pbn(hands)
        res = dds.CalcDDtablePBN(self.tableDealPBN, self.myTable)
        return convert_table(self.myTable)
