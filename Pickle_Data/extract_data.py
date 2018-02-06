from __future__ import print_function

# Ian Duleba
#
#
# Attention!!
# To run this code you'll need at least 4 Gb of free memory if you want to search the entire database!
#
# First you should unrar the file All.rar and it has 1 Gb in size when uncompressed!
#
# Put the file encode_and_parsing.py in the same folder that this script. It's in the folder auxiliary_functions of
# the repository. It has Dudu's functions to encode and decode the bidding. Check it out to see our definitions in
# more detail.
#
# After that you are good to go. You can import this file inside some other code and call load_file(#insert directory
#  of All.bin#) or search_biddings(DATA, #list of biddings to search#).
#
# If it's easier, you can put your code here as well.
#

import numpy as np
import pickle
import time
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import auxiliary_functions.encode_and_parsing as eap


class BridgeDeal:
    # Example of object
    # BridgeDeal(
    # 	bbo_file = 00013,
    # 	tournament = None,
    # 	players = None,
    # 	hands = [[False False False False  True False False False  True  True False  True
    #   False False False  True False False False  True False False False False
    #   False  True False  True  True False False  True False False False False
    #    True False False  True False False False  True False False False False
    #   False False False False]
    #  [False False  True  True False  True False False False False  True False
    #   False  True False False False  True False False False  True False False
    #    True False  True False False False  True False False False  True False
    #   False False False False False False False False False  True False False
    #   False False  True False]
    #  [ True False False False False False False  True False False False False
    #   False False False False  True False  True False  True False False False
    #   False False False False False  True False False  True False False  True
    #   False  True False False False  True  True False False False False False
    #    True False False  True]
    #  [False  True False False False False  True False False False False False
    #    True False  True False False False False False False False  True  True
    #   False False False False False False False False False  True False False
    #   False False  True False  True False False False  True False  True  True
    #   False  True False False]],
    # 	bidding = [3, 0, 0, 0],
    # 	leader = 0,
    # 	dealer = 3,
    # 	lead = SJ,
    # 	vuln = b
    # )
    def __init__(self, bbo_file, tournament, players, hands, bidding, leader, dealer, lead, vuln):
        self.bbo_file = bbo_file  # number specifying the id of the .lin given by bbo
        self.tournament = tournament  # not done yet!
        self.players = players  # not done yet!
        self.hands = hands  # 4 hands, each as a 52 matrix with 1 in the entries in which the card is present
        self.bidding = bidding  # the bidding sequence as encoded in encode_and_parsing
        self.leader = leader  # i.e. the person that puts the first card in the game, as a number(0-3)
        self.dealer = dealer  # i.e. the person that puts the first bids, as a number (0-3)
        self.lead = lead  # i.e. the first card to be played
        self.vuln = vuln  # i.e. vulnerability{0, b, e, p, n} TODO @Zigfrid, what do this mean, can encode this better?

    def __eq__(self, other):
        return self.bbo_file == other.bbo_file and self.tournament == other.tournament and self.players == other.players and self.bidding == other.bidding and (
                self.hands == other.hands).all() and self.leader == other.leader and self.dealer == other.dealer and self.lead == other.lead and self.vuln == other.vuln

    def __str__(self):
        return "BridgeDeal(\n\tbbo_file = " + str(self.bbo_file) + ", \n\ttournament = " + str(self.tournament) + \
               ", \n\tplayers = " + str(self.players) + ", \n\thands = " + str(self.hands) + ", \n\tbidding = " + \
               str(self.bidding) + ", \n\tleader = " + str(self.leader) + ", \n\tdealer = " + str(self.dealer) + \
               ", \n\tlead = " + str(self.lead) + ", \n\tvuln = " + str(self.vuln) + "\n)"


# save DATA to file


def save_file(path, data):
    f = open(path, "wb")
    pickle.dump(data, f)
    f.close()


# load DATA from file


def load_file(path):
    f = open(path, "rb")
    data = pickle.load(f)
    f.close()
    return data


# We are going to get all matches with a particular bidding. For example, any of the following list:
# biddings = [['1N', 'p', 'p', 'p'], ['p', '1N', 'p', 'p', 'p'], ['p', 'p', '1N', 'p', 'p', 'p'], ['p', 'p', 'p', '1N', 'p', 'p', 'p']]
# and we return a list with the matches


def find_biddings(DATA, biddings):
    DATA_match = []

    # Dudu has created a coded version of the bidding, it occupies less space and it'll be easier to run ML and DL later
    # We need to encode the bidding
    bidding_encoded = []
    for bidding in biddings:
        bidding_encoded.append(eap.encode_raw_Bidding(bidding))

    for deal in DATA:
        for bidding in bidding_encoded:
            if bidding == deal.bidding:
                DATA_match.append(deal)

    return DATA_match


def extract_to_temp(in_pickle, biddings):
    start = time.time()

    print("Reading data from disk...")
    # let's load the entire database (4 Gb in memory)
    # in my case the file is in the same folder.
    data = load_file(in_pickle)

    end_load = time.time()
    print(" ...Done. Time to read data from disk: {:,.2f} seconds".format(end_load - start))  # time to retrieve DATA

    print("Searching for biddings:")
    print(biddings)

    data_match = find_biddings(data, biddings)

    end_search = time.time()
    print(" ...Done. Searched in: {:,.2f} seconds".format(end_search - end_load))  # time to retrieve DATA
    print("Number of games found: " + str(len(data_match)))

    return data_match
    # Do whatever... ML, DL...


# now, if you want to save to file


def extract_to_pickle(in_pickle, out_dir, biddings):
    outfile = "Search.bin"
    if out_dir != "":
        outfile = out_dir + "/" + outfile
    data = extract_to_temp(in_pickle, biddings)
    save_file(outfile, data)

#this tests if the data is coherent
def test_extract():
    test_data = extract_to_temp("All.bin", [['1N', 'p', 'p', 'p']])
    bugged_id = []
    for i in range(len(test_data)):
        if not eap.is_card_in_hand(test_data[i].hands[0], test_data[i].lead):
            bugged_id.append(i)
    for id in bugged_id:
        print(test_data[id])


if __name__ == '__main__':
    #test_extract()
    # This is probably how you'll use it, ../1NTPPP comes to the parent directory and enters in the 1NTPPP folder

    extract_to_pickle("All.bin", "../1NTPPP",
                      [['p', '1S', 'p', 'p', 'p']])

# ['1N', 'p', 'p', 'p'], ['p', '1N', 'p', 'p', 'p'], ['p', 'p', '1N', 'p', 'p', 'p'], ['p', 'p', 'p', '1N', 'p', 'p', 'p']