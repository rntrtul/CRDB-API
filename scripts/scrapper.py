import requests
import csv
from bs4 import BeautifulSoup

BASEURL = "https://criticalrole.fandom.com"
EPLIST = "/wiki/List_of_episodes"
page = requests.get(BASEURL + EPLIST)

soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='mw-content-text')
tables = soup.find_all('table', class_="wikitable sortable")
writer = csv.writer(open ('TD-Episode-list.csv', 'w'))
writer.writerow(["Campaign", "Epiosde", "Title", "Description"])

for table in tables:
  rows = table.find_all('tr')
  
  for row in rows:
    csvRow = []
    a = row.find('a')
    if None == a:
      continue
    title = a.get('title')
    if title.endswith('(episode)'):
      title = title[:-10]

    link = a.get('href')
    page = requests.get(BASEURL + link)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='mw-content-text')
    paragraphs = results.find_all('p')
    rightP = paragraphs[0]
    found = False
    for paragraph in paragraphs:
      if title in paragraph.text:
        found = True
        rightP = paragraph
        break
    
    if found == False:
      continue
    text = rightP.text
    
    infoCEP = text[text.find('(')+1:text.find(')')]
    xIndex = infoCEP.find('x')
    print(infoCEP)
    campaign = int(infoCEP[:xIndex]) 
    episode = int(infoCEP[xIndex + 1:])
    description = text[text.find('.') + 2:len(text)-1]

    csvRow.extend([campaign, episode, title, description])
    writer.writerow(csvRow)
    