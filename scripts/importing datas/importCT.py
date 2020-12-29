from episodes.models import Episode
from campaigns.models import Campaign
from encounters.models import CombatEncounter, CombatApperance, InitiativeOrder
import csv


def makeCombatEncounter(camp_num):
    def get_sec(time_str):
        h, m, s = time_str.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)

    C1DIR = "/home/lightbulb/CritRoleDB/zdata/C1/C1 Times + Attendance/TD Combat Times.csv"
    C2DIR = "./WM Combat Times.csv"

    from episodes.models import Episode
    from campaigns.models import Campaign
    from encounters.models import CombatEncounter
    import csv

    myFile = open(C2DIR, newline='')
    reader = csv.reader(myFile)
    campaign = Campaign.objects.get(num=camp_num)

    next(reader)
    next(reader)
    next(reader)
    for row in reader:
        name = row[0]
        ep_num = int(row[1][3:])
        ep = Episode.objects.get(campaign=campaign, num=ep_num)

        start = get_sec(row[3])
        end = get_sec(row[4])
        rounds = int(row[5]) if row[5] else 0
        note = row[8]

        ce = CombatEncounter.objects.get_or_create(episode=ep, name=name, start=start, end=end, rounds=rounds,
                                                   notes=note)
        if ce[1]:
            print("CREATED: " + name + " " + str(ep_num) + " " + str(start) + " " + str(end) + " " + str(rounds) + note)


def makeCombatApperance():
    from encounters.models import CombatEncounter, CombatApperance, InitiativeOrder
    from rolls.models import Rolls
    ces = CombatEncounter.objects.all()

    for encounter in ces:
        encounter_rolls = Rolls.objects.filter(ep=encounter.episode, timestamp__range=(encounter.start, encounter.end))
        for roll in encounter_rolls:
            ch = roll.character
            apperance = CombatApperance.objects.get_or_create(encounter=encounter, character=ch)
            if apperance[1]:
                print("CREATED: " + ch.name + " in: " + encounter.name)


def makeInitiative():
    from encounters.models import CombatEncounter, CombatApperance, InitiativeOrder
    from rolls.models import Rolls, RollType
    ces = CombatEncounter.objects.all().filter(episode__num__gte=99)
    initiative = RollType.objects.get(name='Initiative')

    for encounter in ces:
        order = {}
        encounter_initative_rolls = Rolls.objects.filter(ep=encounter.episode,
                                                         timestamp__range=(encounter.start, encounter.end),
                                                         roll_type=initiative)

        for roll in encounter_initative_rolls:
            if roll.character in order:
                if (order[roll.character].final_value is None and roll.final_value) or (
                        roll.final_value and roll.final_value > order[roll.character].final_value):
                    order[roll.character] = roll
            else:
                order[roll.character] = roll

        order_sorted = {k: v for k, v in sorted(order.items(), key=lambda item: item[1].final_value, reverse=True)}

        if order_sorted != {}:
            for counter, ord in enumerate(order_sorted.items()):
                rank = counter + 1
                init = InitiativeOrder.objects.get_or_create(encounter=encounter, character=ord[0], roll=ord[1],
                                                             rank=rank)
                if init[1]:
                    print("CREATED: " + ord[0].name + " " + str(rank))


# makeCombatEncounter(2)
# makeCombatApperance()
makeInitiative()
