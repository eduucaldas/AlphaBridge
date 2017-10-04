#You should run this code inside the folder raw_lin_data from our project. Check our github
#start reading from the Main()

import os
import re
import numpy as np
import pickle
import time

class BridgeHand:
	def __init__(self, hands, bidding, leader, dealer, lead, vuln):
		self.hands = hands
		self.bidding = bidding
		self.leader = leader
		self.dealer = dealer
		self.lead = lead
		self.vuln = vuln
	def __eq__(self, other):
		return self.bidding == other.bidding and (self.hands == other.hands).all() and self.leader == other.leader and self.dealer == other.dealer and self.lead == other.lead and self.vuln == other.vuln

#list of commands
commands = {'md':0, 'sv':1, 'pc':2, 'mb':3, 'ob':4, 'qx':5, 'mc':6, 'pg':7, 'nt':8, 'vg':9, 'rs': 10, 'pn': 11, 'an':12, 'st': 13}

#from observation order of hands is always: SWNE
PLAYERS = {0:'S', 1:'W', 2:'N', 3:'E'}
#from observation order of suits is always: SHDC
SUITMAP = {'S':0, 'H':1, 'D':2, 'C':3}

OUT_OF_RANGE = 'U'# dirty trick: U for no out of range exception in SUITS
SUITS = ['S', 'H', 'D', 'C', OUT_OF_RANGE] 
#this is how the cards are described in the .lin
CARDMAP = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}

#for later purposes##################
BIDS = {}
#####################################

#resume of meaning for lin files
#qx -> begin game
#md -> show hands
#sv -> start bidding
#mb -> make bid
#pc -> next card
#pg -> next line, followed by ||
#mc -> finish game

#Count where the error occurred, e.g. if it was in dealer
errorLog = {'dealer':0, 'hands': 0,'entame': 0, 'bid':0, 'leader':0}
#we can perhaps implement it to show in which file the error occurred occurred

#for readability and making it easier to change after :)
error = {'dealer':-1, 'hands': None, 'entame': None, 'bid':None, 'leader':-1}

"""
Auxiliar functions#############################################################
"""
def vectorizing(handText):
    """
    input:
       string in format:"SKT32HJ984DJT52C9"
    comments:
       Here i do a dirty trick, i add a char OUT_OF_RANGE to handText
       so that when we have an indicator of the end of hand.
    output:
       hand:
           HandVector = 52-binary vector, with ones when the player has the card
    """
    hand = np.zeros(52, dtype=bool)
    end = 0   #should see if its S
    handText = handText + OUT_OF_RANGE #adds stopping character
    for suit in range(4):
        begin = end + 1
        end = handText.find(SUITS[suit+1])
        if(end == -1 or end < begin): #then we haven`t found the next suit, which is a problem according to our format
            errorLog['hands']+=1
            return error['hands']
        for i in range(begin,end):
            if not (handText[i] in CARDMAP):
                errorLog['hands'] += 1
                return error['hands']
            else:
                hand[suit*13 + CARDMAP[handText[i]]-2] = True
    #take out our OUT_OF_RANGE? not necessary :)
    return hand


def vectorizing3(handsText):
    """
    input:
       string in format:"SKT32HJ984DJT52C9,SAQJ86HK63DK93C75,S94HT5D864CAQJT62"
    comments:
    output:
       4 HandVectors
    """
    handsText = handsText.split(',')
    
    for hT in handsText:
        if(len(hT) != 17):
            errorLog['hands'] += 1
            return error['hands']
    
    hands = []
    for handT in handsText:
        h = vectorizing(handT)
        if(h == None):
            return error['hands']
        else:
            hands.append(h)
    
    one = np.ones(len(hands[0]), dtype=bool)
    hands.append(one ^ hands[0] ^ hands[1] ^ hands[2])#appends the missing hand
    #may need to verify if hands[3] is valable
    return hands
"""
###############################################################################
"""

