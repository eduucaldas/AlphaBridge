import gym
from gym import spaces
import numpy as np
from rl.tools.utils import Solver

def to_categorical(y, num_classes=None):
    y = np.array(y, dtype='int')
    input_shape = y.shape
    if input_shape and input_shape[-1] == 1 and len(input_shape) > 1:
        input_shape = tuple(input_shape[:-1])
    y = y.ravel()
    if not num_classes:
        num_classes = np.max(y) + 1
    n = y.shape[0]
    categorical = np.zeros((n, num_classes))
    categorical[np.arange(n), y] = 1
    output_shape = input_shape + (num_classes,)
    categorical = np.reshape(categorical, output_shape)
    return categorical

class BiddingEnv(gym.Env):
    B  = { 
           '1N': 0, '1S': 1, '1H': 2, '1D': 3, '1C': 4,
           '2N': 5, '2S': 6, '2H': 7, '2D': 8, '2C': 9,
           '3N': 10, '3S': 11, '3H': 12, '3D': 13, '3C': 14,
           '4N': 15, '4S': 16, '4H': 17, '4D': 18, '4C': 19,
           '5N': 20, '5S': 21, '5H': 22, '5D': 23, '5C': 24,
           '6N': 25, '6S': 26, '6H': 27, '6D': 28, '6C': 29,
           '7N': 30, '7S': 31, '7H': 32, '7D': 33, '7C': 34,
           'PASS': 35
         }
    
    
    CARDMAP = {
        'S2': 0, 'S3': 1, 'S4': 2, 'S5': 3, 'S6': 4, 'S7': 5, 'S8': 6,
        'S9': 7, 'ST': 8, 'SJ': 9, 'SQ': 10, 'SK': 11, 'SA': 12,
        'H2': 13, 'H3': 14, 'H4': 15, 'H5': 16, 'H6': 17, 'H7': 18,
        'H8': 19, 'H9': 20, 'HT': 21, 'HJ': 22, 'HQ': 23, 'HK': 24, 'HA': 25,
        'D2': 26, 'D3': 27, 'D4': 28, 'D5': 29, 'D6': 30, 'D7': 31, 'D8': 32,
        'D9': 33, 'DT': 34, 'DJ': 35, 'DQ': 36, 'DK': 37, 'DA': 38,
        'C2': 39, 'C3': 40, 'C4': 41, 'C5': 42, 'C6': 43, 'C7': 44,
        'C8': 45, 'C9': 46, 'CT': 47, 'CJ': 48, 'CQ': 49, 'CK': 50, 'CA': 51
    }
    
    C = to_categorical(list(CARDMAP.values()))
    
    def __init__(self):
        self.deal = self.random_deal()
        self.north = self.deal[:13]
        self.south = self.deal[13:26]
        self.WE = self.deal[26:]
        self.biddings = []
        self.steps = 0
        self.num_envs = 4
        self.solver = Solver()
        self.action_space = spaces.Discrete(36)
        low = np.zeros(2548)
        self.observation_space = spaces.Box(low=low, high=1+low, dtype=np.int32)
    
    def step(self, action):
        r = 1
        done = False
        self.biddings.append(action)
        try:
            s_ = self.get_state()
        except:
            return 
        if len(self.biddings) == 1:
            if action == 35:
                r = -20
                done = True
        elif action < self.biddings[-2]:
            r = -20
            done = True
        elif action == 35:
            north, south, we = self.get_cards()
            r = -self.solver.mean_score(4, self.biddings[-2]%5, north, south, we)
            done = True
        self.steps += 1
        return s_, r, done, None
    
    def get_state(self):
        s = np.zeros((36, 52))
        for i, b in enumerate(self.biddings):
            s[i][:36] = b
        if self.steps % 2 == 0:
            return np.concatenate((self.north, s)).ravel()
        else:
            return np.concatenate((self.south, s)).ravel()
    
    def random_deal(self):
        deal = BiddingEnv.C.copy()
        np.random.shuffle(deal)
        return deal

    def get_cards(self):
        res = [np.argmax(c) for c in self.deal]
        north = res[:13]
        south = res[26:39]
        we = res[13:26]
        we.extend(res[39:])
        return north, south, we
    
    def reset(self):
        self.biddings = []
        self.steps = 0
        return self.get_state()
    
    def render(self):
        return 
    
    def close(self):
        return
