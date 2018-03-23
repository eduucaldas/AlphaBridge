import itertools
import numpy as np

def permute_shdc(hand, lead):
    color = lead//13
    hand[lead] = -1
    s = hand[:13]
    h = hand[13:26]
    d = hand[26:39]
    c = hand[39:52]
    permuted_hands = [np.concatenate(hd) for hd in itertools.permutations([s, h, d, c])]
    return list(map(np.abs, permuted_hands)), list(map(np.argmin,permuted_hands))
