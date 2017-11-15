#Ian Duleba

#Only run this code if there is something wrong with the file All.bin (which I hope there isn't but it would be great if someone were to double check it).
#Otherwise you don't need stress in your life, just go away.

#I uploaded a compressed file called All.rar with the results. Be aware! The entire list has 1 Gb when uncompressed.

#You should run this code inside the folder raw_lin_data from our project, it assumes the structure of folders as I have defined it.

#And don't forget to put inside the same folder the file encode_and_parsing.py which has Dudu's functions. It's in the folder auxiliary_functions of the repository.

#start reading from the Main()

import sys
import os
import re
import numpy as np
import pickle
import time
import encode_and_parsing as eap

class BridgeDeal:
	def __init__(self, bbo_file, tournament, players, hands, bidding, leader, dealer, lead, vuln):
		self.bbo_file = bbo_file
		self.tournament = tournament
		self.players = players
		self.hands = hands
		self.bidding = bidding
		self.leader = leader
		self.dealer = dealer
		self.lead = lead
		self.vuln = vuln
	def __eq__(self, other):
		return self.bbo_file == other.bbo_file and self.tournament == other.tournament and self.players == other.players and self.bidding == other.bidding and (self.hands == other.hands).all() and self.leader == other.leader and self.dealer == other.dealer and self.lead == other.lead and self.vuln == other.vuln



#This function interprets the list received (variable "contents"): it will find all good matches (well formatted) and append them to DATA, in order of ocurrence
def interpret(contents, DATA, bbo_file):

	#initializing lists
	game = []
	leads = []
	biddings = []

	#auxiliary variables
	hands_texts=[] #hands of a match in the form: 1SKT32HJ984DJT52C9,SAQJ86HK63DK93C75,S94HT5D864CAQJT62,S75HAQ72DAQ7CK843
	bidding=[] #bidding of a match
	lead=-1 #=-1 while we do not read a "pc", = the lead string after reading a "pc"
	i=0 #counter

	#loop through the "contents"
	while (i<len(contents)):
		#if we find a command in position i
		if(eap.isCommand(contents[i])):

			#we need to know which command

			if eap.commands[contents[i]] == 0: #md, start of hands in the next item on the list

				if len(hands_texts)!=len(leads): #error handling, no information about the previous game

					if len(hands_texts)>len(leads):
						del hands_texts[-1] #we exclude since the match was dropped by the players
					else:
						return False #there are only 4 files that fit this condition, we shall ignore them

				#reset auxiliary variables, we are reading a new match
				bidding=[]
				lead=-1
				hands_texts.append(contents[i+1])
				i=i+2

			elif eap.commands[contents[i]] == 1: #sv, start of bidding in the next item on the list
				if contents[i+1] != '':
					bidding=[]
					bidding.append(contents[i+1])
				i=i+2

			elif eap.commands[contents[i]] == 2: #pc, lead is the next item on the list
				if lead==-1:
					#flush bidding
					biddings.append(bidding)

					#get lead
					lead=contents[i+1]
					leads.append(lead)
				i=i+2

			elif eap.commands[contents[i]] == 3: #mb, bidding in the next item on the list
				if contents[i+1] != '':
					bidding.append(contents[i+1])
				i=i+2

			elif eap.commands[contents[i]] == 5: #qx, start of hands (some files do not have the command md, the start of hands, and we will treat them here)

				#lets make sure there is no md following down the list
				if (contents[i+2]!='md' and contents[i+3]!='md' and contents[i+4]!='md' and contents[i+5]!='md' and contents[i+6]!='md'): 

					#if we look 2 items ahead, it should be the hands
					#note: 54 is the correct length for a string like:
					#1SKT32HJ984DJT52C9,SAQJ86HK63DK93C75,S94HT5D864CAQJT62,S75HAQ72DAQ7CK843
					if(len(contents[i+2])==54):

						if len(hands_texts)!=len(leads): #error handling, no information about the previous game

							if len(hands_texts)>len(leads): #we exclude since the match was dropped by the players
								del hands_texts[-1]
							else:
								return False #there are only 4 files that fit this condition, we shall ignore them

						#reset auxiliary variables, we are reading a new match
						bidding=[]
						lead=-1
						hands_texts.append(contents[i+2])
						i=i+3
					else:
						i=i+1

				#but if there is, we just skip the item
				#note: we could have just jumped to the nearest md, but whats the hurry?
				else:
					i=i+1

			#if it is some other command, we skip it
			#note: we could have done i=i+2, but there are a few problematic files, so better safe than sorry.
			else:
				i=i+1

		#contents[i] is not a command
		else:
			i=i+1 #we read the next item in the list

	if len(hands_texts)!=len(leads): #no information about the game
		if len(hands_texts)>len(leads):
			del hands_texts[-1]
		else:
			return False #there are only 4 files that fit this condition, we shall ignore them

	#lets recheck if we didint include incomplete games
	#not necessary, but I have OCD
	if(len(leads)!=len(hands_texts) or len(biddings)!=len(hands_texts)):
		#print(len(hands_texts),len(leads),len(biddings))
		return False
	
	#lets create BridgeDeal's objects from matches that dont have any errors in them and then append them in DATA
	for i in range(len(hands_texts)):

		dealer, hands = eap.pick_hands(hands_texts[i])
		game.append(hands)

		if ((hands != eap.error['hands']) and (dealer != eap.error['dealer'])): #error check
			leader, game[i] = eap.pick_lead(hands_texts[i], leads[i], game[i])

			#note: the first item of a bidding is the vulnerability
			#Dudu created a coded version of the bidding, it occupies less space and it'll be easier to run ML and DL later. 
			biddings_encoded = eap.encodeRaw_Bidding(biddings[i][1:])

			if (leader != eap.error['leader']) and (biddings_encoded != eap.error['bidding']): #error check
				#create a BridgeDeal object and append it to DATA
				DATA.append(BridgeDeal(bbo_file, None, None, game[i], biddings_encoded, leader, dealer, leads[i], biddings[i][0]))

	return True
			


