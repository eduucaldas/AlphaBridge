import re
import numpy as np
import pandas as pd

SUITMAP = {'S':0, 'H':1, 'D':2, 'C':3}
CARDMAP = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}

def card_to_int(card):
    return SUITMAP[card[0]] * 13 + (CARDMAP[card[1]] - 2)

def vectorize_hand(hand):
    v = np.zeros((4,13))
    for x in hand:
        for y in x[1]: 
            v[SUITMAP[x[0]]][CARDMAP[y] - 2] = 1
    return np.ravel(v)

def vectorize(gameLine):
    gameLine = gameLine.upper()
    assert re.match(r"[\w\d]*,[\w\d]*,[\w\d]*,[\w\d]*\|[\w\d]*", gameLine)
    hands, entame = gameLine.split('|')
    hands = hands.split(',')
    suit, card = entame[0], entame[1]
    r = re.compile(".*"+suit+"[AKQJT\d]*"+card+".*")
    player = 0
    for i, h in enumerate(hands):
        if re.findall(r, h):
            player = i
    regex = re.compile("([SHDC])([AKQJT\d]*)")
    hands = list(map(lambda s: re.findall(regex, s), hands))
    vectorized = list(map(vectorize_hand, hands))
    vectorized.append(vectorized[player])
    vectorized.append(card_to_int(entame))
    return  np.array(vectorized)


def archive_to_dataframe(filename):
    with open(filename) as gameText:
        gameLines = gameText.read().split('\n')
    gameLines = gameLines[:-1]
    v = vectorize(gameLines[0])
    v = np.array([ vectorize(line) for line in gameLines ])
    index = np.arange(len(gameLines))
    df = pd.DataFrame(v, index=index, columns = ['player1', 'player2', 'player3', 'player4', 'player', 'entame'])
    return df
