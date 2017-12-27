# -*- coding: utf-8 -*-
"""
This code gives tools to parse the heading of .lin files for useful data
These informations are associated each to one .lin, should probably be linked to their number instead of the games
the .lin used for examples were 46370 if you want to check it:
http://www.bridgebase.com/tools/handviewer.html?bbo=y&linurl=http://www.bridgebase.com/tools/vugraph_linfetch.php?id=46370
"""
#These two below, have to be updated to merge into Encode_and_Parsing
errorLog = {'dealer':0, 'hands': 0,'lead': 0, 'bid':0, 'leader':0, 'bidding': 0, 'heading': 0}
error = {'dealer':-1, 'hands': None, 'lead': None, 'bid':None, 'leader':-1, 'bidding': None, 'contract': None,'declarer': None, 'tricks': -1}

PLAYERS = {0:'S', 1:'W', 2:'N', 3:'E'}
OUT_OF_RANGE = 'U'# dirty trick: U for no out of range exception in SUITS
SUITS = ['S', 'H', 'D', 'C', OUT_OF_RANGE] 
SUITSBID = ['N'] + SUITS[:4]

def parse_vg(raw_input):
	#input:
    #    String in the format:
    #	 "[Name Tournament],[Round],[?],[# of 1st game],[# of last game],[Team 1],[CarryOver Team 1],[Team 2],[CarryOver Team 2]"
    #	 Example:
    #	 "XL-th International Bridge Festival Varna,Teams KWS- Round 11,I,1,32,Bridge +,0,Grisho,0"
    #comments:
    #	 Don`t know what is [?], but want to save it anyways
    #output:
    #    all information that was in the string
    
    #name_tournament, round_name, weird_char, first_game, last_game, team_1, carryOver1, team_2, carryOver2 = raw_input.split(',')
    return raw_input.split(',')# gotta analyse cases for team tournamentes and player tournaments
################################################
def parse_result(code):
	#input:(gotta finish this)
	#    Result, in the format:(gotta finish this)
	#	 ABC(X)DE, AB: contract, 
	#	 Examples:(gotta finish this)
	#	 1NW=,3NW-2,5CSx-2,PASS
	#comments:
	#	 Still gotta find out how redouble is encoded
	#	 Problem with redouble!, verify if it is really xx in test!
	#output:
	#   (isPass, contract, declarer, double, tricks) 
	#	(isPass as bool, contract as "[level][trump]", declarer as char, double as int (almost bool but, if redouble then 2), number of tricks as int)

	isPass = False
	contract = error['contract']
	declarer = error['declarer']
	double = 0
	tricks = error['tricks']

	if(len(code) < 4):
		errorLog['heading']+=1
	elif(code == "PASS"):
		isPass = True
	else:
		pt = 0#this is the pointer in the array
		if(((int(code[pt])-1) in range(7)) and (code[pt + 1] in SUITSBID)):
			contract = code[pt:pt+2]
		else:
			errorLog['heading']+=1
			return (isPass, contract, declarer, double, tricks)
		pt+=2

		if(code[pt] in PLAYERS.values()):
			declarer = code[pt]
		else:
			errorLog['heading']+=1
			return (isPass, contract, declarer, double, tricks)

		double = 0
		pt += 1#beginning of the tricks parsing
		if(code[pt] == 'x' and len(code) > pt + 1):
			pt += 1
			double = 1
		if(code[pt] == 'x' and len(code) > pt + 1):#what is the code for redouble, i think it is 'xx'
			pt += 1
			double = 2

		tricks = 6 + int(code[0])
		
		if(code[pt] == '+'):
			if((len(code) == pt + 2) and (tricks + int(code[pt+1]) in range(14))):
				tricks += int(code[pt+1])
			else:
				errorLog['heading']+=1
		elif(code[pt] == '-'):
			if((len(code) == pt + 2) and (tricks - int(code[pt+1]) in range(14))):
				tricks -= int(code[pt+1])
			else:		
				errorLog['heading']+=1
		elif(code[pt] != '='):
			errorLog['heading']+=1

	return (isPass, contract, declarer, double, tricks)



def parse_rs(raw_input):
	#input:
    #    String in the format:
    #	 "{,}[result_1],...,[result_n]", with n = 2*[number of rooms]
    #	 Example:
    #	 ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,4HE=,3NW-2,2NE=,2CE+1,7NW=,7DE=,3NS=,3NN+1,2SN+1,2SN+1,6HN+1,6HN=,2CS+1,3NS+1,3NW-1,3NW="
    #comments:
    #	 
    #output:
    #    all information that was in the string

    return [parse_result(res) for res in raw_input.split(',') if res != ""]
################################################
def swap(v, a,b):
	(v[a],v[b]) = (v[b],v[a])

def parse_pn(raw_input):
	#input:
    #    String in the format:
    #	 "[player_1],...,[player_n]", with n from 8 to 12(according to zigfrid)
    #	 Example:
    #	 "Vanchev,Draganov,Bosev,Donev,Tsonchev,Karaivanov,Marashev,Gunev"
    #comments:
    #	 sometimes players have North, South, West or East as names, are these bots?
    #	 Uncomment in ROOMS to get a 2-tuple of the rooms instead
    #	 Can there really be 12 players, yet to find
    #output:
    #    2-tuple with the 2 teams in the order SWNE(perhaps teams have 6 players)
    
    players = raw_input.split(',')
    #ROOMS
    #openRoom = players[0:len(players)/2]
    #closedRoom = players[len(players)/2:len(players)]
    #return (openRoom, closedRoom)
    #ROOMS
    (team_1, team_2) = (players[0:len(players)/2:2] + players[len(players)/2+1:len(players):2],players[1:len(players)/2 +1:2]+players[len(players)/2:len(players):2])
    swap(team_1, 1, 2)
    swap(team_2, 1, 2)
    swap(team_2, 0, 1)
    swap(team_2, 2, 3)
    return (team_1, team_2)


def test_parse_rs():
    raw_in = ",,,,,,,,,,,,,,,,,,,PASS,4HE=,3NW-2,2NE=,2CE+1,7NWx=,7DE=,3NS=,3NN+1,2SN+1,2SN+1,6HN+1,6HN=,2CS+1,3NS+1,3NW-1,3NW="
    treated = parse_rs(raw_in)
    inp = [res for res in raw_in.split(',') if res != ""]
    print(zip(inp, treated))

def test_parse_pn():
	raw_in = "Bjerkset,Olsen,Stafne,Bjørkan,South,West,North,East"
	print(raw_in)
	print(parse_pn(raw_in))

def test_parse_vg():
	meaning = ["[Name Tournament]","[Round]","[?]","[# of 1st game]","[# of last game]","[Team 1]","[CarryOver Team 1]","[Team 2]","[CarryOver Team 2]"]
	raw_in = "Norwegian Swiss Teams,Match 14 of 16,I,8,14,STAR,0,Veggen,0"
	treated = parse_vg(raw_in)
	print(zip(meaning, treated))

#if __name__ == "__main__":
#	test_parse_rs()
	