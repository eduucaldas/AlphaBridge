'''
parsingFromVector.py

Last updated: 10/04/17
Author: Eduardo Caldas

This script:
    defines 2 functions:
        pick_hands: gives hands of players from a handsTxt
        pick_entame: gives the leader and rotates hands to order of playing
'''
    
import numpy as np

#list of all commands in the lin files
commands = {'md':0, 'sv':1, 'pc':2, 'mb':3, 'qx':4, 'mc':5, 'pg':6, 'nt':7, 'vg':8, 'rs': 9, 'pn': 10, 'an':11, 'ob':12, 'st': 13, '': 14}

#from observation order of hands is always: SWNE
PLAYERS = {0:'S', 1:'W', 2:'N', 3:'E'}
#from observation order of suits is always: SHDC
SUITMAP = {'S':0, 'H':1, 'D':2, 'C':3}

OUT_OF_RANGE = 'U'# dirty trick: U for no out of range exception in SUITS
SUITS = ['S', 'H', 'D', 'C', OUT_OF_RANGE] 
#this is how the cards are described in the .lin
CARDMAP = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}

#for later purposes##################
BIDS = {}
#####################################

#resume of meaning for lin files
#qx -> begin game
#md -> show hands
#sv -> start bidding
#mb -> make bid
#pc -> next card
#pg -> next line, followed by ||
#mc -> finish game

#Count where the error occurred, e.g. if it was in dealer
errorLog = {'dealer':0, 'hands': 0,'entame': 0, 'bid':0, 'leader':0}
#we can perhaps implement it to show in which file the error occurred occurred

#for readability and making it easier to change after :)
error = {'dealer':-1, 'hands': None, 'entame': None, 'bid':None, 'leader':-1}

"""
Auxiliar functions#############################################################
"""
def vectorizing(handText):
    """
    input:
       string in format:"SKT32HJ984DJT52C9"
    comments:
       Here i do a dirty trick, i add a char OUT_OF_RANGE to handText
       so that when we have an indicator of the end of hand.
    output:
       hand:
           HandVector = 52-binary vector, with ones when the player has the card
    """
    hand = np.zeros(52, dtype=bool)
    end = 0   #should see if its S
    handText = handText + OUT_OF_RANGE #adds stopping character
    for suit in range(4):
        begin = end + 1
        end = handText.find(SUITS[suit+1])
        if(end == -1 or end < begin): #then we haven`t found the next suit, which is a problem according to our format
            errorLog['hands']+=1
            return error['hands']
        for i in range(begin,end):
            if not (handText[i] in CARDMAP):
                errorLog['hands'] += 1
                return error['hands']
            else:
                hand[suit*13 + CARDMAP[handText[i]]-2] = True
    #take out our OUT_OF_RANGE? not necessary :)
    return hand


def vectorizing3(handsText):
    """
    input:
       string in format:"SKT32HJ984DJT52C9,SAQJ86HK63DK93C75,S94HT5D864CAQJT62"
    comments:
    output:
       4 HandVectors
    """
    handsText = handsText.split(',')
    
    for hT in handsText:
        if(len(hT) != 17):
            errorLog['hands'] += 1
            return error['hands']
    
    hands = []
    for handT in handsText:
        h = vectorizing(handT)
        if(h == None):
            return error['hands']
        else:
            hands.append(h)
    
    one = np.ones(len(hands[0]), dtype=bool)
    hands.append(one ^ hands[0] ^ hands[1] ^ hands[2])#appends the missing hand
    #may need to verify if hands[3] is valable
    return hands
"""
###############################################################################
"""

def pick_hands(gameLine):
    """
    input: 
       string in format:"1SKT32HJ984DJT52C9,SAQJ86HK63DK93C75,S94HT5D864CAQJT62,S75HAQ72DAQ7CK843"
                         or "1SKT32HJ984DJT52C9,SAQJ86HK63DK93C75,S94HT5D864CAQJT62"
    comments:
       First integer =  for the dealer in the format [1-4], where 4 is E
       Sometimes there`s only 3 hands, since the forth is redundant
       There`s always the suit indicator, even when there are no cards of the suit.
    output:
       dealer::
           in the format [0-3], where 3 is E
       vector of hands:
           4 HandVectors
    """
    gameLine = gameLine.upper()
    dealer = error['dealer']
    hands = error['hands']
    begin = gameLine.find(SUITS[0]) ##beginning of hands, namely the first spades that he encounters
    if(begin == 1):
        if(int(gameLine[0]) < 1 or int(gameLine[0]) > 4):
            errorLog['dealer'] += 1
        else:
            handsText = gameLine[1:]
            dealer = int(gameLine[0]) - 1#puts dealer in the format we want
            if(len(handsText) == 71 or len(handsText) == 53):
                #in the case of 4 hands, reduce it to 3 and solve
                handsText = handsText[:53]
                hands = vectorizing3(handsText)
            else:
                errorLog['hands'] += 1
    else:
        errorLog['dealer'] += 1
       
    return dealer, hands




def pick_entame(handsText, entame, hands):
    """
    input: 
       hands in the text format, entame as string, hands in vector format
    comments:
       hands in text format, because it`s easier to find cards in this format
       we suppose handsText is in the good format, since otherwise we`d already have an error handling in pick_hands
    output:
        leader:
           may be error['leader'] if there`s a problem with entame formatting
           format: [0-3] according to PLAYERS
        hands: 
           4 HandVectors in the order they`ll be played
    """
    handsText = handsText[1:].upper().split(',')
    suitEntame = entame[0].upper()
    rankEntame = entame[1].upper()
    if(suitEntame in SUITMAP and rankEntame in CARDMAP):
        suitCode = SUITMAP[suitEntame]
        nextSuit = SUITS[suitCode + 1]
        leader = 3 # if we dont find the entame below the leader gotta be the 4 guy
        for h in range(len(handsText)):      
            #print(h)
            begin = handsText[h].find(suitEntame)
            end = handsText[h].find(nextSuit)
            if(end == -1):
                end = len(handsText[h])
            if(handsText[h][begin:end].find(rankEntame) != -1):
                leader = h #here we found the guy that entamed, the leader
                break
        hands = np.roll(hands, leader)
    else:
        errorLog['entame'] += 1
        leader = error['leader'] 
    
    return leader, hands

"""
Dudu
###############################################################################
"""
"""

hand_ex = "1SKT32HJ984DJT52C9,SAQJ86HK63DK93C75,S94HT5D864CAQJT62"
entame = "SJ"
dealer, hands = pick_hands(hand_ex)
leader, hands = pick_entame(hand_ex, entame, hands)
print(hands.nbytes)
print(hands, PLAYERS[leader], dealer, entame,)
print(errorLog)	
"""
