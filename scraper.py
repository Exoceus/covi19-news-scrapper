from bs4 import BeautifulSoup
from requests import get
import re
import json

url = 'https://www.snopes.com/collections/new-coronavirus-collection/'
response = get(url)

soup = BeautifulSoup(response.text, 'html.parser')
relevant_body = soup.find("div", {"class": "card"}).ul
items = relevant_body.find_all('a')

links = []

for link in items:
    links.append(link.get('href'))

data = []

for link in links:
    url = link
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    main_container = soup.find("section", {"class": "collected-list"})
    cards = soup.find_all("div", {"class": "card-body"})
    card = {'title': '', 'subtitle': '', 'value': ''}

    for entry in cards:
        print(entry.prettify()[:500], "\n")
        if entry.find("h5") != None:
            card['title'] = entry.find("h5").text
            card['subtitle'] = entry.find("p").text
            temp_string = entry.find("div", {"class": "media-body"}).text
            card['value'] = re.sub('\s+', '', temp_string)

        data.append(card)

        card = {'title': '', 'subtitle': '', 'value': ''}
    # cards = relevant_body.find_all("article")

pyDict = {}
pyDict['data'] = [data]

json_data = json.dumps(pyDict)
print(json_data)
