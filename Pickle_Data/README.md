#Pickle_Data
This is the package for our pickle Database and its inteface


## Contents:
1. All.rar: Compressed Database. 1st thing: Uncompress it. It'll generate All.bin,
which is our database as a pickle, you'll manipulate it through extract_data
2. extract_data: Interface with the database. It can do: 

    a. load, through load_file, which reads from a pickle.
    
    b. save, through save_file, which saves a pickle
    
    c. extract, through extract_to_pickle, which performs a search by bidding and 
    saves the matching items in a pickle.
    
    Ps.: It does everything storing data in BridgeDeal objects, explained below 
3. old: legacy code


## BridgeDeal
This is the object for the extracted data. It has the following attributes.
### Attributes
1. bbo_file: Number of the lin file from which it originated
2. tournament: Tournament name [TO-DO]
3. Players: Players names in the order: [TO-DO]
4. hands: hands as 52-vector of booleans, each one representing the presence of a card
5. bidding: the sequence of bidding in the form of a vector of numbers representing each bid
6. leader: the player that led, placed the lead
7. dealer: the player that started the contract
8. vuln: Vulnerability

### Example:
Example of object
    BridgeDeal(
    	bbo_file = 00013,
    	tournament = None,
    	players = None,
    	hands = [[False False False False  True False False False  True  True False  True
      False False False  True False False False  True False False False False
      False  True False  True  True False False  True False False False False
       True False False  True False False False  True False False False False
      False False False False]
     [False False  True  True False  True False False False False  True False
      False  True False False False  True False False False  True False False
       True False  True False False False  True False False False  True False
      False False False False False False False False False  True False False
      False False  True False]
     [ True False False False False False False  True False False False False
      False False False False  True False  True False  True False False False
      False False False False False  True False False  True False False  True
      False  True False False False  True  True False False False False False
       True False False  True]
     [False  True False False False False  True False False False False False
       True False  True False False False False False False False  True  True
      False False False False False False False False False  True False False
      False False  True False  True False False False  True False  True  True
      False  True False False]],
    	bidding = [3, 0, 0, 0],
    	leader = 0,
    	dealer = 3,
    	lead = SJ,
    	vuln = b
    )
