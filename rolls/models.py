from django.db import models
from episodes.models import Episode
from characters.models import Character
import time

# Create your models here.
#add boolean fields, skill, save, ability
class RollType(models.Model):
  name = models.TextField()
  def __str__(self):
    return self.name
#maybe add advantage type table instead of advantage field
class Rolls(models.Model):
  time_stamp = models.IntegerField(default=0)
  natural_value = models.IntegerField(default=0)
  final_value = models.IntegerField(default=0)
  notes = models.TextField()
  roll_type = models.ForeignKey(RollType, related_name='rolls', on_delete=models.CASCADE)
  ep = models.ForeignKey(Episode, related_name='rolls', on_delete=models.CASCADE)
  character = models.ForeignKey(Character, related_name='rolls', on_delete=models.CASCADE)

  def time_formated (self):
    return time.strftime("%-H:%M:%S", time.gmtime(self.time_stamp))