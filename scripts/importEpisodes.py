import csv

def readInEpisode(timePath,metaReader):
  from rolls.models import Rolls, RollType
  from episodes.models import Episode, Campaign
  import csv

  timeReader = csv.reader(open(timePath))
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
    fhs = 9
    fhe = 10
    shs = 11
    she = 12
  
    campaign = Campaign.objects.update_or_create(num=campRow[0], name=campRow[1])

    if campaign[0].num == 2:
      fhs = 7
      fhe = 8
      shs = 9
      she = 10
    
    num = int(metaRow[1])
    title = metaRow[2]
    description = metaRow[3]

    length = int(float(timeRow[1]))
    first_half_start = int(float(timeRow[fhs]))
    first_half_end = int(float(timeRow[fhe]))
    second_half_start = '';
    second_half_end = '';
    if timeRow[shs] != '':
      second_half_start = int(float(timeRow[shs]))
    if timeRow[she] != '':
      second_half_end = int(float(timeRow[she]))
    
    if second_half_start == '':
      episode = Episode.objects.update_or_create(campaign= campaign[0], num=num, title=title, description=description, length=length,first_half_start=first_half_start,
                                                  first_half_end=first_half_end)
    else :
      episode = Episode.objects.update_or_create(campaign= campaign[0], num=num, title=title, description=description, length=length,first_half_start=first_half_start,
                                              first_half_end=first_half_end, second_half_start=second_half_start, second_half_end=second_half_end)

DATADIR = "zdata/"
C1DIR = "C1/"
C2DIR = "C2/"
C1TA = DATADIR + C1DIR + "C1 Times + Attendance"
C2TA = DATADIR + C2DIR + "C2 Times + Attendance"

file = "Episode-list.csv"
metaReader = csv.reader(open(file))
next(metaReader)
readInEpisode(C1TA + "/TD Campaign.csv", metaReader)
readInEpisode(C2TA + "/WM Campaign.csv",metaReader)
