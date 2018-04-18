import tensorflow
from baselines import deepq
import gym
import pandas as pd
from rl.env.bidding_env2 import BiddingEnv2
from rl.env.bidding_env2 import create_dataframe

df = pd.read_csv("sym_deals.csv").dropna()
df = df.drop(df.columns[0], axis=1) 
env = BiddingEnv2(df)


model = deepq.models.cnn_to_mlp(
    convs=[(256, 16, 1), (128, 8, 1), (64, 4, 1)],
    hiddens=[128, 128],
    dueling=True)

act = deepq.learn(
    env,
    q_func=model,
    lr=1e-3,
    max_timesteps=300000,
    gamma=1,
    buffer_size=100000,
    exploration_fraction=0.4,
    exploration_final_eps=0.01,
    print_freq=10,
)
