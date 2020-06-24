from characters.models import Character, ClassTaken, CharacterType
from classes.models import Class
from races.models import Race
import csv

charName = "characters.csv"

with open(charName, newline='') as myFile:
  rollReader = csv.reader(myFile)

  next(rollReader)
  for row in rollReader:
    first_name = row[0]
    last_name = row[1]
    race = Race.objects.get_or_create(name=row[3])
    classs = Class.objects.get_or_create(name=row[4])
    charType = CharacterType.objects.get_or_create(name="PC")
    
    character = Character.objects.update_or_create(first_name = first_name, last_name = last_name,race = race[0], char_type=charType[0])
    level = 10
    classCharRelation = ClassTaken.objects.update_or_create(character_id = character[0], class_id=classs[0],level=level)

    if character[1] == False:
      print("duplicate character " + first_name + ", did not add to DB")
    