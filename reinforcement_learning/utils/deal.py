import numpy as np

CARDMAP = {
    0:'2', 1:'3', 2:'4', 3:'5', 4:'6', 5:'7', 6:'8', 7: '9', 8:'T', 9:'J', 10:'Q', 11:'K', 12:'A'
}


def convert_card(n):
    return CARDMAP[n % 13], n//13

def convert_categoricalhand(chand):
    cards = [[], [], [], []]
    for c in chand:
        card, color = convert_card(np.argmax(c))
        cards[color] += card
    res = []
    for c in cards:
        c.reverse()
        res.append("".join(c))
    return ".".join(res)

def convert_deal(deal):
    north = deal[:13]
    south = deal[13:26]
    east = deal[26:39]
    west = deal[39:]
    res = "N:"
    res += " ".join([convert_categoricalhand(h) for h in [north, south, east, west]])
    return bytes(res, "utf8")