#Ian Duleba 28/09/2017
#This script dowloads lin files numbered from 42300 and 53439
#So that we can complete the database from https://github.com/eitazhou/bridge_played_hands/tree/master/raw_lin_data
#You should run it in raw_lin_data
#Only run it if you want to download the files again, I have already uploaded them in github

from multiprocessing.pool import ThreadPool
from time import time as timer
from urllib2 import urlopen
import os

start = 42300 #1st lin file we want (the last in bridge_played_hands is 42367)
end = 53439 #last one (game played on 2017-09-24)

SITE = "http://www.bridgebase.com/tools/vugraph_linfetch.php?id="
urls = [SITE+str(s) for s in range(start,end+1)] #urls of the files

#creating the folders
#Let's keep the format from bridge_played_hands:
#name of the folder = first three digits of the lin files
for directory in [str(s) for s in range(423,534+1)]:
	if not os.path.exists(directory):
		os.makedirs(directory)

def fetch_lin_file(url):
	#name of the folder = first three digits of the lin files
	filename = url[-5:-2]+"/"+url[-5:]

	try:
		response = urlopen(url)
		f=open(filename+'.lin', 'w')
		f.write(response.read())
		f.close()
		return url, None

	except Exception as e:
		return url, e

#download them in parallel
#based on https://stackoverflow.com/questions/16181121/a-very-simple-multithreading-parallel-url-fetching-without-queue
start = timer()
results = ThreadPool(20).imap_unordered(fetch_lin_file, urls)#20 requests at a time
for url, error in results:
    if error is None:
        print("%r fetched in %ss" % (url[-5:], timer() - start))
    else:
        print("Error fetching %r: %s" % (url, error))
print("Elapsed Time: %s" % (timer() - start,))
