from characters.models import Character, CharacterType
from campaigns.models import Campaign
from episodes.models import Episode
from races.models import Race
from items.models import Potion, PotionUsage
import csv


def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


DIR = "./Potions Consumed - Wildemount - Wildemount Potions.csv"

myFile = open(DIR, newline='')
reader = csv.reader(myFile)
npc = CharacterType.objects.get_or_create(name="NPC")
campaign = Campaign.objects.get(num=2)


next(reader)
for row in reader:
    ep = Episode.objects.get(num=row[0], campaign=campaign)
    if row[1].startswith('p1'):
        time = row[1][4:]
    else:
        time = row[1]

    time = get_sec(time)
    by = Character.objects.get(name=row[2])
    try:
        to = Character.objects.get(name=row[3])
    except:
        if row[3] == "Clarota":
            races = Race.objects.get_or_create(name="Illithid")
            race = races[0]
        else:
            race = Race.objects.get(name="Human")
        to, created = Character.objects.get_or_create(full_name=row[3], name=row[3], char_type=npc[0], race=race)

    potion, potion_made = Potion.objects.get_or_create(name=row[4])

    if potion_made:
        print("POTION CREATED", potion.name)

    note = row[5]
    pu, created = PotionUsage.objects.get_or_create(by=by, to=to, episode=ep, potion=potion, timestamp=time,
                                                    notes=note)

    if created:
        print("USAGE MADE", ep.title, potion.name)
