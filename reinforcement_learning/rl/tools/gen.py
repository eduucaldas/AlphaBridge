#from rl.tools.utils import Solver
import numpy as np
import pandas as pd
import os
from rl.tools.dds import Solver

def write(f, north, south, dds):
    cards = np.concatenate((north, south))
    cards = ",".join(map(str, cards))
    dds = ",".join(map(str, dds))
    f.write(cards+"\n")
    f.write(dds+"\n\n")
    


def main(N):
    s = Solver()
    if os.path.exists("./data"):
        f = open('./data/dds.deals', 'a')
    else:
        f = open('./data/dds.deals', 'w')
    for k in range(N):
        x = np.random.permutation(range(52))
        north = x[:13]
        south = x[13:26]

        we = x[26:]
        dds = s.mean_score2(4, north, south, we)
        write(f, north, south, dds)
        if (k%10==0):
            print(k,"/",N)
    f.close()
    return
            

