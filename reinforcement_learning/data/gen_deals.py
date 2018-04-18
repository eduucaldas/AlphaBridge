import numpy as np



def gen(n):
    x = np.random.permutation(range(52))
    ns = x[:26]
    return [np.append(ns, np.random.permutation(x[26:])) for _ in range(n)]

def gen_deals(N, n):
    return map(lambda _: gen(n), range(N))
