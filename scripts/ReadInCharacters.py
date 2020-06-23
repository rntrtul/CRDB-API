from characters.models import Character, Class, ClassTaken, CharacterType
from races.models import Race
import csv

rollsName = "characters.csv"

with open(rollsName, newline='') as myFile:
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
      print("duplicate character, did not add to DB")
    
      

#delete these after testing views and stuff
#as reading in rolls will create a new rolltype, episode, character name if not found 

