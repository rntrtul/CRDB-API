from rolls.models import Rolls, Kill
from characters.models import Character, CharacterType
from races.models import Race
import re

def makeKills():
  from rolls.models import Rolls, Kill
  from characters.models import Character, CharacterType
  from races.models import Race
  import re

  kill_rolls = Rolls.objects.filter(kill_count__gte = 1)

  charMatch = re.compile(r"to [a-zA-Z', ]+")
  npc = CharacterType.objects.get(name="NPC")
  uk = Race.objects.get(name="unknown")
  for roll in kill_rolls.order_by('ep__title', 'timestamp'):
    title = roll.ep.title
    if roll.kill_count == 1:
      if roll.damage == "":
        if title == "Arrival at Kraghammer":
          ch = Character.objects.get(name="Goblin")
          kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
        elif title == "Into the Greyspine Mines":
          ch = Character.objects.get(name="Duergar")
          kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
        elif title == "The Temple Showdown":
          ch = Character.objects.get(name="Goblin")
          kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
        elif title == "Skyward":
          if roll.timestamp == 10846 or roll.timestamp == 11885:
            ch = Character.objects.get(name="Rider")
            kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
          elif roll.timestamp == 11422 or roll.timestamp == 12218:
            ch = Character.objects.get(name="Wyvern")
            kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
        elif title == "Crimson Diplomacy":
          ch = Character.objects.get(name="Broker")
          kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
        elif title == "Omens":
          if roll.timestamp == 5081:
            ch = Character.objects.get(name="Purple worm")
            kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
          elif roll.timestamp == 5669:
            ch = Character.objects.get(name="Frost worm")
            kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
        elif title == "In Ruins":
          ch = Character.objects.get_or_create(name="Looting Thug", char_type=npc, race=uk)
          kill = Kill.objects.get_or_create(roll=roll,killed=ch[0],count=1)
        elif title == "Test of Pride":
          ch = Character.objects.get(name="Suda")
          kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
        elif title == "Cloak and Dagger":
          if roll.timestamp == 11498:
            ch = Character.objects.get(name="Luska")
            kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
          elif roll.timestamp == 15805:
            ch = Character.objects.get(name="Orthax")
            kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
          else:
            ch = Character.objects.get(name="Ripley")
            kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
        elif title == "Vorugal":
          if roll.timestamp == 15891:
            ch = Character.objects.get(name="Yenk")
            kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
          if roll.timestamp == 16515:
            ch = Character.objects.get(name="Vorugal")
            kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
        elif title == "Clash at Daxio":
          ch = Character.objects.get(name="Ember roc")
          kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
        elif title == "Thordak":
          ch = Character.objects.get(name="Rider")
          kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
        elif title == "Unfinished Business":
          ch = Character.objects.get(name="Skeleton")
          kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
        elif title == "Breaching the Emberhold":
          ch = Character.objects.get(name="Duergar")
          kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
        elif title == "Denouement":
          if roll.timestamp == 2616:
            ch = Character.objects.get_or_create(name="Countess",char_type=npc,race=uk)
            kill = Kill.objects.get_or_create(roll=roll,killed=ch[0],count=1)
          else:
            ch = Character.objects.get(name="Orthax")
            kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
        elif title == "Bats out of Hell":
          ch = Character.objects.get(name="Imp")
          kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
        elif title == "The Midnight Chase":
          ch = Character.objects.get(name="Zombie")
          kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
        elif title == "A Storm of Memories":
          ch = Character.objects.get_or_create(name="Lighning Celestial", char_type=npc, race=uk)
          kill = Kill.objects.get_or_create(roll=roll,killed=ch[0],count=1)
        elif title == "The Beat of the Permaheart":
          ch = Character.objects.get_or_create(name="Heart", char_type=npc, race=uk)
          kill = Kill.objects.get_or_create(roll=roll,killed=ch[0],count=1)
        elif title == "Reunions":
          ch = Character.objects.get(name="Ghost")
          kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
        else:
          print(roll.ep.title, roll.damage, roll.timestamp, roll.kill_count, roll.character.name)
    elif roll.kill_count > 1:
      if roll.damage != "":
        if title == "The Climb Within":
          ch = Character.objects.get_or_create(name="Troll")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 2)
        elif title == "Escape from the Underdark":
          ch = Character.objects.get_or_create(name="Intellect Devourer", char_type=npc, race = uk)
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 2)
        elif title == "Beyond the Eyes of Angels":
          ch = Character.objects.get_or_create(name="Zombies")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 2)
        elif title == "Cindergrove Revisited":
          ch = Character.objects.get_or_create(name="Fire elemental")
          if roll.timestamp == 7404:
            kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 2)
          elif roll.timestamp == 8842:
            kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 1)
            ch = Character.objects.get_or_create(name="Lfe")
            kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 1)
          elif roll.timestamp == 3960:
            ch = Character.objects.get_or_create(name="Salamander", char_type=npc, race = uk)
            kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 2)
            ch = Character.objects.get_or_create(name="Fatty Albanker", char_type=npc, race = uk)
            kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 1)
        elif title == "The Kill Box":
          ch = Character.objects.get_or_create(name="Peasant")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 2)
        elif title == "Reflections":
          ch = Character.objects.get_or_create(name="Doppelganger caleb")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 1)
          ch = Character.objects.get_or_create(name="Doppelganger fjord")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 1)
        elif title == "Stoke the Flames":
          ch = Character.objects.get_or_create(name="Vs") #vampires
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 2)
        elif title == "Dark Waters":
          ch = Character.objects.get_or_create(name="Sea spawn")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 2)
        elif title == "Unfinished Business":
            ch = Character.objects.get_or_create(name="Skeleton")
            if roll.timestamp == 16903:
              kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 1)
              ch = Character.objects.get_or_create(name="Minotaur skeleton")
              kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 1)
            elif roll.timestamp == 7213:
              kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 4)
            elif roll.timestamp == 14970:
              kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 5)
        elif title == "Enter Vasselheim":
          ch = Character.objects.get_or_create(name="Spiders")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 1)
        elif title == "Duplicity":
          ch = Character.objects.get_or_create(name="Incubus")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 1)
          ch = Character.objects.get_or_create(name="Caduceus")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 1)
        elif title == "The Folding Halls":
          ch = Character.objects.get_or_create(name="B")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 3)
        elif title == "Attack on the Duergar Warcamp":
          ch = Character.objects.get_or_create(name="Soldiers")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 3)
        elif title == "K'Varn Revealed":
          if roll.timestamp == 1980:
            ch = Character.objects.get_or_create(name="Ghoul", char_type=npc, race=uk)
            kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 3)
          elif roll.timestamp == 6703:
            ch = Character.objects.get_or_create(name="Gricks")
            kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 5)
        elif title == "The Sunken Tomb":
          ch = Character.objects.get_or_create(name="Kt archpriest")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 1)
          ch = Character.objects.get_or_create(name="Kt")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 2)
        elif title == "Xhorhas":
          ch = Character.objects.get_or_create(name="Gnoll")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 3)
        elif title == "The Cathedral":
          ch = Character.objects.get_or_create(name="Cultists")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 4)
        elif title == "Dangerous Dealings":
          ch = Character.objects.get_or_create(name="Rider")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 4)
        elif title == "Beneath Bazzoxan":
          ch = Character.objects.get_or_create(name="Orc")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 4)
        elif title == "The Throne Room":
          ch = Character.objects.get_or_create(name="Soldiers")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 5)
        elif title == "Against the Tide of Bone":
          ch = Character.objects.get_or_create(name="Skeletons")
          if roll.timestamp == 2391:
            kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 5)
          elif roll.timestamp == 1792:
            kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 12)
        elif title == "Arrival at Kraghammer":
          ch = Character.objects.get_or_create(name="Goblin")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 5)
        elif title == "Clash at Daxio":
          ch = Character.objects.get_or_create(name="Lizardfolk", char_type=npc, race=uk)
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 6)
        elif title == "In Hot Water":
          ch = Character.objects.get_or_create(name="Crew")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 4)
          ch = Character.objects.get_or_create(name="Barlgura")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 1)
          ch = Character.objects.get_or_create(name="Vera")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 1)
        elif title == "The Trick about Falling":
          ch = Character.objects.get_or_create(name="Duregar", char_type=npc, race=uk)
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 12)
        elif title == "Gunpowder Plot":
          ch = Character.objects.get_or_create(name="Undead", char_type=npc, race=uk)
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 30)
      else:
        if title == "Breaching the Emberhold":
          ch = Character.objects.get_or_create(name="Duergar Prison Guards", char_type=npc, race = uk)
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 2)
        elif title == "Against the Tide of Bone":
          ch = Character.objects.get_or_create(name="Skeletons")
          kill = Kill.objects.get_or_create(roll=roll, killed = ch[0], count = 7)
        else:
          print(roll.ep.title, roll.damage, roll.timestamp, roll.kill_count, roll.character.name)


#makeKills()

npc = CharacterType.objects.get(name="NPC")
uk = Race.objects.get(name="unknown")

for roll in Rolls.objects.filter(kill_count__gte = 1).order_by('ep__num', 'timestamp'):
  recorded = Kill.objects.filter(roll=roll)
  if len(recorded) == 0:
    title = roll.ep.title
    if title == "Into the Greyspine Mines":
      if roll.timestamp == 8525 or roll.timestamp == 9090:
        ch = Character.objects.get_or_create(name="Umberhulk", char_type=npc, race = uk)
        kill = Kill.objects.get_or_create(roll=roll,killed=ch[0],count=1)
      elif roll.timestamp == 9985:
        ch = Character.objects.get(name="Intellect Devourer")
        kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
      elif roll.timestamp == 10105:
        ch = Character.objects.get(name="Duergar")
        kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
    elif title == "Umbrasyl":
      ch = Character.objects.get(name="Umbrasyl")
      kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)
    elif title == "Beyond the Eyes of Angels":
      ch = Character.objects.get(name="Spider")
      kill = Kill.objects.get_or_create(roll=roll,killed=ch,count=1)

        
    print(roll.ep.title, roll.time_formated(),roll.timestamp, roll.damage)