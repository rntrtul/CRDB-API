from rolls.models import Rolls, RollType
from characters.models import Character
from collections import Set
from damages.models import DamageType, Damage
import re

def get_misses(all, matched):
  from collections import Set
  diff = set(all) - set(matched)
  
  ep_misses = {}
  for roll in diff:
    if roll.ep.title in ep_misses:
      ep_misses[roll.ep.title] += 1
    else:
      ep_misses[roll.ep.title] = 1

  misses = 0
  for ep in ep_misses:
    misses += ep_misses[ep]
    print(ep, ep_misses[ep])
  
  print("Total misses", misses)
  return misses


# returns list of tuples for all matched damage types and count of regex matches (not same as len of list)
# tuple: (dmg, matched type, start in og string, end in og string)
def get_damages(damage_str):
  import re
  dmgType = {
    'acid': "Acid",
    'bludgeoning': "Bludgeoning",
    'bludge': "Bludgeoning",
    'bludgeon': "Bludgeoning",
    'bludg':"Bludgeoning",
    'fall': "Bludgeoning",
    'crushing': "Bludgeoning",
    'impact': "Bludgeoning",
    'cold': "Cold",
    'ice': "Cold",
    'fire': "Fire",
    'bb': "Fire",
    'force': "Force",
    'lightning': "Lightning",
    'ltng': "Lightning",
    'lighting': "Lightning",
    'necrotic': "Necrotic",
    'necro': "Necrotic",
    'hex': "Necrotic",
    'piercing': "Piercing",
    'pierce': "Piercing",
    'bramble': "Piercing",
    'poison': "Poison",
    'psychic': "Psychic",
    'radiant': "Radiant",
    'radian': "Radiant",
    'holy': "Radiant",
    'slashing': "Slashing",
    'slashing': "Slashing",
    'slash': "Slashing",
    'slashin':"Slashing",
    'thunder': "Thunder",
    'sa': "Sneak Attack",
    'sneak': "Sneak Attack",
    'hm': "Hunter's Mark", 
    'gwm': "Great Weapons Master",
    'ss': "Sharp Shooter",
    'brutal': "Brutal Critical",
    'enlarge': "Enlarge", #is 1d4 extra weapon damage
    'dragon': "Dragon", #is probalby just the weapon damage
    'slashing/necrotic': 'Slashing + Necrotic',
    'piercing/necrotic': 'Piercing + Necrotic',
    'slashing/radiant': "Slashing + Radiant",
    'lightning/radiant': "Lightning + Radiant",
    'piercing/lightning': "Piercing + Lightning",
    'lightning/piercing': "Piercing + Lightning",
    'slashing/psychic': "Slashing + Psychic",
    'sa/hm': "Sneak Attack + Hunter's Mark",
    'hm/sa': "Sneak Attack + Hunter's Mark",
    "slashing/psychic/radiant": "Slashing + Psychic + Radiant",
    "slashing/radiant/dragon": "Slashing + Radiant + Dragon ",
    "piercing/fire" : "Piercing + Fire",
    "piercing/psychic" : "Piercing + Psychic",
  }
  damage_value = -1000 #for helping with debug
  damageType = re.compile(r"\d+(?! \([\/\w]+ )(?: [x\d\/\(\)]+)? (?!to)[\w\/]+|\d\d? (?:\([\dx+\/]+\) )?to|\d+ ?\+")
  type_matches = damageType.findall(damage_str)
  
  damages = []
  for match in type_matches:
    splited = match.split(' ')
    start = damage_str.find(match)
    end = start + len(match)
    try:
      damage_value = int(splited[0])
    except:
      damage_value = -9999 #should be immediately obvious if this exists in db

    damage_type = "NOTHING FOUND" #help to see if everything is working

    if len(splited) > 1 and splited[1].lower() in dmgType:
      damage_type = dmgType[splited[1].lower()]
      #damages.append((damage_value ,dmgType[splited[1].lower()],start, end))
    elif len(splited) > 2 and splited[2].lower() in dmgType:
      damage_type = dmgType[splited[2].lower()]
      #damages.append((damage_value ,dmgType[splited[2].lower()],start, end))
    elif len(splited) == 2 and splited[1].lower() == "to":
      damage_type = "Currently Unknown"
      #damages.append((damage_value ,"Currently Unknown",start, end))
    elif len(splited) == 3 and splited[1].startswith('('):
      damage_type = "Currently Unknown"
      #damages.append((damage_value ,"Currently Unknown",start, end))
    elif len(splited) == 1 and splited[0].endswith('+'):
      damage_type = "Currently Unknown"
      damage_value = int(splited[0][:-1])
      #damages.append((int(splited[0][:-1]) ,"Currently Unknown",start, end))
    elif len(splited) == 2 and splited[1] == '+':
      damage_type = "Currently Unknown"
      #damages.append((damage_value ,"Currently Unknown",start, end))

    if damage_value == -1000 or damage_value == -9999 or damage_type == "NOTHING FOUND":
      #print('ERROR no type found for:',match, 'in:', damage_str)
      poo =True
    else:
      damages.append((damage_value ,damage_type,start, end))

  return damages, len(type_matches)

