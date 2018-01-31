from __future__ import print_function

#Ian Duleba
#
#
#Attention!!
#To run this code you'll need at least 4 Gb of free memory if you want to search the entire database!
#
#First you should unrar the file All.rar and it has 1 Gb in size when uncompressed!
#
#Put the file encode_and_parsing.py in the same folder that this script. It's in the folder auxiliary_functions of the repository.
#It has Dudu's functions to encode and decode the bidding. Check it out to see our definitions in more detail.
#
#After that you are good to go. You can import this file inside some other code and call load_file(#insert directory of All.bin#) or search_biddings(DATA, #list of biddings to search#).
#
#If it's easier, you can put your code here as well.
#

import numpy as np
import cPickle as pickle
import time
import encode_and_parsing as eap

class BridgeDeal:
	def __init__(self, bbo_file, tournament, players, hands, bidding, leader, dealer, lead, vuln):
		self.bbo_file = bbo_file
		self.tournament = tournament #not done yet!
		self.players = players #not done yet!
		self.hands = hands
		self.bidding = bidding
		self.leader = leader
		self.dealer = dealer
		self.lead = lead
		self.vuln = vuln
	def __eq__(self, other):
		return self.bbo_file == other.bbo_file and self.tournament == other.tournament and self.players == other.players and self.bidding == other.bidding and (self.hands == other.hands).all() and self.leader == other.leader and self.dealer == other.dealer and self.lead == other.lead and self.vuln == other.vuln

#save DATA to file
def save_file(path, DATA):
	f = open(path, "wb")
	pickle.dump(DATA, f)
	f.close()

#load DATA from file
def load_file(path):
	f = open(path, "rb")
	DATA = pickle.load(f)
	f.close()
	return DATA

#We are going to get all matches with a particular bidding. For example, any of the following list:
#biddings = [['1N', 'p', 'p', 'p'], ['p', '1N', 'p', 'p', 'p'], ['p', 'p', '1N', 'p', 'p', 'p'], ['p', 'p', 'p', '1N', 'p', 'p', 'p']]
#and we return a list with the matches
def find_biddings(DATA, biddings):
	DATA_match=[]

	#Dudu has created a coded version of the bidding, it occupies less space and it'll be easier to run ML and DL later.
	#We need to encode the biddingit
	bidding_encoded = []
	for bidding in biddings:
		bidding_encoded.append(eap.encodeRaw_Bidding(bidding))

	for deal in DATA:
		for bidding in bidding_encoded:
			if bidding == deal.bidding:
				DATA_match.append(deal)

	return DATA_match

if __name__ == "__main__":
	
	start = time.time()

	DATA=[] #list of BridgeDeal objects
	
	print("Reading data from disk...")
	#let's load the entire database (4 Gb in memory)
	#in my case the file is in the same folder.
	DATA = load_file("All.bin")

	end_load = time.time()
	print(" ...Done. Time to read data from disk: {:,.2f} seconds".format(end_load - start)) #time to retrieve DATA


	#as an example, lets search for:
	biddings = [['1N', 'p', 'p', 'p'], ['p', '1N', 'p', 'p', 'p'], ['p', 'p', '1N', 'p', 'p', 'p'], ['p', 'p', 'p', '1N', 'p', 'p', 'p']]

	print("Searching for biddings:")
	print(biddings)
	
	DATA_match = find_biddings(DATA, biddings)

	end_search = time.time()
	print(" ...Done. Searched in: {:,.2f} seconds".format(end_search - end_load)) #time to retrieve DATA
	print("Number of games found: " + len(DATA_match))

	#Do whatever... ML, DL...

	#now, if you want to save to file
	#save_file("Search.bin", DATA_match)
	
