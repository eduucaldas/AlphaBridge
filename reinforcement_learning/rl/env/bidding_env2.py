import gym
from gym import spaces
import numpy as np


def create_dataframe(name):
    columns = ["cardN{i}".format(i=i) for i in range(1, 14)]
    columns.extend(["cardS{i}".format(i=i) for i in range(1, 14)])
    columns.extend(["ddsNT_{c}".format(c=c) for c in list("NSEW")])
    columns.extend(["ddsS_{c}".format(c=c) for c in list("NSEW")])
    columns.extend(["ddsH_{c}".format(c=c) for c in list("NSEW")])
    columns.extend(["ddsD_{c}".format(c=c) for c in list("NSEW")])
    columns.extend(["ddsC_{c}".format(c=c) for c in list("NSEW")])
    df = pd.DataFrame(columns=columns)
    c = 0
    with open(name, 'r') as file:
        while True:
            try:
                data = []
                for _ in range(100):
                    _cards = file.readline()
                    if _cards == '':
                        df = df.append(pd.DataFrame(data, columns=columns))
                        return df
                    _cards = np.fromstring(_cards, sep=',')
                    _dds = file.readline()
                    _dds = _dds.replace("\n", "")
                    _dds = _dds.replace("[", "")
                    _dds = _dds.replace("]", "")
                    _dds = _dds.split(",")
                    _dds = np.array(list(map(lambda l: np.fromstring(l, dtype=float, sep=' ') , _dds)))
                    _dds = _dds.ravel()
                    data.append(np.concatenate((_cards, _dds)))
                    file.readline()
                    c += 1
                #print(c)
                df = df.append(pd.DataFrame(data, columns=columns))
            except:
                pass
        
        return df

class BiddingEnv2(gym.Env):
    def __init__(self, df):
        low = np.zeros((52, 52))
        high = low + 1
        self.df = df
        self.reset()
        self.action_space = spaces.Discrete(36)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.int8)
        self.df = df

    def get_cards_state(self):
        north = np.zeros((13, 52))
        for i, card in enumerate(self.north):
            north[i][card] = 1
        south = np.zeros((13, 52))
        for i, card in enumerate(self.south):
            south[i][card] = 1
        return north, south

    def get_state(self):
        n = len(self.biddings)
        self.s[3 + n][self.biddings[-1]] = 1
        self.s[-1][self.biddings[-1]+1:] = np.ones(52-self.biddings[-1]-1)
        if self.steps % 2 == 0:
            self.s[:13] = self.north_state
        else:
            self.s[:13] = self.south_state
        return self.s

    def step(self, action):
        r = 1
        done = False
        if len(self.biddings) == 0:
            if action == 35:
                r = 0
                return self.s, r, done, None
        elif action <= self.biddings[-1]:
            r = 0
            return self.s, r, done, None
        elif action == 35:
            r = 100/(1+int(self.dds[self.biddings[-1] % 5][self.steps % 2]))
            r -= len(self.biddings)
            #r = 100/(1 + self.solver.mean_score(4, self.biddings[-1] % 5, self.north, self.south, self.we))
            done = True
            return self.s, r, done, None
        self.biddings.append(action)
        self.steps += 1
        s_ = self.get_state()
        return s_, r, done, None
            
                

    def rand_deal(self):
        x = np.random.permutation(range(52))
        north = x[:13]
        north.sort()
        south = x[13:26]
        south.sort()
        we = x[26:]
        return north, south, we

    def reset(self):
        sample = self.df.sample()
        self.north = (sample[["cardN{i}".format(i=i) for i in range(1, 14)]]).astype(np.int8).values
        self.south = (sample[["cardS{i}".format(i=i) for i in range(1, 14)]]).astype(np.int8).values
        self.we = np.random.permutation(range(52))
        self.we = np.delete(self.we, self.north)
        self.we = np.delete(self.we, self.south)
        self.north_state, self.south_state = self.get_cards_state()
        self.dds = np.array(sample.values.tolist()[0][26:]).reshape((5, 4))
        self.biddings = []
        self.s = np.zeros((52, 52))
        self.steps = 0
        return self.s

    def render(self):
        return

    def close(self):
        return
