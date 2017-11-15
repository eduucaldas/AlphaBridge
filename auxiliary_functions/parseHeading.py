"""
This code gives tools to parse the heading of .lin files for useful data
These informations are associated each to one .lin, should probably be linked to their number instead of the games
"""


def parse_vg(raw_input):
	#input:
    #    String in the format:
    #	 "[Name Tournament],[Round],[?],[# of 1st game],[# of last game],[Team 1],[CarryOver Team 1],[Team 2],[CarryOver Team 2]"
    #	 Example:
    #	 "C 2017 Vanderbilt QF,1 of 4,I,1,15,Schermer,0,Rosenthal,0"
    #comments:
    #	 Don`t know what is [?], but want to save it anyways
    #output:
    #    all information that was in the string
################################################
def parse_result():
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
    #	 "[result_1],...,[result_n]", with n = 2*[number of rooms]
    #	 Example:
    #	 "1NW=,3NW-2,3SS-2,2NW-2,5CSx-2,4SW+1,PASS,3NN-1,5SS=,5CEx-4,6HW-1,4HW+1,1NE+2,2HE+1,1NN=,1SW+1,4SW+2,6DW-1,1NW+1,3NW=,2HE-3,4SW-4,4HE=,4HE-1,3SE-1,3SE-3,2DEx-1,3NS=,2DN=,2DN+2"
    #comments:
    #	 
    #output:
    #    all information that was in the string
################################################

def parse_pn(raw_input):
	#input:
    #    String in the format:
    #	 "[player_1],...,[player_n]", with n from 8 to 12(according to zigfrid)
    #	 Example:
    #	 "De Knijff,Olanski,Fredin,Vainikonis,Skrzypczak,Blakset,Gierulski,Bruum"
    #comments:
    #	 
    #output:
    #    list of players in the right order(see HowToReadHeading)