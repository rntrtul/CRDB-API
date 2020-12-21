from django.db import models
from characters.models import Character, StatSheet
from episodes.models import Episode

# Create your models here.
class Spell(models.Model):
  name = models.TextField()
  level = models.IntegerField(default=0,blank=True)
  cantrip = models.BooleanField(default=False, blank=True)

class SpellCast(models.Model):
  timestamp = models.IntegerField(default=0)
  episode = models.ForeignKey(Episode, related_name='casts', on_delete=models.CASCADE)
  spell = models.ForeignKey(Spell, related_name='casts', on_delete=models.CASCADE)
  character = models.ForeignKey(Character, related_name='casts', on_delete=models.CASCADE)
  cast_level = models.IntegerField()
  notes = models.TextField(blank=True)

class LearnedSpell(models.Model):
  spell = models.ForeignKey(Spell, related_name='learned_by', on_delete=models.CASCADE)
  sheet = models.ForeignKey(StatSheet, related_name='learned_spells', on_delete=models.CASCADE)