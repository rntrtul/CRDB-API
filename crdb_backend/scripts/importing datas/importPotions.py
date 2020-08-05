from characters.models import Character,CharacterType
from episodes.models import Episode
from races.models import Race
from items.models import Potion, PotionUsage
import csv

DIR = "/home/lightbulb/CritRoleDB/zdata/C1/TD Potions.csv"

myFile = open(DIR, newline='')
reader = csv.reader(myFile)
npc = CharacterType.objects.get_or_create(name="NPC")

next(reader)
for row in reader:
  ep = Episode.objects.get(num=row[0])
  if row[1].startswith('p1'):
    time = row[1][4:]
  else:
    time = row[1]
  time = int(float(time))
  by = Character.objects.get(name=row[2])
  try:
    to = Character.objects.get(name=row[3])
  except:
    if row[3] == "Clarota":
      races = Race.objects.get_or_create(name="Illithid")
      race= races[0]
    else:
      race = Race.objects.get(name="Human")
    to,created = Character.objects.get_or_create(full_name=row[3],name=row[3],char_type = npc[0],race=race)

  potion = Potion.objects.get_or_create(name=row[4])
  note = row[5]
  pu = PotionUsage.objects.get_or_create(by=by,to=to,episode=ep,potion=potion[0],timestamp=time,notes=note)
  if pu[1]:
    print("potion usage was created in episode" + str(ep.num))