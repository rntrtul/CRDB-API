import PyPDF2
import os
import math

boxList = {
  11: "Strength Save",
  18: "Dexterity Save",
  19: "Constitution Save",
  20: "Intelligence Save",
  21: "Wisdom Save",
  22: "Charisma Save",
  23: "Acrobatics",
  24: "Animal Handling",
  25: "Arcana",
  26: "Athletics",
  27: "Deception",
  28: "History",
  29: "Insight",
  30: "Intimidation",
  31: "Investigation",
  32: "Medicine",
  33: "Nature",
  34: "Perception",
  35: "Performance",
  36: "Persuasion",
  37: "Religion",
  38: "Sleight of Hand",
  39: "Stealth",
  40: "Survival"
}

wantedFields = ["ClassLevel","PlayerName","CharacterName","Race","Alignment","Inspiration","ProfBonus","AC","Initiative",
              "Speed","HPMax","HDTotal","STR","DEX","INT","CON","WIS","CHA","ST Strength","ST Dexterity","ST Constitution",
              "ST Intelligence","ST Wisdom","ST Charisma","Acrobatics","Animal","Athletics","Deception","History","Insight",
              "Intimidation","Investigation","Arcana","Perception","Nature","Performance","Medicine","Religion","Stealth",
              "Persuasion","SleightofHand","Survival","AttacksSpellcasting","Passive","ProficienciesLang","Features and Traits",
              "Equipment","Wpn Name","Wpn1 AtkBonus","Wpn1 Damage","Wpn Name 2","Wpn2 AtkBonus","Wpn2 Damage","Wpn Name 3",
              "Wpn3 AtkBonus","Wpn3 Damage","Spellcasting Class 2","SpellSaveDC 2","SpellAtkBonus 2"]

wantCleaned = ["ProficienciesLang","Features and Traits","Equipment","Wpn Name","Wpn1 AtkBonus","Wpn1 Damage","Wpn Name 2",
                "Wpn2 AtkBonus","Wpn2 Damage","Wpn Name 3","Wpn3 AtkBonus","Wpn3 Damage","AttacksSpellcasting"]

def formatField(val):
  rless = val.replace(r'\r', ',')
  rless = rless.replace('\n', ',')
  rless = rless.replace('\r\n', ',')
  if rless[0] == 'b':
    rless = rless[1:]
  if rless.startswith('\"'):
    rless = rless[1:]
  if rless.endswith("\""):
    rless = rless[:-1]
  rless = rless.strip()
  return rless


def storeCharSheet(fileName,dirpath):
  path = os.path.join(dirpath,fileName)
  curPdf = open(path,'rb')
  pdfReader = PyPDF2.PdfFileReader(curPdf)

  fields = pdfReader.getFields()
  newName = fileName[:-4] + ".txt"
  writer = open("sheets/" + newName, 'w')
  count = 0
  lvl = "cantrip"

  for field in fields.items():
    toWrite = ""
    cleanField = field[0].strip()
    failed = False
    if cleanField in wantedFields:
      try:
        value = str(field[1]['/V'])
      except:
        value = "None"
      if value == "/Yes":
        value = "0"
      if cleanField in wantCleaned:
        formatted = formatField(value)
        toWrite = cleanField + ": \"" + formatted + "\"\n"  
      else:
        toWrite = cleanField + ": \"" + value.strip() + "\"\n"  
    elif cleanField.startswith("Check Box"):
      boxNum = int(field[0][10:])
      try:
        isProf = field[1]['/V'][1:]
        toWrite = "Proffcient in: \"" + boxList[boxNum] + "\"\n"
      except:
        failed = True
    elif cleanField.startswith("Spells"):
      count+=1
      if count < 8:
        lvl = "cantrip"
      if count < 60:
        lvl = str(math.ceil((count-7)/13))
      elif count < 87:
        lvl = str(math.ceil((count - 59) / 9) + 4)
      else:
        lvl = str(math.ceil((count - 86) / 7) + 7)
      #1014-1024 cantrip 
      #13 rows lvl 1,2,3,4. 9 rows lvl 5,6,7 . 7 rows lvl 8,9
      try:
        spell = field[1]['/V']
        if spell != '' and spell != "???":
          toWrite = "Spell lvl " + lvl + ": \"" + spell + "\"\n"
      except:
        failed = True
    elif cleanField.startswith("SlotsTotal"):
      try:
        slots = field[1]['/V']
        if lvl == "cantrip":
          toWrite = "Slots at lvl 1: " + slots + "\n"
        elif slots != "":
          toWrite = "Slots at lvl " + str(int(lvl) + 1) + ": " + slots + '\n'
      except:
        failed = True
    elif cleanField.startswith("SpellSaveDC"):
      try:
        spellDC = field[1]['/V']
        toWrite = "SpellSaveDC: " + spellDC + '\n'
      except:
        failed = True
    
    if not failed:
      writer.write(toWrite)
  curPdf.close()


C1SHEETS = "/home/lightbulb/Desktop/CRDB Data May 25 2020/C1/C1 char sheets/"

#storeCharSheet("Keyleth_L14.pdf", C1SHEETS)

for dirpath,dirnames,files in os.walk(C1SHEETS):
  files.sort()
  for file in files:
    if file.endswith(".pdf") :
      storeCharSheet(file,dirpath)