from os import walk
from data.tools import vectorize
from data.tools import parse_lin
from multiprocessing import Pool
import pandas as pd
import data.enums as enums

def fvect(u):
    if len(u[1]) < 24:
        return vectorize(u[0], u[1])
    else:
        return None

def function_file(file):
    parsed = parse_lin(file)
    if parsed != None:
        return [fvect(u) for u in parsed] 
    return None

def parse_deal():
    files = []
    for (dirpath, dirnames, filenames) in walk("./deals"):
        files.extend([dirpath+'/'+fname for fname in filenames])

    with Pool(5) as p:
        res = p.map(function_file, files)

    res = [x for x in res if x is not None]
    res = [y for x in res for y in x if y is not None]
    return res

def create_dataframe(data):
    columns = []
    for hand in ['south', 'west', 'north', 'east']:
        columns.extend(['{1}{0}'.format(i+1, hand) for i in range(13)])
    columns.extend(['leader', 'lead'])
    columns.extend(['bidding{0}'.format(i+1) for i in range(24)])
    df = pd.DataFrame(data, columns=columns, dtype='int32')
    return df

def save_df(df,name):
    store = pd.HDFStore(name, "w", complib=str("zlib"), complevel=5)
    store.put('df', df, data_columns=df.columns)
    store.close()

def load_df(name):
    df = pd.read_hdf(name)
    return df
    

def leader_hand(i,leader, south, west, north, east):
    p = leader[i]
    if p == 0:
        return south[i]
    elif p == 1:
        return west[i]
    elif p == 2:
        return north[i]
    else:
        return east[i]

def search_bidding(bidding):
    df = pd.read_hdf('./data/store.hdfs')
    bidding = bidding.split(",")
    query_string = " & ".join(
            ["bidding{i} == {bid}".format(i=i+1,bid=enums.BIDSMAP[bidding[i]]) for i in range(len(bidding))]
            )
    dfq = df.query(query_string)
    del df
    south = list(dfq[["south{i}".format(i=i) for i in range(1,14)]].values)
    west = list(dfq[["west{i}".format(i=i) for i in range(1,14)]].values)
    north = list(dfq[["north{i}".format(i=i) for i in range(1,14)]].values)
    east = list(dfq[["east{i}".format(i=i) for i in range(1,14)]].values)
    leader = dfq.leader.values
    leader = [leader_hand(i, leader, south, west, north, east) for i in range(len(leader))]
    lead = list(dfq.lead.values)
    return pd.DataFrame({"south":south,"west":west,"north":north,"east":east,"leader":leader,"lead":lead}, dtype="int8")
    
    
def create_dataframe2(pickle_name,store_name):
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
