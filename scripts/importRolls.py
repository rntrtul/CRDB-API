from rolls.models import Rolls, RollType
from episodes.models import Episode, Campaign
from characters.models import Character
import csv
import os


DATADIR = "zdata/"
C1DIR = "C1/"
C1ROLLS = DATADIR + C1DIR + "C1 Character Rolls/"
C2ROLLS = "/home/lightbulb/CritRoleDB/zdata/C2/C2 Character Rolls/"
INVALID_VALS= ['Unknown', 'Unkown', 'N/A', 'NA', '--', '', '#REF!','unknown', 'unkown', 'Misfire', 'Success','Fail', 'Unnknown', 'unnknown', 'uknown', 'Uknown', 'Unkknown', 'unkknown']
EPSDONE = 95

#Success for pepperbox c1e33
#Rolls.objects.all().delete()
for dirpath,dirnames,files in os.walk(C2ROLLS):
  
  files.sort()
  filesLeft = files[EPSDONE:]  #speed up inserting rollss

  for file_name in filesLeft:
    if not file_name.endswith("-CR.csv"):
      continue
    
    rollReader = csv.reader(open(C2ROLLS +  file_name))

    next(rollReader)  
    camp = Campaign.objects.get(num=int(file_name[1]))
    for row in rollReader:
      TIMEROW = 1
      NAMEROW = 2
      TYPEROW = 3
      TOTALROW = 4
      NATROW = 5
      DAMAGEROW = 7
      NOTEROW = 9
      notes = ''
      ep_num = row[0][3:]
      #print(ep_num)
      if row[0].endswith('p1') or row[0].endswith('p2'):
        ep = Episode.objects.get(num=int(row[0][:-3]),campaign=camp)
        notes += (row[0][3:] + " ")
      else:
        ep = Episode.objects.get(num=int(ep_num),campaign=camp)
      
      if ep.num >=20 and ep.num <=51:
        TIMEROW = 2
        NAMEROW = 3
        TYPEROW = 4
        TOTALROW = 5
        NATROW = 6
        DAMAGEROW = 8
        NOTEROW = 10

      timeStamp = int(float(row[TIMEROW]))

      if row[NAMEROW] == '' or row[NAMEROW].capitalize() == 'Others' or row[NAMEROW].capitalize() == 'Grenade' or row[NAMEROW] == 'NA':
        #gernade is from episode 19
        continue #skip when a bunch of people rolled at once, maybe add those back in through admin site
      adjustedname = row[NAMEROW].capitalize()
      if adjustedname == "Veth":
        adjustedname = "Nott"
      character = Character.objects.get(name=adjustedname)
      type = RollType.objects.get_or_create(name=row[TYPEROW])

      totalVal = 0 #change it so that if value not there have null, help differentiate between actual 0 rolls and even negative values

      if row[TOTALROW].strip().startswith('Natural'):
        totalVal = int(row[TOTALROW][8:])
      elif row[TOTALROW].startswith('Nat'):
        natless = row[TOTALROW][3:]
        if natless.endswith('?'):
          totalVal = int(natless[:-1])
        elif '=' in natless:
          totalVal = int(natless[:-3]) #assuming for nat 20 if 1 probably get '' can't convert to int
        else:
          totalVal = int(natless)
      elif row[TOTALROW].endswith('ish'):
        totalVal = int(row[TOTALROW][:-3])
      elif row[TOTALROW].startswith('>'):
        totalVal = int(row[TOTALROW][1:]) + 1
      elif row[4].startswith('<'):
        totalVal = int(row[TOTALROW][1:]) - 1
      elif row[TOTALROW].endswith('+'):
        totalVal = int(row[TOTALROW][:-1])
      elif row[TOTALROW] not in INVALID_VALS: 
        totalVal = int(row[TOTALROW])

      natVal = 0 #change it so that if value not there have null
      
      if row[NATROW].startswith('>'):
        totalVal = int(row[NATROW][1:]) + 1
      elif row[NATROW].startswith("Nat"):
        natless = row[NATROW][3:]
      elif row[NATROW].startswith('<'):
        totalVal = int(row[NATROW][1:]) - 1
      elif row[NATROW] not in INVALID_VALS:
        natVal = int(row[NATROW])
      damage = ""
      damage +=  row[DAMAGEROW]
      notes += row[NOTEROW]

      roll, created = Rolls.objects.update_or_create(ep=ep, time_stamp=timeStamp,roll_type=type[0],final_value=totalVal,
                                                    natural_value=natVal, notes=notes, character=character,damage =damage)
      if created == False:
        print("duplicate roll at time: " + str(timeStamp) + "in ep: " + str(ep.num)+ ", did not add to DB")