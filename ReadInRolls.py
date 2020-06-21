from rolls.models import Rolls, RollType
from episodes.models import Episode, Campaign
import csv

def findCamp (campaignNum):
  import csv
  campInfo = "campaign.csv"
  campReader = csv.reader(open(campInfo))
  camp = []
  for row in campReader:
    if campaignNum == row[0]:
      camp = row
      break
  
  campaign = Campaign.objects.get_or_create(num=camp[0])
  return campaign[0]

def getEp(Epnum):
  import csv
  epInfo = "Episode-list.csv"
  epReader = csv.reader(open(epInfo))
  ep = []
  for row in epReader:
    if Epnum == row[1]:
      ep = row
      break
  
  camp = findCamp(row[0])
  episode = Episode.objects.get_or_create(campaign= camp, num = ep[1], title=ep[2], description=ep[3])
  return episode[0]

rollsName = "C1-E001-CR.csv"

Rolls.objects.all().delete()
RollType.objects.all().delete()
with open(rollsName, newline='') as myFile:
  rollReader = csv.reader(myFile)

  next(rollReader)
  for row in rollReader:
    ep = getEp(row[0])
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

    roll, created = Rolls.objects.get_or_create(ep=ep, timeStamp=timeStamp,rollType=type[0],finalValue=totalVal, naturalValue=natVal, notes=notes)
    if created == False:
      print("duplicate roll, did not add to DB")

#delete these after testing views and stuff
#as reading in rolls will create a new rolltype, episode, character name if not found 

