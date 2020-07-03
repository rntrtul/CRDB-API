from episodes.models import Episode
from characters.models import Character
from campaigns.models import Campaign
from spells.models import SpellCast, Spell
import datetime
import csv
import os

DATADIR = "zdata/"
C1DIR = "C1/"
C1ROLLS = DATADIR + C1DIR + "C1 Spells Cast/"
EPSDONE = 96
C2SPELLS = "/home/lightbulb/CritRoleDB/zdata/C2/C2 Spells Cast/"

for dirpath,dirnames,files in os.walk(C2SPELLS):
  camp = Campaign.objects.get(num="2")
  files.sort()
  filesLeft = files[EPSDONE:]  #speed up inserting rollss when restarting due to error

  for file_name in filesLeft:
    if not file_name.endswith("-SC.csv"):
      continue
    
    spellReader = csv.reader(open(C2SPELLS +  file_name))
    
    ep_num = int(file_name[4:7])
    ep = Episode.objects.get(num=ep_num, campaign=camp)

    next(spellReader)  
    for row in spellReader:
      TIMEROW = 0
      NAMEROW = 1
      SPELLROW = 2
      LVLROW = 3
      CASTROW = 4
      NOTEROW = 5
      if camp.num == 2 and ep.num >=20 and ep.num <=51:
        TIMEROW = 1
        NAMEROW = 2
        SPELLROW = 3
        LVLROW = 4
        CASTROW = 5
        NOTEROW = 6
      timestamp = row[TIMEROW]
      if timestamp.startswith('p'):
        part = timestamp[1]
        timestamp = timestamp[4:]
        h,m,s = timestamp.split(':')
        timestamp = int(datetime.timedelta(hours=int(h),minutes=int(m),seconds=int(s)).total_seconds())
        if part == "2":
          if ep_num == 31:
            timestamp += 8013 #2:13:33 p1 length 
          elif ep_num == 33:
            timestamp += 8084 # 2:14:44 p1 length
          elif ep_num == 35:
            timestamp+= 7704 # 2:08:24 p1 length
      else:
        timestamp = int(float(timestamp))

      if row[NAMEROW] == "Veth":
        char = Character.objects.get(name="Nott")
      else:
        char = Character.objects.get(name=row[NAMEROW].strip())
      lvl  = row[LVLROW].strip()
      if lvl == "Cantrip" or lvl == 'cantrip':
        spell,created = Spell.objects.update_or_create(name=row[SPELLROW], defaults={'cantrip': True})
      elif lvl == '-' or lvl == "Unknown":
        lvl = 0
      else:
        lvl = int(lvl)
        spell,created = Spell.objects.update_or_create(name=row[SPELLROW], defaults={'level': lvl})
      if created:
        print(spell.name + " created")

      cast_at = row[CASTROW].strip()
      if cast_at == "Cantrip" or cast_at == 'cantrip' or cast_at == 'Cantrrip':
        cast_at=0
      elif cast_at == '-' or cast_at == "Unknown":
        cast_at = 0
      else:
        cast_at = int(cast_at)
      
      note = row[NOTEROW]

      spellcast, created = SpellCast.objects.update_or_create(spell=spell,episode=ep,character=char,cast_level=cast_at,notes=note)
      if created:
        print(str(ep.num) + " @ " + str(timestamp) + " " + char.name + " casted: " + spell.name + " :" + note)