# returns list of tuples with characters found in damage string and a count of how many
# tuple: (character name matched, count, position in original string)
def get_characters(dmg): 
  from characters.models import Character
  import re
  import inflect
  charCount = re.compile(r"(?:to|,|and) (?:\d{1,2}(?![a-zA-Z\(\d/\) ]* to))?(?:(?! and)[a-zA-Z' ])+(?:\(\d\))?")
  matches = charCount.findall(dmg)
  inflect = inflect.engine()

  characters = []
  count = 0
  for match in matches:
    split = match.split(' ')
    name = match.strip()
    if name.startswith('to'):
      name = name[2:].strip()
    if name.startswith(','):
      name = name[1:].strip()
    if name.startswith('and'):
      name = name[3:].strip()
  
    name_split = name.split(' ')

    if len(name_split) > 1 and name_split[0].isdigit():
      name = " ".join(name_split[1:]).strip()
    if name.endswith(')'):
      name_split = name.split(' ')
      name = " ".join(name_split[:-1])

    if name.isdigit():
      continue
      
    #print(match, 'with name', name)
    pos = dmg.find(match)
    count += 1
    if len(split) > 1 and split[1].isdigit():
      try:
        ch = Character.objects.get(name=name)
        characters.append((name, int(split[1]),pos))
      except:
        try:
          if inflect.singular_noun(name) != False:
            new_name = inflect.singular_noun(name).capitalize()
            ch = Character.objects.get(name=new_name)
            characters.append((new_name, int(split[1]),pos))
          else: 
            junk = 0
            #print("ERROR could not find char with name", name)
        except :
          junk = 0
          #print("ERROR couldn't find char with name", name)

      count += int(split[1]) - 1
    elif len(split) > 2 and split[2].startswith('('):
      char_count = int(split[2][1:-1])
      try:
        ch = Character.objects.get(name=name)
        characters.append((name, char_count,pos))
      except:
        try:
          if inflect.singular_noun(name) != False:
            new_name = inflect.singular_noun(name).capitalize()
            ch = Character.objects.get(name=new_name)
            characters.append((new_name, char_count,pos))
          else: 
            junk = 0
            #print("ERROR could not find char with name", name)
        except :
          junk = 0
          #print("ERROR couldn't find char with name", name)

      count += char_count - 1
    else:
      try:
        ch = Character.objects.get(name=name.capitalize())
        characters.append((name.capitalize(),1,pos))
      except :
        try:
          ch = Character.objects.get(name=name)
          characters.append((name,1,pos))
        except:
          print("ERROR didn't find char with name", name)

  return characters, count


all_rolls = Rolls.objects.filter(roll_type = RollType.objects.get(name="Damage")).order_by('ep__num','time_stamp').all()

count = 0
type_count = 0
type_groups = 0
damage_idd = 0
damage_dealt = []

for roll in all_rolls:
  dmg = roll.damage
  
  damages, type_matches = get_damages(dmg)
  characters, char_matches = get_characters(dmg)

  damage_group = []
  if len(damages) > 1:
    curr_group = []
    for idx, dmg_type in enumerate(damages):
      if len(damages) -1 == idx:
        if len(curr_group) != 0:
          curr_group.append(dmg_type)
          damage_group.append(curr_group)
        else:
          damage_group.append([dmg_type])
        break 
      
      one_group = True
      for char in characters:
        if dmg_type[2] <= char[2] and damages[idx+1][2] >= char[2]:
          one_group = False
      
      if one_group:
        curr_group.append(dmg_type)
      elif len(curr_group) != 0:
        curr_group.append(dmg_type)
        damage_group.append(curr_group)
        curr_group = []
      else:
        damage_group.append([dmg_type])
  elif damages:
    damage_group.append([damages[0]])
  
  for char in characters:
    for dmg in reversed(damage_group):
      if dmg[0][2] <= char[2]:
        group = dmg
        break

    for dummy in range(0,char[1]):
      for type in group:
        damage_dealt.append((roll,char[0],type[0],type[1])) 
  

  damage_idd += len(damages)
  count += char_matches
  type_count += type_matches
  type_groups += len(damage_group)

#iterate through damage_dealt and save into db
dmg_total = 0
created = 0
for dd in damage_dealt:
  try:
    dmg_total += dd[2]
    dt = DamageType.objects.get(name=dd[3])
    ch = Character.objects.get(name=dd[1])
    r = dd[0]
    dealt = Damage.objects.get_or_create(roll=r, by=r.character, to=ch, damage_type=dt, points=dmg_total)
    if dealt[1]:
      created+= 1
      print("CREATED:", dd[0].character.name, 'dealt', dd[2], dd[3] , 'to', dd[1], 'in', dd[0].ep.num)
  except:
    print(dd)


print("TOTAL DAMAGE DEALT:", dmg_total)
print("Regex char matches:", count)
print("Regex type matches:", type_count)
print("Damage types ID'd:", damage_idd)
print("Damage Groups:", type_groups)
print("Damage roll count:", len(all_rolls))
print("Target damage instances: 4368")
print("Our damage instances:", len(damage_dealt))
print("Created:", created)
