from rolls.models import Rolls, Advantage, AdvantageType
from episodes.models import Episode
from campaigns.models import Campaign
from fuzzywuzzy import fuzz
from collections import deque

roll_que = deque()
eps = Episode.objects.order_by('num')
rolls = Rolls.objects.all()

ADVANTAGE = AdvantageType.objects.get(name="Advantage")
DISADVANTAGE = AdvantageType.objects.get(name="Disadvantage")
LUCK = AdvantageType.objects.get(name="Luck")
FP = AdvantageType.objects.get(name="Fragment of Possibility")


def get_ratio(notes):
    from fuzzywuzzy import fuzz
    global ADVANTAGE, DISADVANTAGE, LUCK, FP
    adv_ratio = [fuzz.partial_ratio('advantage', notes), ADVANTAGE]
    dis_ratio = [fuzz.partial_ratio('disadvantage', notes), DISADVANTAGE]
    luck_ratio = [fuzz.partial_ratio('luck', notes), LUCK]
    frag_ratio = [fuzz.partial_ratio('fragment of possibility', notes), FP]

    return sorted([adv_ratio, dis_ratio, luck_ratio, frag_ratio], key=lambda el: el[0])[-1]


for ep in eps.all():
    ep_count = 0
    ep_rolls = rolls.filter(ep=ep).order_by('timestamp')
    for roll in ep_rolls.all():
        ratio, category = get_ratio(roll.notes.lower())

        if ratio >= 85:
            roll_range = ep_rolls.filter(character=roll.character, roll_type=roll.roll_type,
                                         timestamp__lte=(roll.timestamp + 2), timestamp__gte=(roll.timestamp - 2))

            for adjacent in roll_range:
                if len(roll_que) <= 1:
                    ep_count += 1
                    roll_que.append((adjacent, category))
                elif roll_que[-1] != adjacent and roll_que[-2] != adjacent:
                    ep_count += 1
                    roll_que.append((adjacent, category))

length = len(roll_que)
target = length / 2
TIMEDIFF = 15

matches = 0
make_count = 0
no_match = []
advantage = 0
disadvantage = 0
loop = 0

while True:
    loop += 1
    top, top_type = roll_que.pop()
    ahead, dmp = roll_que[-1]

    if top.character == ahead.character and abs(top.timestamp - ahead.timestamp) <= TIMEDIFF:
        now, now_type = roll_que.pop()
        miss_ratio = max(fuzz.partial_ratio('disregarded', top.notes), fuzz.partial_ratio('ignored', top.notes))

        (missed, used) = (top, now) if miss_ratio >= 80 else (now, top)

        if top_type.name == "Advantage":
            advantage += 1
        elif top_type.name == "Disadvantage":
            disadvantage += 1

        adv_relate, created = Advantage.objects.get_or_create(type=top_type, used=used, disregarded=missed)
        # adv_relate, created = [0, True]

        if created:
            print("Linked following as", top_type.name)
            print(used.ep.num, used.timestamp, used.character.name, used.final_value, used.notes, top_type.name)
            print(missed.ep.num, missed.timestamp, missed.character.name, missed.final_value, missed.notes,
                  now_type.name)
            make_count += 1

        matches += 1
    else:
        no_match.append(top)

    if len(roll_que) == 0:
        break

# print("missed:")
# for missed in no_match:
#     print(missed.ep.title, missed.timestamp, missed.character.name, missed.final_value, missed.notes)

# disregarded, ignored, final_value = 0 is diregareded roll and other is not
# need to leave the 75ish lone ones with blank other roll, manually look at notes and delete ones which aren't rolls


print("___________________")
print("matches:", str(matches))
print("target:", str(target))
print("adv:", str(advantage))
print("dis:", str(disadvantage))
print("___________________")
print("created:", make_count)
