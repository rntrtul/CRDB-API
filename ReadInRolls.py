from rolls.models import Rolls, RollType
from episodes.models import Episode, Campaign
import csv

def getEpisode(num):
  import csv
  from episodes.models import Episode, Campaign
  file = "Episode-list.csv"
  reader = csv.reader(open(file))
  next(reader)
  foundRow = []
  for row in reader:
    if num == row[1]:
      foundRow = row
      break
  
  campFile = "campaign.csv"
  campReader = csv.reader(open(campFile))
  next(campReader)
  campRow = []
  for row in campReader:
    if foundRow[0] == row[0]:
      campRow = row
      break
  
  campaign = Campaign.objects.get_or_create(num=campRow[0], name=campRow[1])
  episode = Episode.objects.get_or_create(campaign= campaign[0], num = foundRow[1], title=foundRow[2], description=foundRow[3])
  return episode[0]


rollsName = "C1-E001-CR.csv"

Rolls.objects.all().delete()
RollType.objects.all().delete()
Episode.objects.all().delete()
Campaign.objects.all().delete()

with open(rollsName, newline='') as myFile:
  rollReader = csv.reader(myFile)

  next(rollReader)
  for row in rollReader:
    ep = getEpisode(row[0])
    timeStamp = int(float(row[1]))
    type = RollType.objects.get_or_create(name=row[3])
    totalVal = 0
    if row[4] == "Nat1":
       totalVal = 1
    elif row[4] == "Nat20": 
      totalVal = 20
    elif row[4] != "Unknown": 
      totalVal = int(row[4])

    natVal = 0
    if row[5] != "Unknown" and row[5] != '':
      natVal = int(row[5])

    notes= row[9]

    roll, created = Rolls.objects.get_or_create(ep=ep, time_stamp=timeStamp,roll_type=type[0],final_value=totalVal, natural_value=natVal, notes=notes)
    if created == False:
      print("duplicate roll, did not add to DB")

#delete these after testing views and stuff
#as reading in rolls will create a new rolltype, episode, character name if not found 

