from django.db import models
from episodes.models import Episode
from rolls.models import Rolls
from characters.models import Character

# Create your models here.

class CombatEncounter(models.Model):
  episode = models.ForeignKey(Episode, related_name='combat_encounters', on_delete=models.CASCADE)
  name = models.TextField()
  start = models.IntegerField(default=0)
  end = models.IntegerField(default=0)
  rounds = models.IntegerField(default=0)
  notes = models.TextField(blank = True)

  def isIn(self, time):
    return time >= self.start and time <= self.end

class CombatApperance(models.Model):
  encounter = models.ForeignKey(CombatEncounter, related_name='apperances', on_delete=models.CASCADE)
  character = models.ForeignKey(Character, related_name='combat_encounters', on_delete=models.CASCADE)

class InitiativeOrder(models.Model):
  encounter = models.ForeignKey(CombatEncounter, related_name='initiatievs', on_delete=models.CASCADE)
  character = models.ForeignKey(Character, related_name='initiatives', on_delete=models.CASCADE)
  roll =  models.ForeignKey(Rolls, on_delete=models.CASCADE)
  rank = models.IntegerField(default = 0)
