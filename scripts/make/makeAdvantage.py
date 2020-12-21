from rolls.models import Rolls, Advantage, AdvantageType
from episodes.models import Episode
from characters.models import Character
from fuzzywuzzy import fuzz
from collections import deque
import regex


roll_que = deque()  
eps = Episode.objects.order_by('num')
rolls = Rolls.objects.all()

for ep in eps.all():
  ep_count = 0
  ep_rolls =  rolls.filter(ep=ep).order_by('timestamp')
  for roll in ep_rolls.all():
    adv_ratio = fuzz.partial_ratio('advantage', roll.notes)
    dis_ratio = fuzz.partial_ratio('disadvantage', roll.notes)
    luck_ratio = fuzz.partial_ratio('luck', roll.notes.lower())
    frag_ratio = fuzz.partial_ratio('fragment of possibility', roll.notes.lower())

    if frag_ratio >= 95:
      count = ep_rolls.filter(character= roll.character, roll_type = roll.roll_type,
                              timestamp__lte=(roll.timestamp + 2), timestamp__gte=(roll.timestamp - 2))
      for adjc in count:
        if len(roll_que) == 0 or len(roll_que) == 1:
          ep_count += 1
          roll_que.append(adjc)
        elif roll_que[-1] != adjc and roll_que[-2] != adjc:
          ep_count += 1
          roll_que.append(adjc)
    elif frag_ratio >= 80:
      print(roll.ep.title, ' ', roll.timestamp, ' ' ,roll.notes)


length = len(roll_que)
TIMEDIFF = 15

matches = 0
no_match = []
advantage = 0
disadvantage = 0
loop = 0

disMatch = regex.compile('disadvantage{s<=1}')
DISADVANTAGE = AdvantageType.objects.get(name="Disadvantage")
ADVATANTAGE = AdvantageType.objects.get(name="Advantage")
LUCK = AdvantageType.objects.get(name="Luck")
FP = AdvantageType.objects.get(name="Fragment of Possibility")

while True:
  loop += 1
  top = roll_que.pop()  
  
  ahead = roll_que[-1]

  if top.character == ahead.character and abs(top.timestamp - ahead.timestamp) <= TIMEDIFF :
    now = roll_que.pop()
    miss_ratio = max(fuzz.partial_ratio('disregarded', top.notes), fuzz.partial_ratio('ignored', top.notes))

    if miss_ratio >= 80:
      missed = top
      used = now
    else:
      missed = now
      used = top

    #if disMatch.search(missed.notes.lower().strip()):
    #  type = DISADVANTAGE
    #  disadvantage +=1
    #else:
    #  type = ADVATANTAGE
    #  advantage += 1


    type = FP
    adv_relate = Advantage.objects.get_or_create(type=type, used= used, disregarded=missed)
    
    if adv_relate[1]:
      print("Linked following as ", type.name)
      print(used.ep.title, ' ',used.timestamp, ' ' ,used.character.name , ' ' ,used.final_value, ' ', used.notes)
      print(missed.ep.title, ' ',missed.timestamp, ' ' ,missed.character.name , ' ' ,missed.final_value, ' ', missed.notes)

    matches += 1
  else :
    no_match.append(top)
  
  if len(roll_que) == 0:
    break


#for missed in no_match:
#  print(missed.ep.title, ' ',missed.time_stamp, ' ' ,missed.character.name , ' ' ,missed.final_value, ' ', missed.notes)

# disregarded, ignored, final_value = 0 is diregareded roll and other is not
# need to leave the 75ish lone ones with blank other roll, manually look at notes and delete ones which aren't rolls


print(str(matches))
target = length /2
print(str(target))
print(str(length)) #actual target is length /2 since grouping each roll into 2
#print("adv: ", str(advantage))
#print("dis: ", str(disadvantage))