import PyPDF2

grogPdf = open('Grog_L20.pdf', 'rb')
keyPdf = open('Keyleth_L20.pdf','rb')
curPdf = grogPdf

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

pdfReader = PyPDF2.PdfFileReader(curPdf)
fields = pdfReader.getFields()

for field in fields.items():
  if field[0].strip() in wantedFields:
      try:
        value = str(field[1]['/V'])
      except:
        value = "None"
      print(field[0] + ": " + value)
  if field[0].startswith("Check Box"):
      boxNum = int(field[0][10:])
      try:
        print("Proffcient in " + boxList[boxNum] + ": " + str(field[1]['/V'][1:]))
      except:
        failed = True

curPdf.close()