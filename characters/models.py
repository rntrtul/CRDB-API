from django.db import models
from races.models import Race
from classes.models import Class
import math

# Create your models here.
class CharacterType(models.Model):
  name = models.CharField(max_length=50)

class Character(models.Model):
  #Combine first_name + last_name + middle name into field name, add nicknames table
  #full_name = models.TextField()
  #name = models.TextField() #generaly use first name or nickName like Percy.
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100, blank=True)
  middle_name = models.CharField(max_length=100, blank=True)
  race = models.ForeignKey(Race, related_name='characters', on_delete=models.CASCADE)
  char_type = models.ForeignKey(CharacterType, related_name='list_of_chars', on_delete=models.CASCADE)

  def is_multiClass(self):  
    if self.classes.count() == 1:
      return False
    else:
      return True

class OtherNames(models.Model):
  #maybe add field to say if its a title or just a nickname
  character = models.ForeignKey(Character, related_name='other_names', on_delete=models.CASCADE)
  nick_name = models.TextField()

class Ability(models.Model):
  name = models.CharField(max_length=25)  

class Alignment(models.Model):
  name = models.TextField()

class Language(models.Model):
  #maybe add what script language is written in (serpate model)
  name = models.CharField(max_length=100)

class Skill(models.Model):
  name = models.CharField(max_length=25)
  ability = models.ForeignKey(Ability, related_name='skills', on_delete=models.CASCADE)

class Spell(models.Model):
  #Split into own app eventually. App will have spell cast logic and some info on spells
  name = models.TextField()

class StatSheet(models.Model):
  #add field for what episode they levelled up on default = 0, use level prog sheet
  # probably get rid of some null foreign key settings after data ingest
  character = models.ForeignKey(Character,related_name='stat_sheets', on_delete=models.CASCADE)
  alignment = models.ForeignKey(Alignment,related_name='stat_sheets', on_delete=models.CASCADE, null=True)
  max_health = models.IntegerField(default=0)
  armour_class = models.IntegerField(default=0)
  speed = models.IntegerField(default=30)
  initiative_bonus = models.IntegerField(default=0)
  proficiency_bonus = models.IntegerField(default=0)
  hit_die = models.CharField(max_length=50)
  inspiration_die = models.IntegerField(default=0)
  equipment = models.TextField(blank=True)
  features_traits = models.TextField(blank=True)
  attacks = models.TextField(blank=True)
  weapons = models.TextField(blank=True) #eventually split into own model and have equipment table have refrence to these maybe
  proficiencies = models.TextField(blank=True)

  casting_ability = models.ForeignKey(Ability, on_delete=models.CASCADE, null=True)
  casting_class = models.TextField(blank=True)
  spell_attack_bonus = models.IntegerField(default=0)
  spell_save = models.IntegerField(default=0)
  #spell slots
  cantrips    = models.IntegerField(default=0)
  slots_one   = models.IntegerField(default=0)
  slots_two   = models.IntegerField(default=0)
  slots_three = models.IntegerField(default=0)
  slots_four  = models.IntegerField(default=0)
  slots_five  = models.IntegerField(default=0)
  slots_six   = models.IntegerField(default=0)
  slots_seven = models.IntegerField(default=0)
  slots_eight = models.IntegerField(default=0)
  slots_nine  = models.IntegerField(default=0)

class SkillList(models.Model):
  stat_sheet = models.ForeignKey(StatSheet, related_name='skills', on_delete=models.CASCADE)
  skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
  modifier = models.IntegerField(default=0)
  profcient = models.BooleanField(default=False)

class AbilityScore(models.Model):
  stat_sheet = models.ForeignKey(StatSheet, related_name='ability_scores', on_delete=models.CASCADE)
  ability = models.ForeignKey(Ability, related_name='scores', on_delete=models.CASCADE)
  score = models.IntegerField(default=10)

  def get_modifier(self):
    return  math.floor((self.score-10)/2)

class SavingThrow(models.Model):
  stat_sheet = models.ForeignKey(StatSheet, related_name='saving_throws', on_delete=models.CASCADE)
  ability = models.ForeignKey(Ability, related_name='saves', on_delete=models.CASCADE)
  modifier = models.IntegerField(default=0)
  profcient = models.BooleanField(default=False)

class LearnedLanguage (models.Model):
  language = models.ForeignKey(Language, related_name='known_by', on_delete=models.CASCADE)
  sheet = models.ForeignKey(StatSheet, related_name='languages', on_delete=models.CASCADE)

class LearnedSpell(models.Model):
  spell = models.ForeignKey(Spell, related_name='known_by', on_delete=models.CASCADE)
  sheet = models.ForeignKey(StatSheet, related_name='learned_spells', on_delete=models.CASCADE)

class ClassTaken(models.Model):
  #need to change so its foreign_id to a stat sheet and character points to sheet
  stat_sheet = models.ForeignKey(StatSheet, related_name="classes", on_delete=models.CASCADE, null=True)
  class_id = models.ForeignKey(Class, related_name = 'characters', on_delete=models.CASCADE)
  level = models.IntegerField(default=0)