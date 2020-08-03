def initDamageType():
  from items.models import DamageType
  damage_names = {
    'ltng': "Lightning",
    'pierce': "Piercing",
    'Fire': "Fire",
    'Piercing': "Piercing",
    'Cold': "Cold",
    'Lightning': "Lightning",
    'slash': "Slashing",
    'fire': "Fire",
    'bludge': "Bludgeoning",
    'necro': "Necrotic",
    'slashing': "Slashing",
    'bludgeoning': "Bludgeoning",
    'bludgeon': "Bludgeoning",
    'lightning': "Lightning",
    'radiant': "Radiant",
    'cold': "Cold",
    'Slashing': "Slashing",
    'force': "Force",
    'bludg':"Bludgeoning",
    'slashin':"Slashing",
    'Slashing': "Slashing",
    'psychic': "Psychic",
  }
  for dmg in damage_names:
    dmgType, created = DamageType.objects.get_or_create(name=damage_names[dmg])
    if created:
      print( dmgType.name + " was created")

def initDice():
  from rolls.models import Die

  sides = [4,6,8,10,12,20]
  for side in sides:
    die, created = Die.objects.get_or_create(sides=side)
    if created:
      print(str(die.sides) + "-sided die was created")

#return name of weapon and nameless input string
def getName(str):
  import re
  nameMatch = re.compile(r'^[a-zA-Z-]+(\ ([a-zA-Z-]*)?)*')
  if str == "":
    return "False", str
  namePos = nameMatch.search(str)
  if not namePos:
    return "False", str
  
  name = str[namePos.start():namePos.end()].strip()
  left = str[namePos.end():].strip()

  return name, left

def getModifier(str):
  import re
  #modMatch = re.compile(r'(\+[^d]?\d+[^d])|^\d+')
  modMatch = re.compile(r'(\+\ ?\d+[^d])|^\+\d+')

  if len(str) == 0:
    return "False", str

  modPos = modMatch.search(str)
  if str[0] == '0':
    mod = "0"
    left = str[2:]
  elif str[1] == "?":
    mod = "+5?"
    left = str[3:].strip()
  elif not modPos:
    return "False", str
  else: 
    mod = str[modPos.start():modPos.end()].strip()
    left = str[modPos.end():].strip()

  mod = mod.replace(' ', '')
  return mod, left

def getDie(str):
  import re
  dieMatch = re.compile(r'\d?d\d*')
  if str == "":
    return "False", str
    
  diePos = dieMatch.search(str)
  if diePos:
    die = str[diePos.start():diePos.end()].strip()
    left = str[diePos.end():].strip()
    return die, left
  else:
    return "False", str

def getDamageType(str):
  damage_names = {
    'ltng': "Lightning",
    'pierce': "Piercing",
    'Fire': "Fire",
    'Piercing': "Piercing",
    'Cold': "Cold",
    'Lightning': "Lightning",
    'slash': "Slashing",
    'fire': "Fire",
    'bludge': "Bludgeoning",
    'necro': "Necrotic",
    'slashing': "Slashing",
    'bludgeoning': "Bludgeoning",
    'bludgeon': "Bludgeoning",
    'lightning': "Lightning",
    'radiant': "Radiant",
    'cold': "Cold",
    'Slashing': "Slashing",
    'force': "Force",
    'bludg':"Bludgeoning",
    'slashin':"Slashing",
    'Slashing': "Slashing",
    'psychic': "Psychic",
  }
  damage_str = ['ltng','pierce', 'Fire','Piercing','Cold','Lightning','slash','fire','bludge','necro','slashing','bludgeoning','bludgeon',
                'lightning','radiant','cold','Slashing','force','bludg','slashin', 'Slashing','psychic']
  if len(str) == 0:
    return "False", str
  idx = str.find(' ')

  if str[-1].isdigit():
    idx = str.find('+')

  if idx ==  -1:
    checkStr = str.strip()
    left = ""
  else:
    checkStr = str[:idx].strip()
    left = str[idx:]

  #print(checkStr)
  if len(checkStr) > 0 and checkStr[-1].isdigit():
    idx = checkStr.find('+')
    checkStr = checkStr[:idx]
    left = str[idx:]
    
  #print("CHECKING: " + checkStr)

  if checkStr in damage_str:
    return damage_names[checkStr], left
  else:
    return "False", str

