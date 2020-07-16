from rolls.models import Rolls, RollType
from episodes.models import Episode
from campaigns.models import Campaign
from characters.models import Character, CharacterType
from races.models import Race

import csv
import re
import os
from collections import deque

def getChars(reader):
  import csv
  from characters.models import Character

  char_list = {}
  header = next(reader)

  for col,name in enumerate(header):
    if name == "Player" or name == "":
      continue

    name = name.strip()
    try:
      char = Character.objects.get(name=name)
      char_list[col] = char
    except:
      try:
        char = Character.objects.get(full_name__contains=name)
        char_list[col] = char
      except:
        print(name , " was not found")
  
  return char_list

#some duplicates in this list due to misspellings
#put nott/veth and veth into nott
# Vax and keyleth
def makeNPC(list):
  from characters.models import Character, CharacterType
  from races.models import Race
  
  NPC = CharacterType.objects.get(name="NPC")
  UnK = Race.objects.get(name='unknown')
  
  for person in damage_to:
    try: 
      ch = Character.objects.get(name = person)
    except:
      if person.strip() != "Nott/Veth" or person.strip() != "Veth" or person.strip() == "Vax and keyleth":
        ch = Character.objects.get_or_create(name=person, full_name = person,race=UnK, char_type=NPC)
        if ch[1]:
          print("CREATED: ",person)





C1DD = "/home/lightbulb/CritRoleDB/zdata/C1/C1 Damage Dealt/"
C2DD = "/home/lightbulb/CritRoleDB/zdata/C2/C2 Damage Dealt/"
EPSDONE = 100

currDD =  C1DD
currCamp = 1

camp = Campaign.objects.get(num=currCamp)

damageRolls = Rolls.objects.filter(roll_type = RollType.objects.get(name="Damage"),ep__campaign =camp )
personMatch = re.compile("to [a-zA-Z ']*")
damageType = re.compile("\d+ (?!to)[a-zA-Z/]+")#matches typoes gets some info when they do critical damages

matches = 0
encounter_matches = 0;
multi_match = 0
count = 0
damage_to = []
que_lengths = 0

for dirpath,dirnames,files in os.walk(currDD):
  files.sort()
  filesLeft = files[EPSDONE:]  #speed up inserting when restarting due to error

  for file_name in filesLeft:
    if not file_name.endswith("-DD.csv"):
      continue
    
    damageReader = csv.reader(open(currDD +  file_name))
    
    ep_num = int(file_name[4:7])
    ep = Episode.objects.get(num=ep_num, campaign=camp)
    encounters = ep.combat_encounters.all()

    #print(file_name) 
    char_list =  getChars(damageReader)
    next(damageReader)
    next(damageReader)

    char_rolls = {}
    ep_damage = damageRolls.filter(ep=ep).order_by('time_stamp')

    damage_que = deque()

    for roll in ep_damage:
      dealt_to = personMatch.findall(roll.damage)
      for person in dealt_to:
        clean = person[3:].strip().lower().capitalize()
        #ch = Character.objects.get(name=clean)
        damage_que.append((roll.final_value, clean,roll))
    
    que_lengths += len(damage_que)

    for char in char_list.items():
      char_rolls[char[0]] = ep_damage.filter(character=char[1]).order_by('time_stamp')

    
    # Do simple matching and see if char has damage roll (won't be good for 2 diff rolls with same value, probably map to first of 2)
    sheet_count = 0
    for row in damageReader:
      for col_num, damage in enumerate(row):
        if col_num not in char_rolls or damage == "":
          continue

        sheet_count+=1
        

    count += sheet_count
    print(ep.title, " sheet conut: ", str(sheet_count), " que len: ", str(len(damage_que)))


total_length = len(damageRolls)



non_PC = 0


print("Total: ", str(total_length))
print("Matches: ", str(matches))
print("Encoutner-Matches: ", str(encounter_matches))
print("Multi-Matches: ", str(multi_match))
print("Numbers in sheet: ", count)
print("Characters dealt to: ", str(len(damage_to)))
print("Non-PC characters: ", str(non_PC))
print("Qeued total: ", str(que_lengths))


    