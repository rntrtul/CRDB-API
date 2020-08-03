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
EPSDONE = 0

#Success for pepperbox c1e33
#Rolls.objects.all().delete()

curr = C1ROLLS
ukTotal = 0
ukNat = 0
for dirpath,dirnames,files in os.walk(curr):
  
  files.sort()
  filesLeft = files[EPSDONE:]  #speed up inserting rollss

  for file_name in filesLeft:
    if not file_name.endswith("-CR.csv"):
      continue
    
    rollReader = csv.reader(open(curr +  file_name))
    print(file_name)
    next(rollReader)  
    camp = Campaign.objects.get(num=int(file_name[1]))
    for row in rollReader:
      TIMEROW = 1
      NAMEROW = 2
      TYPEROW = 3
      TOTALROW = 4
      NATROW = 5
      DAMAGEROW = 7
      KILLROW = 8
      NOTEROW = 9
      notes = ''
      if camp.num == 1 :
        ep_num = row[0]
      else:
        ep_num = row[0][3:]

      #print(ep_num)
      if row[0].endswith('p1') or row[0].endswith('p2'):
        ep = Episode.objects.get(num=int(row[0][:-3]),campaign=camp)
        notes += (row[0][3:] + " ")
      else:
        ep = Episode.objects.get(num=int(ep_num),campaign=camp)
      
      if camp.num == 2 and ep.num >=20 and ep.num <=51:
        TIMEROW = 2
        NAMEROW = 3
        TYPEROW = 4
        TOTALROW = 5
        NATROW = 6
        DAMAGEROW = 8
        KILLROW = 9
        NOTEROW = 10

      timeStamp = int(float(row[TIMEROW]))

      if row[NAMEROW] == '' or row[NAMEROW].capitalize() == 'Others' or row[NAMEROW].capitalize() == 'Grenade' or row[NAMEROW] == 'NA':
        #gernade is from episode 19
        continue #skip when a bunch of people rolled at once, maybe add those back in through admin site
      adjustedname = row[NAMEROW].capitalize()
      if adjustedname == "Veth":
        adjustedname = "Nott"
      character = Character.objects.get(name=adjustedname)
      #type = RollType.objects.get(name=row[TYPEROW])

      totalVal = 0 #change it so that if value not there have null, help differentiate between actual 0 rolls and even negative values
      valid_total = True
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
      else:
        valid_total = False

      natVal = 0 #change it so that if value not there have null
      valid_nat = True
      if row[NATROW].startswith('>'):
        natVal = int(row[NATROW][1:]) + 1
      elif row[NATROW].startswith("Nat"):
        natless = row[NATROW][3:]
      elif row[NATROW].startswith('<'):
        totalVal = int(row[NATROW][1:]) - 1
      elif row[NATROW] not in INVALID_VALS:
        natVal = int(row[NATROW])
      else:
        valid_nat = False
        
      damage = ""
      damage +=  row[DAMAGEROW]

      kill_count = 0
      if row[KILLROW] != "" and row[KILLROW] != '?' and not row[KILLROW].startswith('0.'):
        kill_count = int(row[KILLROW])
      if row[KILLROW].startswith('0.'):
        kill_count = 1 

      notes += row[NOTEROW]
      
      #print(row)
      #print(str(ep.num), str(timeStamp), character.name, str(totalVal),  str(natVal), notes)
      try:
        roll = Rolls.objects.get(ep=ep,time_stamp=timeStamp,character = character,notes=notes,natural_value=natVal, final_value=totalVal, damage=damage)
      except: 
        if not valid_nat:
          natVal = None
        if not valid_total:
          totalVal = None
        roll = Rolls.objects.get(ep=ep,time_stamp=timeStamp,character = character,notes=notes,natural_value=natVal, final_value=totalVal, damage=damage)

      if not valid_nat:
        ukNat+=1   
        roll.natural_value = None 
        roll.save()
      if not valid_total:
        ukTotal+=1
        roll.final_value = None
        roll.save()
      #if kill_count != 0:
      #  roll.kill_count = kill_count
      #  roll.save()
      #  print(kill_count)
      #roll, created = Rolls.objects.update_or_create(ep=ep, time_stamp=timeStamp,final_value=totalVal,natural_value=natVal, notes=notes, character=character,damage =damage)
      #if created :
      #  print("Created roll at time: " + str(timeStamp) + "in ep: " + str(ep.num))

print("Unknown nats:", str(ukNat))
print("Unknown totals:", str(ukTotal))