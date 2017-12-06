"""
This code gives tools to parse the heading of .lin files for useful data
These informations are associated each to one .lin, should probably be linked to their number instead of the games
the .lin used for examples were 46370 if you want to check it:
http://www.bridgebase.com/tools/handviewer.html?bbo=y&linurl=http://www.bridgebase.com/tools/vugraph_linfetch.php?id=46370
"""



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
    #output:
    #    (gotta finish this)


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

    return [parse_result(res) for res in raw_input.split(',')]
################################################

def parse_pn(raw_input):
	#input:
    #    String in the format:
    #	 "[player_1],...,[player_n]", with n from 8 to 12(according to zigfrid)
    #	 Example:
    #	 "Vanchev,Draganov,Bosev,Donev,Tsonchev,Karaivanov,Marashev,Gunev"
    #comments:
    #	 
    #output:
    #    list of players in the right order(see HowToReadHeading)
    
