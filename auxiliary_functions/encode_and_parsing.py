# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 10:18:39 2017

@author: eduai_000
"""
import numpy as np

# list of all commands in the lin files
commands = {'md': 0, 'sv': 1, 'pc': 2, 'mb': 3, 'ob': 4, 'qx': 5, 'mc': 6, 'pg': 7, 'nt': 8, 'vg': 9, 'rs': 10,
            'pn': 11, 'an': 12, 'st': 13}

# from observation order of hands is always: SWNE
PLAYERS = {0: 'S', 1: 'W', 2: 'N', 3: 'E'}
# from observation order of suits is always: SHDC
SUITMAP = {'S': 0, 'H': 1, 'D': 2, 'C': 3}

OUT_OF_RANGE = 'U'  # dirty trick: U for no out of range exception in SUITS
SUITS = ['S', 'H', 'D', 'C', OUT_OF_RANGE]
# this is how the cards are described in the .lin
CARDMAP = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

# SUITSBID = ['N'] + SUITS[:4]
# BIDS = ['P','R','D'] + [str(i + 1) + s for i in range(7) for s in SUITSBID]
BIDS = ['P', 'R', 'D',
        '1N', '1S', '1H', '1D', '1C',
        '2N', '2S', '2H', '2D', '2C',
        '3N', '3S', '3H', '3D', '3C',
        '4N', '4S', '4H', '4D', '4C',
        '5N', '5S', '5H', '5D', '5C',
        '6N', '6S', '6H', '6D', '6C',
        '7N', '7S', '7H', '7D', '7C']
# BIDSMAP = dict(zip(BIDS, range(len(BIDS))))
BIDSMAP = {'P': 0, 'R': 1, 'D': 2,
           '1N': 3, '1S': 4, '1H': 5, '1D': 6, '1C': 7,
           '2N': 8, '2S': 9, '2H': 10, '2D': 11, '2C': 12,
           '3N': 13, '3S': 14, '3H': 15, '3D': 16, '3C': 17,
           '4N': 18, '4S': 19, '4H': 20, '4D': 21, '4C': 22,
           '5N': 23, '5S': 24, '5H': 25, '5D': 26, '5C': 27,
           '6N': 28, '6S': 29, '6H': 30, '6D': 31, '6C': 32,
           '7N': 33, '7S': 34, '7H': 35, '7D': 36, '7C': 37}
# Count where the error occurred, e.g. if it was in dealer
errorLog = {'dealer': 0, 'hands': 0, 'lead': 0, 'bid': 0, 'leader': 0, 'bidding': 0}
# we can perhaps implement it to show in which file the error occurred occurred

# for readability and making it easier to change after :)
error = {'dealer': -1, 'hands': None, 'lead': None, 'bid': None, 'leader': -1, 'bidding': None}


# resume of meaning for lin files
# qx -> begin game
# md -> show hands
# sv -> start bidding
# mb -> make bid
# pc -> next card
# pg -> next line, followed by ||
# mc -> finish game


def pretreatBidding(raw_bidding):
    # input:
    #    list of raw_bid strings
    # comments:
    #    bids should be something in BIDS, not case sensitive and maybe with a '!' at the end, we fiz all this problems
    # output:
    #    list of bid strings, all capitalized and with no '!'
    bidding = []
    for bid in raw_bidding:
        bid = bid.upper()  # fix caseSensitive
        bid = bid.replace("!", "")  # fix '!'
        if (isValidBid(bid)):  # fix: in BIDS
            bidding.append(bid)
        else:
            errorLog['bidding'] += 1
            return error['bidding']

    return bidding


def encodeBid(bid):
    # input:
    #    bid as string.
    # comments:
    #    verifies if valid bid, ie whether its on our BIDS
    # output:
    #    puts in the code according to BIDSMAP
    code = BIDSMAP.get(bid, error['bid'])
    if (code == error['bid']):
        errorLog['bid'] += 1
    return code


def decodeBid(code):
    # input:
    #    bid coded, as an integer [0-37]
    # comments:
    #    Verifies if code is in our BIDS, warning message appears
    # output:
    #    bid as a human readable bid
    try:
        return BIDS[code]
    except IndexError:
        print('your code was weird')
        return error['code']


def encodeBidding(bidding):
    # input:
    #    pretreated bidding as a list of strings
    # comments:
    #
    # output:
    #    code as list of codes coming from each bid
    if (bidding == error['bidding']):
        return error['bidding']
    errorStart = errorLog['bid']
    code = [encodeBid(bidding[i]) for i in range(len(bidding))]
    if (errorLog['bid'] - errorStart == 0):
        return code
    else:
        errorLog['bidding'] += 1
        return error['bidding']


def isValidBid(bid):
    # input:
    #    bid as string
    # comments:
    #    Attention, this verifies only if the bid has the right size, with '!' or not
    # output:
    #    boolean: is it in the proper format
    return (bid in BIDS)


###################Main Functions##########################
def encode_raw_Bidding(raw_bidding):
    # input:
    #    list of raw_bidding, just as they came out from @Ian, like this: ['p', '1D', '1S', '2C', '2S', '3C', 'p', '4C', 'p', '5C', 'p', 'p', 'p']
    # comments:
    #    Look at other functions, has error handling
    # output:
    #    code following BIDSMAP
    bidding = pretreatBidding(raw_bidding)
    return encodeBidding(bidding)


def decodeBidding(code):
    # input:
    #    code fo the bidding
    # comments:
    #    decodeBid has some python error handling :), if there`s a problem it`ll print message
    # output:
    #    bidding as list of strings
    if (code == None):
        return None
    else:
        return [decodeBid(c) for c in code]


#############################################

def testDudu(raw_data):
    # input:
    #    format: "1S|mb|p|mb|2D|mb|p|mb|3S!|mb|p|mb|4H|mb|d|mb|p|mb|p|mb|r|mb|p|mb|4N|mb|p|mb|5H|mb|p|mb|5N|mb|p|mb|6S|mb|p|mb|p"
    # comments:
    #    for the input just pick any .lin and pick the string between the first and the last |mb|
    # output:
    #    prints the bidding list as it was read, the code list, and the bidding decoded from the code
    # raw_data.split("|mb|")
    # print(raw_data)
    code = encode_raw_Bidding(raw_data)
    bidding = decodeBidding(code)
    print(code)
    print(bidding)

# testDudu(['p', '1D', '1S', '2C', '2S', '3C', 'p', '4C', 'p', '5C', 'p', 'p', 'p'])

'''
parsingFromVector.py

Last updated: 10/04/17
Author: Eduardo Caldas

This script:
    defines 2 functions:
        pick_hands: gives hands of players from a handsTxt
        pick_lead: gives the leader and rotates hands to order of playing
'''

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
    end = 0  # should see if its S
    handText = handText + OUT_OF_RANGE  # adds stopping character
    for suit in range(4):
        begin = end + 1
        end = handText.find(SUITS[suit + 1])
        if (
                end == -1 or end < begin):  # then we haven`t found the next suit, which is a problem according to our format
            errorLog['hands'] += 1
            return error['hands']
        for i in range(begin, end):
            if not (handText[i] in CARDMAP):
                errorLog['hands'] += 1
                return error['hands']
            else:
                hand[suit * 13 + CARDMAP[handText[i]] - 2] = True
    # take out our OUT_OF_RANGE? not necessary :)
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
        if (len(hT) != 17):
            errorLog['hands'] += 1
            return error['hands']

    hands = []
    for handT in handsText:
        h = vectorizing(handT)
        if (h == None):
            return error['hands']
        else:
            hands.append(h)

    one = np.ones(len(hands[0]), dtype=bool)
    hands.append(one ^ hands[0] ^ hands[1] ^ hands[2])  # appends the missing hand
    # may need to verify if hands[3] is valable
    return hands


"""
###############################################################################
"""


def pick_hands(game_line):
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
    game_line = game_line.upper()
    dealer = error['dealer']
    hands = error['hands']
    begin = game_line.find(SUITS[0])  # beginning of hands, namely the first spades that he encounters
    if begin == 1:
        if int(game_line[0]) < 1 or int(game_line[0]) > 4:
            errorLog['dealer'] += 1
        else:
            handsText = game_line[1:]
            dealer = int(game_line[0]) - 1  # puts dealer in the format we want
            if len(handsText) == 71 or len(handsText) == 53:
                # in the case of 4 hands, reduce it to 3 and solve
                handsText = handsText[:53]
                hands = vectorizing3(handsText)
            else:
                errorLog['hands'] += 1
    else:
        errorLog['dealer'] += 1

    return dealer, hands


def pick_lead(hands_text, lead, hands):
    """
    input:
       hands in the text format, lead as string, hands in vector format
    comments:
       hands in text format, because it`s easier to find cards in this format
       we suppose handsText is in the good format, since otherwise we`d already have an error handling in pick_hands
    output:
        leader:
           may be error['leader'] if there`s a problem with lead formatting
           format: [0-3] according to PLAYERS
        hands:
           4 HandVectors in the order they`ll be played
    """
    hands_text = hands_text[1:].upper().split(',')
    suitlead = lead[0].upper()
    ranklead = lead[1].upper()
    if (suitlead in SUITMAP and ranklead in CARDMAP):
        suitCode = SUITMAP[suitlead]
        nextSuit = SUITS[suitCode + 1]
        leader = 3  # if we dont find the lead below the leader gotta be the 4 guy
        for h in range(len(hands_text)):
            # print(h)
            begin = hands_text[h].find(suitlead)
            end = hands_text[h].find(nextSuit)
            if (end == -1):
                end = len(hands_text[h])
            if (hands_text[h][begin:end].find(ranklead) != -1):
                leader = h  # here we found the guy that lead, the leader
                break
        hands = np.roll(hands, leader)
    else:
        errorLog['lead'] += 1
        leader = error['leader']

    return leader, hands


def is_command(info):
    if (info in commands):
        return True
    return False


"""
Dudu
###############################################################################
"""
"""

hand_ex = "1SKT32HJ984DJT52C9,SAQJ86HK63DK93C75,S94HT5D864CAQJT62"
lead = "SJ"
dealer, hands = pick_hands(hand_ex)
leader, hands = pick_lead(hand_ex, lead, hands)
print(hands.nbytes)
print(hands, PLAYERS[leader], dealer, lead,)
print(errorLog)
"""