def getSides(str):
  if str[0] == "d":
    return 1, int(str[1:])
  else:
    return int(str[0]), int(str[2:])

from characters.models import StatSheet
from items.models import DamageType, Weapon, WeaponDamage, WeaponeOwned
from rolls.models import Die

sheet_list = StatSheet.objects.all()
for sheet in sheet_list:
  weap = sheet.weapons
  weaps = weap.split('\n')

  for weapon in weaps:
    cleanedWpn = weapon.strip()
    if cleanedWpn != "0 0 0":
      #print(cleanedWpn)

      name, left = getName(cleanedWpn)
      
      if name == "False":
        continue
      wpn,created = Weapon.objects.get_or_create(name=name)
      if created:
        print(wpn.name + " was created")


      atkbonus, left = getModifier(left)
      if atkbonus != "False":
        cleaner = atkbonus.replace("?", "")
        #print(cleaner)
        if cleaner == "+":
          cleaner = 0
        wpn.attack_bonus = int(cleaner)
        wpn.save()
        weaponOwner,created = WeaponeOwned.objects.get_or_create(weapon=wpn, sheet=sheet)
        if created:
          print(wpn.name + " is owned by " + sheet.character.name)
      
      die1, left = getDie(left)
      type1, left = getDamageType(left)
      die1Mod, left = getModifier(left)
      if type1 == "False":
        type1, left = getDamageType(left)
      die2, left = getDie(left)
      die2Mod, left = getModifier(left)
      type2, left = getDamageType(left)
      if die2Mod == "False":
        die2Mod ,left = getModifier(left)

      if die1 != "False":
        if die1 == "d":
          num = 1
          sides = 6
        else: 
          num, sides = getSides(die1)
        die = Die.objects.get(sides=sides)
      
      if die1Mod != "False" and die1Mod.endswith('?'):
        die1Mod = die1Mod.replace("?", "")
        die1Mod = int(die1Mod)

      if type1 != "False":
        dt1 = DamageType.objects.get(name=type1)

      if die1 != "False" and die1Mod != "False" and type1 != "False":
        wpnDmg1, created = WeaponDamage.objects.get_or_create(weapon=wpn,die=die, modifier = die1Mod,damage_type = dt1, die_num=num)
        if created:
          print(wpn.name + " damage 1 created")
      elif die1 != "False" and die1Mod != "False":
        wpnDmg1, created = WeaponDamage.objects.get_or_create(weapon=wpn,die=die, modifier = die1Mod,die_num=num)
        if created:
          print(wpn.name + " damage 1 created(no Type)")
      elif die1 != "False" and type1 != "False":
        wpnDmg1, created = WeaponDamage.objects.get_or_create(weapon=wpn,die=die, modifier = 0,damage_type = dt1, die_num=num)
        if created:
          print(wpn.name + " damage 1 created (no modifier)")

      if die2 != "False":
        if die2 == "d":
          num = 1
          sides = 6
        else: 
          num, sides = getSides(die2)
        die = Die.objects.get(sides=sides)
      
      if die2Mod != "False" and die2Mod.endswith('?'):
        die2Mod = die2Mod.replace("?", "")
        die2Mod = int(die2Mod)

      if type2 != "False":
        dt2 = DamageType.objects.get(name=type2)
      
      if die2 != "False" and die2Mod != "False" and type2 != "False":
        wpnDmg2,created = WeaponDamage.objects.get_or_create(weapon=wpn,die=die, modifier = die2Mod,damage_type = dt2,die_num = num)
        if created:
          print(wpn.name + " damage 2 created")
      elif die2 != "False" and die2Mod != "False":
        wpnDmg2,created = WeaponDamage.objects.get_or_create(weapon=wpn,die=die, modifier = die2Mod,die_num = num)
        if created:
          print(wpn.name + " damage 2 created (no type)")
      elif die2 != "False" and type2 != "False":
        wpnDmg2,created = WeaponDamage.objects.get_or_create(weapon=wpn,die=die, modifier = 0,damage_type = dt2,die_num = num)
        if created:
          print(wpn.name + " damage 2 created (no modifier)")

