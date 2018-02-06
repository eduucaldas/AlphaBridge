# AlphaBridge
IA qui implemente l'entame au bridge


--------------------------------------
## How to Use:
This project is designed in modules, each of them has different usages:
1. Download_BBO: Downloads .lin files from Vugraph in BBO
2. parsing: Parses the .lin files to create a database with BridgeDeal objects in form of pickles
3. Pickle_Data: Interface with the database. Can do save/write/extract with bidding
4. Learning: Learning algorithms that use the result of the extract as data.

## Contents:
### Learning
Folder with the learning algorithms, you will probably need to extract some data
 here, follow-up instructions in Learning/README
1. 1nt.ipynb: Approach using Scikit learn machine learning machinery (Zig) 

2. CNN_version1_for_1NTPPP.ipynb: Approach using CNN with TensorFlow (P-E)

3. Deep Learning: Approach using FFNN with TF (Zyied)

4. template_use_data: template on how to extract data from the extracted pickle.

5. path_jupy: work_around for importing other modules to jupyter

6. Search.bin (you'll add this): This will be the result of your extraction

### auxiliary_functions
Folder with parsing auxiliary functions that could be useful in many ways.
1. encode_and_parsing:

  a. encode: Encode and Decode the String representing the bidding to an array of numbers
  
  b. parsing: functions for reading the hands of players and determining the lead. Hands are encoded in 4 52-vectors of booleans representing the presence or not of the card, one for each player

2. parseHeading: Tools to decode the heading of .lin files according to HowToReadHeading

3. HowToReadHeading: Human decoding of .lin headings

### Download_BBO
1. raw_lin_data: .lin from 42300 to 53439, downloaded from BBO. The rest (00000-42299) are in
 "https://github.com/eitazhou/bridge_played_hands/tree/master/raw_lin_data"
 ATTENTION, don't overwrite directory 121 that is here, it comes with minor bugs from BBO

2. downBBOpX.py: X stands for the python version. Downloads results of a search from: "http://www.bridgebase.com/vugraph_archives/vugraph_archives.php"

3. download_BBO_new_lins: script used to download raw_lin_data. Should run again if you want most recent games (last ran 29/09/17)

### parsing
1. Parsing_first_try: Quick parsing to generate the 1NTPPP data used on first analysis

2. extract_part0.py: Final extraction, parses all files and generates a pickle, All.bin, which is compressed as .rar in the Pickle_Data

### Pickle_Data
Folder with the data we were able to extract and interface to interact with this data
1. All.rar: All the data we obtained,(~2 million games). It is nothing more than a list of BridgeDeal's objects generated by "extract_part0.py". Be aware! The file has 1 Gb when uncompressed. To use it take a look at "extract_data.py".

2. extract_data.py: This script allows you to manipulate (read/search/save) our database of played hands. Probably the file you are looking for. The data is extracted in the form of a BridgeDeal Object with all the information, check the Readme of this directory for more info.

### SQL_Data
1. tournament-script.sql: Skeleton of the SQL database

## Aknowledgements
Thank you Véronique Ventos and Tristan for the guidance in this daring project
And specially to every member of the team: 
Ayman, Eduardo, Ian, Pierre-Emmanuel, Yann, Zigfrid and Zyied!
