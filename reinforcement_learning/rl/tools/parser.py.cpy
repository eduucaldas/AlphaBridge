from ctypes import *
import hands
from enums import MYMAP

dds = CDLL("./libdds.so")

class ddTableResults(Structure):
    _fields_ = [
        ("resTable", c_int * 5 * 4)
        ]

class ddTableDealPBN(Structure):
    _fields_ = [
        ("cards", c_char * 80)
        ]
    

InitStart = dds.InitStart
InitStart.argtypes = [c_int, c_int]
    
CalcDDtablePBN = dds.CalcDDtablePBN
CalcDDtablePBN.argtypes = [ddTableDealPBN, POINTER(ddTableResults)]

mydeal = ddTableDealPBN()
mydeal.cards = hands.PBN

res = ddTableResults()
myres = pointer(res)


def hand_to_pbn(hand):
    l = [[],[],[],[]]
    for c in hand:
        l[c//13] += MYMAP[c % 13]
    s = "".join(l[0])
    h = "".join(l[1])
    d = "".join(l[2])
    c = "".join(l[3])
    return ".".join([s,h,d,c]) 

def hands_to_pbn(hands):
    hands.sort()
    hands.reverse()
    south = hand_to_pbn(hands[:13])
    west = hand_to_pbn(hands[13:26])
    north = hand_to_pbn(hands[26:39])
    east = hand_to_pbn(hands[39:])
    res = "N:{north} {west} {south} {east}".format(north=north, west=west, south=south, east=east)
    return bytes(res, 'utf8')

def calc_table(pbn_hands):
    deal = ddTableDealPBN()
    deal.cards = pbn_hands

    res = ddTableResults()
    myres = pointer(res)

    x = CalcDDtablePBN(deal, myres)
    y = list(res.resTable)
    return [list(z) for z in y]
    
