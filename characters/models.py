from django.db import models
from races.models import Race
from classes.models import Class
from players.models import Player
import math


# Create your models here.
class CharacterType(models.Model):
    name = models.CharField(max_length=50)


class Character(models.Model):
    full_name = models.TextField(blank=True)
    name = models.TextField(blank=True)  # generaly use first name or nickName like Percy.
    # background = models.TextField() OR models.ForeignKey(Background)
    race = models.ForeignKey(Race, related_name='characters', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='characters', on_delete=models.CASCADE, blank= True, null = True)
    char_type = models.ForeignKey(CharacterType, related_name='characters', on_delete=models.CASCADE)

    def curr_sheet(self):
        return self.stat_sheets.order_by('-max_health')[0]


class OtherNames(models.Model):
    # maybe add field to say if its a title or just a nickname
    character = models.ForeignKey(Character, related_name='other_names', on_delete=models.CASCADE)
    nick_name = models.TextField()


class Ability(models.Model):
    name = models.CharField(max_length=25)


class Alignment(models.Model):
    name = models.TextField()


class Skill(models.Model):
    name = models.CharField(max_length=25)
    ability = models.ForeignKey(Ability, related_name='skills', on_delete=models.CASCADE)


class StatSheet(models.Model):
    # probably get rid of some null foreign key settings after data ingest
    character = models.ForeignKey(Character,related_name='stat_sheets', on_delete=models.CASCADE)
    alignment = models.ForeignKey(Alignment,related_name='stat_sheets', on_delete=models.CASCADE, null=True)
    max_health = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    armour_class = models.IntegerField(default=0)
    speed = models.IntegerField(default=30)
    initiative_bonus = models.IntegerField(default=0)
    proficiency_bonus = models.IntegerField(default=0)  # remove since always based on total level
    hit_die = models.CharField(max_length=50)  # remove since can be calculated from level + class
    inspiration_die = models.IntegerField(default=0)  # remove can be calcualted from calss
    equipment = models.TextField(blank=True)
    features_traits = models.TextField(blank=True)
    attacks = models.TextField(blank=True)
    weapons = models.TextField(blank=True)  # eventually split into own model and have equipment table point here
    proficiencies = models.TextField(blank=True)

    casting_ability = models.ForeignKey(Ability, on_delete=models.CASCADE, null=True)
    casting_class = models.TextField(blank=True) # maybe make foreignkey
    spell_attack_bonus = models.IntegerField(default=0, blank=True, null =True)
    spell_save = models.IntegerField(default=0, blank=True, null =True)
    # spell slots
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

    def get_level(self):
        lvl = 0
        for cls in self.classes.all():
            lvl += cls.level
        return lvl

    def get_level_verbose(self):
        verb = ""
        splitter = ""
        for cls in self.classes.all():
            verb += splitter + cls.class_id.name + ", " + str(cls.level)
            splitter = " / "
        return verb


class SkillList(models.Model):
    stat_sheet = models.ForeignKey(StatSheet, related_name='skills', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    modifier = models.IntegerField(default=0)
    proficient = models.BooleanField(default=False)


class AbilityScore(models.Model):
    stat_sheet = models.ForeignKey(StatSheet, related_name='ability_scores', on_delete=models.CASCADE)
    ability = models.ForeignKey(Ability, related_name='scores', on_delete=models.CASCADE)
    score = models.IntegerField(default=10)

    def get_modifier(self):
        return math.floor((self.score-10)/2)


class SavingThrow(models.Model):
    stat_sheet = models.ForeignKey(StatSheet, related_name='saving_throws', on_delete=models.CASCADE)
    ability = models.ForeignKey(Ability, related_name='saves', on_delete=models.CASCADE)
    modifier = models.IntegerField(default=0)
    proficient = models.BooleanField(default=False)


class ClassTaken(models.Model):
    stat_sheet = models.ForeignKey(StatSheet, related_name="classes", on_delete=models.CASCADE, null=True)
    class_id = models.ForeignKey(Class, related_name = 'sheets', on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