def pick_hands(gameLine):
    """
    input: 
       string in format:"1SKT32HJ984DJT52C9,SAQJ86HK63DK93C75,S94HT5D864CAQJT62,S75HAQ72DAQ7CK843"
                         or "1SKT32HJ984DJT52C9,SAQJ86HK63DK93C75,S94HT5D864CAQJT62"
    comments:
       First integer =  for the dealer in the format [1-4], where 4 is E
       Sometimes there`s only 3 hands, since the forth is redundant
       There`s always the suit indicator, even when there are no cards of the suit.
    output:
       dealer::
           in the format [0-3], where 3 is E
       vector of hands:
           4 HandVectors
    """
    gameLine = gameLine.upper()
    dealer = error['dealer']
    hands = error['hands']
    begin = gameLine.find(SUITS[0]) ##beginning of hands, namely the first spades that he encounters
    if(begin == 1):
        if(int(gameLine[0]) < 1 or int(gameLine[0]) > 4):
            errorLog['dealer'] += 1
        else:
            handsText = gameLine[1:]
            dealer = int(gameLine[0]) - 1#puts dealer in the format we want
            if(len(handsText) == 71 or len(handsText) == 53):
                #in the case of 4 hands, reduce it to 3 and solve
                handsText = handsText[:53]
                hands = vectorizing3(handsText)
            else:
                errorLog['hands'] += 1
    else:
        errorLog['dealer'] += 1
       
    return dealer, hands




def pick_entame(handsText, entame, hands):
    """
    input: 
       hands in the text format, entame as string, hands in vector format
    comments:
       hands in text format, because it`s easier to find cards in this format
       we suppose handsText is in the good format, since otherwise we`d already have an error handling in pick_hands
    output:
        leader:
           may be error['leader'] if there`s a problem with entame formatting
           format: [0-3] according to PLAYERS
        hands: 
           4 HandVectors in the order they`ll be played
    """
    handsText = handsText[1:].upper().split(',')
    suitEntame = entame[0].upper()
    rankEntame = entame[1].upper()
    if(suitEntame in SUITMAP and rankEntame in CARDMAP):
        suitCode = SUITMAP[suitEntame]
        nextSuit = SUITS[suitCode + 1]
        leader = 3 # if we dont find the entame below the leader gotta be the 4 guy
        for h in range(len(handsText)):      
            #print(h)
            begin = handsText[h].find(suitEntame)
            end = handsText[h].find(nextSuit)
            if(end == -1):
                end = len(handsText[h])
            if(handsText[h][begin:end].find(rankEntame) != -1):
                leader = h #here we found the guy that entamed, the leader
                break
        hands = np.roll(hands, leader)
    else:
        errorLog['entame'] += 1
        leader = error['leader'] 
    
    return leader, hands


def isCommand(info):
	if(info in commands):
		return True
	return False


