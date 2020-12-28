from characters.models import ClassTaken, Ability, AbilityScore, Skill, SkillList, Character, StatSheet, SavingThrow, \
    Alignment
from spells.models import Spell, SpellCast, LearnedSpell
from classes.models import Class
from episodes.models import LevelProg, Episode
from campaigns.models import Campaign
import os
import re

abilities = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
skills = ["Acrobatics", "Animal Handling", "Athletics", "Deception", "History", "Insight", "Intimidation",
          "Investigation", "Arcana",
          "Perception", "Nature", "Performance", "Medicine", "Religion", "Stealth", "Persuasion", "Sleight of Hand",
          "Survival"]
alignments = ["Lawful Good", "Lawful Neutral", "Lawful Evil", "Neutral Good", "Neutral", "Neutral Evil",
               "Chaotic Good", "Chaotic Neutral", "Chaotic Evil"]
languages = ["Common", "Dwarvish", "Elvish", "Giant", "Gnomish", "Goblin", "Halfling", "Orc", "Abyssal",
             "Celestial", "Draconic", "Deep Speech", "Infernal", "Primordial", "Sylvan", "Undercommon"]


def init_ability(abils):
    from characters.models import Ability
    print("Creating Abilities:")
    for ability in abils:
        abil = Ability.objects.get_or_create(name=ability)
        if abil[1]:
            print(ability + " was created")


def init_skills(skills, abils):
    from characters.models import Ability, Skill
    print("Creating Skills:")
    for skill in skills:
        if skill in ["Athletics"]:
            ability = abils[0]
        elif skill in ["Acrobatics", "Stealth", "Sleight of Hand"]:
            ability = abils[1]
        elif skill in ["Arcana", "History", "Investigation", "Nature", "Religion"]:
            ability = abils[3]
        elif skill in ["Animal Handling", "Insight", "Medicine", "Perception", "Survival"]:
            ability = abils[4]
        elif skill in ["Deception", "Intimidation", "Performance", "Persuasion"]:
            ability = abils[5]

        ab = Ability.objects.get(name=ability)
        sk = Skill.objects.get_or_create(name=skill, ability=ab)
        if sk[1]:
            print(skill + " was created")


def init_alignment(alligns):
    from characters.models import Alignment
    print("Creating Allignments:")
    for align in alligns:
        al = Alignment.objects.get_or_create(name=align)
        if al[1]:
            print(align + " was created.")


def initLanguages(langs):
    from languages.models import Language
    print("Creating Languages:")
    for lang in langs:
        l = Language.objects.get_or_create(name=lang)
        if l[1]:
            print(lang + " was created")


def findLevelUpEp(name, lvl, camp):
    import csv

    C1PROG = "/home/lightbulb/CritRoleDB/crdb_backend/zdata/C1/TD Level Prog.csv"
    C2PROG = "/home/lightbulb/CritRoleDB/crdb_backend/zdata/C2/WM Level Prog.csv"
    C1charColumn = {"Vex'ahlia": 1, "Vax'ildan": 2, "Grog": 3, "Keyleth": 4, "Percy": 5, "Scanlan": 6, "Pike": 7,
                    "Taryon": 8, "Tiberius": 9, }
    C2charColumn = {"Caleb": 1, "Nott": 2, "Jester": 3, "Beau": 4, "Fjord": 5, "Molly": 6, "Yasha": 7, "Caduceus": 8}

    if camp == 1:
        CURRPROG = C1PROG
        CURRCHARCOL = C1charColumn
    else:
        CURRPROG = C2PROG
        CURRCHARCOL = C2charColumn

    if not name in CURRCHARCOL:
        return 0

    with open(CURRPROG, newline='') as myFile:
        reader = csv.reader(myFile)
        next(reader)
        for row in reader:
            if row[0] == lvl:
                ep = row[CURRCHARCOL[name]][2:]
                ep = ep.strip()
                if ep.endswith('?'):
                    ep = ep[:-1]
                elif ep == '':
                    return 0
                return int(ep)

    return 0


