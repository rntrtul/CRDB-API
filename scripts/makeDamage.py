from rolls.models import Rolls, RollType
from episodes.models import Episode
from campaigns.models import Campaign
from characters.models import Character, CharacterType
from races.models import Race

import csv
import re
import os
from collections import deque

def getCharDamage(reader):
  import csv
  from characters.models import Character
  from collections import deque
  char_list = {}
  char_dmg = {}

  header = next(reader)

  for col, name in enumerate(header):
    if name == "Player" or name == "":
      continue

    name = name.strip()

    try:
      char = Character.objects.get(name=name)
      char_list[col] = char
      char_dmg[char.name] = deque()
    except:
      try:
        char = Character.objects.get(full_name__contains=name)
        char_list[col] = char
        char_dmg[char.name] = deque()
      except:
        print(name , "was not found")
 
  next(reader)
  next(reader)
  sheet_count = 0
  for row in reader:
    for col_num, damage in enumerate(row):
      if col_num not in char_list or damage.strip() == "":
        continue
      sheet_count += 1
      char_dmg[char_list[col_num].name].append(int(damage.strip()))

  return char_dmg, sheet_count

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
EPSDONE = 0

currDD =  C1DD
currCamp = 1

camp = Campaign.objects.get(num=currCamp)

damageRolls = Rolls.objects.filter(roll_type = RollType.objects.get(name="Damage"),ep__campaign =camp )

damage_to = []
matches = 0
sheet_count = 0
errors = 0
misses = 0
for dirpath,dirnames,files in os.walk(currDD):
  files.sort()
  filesLeft = files[EPSDONE:]  #speed up inserting when restarting due to error

  for file_name in filesLeft:
    if not file_name.endswith("-DD.csv"):
      continue
    
    damageReader = csv.reader(open(currDD +  file_name))
    print(file_name)
    ep_num = int(file_name[4:7])
    ep = Episode.objects.get(num=ep_num, campaign=camp)

    pair = getCharDamage(damageReader)
    ep_damage = damageRolls.filter(ep=ep).order_by('time_stamp')
    
    char_damage_roll = {}

    char_damage_dealt = pair[0]
    sheet_count += pair[1]
    # add (roll, person_to, damage type) here for all rolls
    # then in other looop only have to deal with adding some damage to see if it matches and percy bleeding
    for roll in ep_damage:
      try: 
        char_damage_roll[roll.character.name].append(roll)
      except:
        char_damage_roll[roll.character.name] = deque()
        char_damage_roll[roll.character.name].append(roll)

    #if ep.num == 113:
    #  for roll in char_damage_roll.items():
    #    print(roll[0], ":", roll[1])
        

    de = deque(ep_damage.all())
    
    #don't iterate over all rolls again do it for char queue. 

    for char in char_damage_roll:
      prev = 0
      if char not in char_damage_dealt:
        continue

      for roll in char_damage_roll[char]:
        if not roll.final_value:
          continue
        try:
          if char_damage_dealt[char]:
            if roll.final_value == char_damage_dealt[char][0]:
              char_damage_dealt[char].pop()
              prev = roll.final_value
              matches +=1
            elif prev == char_damage_dealt[char][0]:
              #while char_damage_dealt[char] and prev == char_damage_dealt[char][0]:
              #  char_damage_dealt[char].pop()
                
                matches+=1
            else:
              misses += 1
            #print( roll.final_value, char_damage_dealt[char][-1])
            #print('ROLL:', roll.character.name, roll.time_stamp, roll.final_value, roll.notes, roll.damage)
          else:
            print("DEQUE EMPTY:",char_damage_dealt[char])
            print('ROLL:', roll.character.name, roll.time_stamp, roll.final_value, roll.notes, roll.damage)
        except Exception as e:
          errors += 1
          print('ERROR:', e)
          print('LENS(dealt, roll):', len(char_damage_dealt), len(char_damage_roll))
          print('ROLL:', roll.character.name, roll.time_stamp, roll.final_value, roll.notes, roll.damage)

print('Matches:', matches, 'Target:', sheet_count)
print('Missed:', misses, "Errors:", errors)
    