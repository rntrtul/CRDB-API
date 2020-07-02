from characters.models import Character, ClassTaken, CharacterType
from classes.models import Class
from players.models import Player
from races.models import Race
import csv

charName = "characters.csv"

#Character.objects.all().delete()
#ClassTaken.objects.all().delete()
with open(charName, newline='') as myFile:
  rollReader = csv.reader(myFile)
  charType = CharacterType.objects.get(name="PC")
  next(rollReader)
  for row in rollReader:
    name = row[0]
    index = name.find((' '))
    first_name = name[:name.find(' ')]
    last_name = name[name.find(' ') + 1: ]
    if index == -1:
      first_name = name
      last_name = ""
    if name.startswith("Percival"):
      first_name = "Percy"
      last_name = "de Rolo"
    elif name.startswith("Nott"):
      last_name = ""
    race = Race.objects.get(name=row[3])
    player = Player.objects.get(full_name=row[2]) 
    used_name = row[1]
    character = Character.objects.update_or_create(first_name = first_name, last_name = last_name, char_type = charType, race=race,
                                                    defaults={'full_name': name, 'name':used_name, 'player':player})

    
    #if player[1]:
    #  print(player[0].full_name + " was created")

    if character[1] == False:
      print("duplicate character " + first_name + ", did not add to DB")
    