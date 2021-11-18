#! /usr/bin/python
# latinCounter.py

import requests
import bs4
import re

# Get the root website
url = 'http://www.thelatinlibrary.com'
res = requests.get(url)
res.raise_for_status()

# Find all links one layer down
soup = bs4.BeautifulSoup(res.text, features='lxml')
layerOneLinks = []
layerOneResponses = soup.select('td a')[:-5]
for res in layerOneResponses:
    layerOneLinks.append(url + '/' + res.get('href'))

# Find all links two layers down
layerTwoLinks = []
for link in layerOneLinks:
        res = requests.get(link)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, features='lxml')
        layerTwoResponses = soup.select('td a')[:-2]
        for res in layerTwoResponses:
            layerTwoLinks.append(url + '/' + res.get('href'))

# Create output file
output_log = open('latinCountsOutput.log', 'w')

# Find all examples of e + h... or ex + h...
rePattern1 = re.compile(r'\be\b h\w+')
rePattern2 = re.compile(r'\bex\b h\w+')

pattern1_counter = 0
pattern2_counter = 0
for link in layerTwoLinks:
    print('Analyzing ' + link)
    try:
        res = requests.get(link)
        res.raise_for_status()
        text = res.text
        matchPattern1 = rePattern1.findall(text)
        pattern1_counter += len(matchPattern1)
        matchPattern2 = rePattern2.findall(text)
        pattern2_counter += len(matchPattern2)
        print('Found ' + str(len(matchPattern1)) + ' examples of e + h...')
        print('Found ' + str(len(matchPattern2)) + ' examples of ex + h...')
        if len(matchPattern1) > 0:
            output_log.write('Found matches of the first type in ' + link + ": \n\n")
            for match in matchPattern1:
                output_log.write(match + ', ')
            output_log.write('\n\n')
        if len(matchPattern2) > 0:
            output_log.write('Found matches of the second type in ' + link + ": \n\n")
            for match in matchPattern2:
                output_log.write(match + ', ')
            output_log.write('\n\n')
    except:
        continue

# Return results
print('Here are the grand totals.')
print('Found ' + str(pattern1_counter) + ' examples of e + h...')
print('Found ' + str(pattern2_counter) + ' examples of ex + h...')
