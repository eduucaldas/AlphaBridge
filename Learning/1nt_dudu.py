# Template to acquire data from pickle
from os import sys
import path_jupy
sys.path.append(path_jupy.give_path())
from Pickle_Data.extract_data import load_file

filename = "Search.bin" # Check whether there is a Search.bin in this directory
data = load_file(filename)  # list of BridgeDeal
# ------------------------------
# Feel free to make everything more modularized. It's just that i had problems with importing in python3 :(


