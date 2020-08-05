from characters.models import Character
from languages.models import Language, LearnedLanguage

languages = ["Common", "Dwarvish", "Elvish", "Giant", "Gnomish", "Goblin", "Halfling", "Orc","Abyssal",
             "Celestial", "Draconic", "Deep Speech", "Infernal", "Primordial","Sylvan", "Undercommon"]


char_list = Character.objects.all()

for char in char_list:
  for sheet in char.stat_sheets.all():
    prof = sheet.proficiencies
    for lang in languages:
      if prof.find(lang) != -1:
        l = Language.objects.get(name=lang)
        learned = LearnedLanguage.objects.get_or_create(sheet=sheet, language=l)
        if learned[1]:
          print("added learned language")