#This function interprets the list received (variable "contents"): it will find all good matches (well formatted) and append them to DATA, in order of ocurrence
def interpret(contents, DATA):

	#initializing lists
	game = []
	entames = []
	biddings = []

	#auxiliary variables
	hands_texts=[] #hands of a match in the form: 1SKT32HJ984DJT52C9,SAQJ86HK63DK93C75,S94HT5D864CAQJT62,S75HAQ72DAQ7CK843
	bidding=[] #bidding of a match
	entame=-1 #=-1 while we do not read a "pc", = the entame string after reading a "pc"
	i=0 #counter

	#loop through the "contents"
	while (i<len(contents)):
		#if we find a command in position i
		if(isCommand(contents[i])):

			#we need to know which command

			if commands[contents[i]] == 0: #md, start of hands in the next item on the list

				if len(hands_texts)!=len(entames): #error handling, no information about the previous game

					if len(hands_texts)>len(entames):
						del hands_texts[-1] #we exclude since the match was dropped by the players
					else:
						return False #there are only 4 files that fit this condition, we shall ignore them

				#reset auxiliary variables, we are reading a new match
				bidding=[]
				entame=-1
				hands_texts.append(contents[i+1])
				i=i+2

			elif commands[contents[i]] == 1: #sv, start of bidding in the next item on the list
				bidding.append(contents[i+1])
				i=i+2

			elif commands[contents[i]] == 2: #pc, entame is the next item on the list
				if entame==-1:
					#flush bidding
					biddings.append(bidding)

					#get entame
					entame=contents[i+1]
					entames.append(entame)
				i=i+2

			elif commands[contents[i]] == 3: #mb, bidding in the next item on the list
				bidding.append(contents[i+1])
				i=i+2

			elif commands[contents[i]] == 5: #qx, start of hands (some files do not have the command md, the start of hands, and we will treat them here)

				#lets make sure there is no md following down the list
				if (contents[i+2]!='md' and contents[i+3]!='md' and contents[i+4]!='md' and contents[i+5]!='md' and contents[i+6]!='md'): 

					#if we look 2 items ahead, it should be the hands
					#note: 54 is the correct length for a string like:
					#1SKT32HJ984DJT52C9,SAQJ86HK63DK93C75,S94HT5D864CAQJT62,S75HAQ72DAQ7CK843
					if(len(contents[i+2])==54):

						if len(hands_texts)!=len(entames): #error handling, no information about the previous game

							if len(hands_texts)>len(entames): #we exclude since the match was dropped by the players
								del hands_texts[-1]
							else:
								return False #there are only 4 files that fit this condition, we shall ignore them

						#reset auxiliary variables, we are reading a new match
						bidding=[]
						entame=-1
						hands_texts.append(contents[i+2])
						i=i+3
					else:
						i=i+1

				#but if there is, we just skip the item
				#note: we could have just jumped to the nearest md, but whats the hurry?
				else:
					i=i+1

			#if it is some other command, we skip it
			#note: we could have done i=i+2, but there are a few problematic files, better safe than sorry.
			else:
				i=i+1

		#contents[i] is not a command
		else:
			i=i+1 #we read the next item in the list

	if len(hands_texts)!=len(entames): #no information about the game
		if len(hands_texts)>len(entames):
			del hands_texts[-1]
		else:
			return False #there are only 4 files that fit this condition, we shall ignore them

	#lets recheck if we didint include incomplete games
	#not necessary, but I have OCD
	if(len(entames)!=len(hands_texts) or len(biddings)!=len(hands_texts)):
		print(len(hands_texts),len(entames),len(biddings))
		return False
	
	#lets create BridgeHand's objects from matches that dont have any errors in them and then append them in DATA
	for i in range(len(hands_texts)):

		dealer, hands = pick_hands(hands_texts[i])
		game.append(hands)

		if ((hands != error['hands']) and (dealer != error['dealer'])): #error check
			leader, game[i] = pick_entame(hands_texts[i], entames[i], game[i])
			if (leader != error['leader']): #error check
				#create a BridgeHand object and append it to DATA
				#note: the first item of a bidding is the vulnerability
				DATA.append(BridgeHand(game[i], biddings[i][1:], leader, dealer, entames[i], biddings[i][0]))

	return True
			


def read_lin_file(file_path, DATA):
	f = open(file_path,"r")

	contents=f.read().replace("\r","").replace("\n","") #we remove \r and \n from the file
	list_of_contents=contents.split("|") #and we split it.

	#lets call interpret; it will append to DATA all wellformed matches present on this file
	readable = interpret(list_of_contents, DATA)	

	f.close()

#reads each file inside the folder
def read_folder(path, DATA):
	for filename in os.listdir(path):
		read_lin_file(path+filename, DATA)
		

#reads all folders in the database (format of the folders and files as created in our project)
def read_folders(DATA):
	for i in range(535): #535 folders, this is hardcoded and it would be better if it wasn't.

		#defines "path", ie, the folders name 
		if i<10:
			path="00"+str(i)+"/"
		else:
			if i<100:
				path="0"+str(i)+"/"
			else:
				path=str(i)+"/"

		print path
		read_folder(path, DATA)

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


if __name__ == "__main__":
	DATA=[] #list of BridgeHand objects

	#Still not done
	#We are going to get all matches with a particular bidding. Any of the following list:
	#bids = [['1N', 'p', 'p', 'p'], ['p', '1N', 'p', 'p', 'p'], ['p', 'p', '1N', 'p', 'p', 'p'], ['p', 'p', 'p', '1N', 'p', 'p', 'p']]

	start = time.time()

	#read_folders(DATA)

	#if you want to read only a specific file, comment "read_folders(DATA)" above and uncomment the line below
	read_lin_file("000/00001", DATA)

	end_parser = time.time()
	print(end_parser - start) #time to run the script

	#How many matches were discarted due to errors?
	print(errorLog)

	#now, we have all the information we need in DATA. We can save it or whatever...
	save_file("All.bin", DATA)
	end_save = time.time()
	print(end_save - end_parser) #time to save DATA

	#loading DATA from a file
	#DATA = load_file("All.bin")
	#end_load = time.time()
	#print(end_load - end_save) #time to retrieve DATA

	#print(DATA[0].hands, DATA[0].bidding, DATA[0].leader, DATA[0].dealer, DATA[0].lead, DATA[0].vuln) 
