from rolls.models import Rolls, RollType
from episodes.models import Episode, Campaign
from characters.models import Character
import csv
import os


DATADIR = "zdata/"
C1DIR = "C1/"
C1ROLLS = DATADIR + C1DIR + "C1 Character Rolls/"
INVALID_VALS= ['Unknown', 'Unkown', 'N/A', '--', '', 'unknown', 'unkown', 'Misfire', 'Success','Fail', 'Unnknown', 'unnknown', 'uknown', 'Uknown', 'Unkknown', 'unkknown']
EPSDONE = 115
#Success for pepperbox c1e33
#Rolls.objects.all().delete()
for dirpath,dirnames,files in os.walk(C1ROLLS):
  
  files.sort()
  filesLeft = files[EPSDONE-2:]  #speed up inserting rollss

  for file_name in filesLeft:
    if not file_name.endswith("-CR.csv"):
      continue
    
    rollReader = csv.reader(open(C1ROLLS +  file_name))

    next(rollReader)  
    for row in rollReader:
      notes = []
      camp = Campaign.objects.get(num=int(file_name[1]))
      if row[0].endswith('p1') or row[0].endswith('p2'):
        ep = Episode.objects.get(num=int(row[0][:-3]),campaign=camp)
        notes.append(row[0][3:] + " ")
      else:
        ep = Episode.objects.get(num=int(row[0]),campaign=camp)

      timeStamp = int(float(row[1]))
      if row[2] == '' or row[2].capitalize() == 'Others' or row[2].capitalize() == 'Grenade':
        #gernade is from episode 19
        continue #skip when a bunch of people rolled at once, maybe add those back in through admin site
      adjustedname = row[2].capitalize()
      character = Character.objects.get(first_name=adjustedname)
      type = RollType.objects.get_or_create(name=row[3])

      totalVal = 0 #change it so that if value not there have null, help differentiate between actual 0 rolls and even negative values

      if row[4].strip().startswith('Natural'):
        totalVal = int(row[4][8:])
      elif row[4].startswith('Nat'):
        natless = row[4][3:]
        if natless.endswith('?'):
          totalVal = int(natless[:-1])
        elif '=' in natless:
          totalVal = int(natless[:-3]) #assuming for nat 20 if 1 probably get '' can't convert to int
        else:
          totalVal = int(natless)
      elif row[4].endswith('ish'):
        totalVal = int(row[4][:-3])
      elif row[4].startswith('>'):
        totalVal = int(row[4][1:]) + 1
      elif row[4].startswith('<'):
        totalVal = int(row[4][1:]) - 1
      elif row[4].endswith('+'):
        totalVal = int(row[4][:-1])
      elif row[4] not in INVALID_VALS: 
        totalVal = int(row[4])

      natVal = 0 #change it so that if value not there have null
      
      if row[5].startswith('>'):
        totalVal = int(row[5][1:]) + 1
      elif row[5].startswith('<'):
        totalVal = int(row[5][1:]) - 1
      elif row[5] not in INVALID_VALS:
        natVal = int(row[5])

      notes += row[9:] # read all columns left as notes, will read non-roll kills from ep c1 e1-e40 (only like 2-3 per episode)

      roll, created = Rolls.objects.update_or_create(ep=ep, time_stamp=timeStamp,roll_type=type[0],final_value=totalVal,
                                                    natural_value=natVal, notes=notes, character=character)
      if created == False:
        print("duplicate roll at time: " + str(timeStamp) + "in ep: " + row[0] + ", did not add to DB")