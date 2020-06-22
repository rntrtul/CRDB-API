from rolls.models import Rolls, RollType
from episodes.models import Episode, Campaign
import csv

file = "Episode-list.csv"
reader = csv.reader(open(file))
next(reader)
for row in reader: 

  campFile = "campaign.csv"
  campReader = csv.reader(open(campFile))
  next(campReader)
  campRow = []
  for line in campReader:
    if row[0] == line[0]:
      campRow = line
      break
  
  campaign = Campaign.objects.get_or_create(num=campRow[0], name=campRow[1])
  num = int(row[1])
  title = row[2]
  description = row[3]
  episode = Episode.objects.get_or_create(campaign= campaign[0], num=num, title=title, description=description)
