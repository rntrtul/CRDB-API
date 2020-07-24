from rolls.models import Rolls, Kill
from characters.models import Character
import re
kill_rolls = Rolls.objects.filter(kill_count__gte = 1)

charMatch = re.compile(r"to [a-zA-Z', ]+")
count = 0
print('ep,time,damage,killed')
for roll in kill_rolls.order_by('kill_count'):
  if roll.kill_count > 1:
    #name = charMatch.search(roll.damage)
    #if name:
    #charName = roll.damage[name.start()+3:name.end()].strip().capitalize().replace(',', '')
    if roll.damage != "":
      print(roll.ep.title + ',' + str(roll.time_stamp) + ',\"' +  roll.damage + '\",' + str(roll.kill_count))
    #else:
    #  print(roll.damage)

# or go through damage word by word and see if damage matches a character name
# max char name is 4 which is laughing hand and cultists
# so keep track of last 4 words in damage field and if it or current name matches charcter name that is a damaged person  
# for single kill just do it and for multiple do < 3   ones by hand for bulk write script
# only relate kills for 1 char in damage field


print(count)
#print(max_char.name)