# How to use!
## Extract the bidding you want to analyse
1. Go to Pickle_Data
2. Unrar the All.rar. This will generate a .bin file, which is our database of objects BridgeDeal compressed in a pickle
3. Go to the end of extract_data, change the search to whatever you want and run. This will create a Search.bin in this Directory
4. To load the pickle just pick the template from 1nt_dudu and paste in your function :)
Ps.: For more detail on the BridgeDeal obj check extract_data

The approach to retrieve the games was discontinued since "extract_part0.py" does a much better job.

---------------------
First try at solving 1NTPPP

To extract games that fit the criteria (1NTPPP), we proceed as follows:

1) We search for the pattern 1NTPPP in the lin files in "raw_lin_files"

2) We format the output from the first part into a more readable string

3) We parse the output from the previous step to a vector and try ML for the first time.

Each step has its folder.

---------------------


