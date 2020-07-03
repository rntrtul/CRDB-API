from races.models import Race
from characters.models import Character, CharacterType
from players.models import Player

comp = CharacterType.objects.get(name="Companion")

r = Race(name="Moorbounder")
r.save()
#type = CharacterType.objects.get(id=comp.id)
player = Player.objects.get(full_name="Liam O'Brien")
char = Character(full_name="Willie",name="Willie", race = r, char_type=comp)
char.save() 