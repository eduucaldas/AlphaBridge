from env.bidding_env import BiddingEnv
from baselines import deepq


model = deepq.models.mlp([64])
env = BiddingEnv()
act = deepq.learn(
        env,
        q_func=model,
        lr=1e-3,
        max_timesteps=100000,
        buffer_size=50000,
        exploration_fraction=0.1,
        exploration_final_eps=0.02,
        print_freq=10,
        callback=None
    )
