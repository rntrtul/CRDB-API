from rolls.models import Rolls, RollType
from episodes.models import Episode, Campaign
from characters.models import Character
import csv
import os

DATADIR = "zdata/"
C1DIR = "C1/"
C1ROLLS = DATADIR + C1DIR + "C1 Character Rolls/"
C2ROLLS = "./"
EPSDONE = 0


# Success for pepperbox c1e33


def get_value(cell):
    invalid_vals = ['Unknown', 'Unkown', 'N/A', 'NA', '--', '', '#REF!', 'unknown', 'unkown', 'Misfire', 'Success',
                    'Fail',
                    'Unnknown', 'unnknown', 'uknown', 'Uknown', 'Unkknown', 'unkknown']
    val = 0
    valid = True
    if cell.strip().startswith('Natural'):
        val = int(cell[8:])
    elif cell.startswith('Nat'):
        natless = cell[3:]
        if natless.endswith('?'):
            val = int(natless[:-1])
        elif '=' in natless:
            val = int(natless[:-3])  # assuming for nat 20 if 1 probably get '' can't convert to int
        else:
            val = int(natless)
    elif cell.endswith('ish'):
        val = int(cell[:-3])
    elif cell.startswith('>'):
        val = int(cell[1:]) + 1
    elif cell.startswith('<'):
        val = int(cell[1:]) - 1
    elif cell.endswith('+'):
        val = int(cell[:-1])
    elif cell not in invalid_vals:
        val = int(cell)
    else:
        valid = False

    return val if valid else None


curr = C2ROLLS
for dirpath, dirnames, files in os.walk(curr):
    files.sort()
    filesLeft = files[EPSDONE:]  # speed up inserting rolls

    for file_name in filesLeft:
        if not file_name.endswith("-CR.csv"):
            continue

        rollReader = csv.reader(open(curr + file_name))
        print(file_name)
        next(rollReader)
        camp = Campaign.objects.get(num=int(file_name[1]))
        for row in rollReader:
            TIMEROW = 1
            NAMEROW = 2
            TYPEROW = 3
            TOTALROW = 4
            NATROW = 5
            DAMAGEROW = 7
            KILLROW = 8
            NOTEROW = 9
            notes = ''
            if camp.num == 1:
                ep_num = row[0]
            else:
                ep_num = row[0][3:]

            # print(ep_num)
            if row[0].endswith('p1') or row[0].endswith('p2'):
                ep = Episode.objects.get(num=int(row[0][:-3]), campaign=camp)
                notes += (row[0][3:] + " ")
            else:
                ep = Episode.objects.get(num=int(ep_num), campaign=camp)

            if camp.num == 2 and 20 <= ep.num <= 51:
                TIMEROW = 2
                NAMEROW = 3
                TYPEROW = 4
                TOTALROW = 5
                NATROW = 6
                DAMAGEROW = 8
                KILLROW = 9
                NOTEROW = 10

            timeStamp = int(row[TIMEROW])

            if row[NAMEROW] == '' or row[NAMEROW].capitalize() == 'Others' or row[NAMEROW].capitalize() == 'Grenade' or \
                    row[NAMEROW] == 'NA':
                # gernade is from episode 19
                continue  # skip when a bunch of people rolled at once, maybe add those back in through admin site
            adjusted_name = row[NAMEROW].capitalize() if row[NAMEROW] != "Veth" else "Nott"

            character = Character.objects.get(name=adjusted_name)
            roll_type = RollType.objects.get(name=row[TYPEROW])

            total_val = get_value(row[TOTALROW])
            nat_val = get_value(row[NATROW])

            damage = ""
            damage += row[DAMAGEROW]

            kill_count = 0
            if row[KILLROW] != "" and row[KILLROW] != '?' and not row[KILLROW].startswith('0.'):
                kill_count = int(row[KILLROW])
            if row[KILLROW].startswith('0.'):
                kill_count = 1

            notes += row[NOTEROW]

            roll, created = Rolls.objects.get_or_create(ep=ep, timestamp=timeStamp, character=character, notes=notes,
                                                        natural_value=nat_val, final_value=total_val, damage=damage,
                                                        kill_count=kill_count, roll_type=roll_type)


            # print([ep.num, timeStamp, character.name, roll_type.name, nat_val, total_val, notes, damage, kill_count])

            if created:
                print("Created roll at time: " + str(timeStamp) + "in ep: " + str(ep.num))
