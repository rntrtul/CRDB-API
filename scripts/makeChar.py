from races.models import Race
from characters.models import Character, CharacterType

r = Race(name="Gloomstalker")
r.save()
type = CharacterType.objects.get(id=1)
char = Character(first_name="Gloomstalker", race = r, char_type=type)
char.save()