def getAbilName(field):
    abilities = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
    if field == "STR":
        return abilities[0]
    elif field == "DEX":
        return abilities[1]
    elif field == "CON":
        return abilities[2]
    elif field == "INT":
        return abilities[3]
    elif field == "WIS":
        return abilities[4]
    elif field == "CHA":
        return abilities[5]


working_campaign = 1
CAMP = Campaign.objects.get(num=working_campaign)

C1SHEETS = "/home/lightbulb/CritRoleDB/crdb_backend/zdata/sheets"
C2SHEETS = "/home/lightbulb/CritRoleDB/crdb_backend/zdata/C2/C2 char sheets/Sheets"
if working_campaign == 1:
    CURR = C1SHEETS
else:
    CURR = C2SHEETS

for dirpath, dirnames, files in os.walk(CURR):
    files.sort()
    # files = files[35:]
    for file in files:
        fileName = file[:-4]
        index = fileName.find("_")
        if index == -1:
            index = fileName.find(" ")

        name = fileName[:index]
        lvl = fileName[index + 2:]
        ep_num = findLevelUpEp(name, lvl, CAMP.num)
        ch = Character.objects.get(name=name)
        sheet, created = StatSheet.objects.get_or_create(character=ch, level=lvl)
        if created:
            print("CREATED stat sheet for", ch.name, "at level", lvl)
        print(file)

        path = os.path.join(dirpath, file)
        reader = open(path, 'r')
        for line in reader:
            field = line[:line.find(":")]
            value = line[line.find(":") + 1:].strip()

            if value.startswith('\"'):
                value = value[1:]
            if value.endswith("\""):
                value = value[:-1]
            if value == "None" or value == "" and field != "Alignment":
                value = "0"

            if field == "ClassLevel":
                classes = re.split(',|/| |', value)
                count = 1
                cls = 0
                lvl = 0
                for one in classes:
                    if one == '':
                        continue
                    if count % 2 == 1:
                        print("ignore")
                    # cls = Class.objects.get_or_create(name=one)
                    else:
                        if one == 'Hunter':
                            continue
                        lvl = int(one)
                        print("ignore")
                    # clt = ClassTaken.objects.get_or_create(stat_sheet=sheet,class_id=cls[0],level=lvl )
                    count += 1
            elif field == "PlayerName":
                print("add player values")
            elif field == "CharacterName":
                print("ignore")
                # sheet.character = Character.objects.get(name=name)
            elif field == "Race":
                print("add racde values")
            elif field == "Alignment" and (value != "" and value != "???"):
                print("ignore")
                # sheet.alignment = Alignment.objects.get(name=value)
            elif field == "Inspiration" and value != "":
                sides = value
                if value.startswith('d'):
                    sides = value[1:]
                print("ignore")
                # sheet.inspiration_die = int(sides)
            elif field == "ProfBonus":
                print("ignore")
                # sheet.proficiency_bonus = int(value)
            elif field == "AC":
                print("ignore")
                # sheet.armour_class = int(value)
            elif field == "Initiative":
                print("ignore")
                # sheet.initiative_bonus = int(value)
            elif field == "Speed":
                print("ignore")
                # sheet.speed = int(value)
            elif field == "HPMax":
                if lvl == 9 and len(value) > 2 and value[2] == '-':
                    value = value[:-3]
                elif value == '':
                    value = "0"
                print("ignore")
                # sheet.max_health = int(value)
            elif field == "HDTotal":
                print("ignore")
                # sheet.hit_die = value
            elif field in ["STR", "DEX", "CON", "INT", "WIS", "CHA"]:
                print("ignore")
                #
                # abil_name = getAbilName(field)
                # abil = Ability.objects.get(name=abil_name)
                # ablisc = AbilityScore.objects.get_or_create(ability = abil, stat_sheet = sheet, score = value)
            elif field.startswith("ST"):
                print("ignore")
                #
                # abil_name = field[3:]
                # abill = Ability.objects.get(name=abil_name)
                # st = SavingThrow.objects.get_or_create(stat_sheet=sheet,ability=abill)
                # st[0].modifier=value
                # st[0].save()
            elif field in skills or field == "SleightofHand" or field == "Sleight of Hand":
                if field == "SleightofHand" or field == "Sleight of Hand":
                    sk_name = "Sleight of Hand"
                else:
                    sk_name = field
                print("ignore")
                # sk = Skill.objects.get(name=sk_name)
                # skl = SkillList.objects.get_or_create(stat_sheet=sheet, skill=sk)
                # skl[0].modifier=value
                # skl[0].save()
            elif field == "AttacksSpellcasting":
                print("ignore")
                # sheet.attacks = value
            elif field == "ProficienciesLang":
                print("ignore")
                # sheet.proficiencies = value.replace('\\n', ' \\n ')
            elif field == "Features and Traits":
                sheet.features_traits = value.replace('\\n', ' \n ')
            elif field == "Equipment":
                print("ignore")
                # sheet.equipment = value.replace('\\n', ' \\n ')
            elif field.startswith("Wpn"):
                print("ignore")
                # sheet.weapons += " " + value
                if field.endswith("Damage"):
                    print("ignore")
                # sheet.weapons += '\n'
            elif field == "Spellcasting Class 2":
                print("ignore")
                # sheet.casting_class = value
            elif field == "SpellSaveDC 2":
                print("ignore")
                # sheet.spell_save = value
            elif field == "SpellAtkBonus 2":
                if value != '':
                    print("ignore")
                # sheet.spell_attack_bonus = value
            elif field.startswith("Spell"):
                print("ignore")
                # spell = Spell.objects.get_or_create(name=value)
                # lp = LearnedSpell.objects.get_or_create(sheet = sheet, spell = spell[0])
            elif field.startswith("Slots"):
                print("ignore")
                #
                # spellLvl = int(field[13:])
                # if value == '':
                #  spellLvl = 0
                # if spellLvl == 1:
                #  sheet.slots_one = value
                # elif spellLvl == 2:
                #  sheet.slots_two = value
                # elif spellLvl == 3:
                #  sheet.slots_three = value
                # elif spellLvl == 4:
                #  sheet.slots_four = value
                # elif spellLvl == 5:
                #  sheet.slots_five = value
                # elif spellLvl == 6:
                #  sheet.slots_six = value
                # elif spellLvl == 7:
                #  sheet.slots_seven = value
                # elif spellLvl == 8:
                #  sheet.slots_eight = value
                # elif spellLvl == 9:
                #  sheet.slots_nine = value
            elif field.startswith("Proffcient in"):
                if value.endswith("Save"):
                    # handle procient in saving throws
                    abil_name = value[:-5]
                    abil = Ability.objects.get(name=abil_name)
                    print("ignore")
                # st = SavingThrow.objects.update_or_create(ability=abil,stat_sheet=sheet, defaults={'proficient': True})
                else:
                    # handle proffcient in skill
                    if value == "SleightofHand" or "Sleight of Hand":
                        sk_name = "Sleight of Hand"
                    else:
                        sk_name = value

                    print("ignore")
                    # sk = Skill.objects.get(name=sk_name)
                    # skl = SkillList.objects.update_or_create(skill=sk, stat_sheet=sheet,defaults={'proficient': True} )

        sheet.save()
        # if ep_num !=0:
        #  ep = Episode.objects.get(num=ep_num, campaign=CAMP)
        #  lp = LevelProg.objects.get_or_create(sheet=sheet, episode = ep, level=sheet.get_level())
        #  if lp[1]:
        #    print(name + " leveled to " + str(lvl) + " on episode " + str(ep_num))