def read_lin_file(file_path, DATA):
	f = open(file_path,"r")

	contents=f.read().replace("\r","").replace("\n","") #we remove \r and \n from the file
	list_of_contents=contents.split("|") #and we split it.

	#lets call interpret; it will append to DATA all wellformed matches present on this file

	#file_path will be something like "XXX/XXXXX" or "XXX/XXXXX.lin"
	if (file_path[-1] == 'n'):
		#file_path[-9:-4] is the file number from bbo
		readable = interpret(list_of_contents, DATA, file_path[-9:-4])
	else:
		#file_path[-5:] is the file number from bbo
		readable = interpret(list_of_contents, DATA, file_path[-5:])

	f.close()

#reads each file inside the folder
def read_folder(path, DATA):
	for filename in os.listdir(path):
		read_lin_file(path+filename, DATA)
		
last_folder = 535 #535 folders, this is hardcoded and it would be better if it wasn't. Meh
#reads all folders in the database (format of the folders and files as created in the project)
def read_folders(DATA):
	for i in range(last_folder): 

		#defines "path", i.e., the folders name 
		if i<10:
			path="00"+str(i)+"/"
		else:
			if i<100:
				path="0"+str(i)+"/"
			else:
				path=str(i)+"/"

		sys.stdout.write("\rProcessing .lin files. Folder: "+path+str(last_folder-1))
    		sys.stdout.flush()
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
	DATA=[] #list of BridgeDeal objects

	start = time.time()

	read_folders(DATA)
	print " ...Done"

	#if you want to read only a specific file, comment "read_folders(DATA)" above and uncomment the line below
	#read_lin_file("508/50871.lin", DATA)
	
	#How many matches were discarted due to errors?
	print "Number of matches discarted due to parsing errors: ", eap.errorLog

	end_parser = time.time()
	print "Time to read from .lin files: {:,.2f} seconds".format(end_parser - start) #time to run the script

	#now, we have all the information we need in DATA. We can save it or whatever...
	save_file("All.bin", DATA)
	end_save = time.time()
	print "Time to save data to disk: {:,.2f} seconds".format(end_save - end_parser) #time to save DATA

	#loading DATA from a file
	#DATA = load_file("All.bin")
	end_load = time.time()
	print "Time to read data from disk: {:,.2f} seconds".format(end_load - end_save) #time to retrieve DATA

	#let's the first deal
	print DATA[0].hands, DATA[0].bidding, DATA[0].leader, DATA[0].dealer, DATA[0].lead, DATA[0].vuln
