from rolls.models import Rolls
from items.models import Weapon, WeaponUsage
from spells.models import Spell

pepper = Weapon.objects.get(name="Pepperbox")
pepper_notes = Rolls.objects.filter(notes__contains=pepper.name)

# iterate over weapon and then get notes list for that then print them out
# test with like 3 weapons (grog, keyleth, vex)
# want waepon usage table that links weapon with a roll 

wpns = Weapon.objects.all()
ls = {}
total = 0
count = 0
for weapon in wpns:
  #skip dagger since it shows up in like 4 different weapon names
  if weapon.name == 'Dagger':
    continue
  wpn_notes = Rolls.objects.filter(notes__contains=weapon.name)
  for roll in wpn_notes:
    #print(str(roll.time_stamp))
    usage = WeaponUsage.objects.get_or_create(weapon=weapon, roll=roll)
    if usage[1]:
      print("created usage for", weapon.name)
  
  length = len(wpn_notes)
  total += length
  count += 1
  ls[weapon.name] = length

lsorted = {k: v for k, v in sorted(ls.items(), key=lambda item: item[1])}
for wpn in lsorted.items():
  print(wpn[0] + " was used: " + str(wpn[1]))

print(str(total) + " total rolls with wepaon name in the notes field")
print(str(count) + " total weapons")

#for roll in pepper_notes:
#  print(roll.roll_type.name + ": " + roll.damage + " (" + roll.notes + ")")