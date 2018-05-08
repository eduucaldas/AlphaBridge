# AlphaBridge
Analysis on the choice of the lead in the game of Contract Bridge.


--------------------------------------
## Modules:
This project is designed in modules, each of them has different usages:
1. data: Downloads .lin files from Vugraph in BBO [5] and parses files to create hdfs dataframe. Also functions to search for specific biddings

2. learning: Different approaches to try and learn through the data of expert players, using CNN and ML methods

3. reinforcement_learning: Uses reinforcement learning based on the articles [1][2], using the OpenAI gym [4] and DDS [3]

4. legacy: Old functions and datasets in the older format.


## Contents:
### Data
This is the data module. It contains:
1. bbo: Scripts to download the .lin bbo files and those files compressed as raw_lin_data_i.7z

2. auxiliary_functions.py: Self-explanatory. For instance, functions to compute longest_color and strongest_color

3. enums.py: dicts to encode different aspects of Bridge

4. parser.py: parses the .lin files and creates a hdfs dataframe.

5. store.hdfs: hdfs dataframe

6. tools.py, enum.py: auxiliary functions and auxiliry dicts, used by parsing

7. symmetry.py: symmetry proposed by a Bridge player, that would generate more data for the case of No trumps


### Learning
Folder with learning methods based on CNNs and ML:
1. 1nt.ipynb: Approach using Scikit learn machine learning machinery

2. CNN_version1_for_1NTPPP.ipynb: Approach using CNN with TensorFlow

3. CNN_main.py: Final code that unifies our CNN approach with optimized parameters for the different objectives, e.g. determine the color of the leading card,  and analysis of correlations according to the bidding analyzed.

4. color_high_low.py: CNN to guess the best color and if should play high or low. Included in CNN_main

5. create_research_tree.py: creates prefix tree, so we can analyze which biddings are more recurrent, we found 72 that showed more than 300 data points.

6. path_jupy, template_use_data.py: Legacy.

7. treat_biddings.py: Pre-treatments to the data


### Reinforcement Learning
[TODO]


### Old
1. encode_and_parsing:

  a. encode: Encode and Decode the String representing the bidding to an array of numbers
  
  b. parsing: functions for reading the hands of players and determining the lead. Hands are encoded in 4 52-vectors of booleans representing the presence or not of the card, one for each player

2. parseHeading: Tools to decode the heading of .lin files according to HowToReadHeading

3. HowToReadHeading: Human decoding of .lin headings



## Aknowledgements
Thank you Véronique Ventos and Tristan for the guidance in this daring project
And specially to every member of the team: 
Ayman, Eduardo, Ian, Pierre-Emmanuel, Yann, Zigfrid and Ziyed!

## Citations
1. Automatic Bridge Bidding Using Deep Reinforcement Learning, Chih-Kuan Yeh
and Hsuan-Tien Lin
2. Contract Bridge Bidding by Learning, Chun-Yen Ho and Hsuan-Tien Lin
3. Double-Dummy Solver, http://privat.bahnhof.se/wb758135/
4. OpenAI, https://openai.com
5. Vugraph archive, http://www.bridgebase.com/vugraph_archives/vugraph_archives.php
