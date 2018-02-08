#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 14:09:53 2018

@author: scander.mustapha
"""

import pickle
import numpy as np
import pandas as pd
from BridgeDeal import BridgeDeal

CARDMAP = {
           's2': 0, 's3': 1, 's4': 2, 's5': 3, 's6': 4, 's7': 5, 's8': 6, 's9': 7, 'st': 8, 'sj': 9, 'sq': 10, 'sk': 11, 'sa': 12,
           'h2': 13, 'h3': 14, 'h4': 15, 'h5': 16, 'h6': 17, 'h7': 18, 'h8': 19, 'h9': 20, 'ht': 21, 'hj': 22, 'hq': 23, 'hk': 24, 'ha': 25,
           'd2': 26, 'd3': 27, 'd4': 28, 'd5': 29, 'd6': 30, 'd7': 31, 'd8': 32, 'd9': 33, 'dt': 34, 'dj': 35, 'dq': 36, 'dk': 37, 'da': 38,
           'c2': 39, 'c3': 40, 'c4': 41, 'c5': 42, 'c6': 43, 'c7': 44, 'c8': 45, 'c9': 46, 'ct': 47, 'cj': 48, 'cq': 49, 'ck': 50, 'ca': 51
           }

def convert_deal(deal):
    south = np.where(deal.hands[0])[0]
    west = np.where(deal.hands[1])[0]
    north = np.where(deal.hands[2])[0]
    east = np.where(deal.hands[3])[0]
    bidding = [0 for _ in range(24)]
    bidding[:len(deal.bidding)] = deal.bidding
    bidding = np.array(bidding)
    dealer = deal.dealer
    leader = deal.leader
    lead = CARDMAP[deal.lead.lower()]
    vuln = deal.vuln
    return [*south, *west, *north, *east, *bidding, dealer, leader, lead, vuln]

def create_dataframe(pickle_name,store_name):
    store = pd.HDFStore(store_name, "w", complib=str("zlib"), complevel=5)
    with open(pickle_name, 'rb') as f:
        data = pickle.load(f)
    
    data = [d for d in data if len(d.bidding) < 25]
    d = map(convert_deal, data)
    columns = []
    for hand in ['south', 'west', 'north', 'east']:
        columns.extend(['{1}{0}'.format(i+1, hand) for i in range(13)])
    columns.extend(['bidding{0}'.format(i+1) for i in range(24)])
    columns.extend(['dealer', 'leader', 'lead', 'vuln'])
    
    
    df = pd.DataFrame(list(d), columns=columns, dtype='int32')
    store.put('df', df, data_columns=df.columns)
    store.close()
