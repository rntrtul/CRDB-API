from django.db import models
from characters.models import Character, StatSheet
from episodes.models import Episode
from rolls.models import Die, Rolls
# Create your models here.
class Potion(models.Model):
  name = models.TextField()
  description = models.TextField(blank=True)

class DamageType(models.Model):
  name = models.TextField()

class Weapon(models.Model):
  name = models.TextField()
  attack_bonus = models.IntegerField(default=0)
 
class WeaponDamage(models.Model):
  die_num  = models.IntegerField()
  modifier = models.IntegerField()
  damage_type =  models.ForeignKey(DamageType, related_name="weapons", on_delete=models.CASCADE, blank=True, null=True)
  weapon =  models.ForeignKey(Weapon, related_name="damages", on_delete=models.CASCADE)
  die =  models.ForeignKey(Die, on_delete=models.CASCADE, blank=True, null=True)

class WeaponeOwned(models.Model):
  sheet = models.ForeignKey(StatSheet, related_name="weapons_owned", on_delete=models.CASCADE)
  weapon = models.ForeignKey(Weapon, related_name="owners", on_delete=models.CASCADE)

class PotionUsage(models.Model):
  by = models.ForeignKey(Character, related_name='potions_administered', on_delete=models.CASCADE)
  to = models.ForeignKey(Character, related_name='potions_consumed', on_delete=models.CASCADE)
  episode = models.ForeignKey(Episode, related_name='potions', on_delete=models.CASCADE)
  potion = models.ForeignKey(Potion, related_name='uses', on_delete=models.CASCADE)
  timestamp = models.IntegerField(default=0)
  notes = models.TextField(blank=True)

class WeaponUsage(models.Model):
  roll = models.ForeignKey(Rolls, on_delete = models.CASCADE)
  weapon = models.ForeignKey(Weapon, related_name='uses', on_delete=models.CASCADE)
  #eventually add damage foreign key here
