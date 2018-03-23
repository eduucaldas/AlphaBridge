import re
import numpy as np
import pandas as pd
import data.enums as enums

def vectorize_hand(hand):
    suits = ['S', 'H', 'D', 'C']
    res = []
    for i in range(4):
        for c in hand[i][1]:
            res.append(enums.CARDMAP[suits[i]+c])
    return np.array(res)

def categorize_hand(hand):
    v = np.zeros(52)
    for c in hand:
        v[int(c)] = 1
    return v

def vectorize_game_line(gameLine):
    try:
        res = []
        gameLine = gameLine.upper()
        if not re.match(r"[\w\d]*,[\w\d]*,[\w\d]*,[\w\d]*\|[\w\d]*", gameLine):
            return None
        hands, lead = gameLine.split('|')
        hands = hands.split(',')
        suit, card = lead[0], lead[1]
        r = re.compile(".*"+suit+"[AKQJT\d]*"+card+".*")
        leader = 0
        for i, h in enumerate(hands):
            if re.findall(r, h):
                leader = i
        regex = re.compile("([SHDC])([AKQJT\d]*)")
        hands = list(map(lambda s: re.findall(regex, s), hands))
        vectorized = np.array(list(map(vectorize_hand, hands)))
        vectorized = np.ravel(vectorized)
        vectorized = np.append(vectorized, [leader, enums.CARDMAP[lead]])
        return vectorized 
    except:
        return None

def vectorize_bidding(bidding):
    bidding = bidding[1:]
    try:
        bidding = [b.upper().replace('!', '') for b in bidding]
        res = [0 for _ in range(24)]
        res[:len(bidding)] = [enums.BIDSMAP[b] for b in bidding]
        return res
    except:
        return None
    

def vectorize(hands, bidding):
    vhands = vectorize_game_line(hands)
    vbidding = vectorize_bidding(bidding)
    return np.append(vhands, vbidding)
    
def parse_lin(name):
    with open(name) as f:
        contents = f.read().replace('\r', '').replace('\n', '')
    contents = contents.split('|')

    leads = []
    biddings = []
    hands= []
    bidding = []
    lead = -1
    i = 0
    while i < len(contents):
        token = contents[i]
        if token in enums.CMDS: 
            if token == 'md':
                if len(hands) > len(leads):
                    del hands[-1]
                elif len(hands) < len(leads):
                    raise NameError("MyError")
                bidding = []
                lead = -1
                hands.append(contents[i + 1])
                i += 2
            elif token == 'sv': 
                if contents[i + 1] != '':
                    bidding = []
                    bidding.append(contents[i + 1])
                i += 2
            elif token == 'pc': 
                if lead == -1:
                    biddings.append(bidding)
                    lead = contents[i + 1]
                    leads.append(lead)
                i += 2
            elif token == 'mb': 
                if contents[i + 1] != '':
                    bidding.append(contents[i + 1])
                i += 2
            elif token == 'qx':
                if not 'md' in contents[i+2:i+7]:
                    if len(contents[i + 2]) == 54:
                        if len(hands) > len(leads):
                            del hands[-1]
                        elif len(hands) < len(leads):
                            raise NameError("MyError")
                        bidding = []
                        lead = -1
                        hands.append(contents[i + 2])
                        i += 2
                    else:
                        i += 1 
                else:
                    i += 1 
            else:
                i += 1 
        else:
            i += 1 

    if len(hands) > len(leads):
        del hands[-1]
    elif len(hands) < len(leads):
        return None
    if len(leads) != len(hands) or len(biddings) != len(hands):
        return None
    gamelines = []
    for i in range(len(hands)):
        gamelines.append(hands[i] +'|'+ leads[i])
    return [(gamelines[i],biddings[i]) for i in range(len(hands))]
