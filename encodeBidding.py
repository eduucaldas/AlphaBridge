# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 10:18:39 2017

@author: eduai_000
"""
OUT_OF_RANGE = 'U'# dirty trick: U for no out of range exception in SUITS

SUITS = ['S', 'H', 'D', 'C', OUT_OF_RANGE] 
#SUITSBID = ['N'] + SUITS[:4]
#BIDS = ['P','R','D'] + [str(i + 1) + s for i in range(7) for s in SUITSBID]
BIDS = ['P', 'R', 'D',
        '1N', '1S', '1H', '1D', '1C',
        '2N', '2S', '2H', '2D', '2C',
        '3N', '3S', '3H', '3D', '3C',
        '4N', '4S', '4H', '4D', '4C',
        '5N', '5S', '5H', '5D', '5C',
        '6N', '6S', '6H', '6D', '6C',
        '7N', '7S', '7H', '7D', '7C']
#BIDSMAP = dict(zip(BIDS, range(len(BIDS))))
BIDSMAP = {'P': 0, 'R': 1, 'D': 2,
           '1N': 3, '1S': 4, '1H': 5, '1D': 6, '1C': 7,
           '2N': 8, '2S': 9, '2H': 10, '2D': 11, '2C': 12,
           '3N': 13, '3S': 14, '3H': 15, '3D': 16, '3C': 17,
           '4N': 18, '4S': 19, '4H': 20, '4D': 21, '4C': 22,
           '5N': 23, '5S': 24, '5H': 25, '5D': 26, '5C': 27,
           '6N': 28, '6S': 29, '6H': 30, '6D': 31, '6C': 32,
           '7N': 33, '7S': 34, '7H': 35, '7D': 36, '7C': 37}
#Count where the error occurred, e.g. if it was in dealer
errorLog = {'dealer':0, 'hands': 0,'entame': 0, 'bid':0, 'leader':0, 'bidding': 0}
#we can perhaps implement it to show in which file the error occurred occurred

#for readability and making it easier to change after :)
error = {'dealer':-1, 'hands': None, 'entame': None, 'bid':None, 'leader':-1, 'bidding': None}

def pretreatBidding(raw_bidding):
    #input:
    #    list of raw_bid strings
    #comments:
    #    bids should be something in BIDS, not case sensitive and maybe with a '!' at the end, we fiz all this problems
    #output:
    #    list of bid strings, all capitalized and with no '!'
    bidding = []
    for bid in raw_bidding:
        bid = bid.upper()#fix caseSensitive
        bid = bid.replace("!", "")#fix '!'
        if(isValidBid(bid)):#fix: in BIDS
            bidding.append(bid) 
        else:
            errorLog['bidding']+=1
            return error['bidding']
    
    
    return bidding
         
def encodeBid(bid):
    #input: 
    #    bid as string. 
    #comments:
    #    verifies if valid bid, ie whether its on our BIDS
    #output:
    #    puts in the code according to BIDSMAP
    code = BIDSMAP.get(bid, error['bid'])
    if(code == error['bid']):
        errorLog['bid']+=1
    return code

def decodeBid(code):
    #input:
    #    bid coded, as an integer [0-37]
    #comments:
    #    Verifies if code is in our BIDS, warning message appears
    #output:
    #    bid as a human readable bid
    try:
        return BIDS[code]
    except IndexError:
        print('your code was weird')
        return error['code'] 
    
def encodeBidding(bidding):
    #input:
    #    pretreated bidding as a list of strings
    #comments:
    #    
    #output:
    #    code as list of codes coming from each bid
    errorStart = errorLog['bid']
    code = [encodeBid(bidding[i]) for i in range(len(bidding))]
    if(errorLog['bid'] - errorStart == 0):
        return code
    else:
        errorLog['bidding']+=1
        return error['bidding']

def isValidBid(bid):
    #input:
    #    bid as string
    #comments:
    #    Attention, this verifies only if the bid has the right size, with '!' or not
    #output:
    #    boolean: is it in the proper format
    return (bid in BIDS)
###################Main Functions##########################
def encodeRaw_Bidding(raw_bidding):
    #input:
    #    list of raw_bidding, just as they came out from @Ian
    #comments:
    #    Look at other functions, has error handling
    #output:
    #    code following BIDSMAP
    bidding = pretreatBidding(raw_bidding)
    return encodeBidding(bidding)  


def decodeBidding(code):
    #input:
    #    code fo the bidding
    #comments:
    #    decodeBid has some python error handling :), if there`s a problem it`ll print message
    #output:
    #    bidding as list of strings
    if(code == None):
        return None
    else:
        return [decodeBid(c) for c in code]
############################################# 

def testDudu(raw_data):
    #input:
    #    format: "1S|mb|p|mb|2D|mb|p|mb|3S!|mb|p|mb|4H|mb|d|mb|p|mb|p|mb|r|mb|p|mb|4N|mb|p|mb|5H|mb|p|mb|5N|mb|p|mb|6S|mb|p|mb|p"
    #comments:
    #    for the input just pick any .lin and pick the string between the first and the last |mb|
    #output:
    #    prints the bidding list as it was read, the code list, and the bidding decoded from the code
    #raw_data.split("|mb|")
    #print(raw_data)
    code = encodeRaw_Bidding(raw_data)
    bidding = decodeBidding(code)
    print(code)
    print(bidding)
        
#testDudu(['p', '1D', '1S', '2C', '2S', '3C', 'p', '4C', 'p', '5C', 'p', 'p', 'p'])

