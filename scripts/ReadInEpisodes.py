from rolls.models import Rolls, RollType
from episodes.models import Episode, Campaign
import csv

DATADIR = "zdata/"
C1DIR = "C1/"
C1TA = DATADIR + C1DIR + "C1 Times + Attendance"

#Episode.objects.all().delete()
file = "Episode-list.csv"
metaReader = csv.reader(open(file))
next(metaReader)
timeReader = csv.reader(open(C1TA + "/TD Campaign.csv"))
next(timeReader)
next(timeReader)
next(timeReader)
next(timeReader)
for metaRow,timeRow in zip(metaReader, timeReader): 

  campFile = "campaign.csv"
  campReader = csv.reader(open(campFile))
  next(campReader)
  campRow = []
  for line in campReader:
    if metaRow[0] == line[0]:
      campRow = line
      break
  
  campaign = Campaign.objects.update_or_create(num=campRow[0], name=campRow[1])
  num = int(metaRow[1])
  title = metaRow[2]
  description = metaRow[3]

  length = int(float(timeRow[1]))
  first_half_start = int(float(timeRow[9]))
  first_half_end = int(float(timeRow[10]))
  second_half_start = '';
  second_half_end = '';
  if timeRow[11] != '':
    second_half_start = int(float(timeRow[11]))
  if timeRow[12] != '':
    second_half_end = int(float(timeRow[12]))
  
  if second_half_start == '':
    episode = Episode.objects.update_or_create(campaign= campaign[0], num=num, title=title, description=description, length=length,first_half_start=first_half_start,
                                                first_half_end=first_half_end)
  else :
    episode = Episode.objects.update_or_create(campaign= campaign[0], num=num, title=title, description=description, length=length,first_half_start=first_half_start,
                                             first_half_end=first_half_end, second_half_start=second_half_start, second_half_end=second_half_end)
