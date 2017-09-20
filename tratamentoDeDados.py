# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 16:19:41 2017

@author: eduai_000
"""

import numpy as np
import re
from collections import deque
from functools import cmp_to_key
PLAYERS = {0:'E', 1:'S', 2:'W', 3:'N'}
SUITMAP = {'S':0, 'H':1, 'D':2, 'C':3}
##added by me
SUITS = ['S', 'H', 'D', 'C', 'N'] ## N for no out of range exception
##
CARDMAP = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}

# for readability...
def rindex(list, elt):
    '''Get the index of the last position matching elt in list

    inputs:
        list: list
        elt: an element inside list

    outputs:
        int
    '''
    
    return len(list) - list[::-1].index(elt) -1
   

class Card(object):
    """Represents a standard playing card.
    
    Attributes:
      suit: integer 0-3
      rank: integer 2-14
      suitname: str in {'C','D','H','S'}
      rankname: str in {'2','3','4','5','6','7','8','9','10','J','Q','K','A'}

    Constructor takes:
      arg1: integer 0-3 corresponding to suit
      arg2: integer 2-14 corresponding to value
    """

    suit_names = ['C', 'D', 'H', 'S']
    rank_names = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank
        self.suitname = self.suit_names[suit]
        self.rankname = self.rank_names[rank-2]

    def __repr__(self):
        """Returns a human-readable string representation."""
        return '%s%s' % (Card.rank_names[self.rank-2], Card.suit_names[self.suit])

    '''
    NOTE:
    
    default comparison is deliberately not implemented so as
    not to confuse users who may implicitly assume a certain 
    suit rank (which is ambiguous outside of bridge).

    Comparison with flexible suit order is implemented below
    in the compare() method.
    '''
    
    def __eq__(self, other):
        return (self.suit == other.suit and self.rank == other.rank)

    def compare(self, other, sorder=(0,1,2,3)):
        '''
        Python 2-style cmp() operation on Card objects. Note:
        suit order defaults to standard bridge order: Clubs <
        Diamonds < Hearts < Spades.

        suitorder: tuple of suits (numerical) from low-to-high
        '''

        self_srank = sorder.index(self.suit)
        other_srank = sorder.index(other.suit)

        if self==other:
            return 0
        elif (self_srank < other_srank):
            return -1
        elif (self_srank == other_srank) and (self.rank < other.rank):
            return -1
        else:
            return 1

class Hand(object):
    """Represents a hand/deck of cards.

    Args:
        initial: list of Card objects

    Attributes:
        cards: list of Card objects.
    """
    
    def __init__(self, initial=None):
        if initial is None:
            self.cards = []
        else:
            self.cards = initial

    def __repr__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return ','.join(res)

    def __getitem__(self, item):
        '''Implementing getitem so that we get iteration and slicing'''
        return self.cards[item]

    def __len__(self):
        return len(self.cards)

    def has(self, other):
        '''Checks whether a Card (other) is in hand'''
        return (other in self.cards)

    def add_card(self, card):
        """Adds a card to the deck."""
        self.cards.append(card)

    def remove_card(self, card):
        """Removes a card from the deck."""
        self.cards.remove(card)
    
    def pop_card(self, i=-1):
        """Removes and returns a card from the deck.

        i: index of the card to pop; by default, pops the last card.
        """
        return self.cards.pop(i)
    
    def sort(self, sorder=(0,1,2,3)):
        """Since comparison is not implemented for Card we
        have to implement card order here. Note that suitorder
        must be passed to the compare method of Card.

        suitorder: tuple of suits (numerical) from low-to-high
        """

        keyfunc = cmp_to_key(lambda x,y: x.compare(y, sorder))

        return Hand(initial=sorted(self, key=keyfunc))

##starts to read from the first S and returns the strings for hands and entame
def pretreat(horribleInput):
    horribleInput = horribleInput.upper()
    
    begin = horribleInput.find(SUITS[0]) ##beginning of hands, namely the first spades that he encounters
    if(begin == -1):
        print("couldnt find 'S' in the horrible input");
    args = horribleInput[begin:].split('|')
    if(len(args) != 2):
        print("there was more than one '|' after the first S(spades)")
    if(len(args[0]) != 71):
        print("the collection of hands(17 chars in each and 3 commas) has a weird length:" + len(args[0]))
    if(len(args[1]) != 2):
        print("entame with plus than 2 chars")
    return args[0], args[1]

#magic! returns vector from text format hand
def vectorizing(handText):
    hand = np.zeros(53)
    end = 0   #should see if its S
    for suit in range(4):
        begin = end + 1
        end = handText.find(SUITS[suit+1])
        for i in range(begin,end):
            hand[suit*13 + CARDMAP[handText[i]]-2] = 1
    return hand
        
# colocar um nome melhor
#return who entamed, in terms of S, W, E, N, with the players hands in the orther they`ll be played
def treatingDudu(horribleInput):
    #handsText com in the format [13],...
    #uniformilizing the inputs
    handsText, entame = pretreat(horribleInput)
    print(handsText)
    print(entame)
    handsText = handsText.split(',')
    suitEntame = entame[0]
    rankEntame = entame[1]
    suitCode = SUITMAP[suitEntame]
    nextSuit = SUITS[suitCode + 1]
    #hands = np.zeros((4, 53))
    #print(suitEntame, nextSuit)
    hands = []
    for h in range(len(handsText)):
        
        begin = handsText[h].index(suitEntame)
        end = handsText[h].find(nextSuit)
        #print(end)
        if(end == -1):
            end = len(handsText[h])
        if(handsText[h][begin:end].find(rankEntame) != -1):
            found = h
            #print(h)
            break
    for h in range(len(handsText)):
        hands.append(vectorizing(handsText[(found+h)%len(handsText)]))
        
    
    #print(found)
    #print(PLAYERS[found])
    
    return PLAYERS[found], hands

#appele treating pour une 'file'
def archiveTreat(filename):
    terribleArchive = open(filename, 'r')
    horribleInputs = terribleArchive.read().split('\n')
    return [treatingDudu(inp) for inp in horribleInputs]
    
#horribleInput = "SAK62H32DAKT6CA84,SJT7HAJ4DQJ982C63,S83HT876D75CKQ752,SQ954HKQ95D43CJT9|DQ"

filename = "terrificInput.txt"
print(archiveTreat(filename))
#print(treatingDudu(horribleInput))