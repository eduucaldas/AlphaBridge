# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 16:19:41 2017

@author: eduai_000
"""
##you gotta take out the newline in the beginning of the file
import numpy as np

PLAYERS = {0:'E', 1:'S', 2:'W', 3:'N'}
SUITMAP = {'S':0, 'H':1, 'D':2, 'C':3}
##added by me
SUITS = ['S', 'H', 'D', 'C', 'N'] ## N for no out of range exception
##
CARDMAP = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}

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
    return hand[0]
        
# colocar um nome melhor
#return who entamed, in terms of S, W, E, N, with the players hands in the orther they`ll be played
def treatingDudu(horribleInput):
    #handsText com in the format [13],...
    #uniformilizing the inputs
    handsText, entame = pretreat(horribleInput)
    #print(handsText)
    #print(entame)
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
    
    return entame, hands[0] ##,PLAYERS[found]

#appele treating pour une 'file'
def archiveTreat(filename):
    terribleArchive = open(filename, 'r')
    horribleInputs = terribleArchive.read().split('\n')
    return [treatingDudu(inp) for inp in horribleInputs]
    
#horribleInput = "SAK62H32DAKT6CA84,SJT7HAJ4DQJ982C63,S83HT876D75CKQ752,SQ954HKQ95D43CJT9|DQ"
#print(treatingDudu(horribleInput))
filename = "temp_final.DAT"
vectorForZigfrid = archiveTreat(filename)

