# BridgeDeal
This is the object for the extracted data. It has the following attributes.
## Attributes
1. bbo_file: Number of the lin file from which it originated
2. tournament: Tournament name
3. Players: Players names in the order: [TO-DO]
4. hands: hands as 4 x 13 matrices of booleans, each one representing the presence of a card
5. bidding: the sequence of bidding in the form of a vector of numbers representing each bid
6. leader: the player that led, placed the lead
7. dealer: the player that started the contract
8. vuln: Vulnerability

## Example:
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
