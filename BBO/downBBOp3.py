#python v3.*
import requests
import re

#This program will download in the format .lin all the results from a search from the URL below

#Search field from the website http://www.bridgebase.com/vugraph_archives/vugraph_archives.php
search='XIX'

URL = 'http://www.bridgebase.com/vugraph_archives/vugraph_archives.php'
payload = (('searchstring', search), ('command', 'search'))
session = requests.session()
r = requests.post(URL, data=payload)

match = re.findall(r'"(http\://www\.bridgebase\.com/tools/vugraph_linfetch\.php\?id=[0-9]+)"', r.text)

for i in range(len(match)):
    name = re.findall(r'=([0-9]+)', match[i])
    print(name)
    response = requests.get(match[i])
    if response.status_code == 200:
        f=open(name[0]+'.lin', 'w')
        f.write(response.content.decode('utf-8'))
        f.close()
    else:
        print('Woops')