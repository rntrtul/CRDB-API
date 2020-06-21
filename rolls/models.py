from django.db import models
from episodes.models import Episode
import time

# Create your models here.
#add boolean fields, skill, save, ability
class RollType(models.Model):
  name = models.TextField()
  def __str__(self):
    return self.name
#maybe add advantage type table instead of advantage field
class Rolls(models.Model):
  timeStamp = models.IntegerField(default=0)
  naturalValue = models.IntegerField(default=0)
  finalValue = models.IntegerField(default=0)
  notes = models.TextField()
  rollType = models.ForeignKey(RollType,on_delete=models.CASCADE)
  ep = models.ForeignKey(Episode, on_delete=models.CASCADE)

  def time_formated (self):
    return time.strftime("%-H:%M:%S", time.gmtime(self.timeStamp))